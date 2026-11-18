"""Source-bound offline crosscheck; writes only this report directory."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from bs4 import BeautifulSoup
import gzip
import hashlib
import json
import yaml
from scripts.feed.review import source_hash, _review_row
from scripts.feed.scope import load_scope, scope_status
from scripts.feed.guard import check_summary, enforce_evidence, normalized_whitespace

BASE = Path('docs/internal/reports/maintenance-2026-11-18')
HIST = BASE / 'historical-disposition'
OUT = BASE / 'publication-crosscheck/historical-actionable-v1.json'
assert not OUT.exists(), 'Frozen report already exists'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def jsha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

canonical = {r['id']: r for r in map(json.loads, Path('data/feed/items.jsonl').read_text().splitlines())}
pos_path = HIST / 'positive-proposals-v4.json'
exc_path = HIST / 'exclusion-proposals-v1.json'
pos = json.loads(pos_path.read_text())
exc = json.loads(exc_path.read_text())
pos_rows = yaml.safe_load((HIST / 'positive-review-rows-v4.yaml').read_text())['items']
exc_rows = yaml.safe_load((HIST / 'exclusion-review-rows-v1.yaml').read_text())['items']
rows = {r['id']: r for r in pos_rows + exc_rows}
pos_ids = {r['id'] for r in pos['items']}
inv_path = Path(pos['input_inventory']['path'])
inventory = {r['id']: r for r in map(json.loads, gzip.open(inv_path, 'rt'))}
owner_path = Path('review/approvals/2026-11-02.yaml')
owner = yaml.safe_load(owner_path.read_text())
prov_path = Path('docs/internal/reports/maintenance-2026-10-30/independent/source-provenance.json')
provenance = {r['id']: r for r in json.loads(prov_path.read_text())['items']}
cache = {}
checks, records = [], []

def check(name, passed, **details):
    checks.append({'check': name, 'passed': bool(passed), **details})

def previous(ref):
    path = ref['path']
    if path not in cache:
        cache[path] = json.loads(Path(path).read_text()) if ref['collection'] else list(map(json.loads, Path(path).read_text().splitlines()))
    value = cache[path]
    return (value[ref['collection']] if ref['collection'] else value)[ref['index']]

check('frozen_proposal_hashes', sha(pos_path) == 'ee6683a9d201b99ded0eef8e976a519ec2319c52784ed36da7db0d7fae3863ce' and sha(exc_path) == '373720956c9cb4070de300d1128e3e17c4b4c92544da946ea3e0263e46907b26')
check('frozen_review_rows', sha(HIST / 'positive-review-rows-v4.yaml') == '00d288088b8acad04993c32fc41b8ba560926b40e8381a89e640dc806b446d89' and sha(HIST / 'exclusion-review-rows-v1.yaml') == 'df206eb8de1d18119b2da84696005d2c6083d67f6bd17d0200433cf509560c14')
check('121_inventory29_unique_actionable', len(inventory) == 121 and len(pos['items']) == 19 and len(exc['items']) == 10 and len(rows) == 29 and set(rows) <= set(inventory))
check('inventory_carryforward_hashes', sha(inv_path) == pos['input_inventory']['sha256'] and sha(pos['input_carryforward']['path']) == pos['input_carryforward']['sha256'])
for proposal in pos['items'] + exc['items']:
    item_id = proposal['id']
    c, r, inv = canonical[item_id], rows[item_id], inventory[item_id]
    positive = item_id in pos_ids
    baseline = _review_row(c)
    # Daily post rows deliberately omit version/abstract; source_hash still binds both.
    visible_fields = ('id', 'title', 'links', 'published', 'updated', 'hf_daily_dates') if c['kind'] in ('post', 'release') else ('id', 'title', 'arxiv_id', 'version', 'published', 'updated', 'hf_daily_dates', 'abstract', 'links', 'summary_zh', 'summary_en')
    rc = {k: r.get(k) == baseline.get(k) for k in visible_fields} 
    rc.update(current_source_hash=r['source_hash'] == proposal['source_hash'] == source_hash(c), inventory_source_hash=source_hash(c) == inv['canonical_source_hash'], first_seen_preserved=proposal['first_seen_preserved'] == c.get('first_seen') == inv['canonical_snapshot'].get('first_seen'), edition_and_review_dates=proposal['edition_date'] == '2026-11-17' and proposal['reviewed_on'] == '2026-11-18', historical_section=r['daily_section'] == 'historical', no_catalog_promotion=r['promote_to_repo'] is False, decision=r['decision'] == ('backlog' if positive else 'reject'))
    approval = proposal['owner_scope_approval']
    owner_checks = None
    if approval:
        old = owner['items'][approval['index']]
        owner_checks = dict(file_sha256=sha(owner_path) == approval['sha256'], exact_owner_record=old == approval['receipt'], same_identity_and_hash=old['id'] == item_id and old['source_hash'] == proposal['source_hash'], scope=old['scope_decision'] == ('approved_for_harness_scope' if positive else 'rejected_from_harness_scope'))
        rc['owner_scope_receipt'] = all(owner_checks.values())
    else:
        rc['no_false_individual_owner_approval'] = positive and bool(proposal['authorization_when_no_item_scope_receipt'])
    refs = proposal['prior_review_records'] if positive else [x['reference'] for x in proposal['prior_review_records']]
    prior_checks = [{**ref, 'passed': sha(ref['path']) == ref['sha256'] and previous(ref)['id'] == item_id} for ref in refs]
    rc['prior_review_hash_identity'] = all(x['passed'] for x in prior_checks)
    source_receipts = [proposal['source']] if positive else proposal['source_receipts']
    source_checks = []
    for src in source_receipts:
        source_checks.append({k: src[k] for k in ('source_file', 'source_sha256', 'text_file', 'text_sha256')})
        source_checks[-1]['checks'] = dict(raw_hash=sha(src['source_file']) == src['source_sha256'], text_hash=sha(src['text_file']) == src['text_sha256'], byte_length=Path(src['source_file']).stat().st_size == src['bytes'], http_success=src['http_status'] == 200 and src['status'] == 'ok')
    rc['current_source_checks'] = all(all(x['checks'].values()) for x in source_checks)
    quote_checks = []
    for q in proposal['quote_checks']:
        path = q['source_file'] if positive else q['new_text_path']
        digest = q['source_sha256'] if positive else q['new_text_sha256']
        abstract_only = (positive and q['match'] == 'exact_canonical_official_abstract_wording_on_unchanged_owner_hash') or (not positive and q['check_scope'] == 'canonical_official_abstract_only')
        text = c['abstract'] if abstract_only else Path(path).read_text()
        norm, quote = normalized_whitespace(text), normalized_whitespace(q['quote'])
        quote_checks.append(dict(kind=q.get('kind') or q.get('check_scope'), source_file=path, source_sha256=digest, quote_sha256=hashlib.sha256(q['quote'].encode()).hexdigest(), passed=sha(path) == digest and quote in norm, normalized_offset=norm.find(quote), source_scope='canonical_official_abstract' if abstract_only else 'restored_source_text'))
    rc['quote_checks'] = all(x['passed'] for x in quote_checks)
    record = dict(id=item_id, title=c['title'], decision=r['decision'], row_json_sha256=jsha(r), checks=rc, owner_scope_checks=owner_checks, prior_review_checks=prior_checks, source_checks=source_checks, quote_checks=quote_checks, formal_publication_pending=True)
    if positive:
        guard = check_summary(c['title'], c['abstract'], **r['summary_override'])
        rc.update(exact_summary=r['summary_override'] == proposal['summary_override'], exact_direction=r['direction_override'] == proposal['direction_override'], exact_quick=r['evidence_quick'] == proposal['evidence_quick'], numeric_guard=guard['ok'], quick_guard=enforce_evidence(c['abstract'], r['evidence_quick']) == r['evidence_quick'], current_scope=scope_status(r['direction_override'], load_scope(Path('.'))) == 'in_scope')
        if item_id in provenance:
            hashes = [x['sha256'] for x in provenance[item_id]['body_receipt']['attempts'] if x.get('sha256')]
            binding = dict(path=str(prov_path), sha256=sha(prov_path), field='items[id].body_receipt.attempts[].sha256')
        else:
            hashes = [x['sha256'] for x in previous(refs[0])['source_quotes'] if x['kind'] == 'official_full_text']
            binding = dict(path=refs[0]['path'], sha256=refs[0]['sha256'], field='items[index].source_quotes[kind=official_full_text].sha256')
        rc['raw_equals_historical'] = source_receipts[0]['source_sha256'] in hashes
        record.update(historical_raw_binding=binding, historical_raw_sha256s=hashes, summary_guard=guard, summary_override=r['summary_override'], direction_override=r['direction_override'], evidence_quick=r['evidence_quick'], semantic_review='Source passages independently read for modification object, feedback, retention, summary meaning and stated limitations; corrected or qualified claims recorded below.')
    else:
        rc.update(explicit_scope_reason=bool(proposal['reason_zh']) and proposal['reason_zh'] in r['note'], numeric_recertification_not_claimed=proposal['numeric_audit_recertified'] is False)
        record.update(semantic_review=proposal['reason_zh'], reading_scope=proposal['reading_scope'], source_counterevidence=proposal['limitations_zh'])
    records.append(record)
check('19_inclusion_checks', all(all(r['checks'].values()) for r in records if r['decision'] == 'backlog'))
check('10_exclusion_checks', all(all(r['checks'].values()) for r in records if r['decision'] == 'reject'))
amendment_checks = []
for filename in ('positive-amendment-v2.json', 'positive-amendment-v3.json', 'positive-amendment-v4.json'):
    amendment = json.loads((HIST / filename).read_text())
    check(filename + '_prior_immutable', sha(amendment['base']['path']) == amendment['base']['sha256'])
    for edit in amendment['amendments']:
        for q in edit.get('source_quotes', []):
            selector = q.get('id') or q.get('selector')
            soup = BeautifulSoup(Path(edit['source_file']).read_text(), 'html.parser')
            element = soup.find(id=selector)
            passed = element is not None and normalized_whitespace(element.get_text(' ', strip=True)) == normalized_whitespace(q['quote'])
            amendment_checks.append(dict(id=edit['id'], source_file=edit['source_file'], source_sha256=sha(edit['source_file']), selector=selector, quote_sha256=hashlib.sha256(q['quote'].encode()).hexdigest(), passed=passed))
check('amendment_exact_html_passages', all(x['passed'] for x in amendment_checks), count=len(amendment_checks))
proposal = next(r for r in exc['items'] if r['id'] == 's2:c9b9cd5e0b6447a180914049754459b00b3cf264')
preprint, journal = [json.loads(Path(x['source_file']).read_text())['message'] for x in proposal['source_receipts']]
check('preprint_reciprocal_identity_and_dates', preprint['DOI'] == '10.31234/osf.io/meuyq_v2' and journal['DOI'] == '10.1016/j.cobeha.2026.101684' and preprint['DOI'] in str(journal['relation']) and journal['DOI'] in str(preprint['relation']) and preprint['published']['date-parts'] == [[2026, 9, 24]] and journal['published']['date-parts'] == [[2026, 12]])
check('hse_corrected_improver', rows['arxiv:2610.35616']['direction_override'] == {'primary': 'harness', 'secondary': ['meta'], 'harness_sub': 'improver'})
check('rsiv_public_discrepancy', all(t in rows['arxiv:2610.35316']['summary_override']['summary_en'] for t in ('overall-results table', 'inconsistent baseline')))
check('no_new_paid_or_github_claims', pos['paid_requests'] == 0 and all(r['paid_requests'] == 0 for r in exc['items']) and all(r['github_writes'] == 0 and r['canonical_writes'] == 0 and r['publication_claimed'] is False for r in pos['items'] + exc['items']))
failures = [c for c in checks if not c['passed']]
bad_rows = [{'id': r['id'], 'failed': [k for k, v in r['checks'].items() if not v]} for r in records if not all(r['checks'].values())]
if failures or bad_rows:
    print(json.dumps(dict(failures=failures, rows=bad_rows, amendments=[x for x in amendment_checks if not x['passed']]), ensure_ascii=False))
    raise SystemExit(1)
semantics = {
    '2610.37905': 'FilingLoop uses prior scored batches and later unattempted cases; online feedback is not independent held-out evaluation.',
    '2610.38392': 'Mostly imposed deletion pressure; safety-gate result is not a deployment failure-frequency estimate.',
    '2610.39122': 'Skill and RL branches are separate experiments, not joint coevolution.',
    '2610.39358': 'Closed-loop policy plus skill updates qualify as coevolution; diagnostic-only experiment freezes skills.',
    '2610.39508': 'SkillCompiler development viewed held-out failures despite frozen test assets.',
    '2610.25568': '83 of 89 and 93.26 percent concern the complete configuration, not isolated instruction-evolution causality.',
    '2610.27889': 'pass@1 advantage reversal is limited to observed settings and budgets.',
    '2610.33487': 'OC-NaVQA Table2 supports 33.10 to 24.72 m; matched_budget refers only to online budget, excluding separate exploration/development cost.',
    '2610.34938': 'S3.p1/p5: 11 evaluated retro-derived adaptations plus one author-written comparison, not 12 solely retro-derived.',
    '2610.28282': 'Validated Skills, executable Tools and local toolchains persist into later harness states.',
    '2610.36826': 'Rubric-harness coevolution keeps task objective fixed; it is not model-weight coevolution.',
    '2610.31789': '93-95 percent first-warm-attempt success denominator is tasks previously solved cold; it excludes cold-unsolved tasks.',
    '2610.32813': 'Runtime decision reuse and companion configuration RSI are separate; full integrated gain does not isolate a component.',
    '2610.35616': 'Writer/evaluator rules and evidence weights evolve in training and transfer forward; target adaptation freezes these rules.',
    '2610.36188': 'Verified PR and CI outcomes revise skill procedures; produced repository code alone is not the Harness claim.',
    '2610.32026': 'Prompt/playbook/library/cadence are inherited; matched-budget inheritance control absent and held-out description accessed. No universal monotonic improvement claim.',
    '2610.29121': '87.0 and 84.2 percent are returned-node held-out scores, not proportions of nodes. Readout is fixed after fitting.',
    '2610.35051': 'Versioned harness with active simulation exploration; fewer rollouts does not establish equal total budgets.',
    '2610.35316': 'Table3 static executability64.98 versus Table4 H0 51.36 unresolved; +28.02 is expressly bound to Table3. Public discrepancy retained, source numbers not altered.'}
for record in records:
    if record['id'] in pos_ids:
        record['semantic_review'] = semantics[record['id'].split(':', 1)[1]]
inputs = dict(positive_proposals=pos_path, positive_rows=HIST / 'positive-review-rows-v4.yaml', exclusions=exc_path, exclusion_rows=HIST / 'exclusion-review-rows-v1.yaml', amendment_v2=HIST / 'positive-amendment-v2.json', amendment_v3=HIST / 'positive-amendment-v3.json', amendment_v4=HIST / 'positive-amendment-v4.json', historical_inventory=inv_path, owner_scope=owner_path, historical_raw_provenance=prov_path, taxonomy=Path('feed/taxonomy.yaml'), quick_policy=Path('feed/prompts/evidence.md'))
result = dict(schema='follow-rsi.publication-crosscheck.v1', reviewed_at=datetime.now(timezone.utc).isoformat(), reviewer='nov18_hf17_crossreview', status='pass', scope='19 current historical inclusion suggestions and10 historical exclusions. Remaining92 dispositions and exact final Nov17 YAML require separate receipts.', scope_boundaries=dict(experimental_replication=False, full_experimental_number_recalculation=False, new_paid_requests=0, source_network_requests=0, owner_human_per_paper_reading=False, github_ci=False, pages_deployment=False), canonical_sha256=sha('data/feed/items.jsonl'), inputs={k: dict(path=str(v), sha256=sha(v)) for k, v in inputs.items()}, counts=dict(check_groups=len(checks), failed_groups=0, inventory=121, actionable=29, inclusions=19, exclusions=10, prior_owner_scope_inclusions=14, prior_owner_scope_exclusions=10, standing_authorization_inclusions=5, restored_source_receipts=sum(len(r['source_checks']) for r in records), source_quote_checks=sum(len(r['quote_checks']) for r in records), amendment_paragraphs=len(amendment_checks), remaining_dispositions_not_checked=92), checks=checks, items=records, amendment_quote_checks=amendment_checks)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
OUT.with_suffix('.md').write_text('# 历史可行动条目独立交叉检查 v1\n\n19 条纳入建议、10 条排除建议通过 ' + str(len(checks)) + ' 组检查，绑定 positive-proposals-v4 与 exclusion-proposals-v1。19 个恢复正文原始 SHA 均与旧审核相同，当前来源、摘要、分类、canonical hash、owner scope 回执及原引句逐项核对。\n\n更正：Phronix 的 93–95% 仅针对冷启动已解决任务；retro 评估对象含作者另写对照；HSE 改为 harness/improver + meta；Budgeted RSI 的 87.0% 是返回节点留出得分。RSIV 公开摘要保留两表基线不一致，未改源数字；ReSight 预算标签仅指在线预算。\n\n本回执不代表实验复现、全表重算、人工逐篇批准或已发布。剩余 92 条处置及最终 11 月 17 日审核稿另行绑定。\n')
print(json.dumps(dict(path=str(OUT), sha256=sha(OUT), counts=result['counts']), ensure_ascii=False))
