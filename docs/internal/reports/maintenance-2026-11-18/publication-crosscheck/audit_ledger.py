"""Independent frozen crosscheck of historical recovery states, without applying them."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import gzip
import hashlib
import json
import yaml

from scripts.feed.review import source_hash

BASE = Path('docs/internal/reports/maintenance-2026-11-18')
RAW = Path('data/feed/raw/maintenance-2026-11-18')
OUT = BASE / 'publication-crosscheck/historical-ledger-v1.json'
assert not OUT.exists()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def jsha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def gzrows(path):
    return list(map(json.loads, gzip.open(path, 'rt')))


ledger_path = RAW / 'historical-disposition/disposition-ledger-v2.jsonl.gz'
old_ledger_path = RAW / 'historical-disposition/disposition-ledger-v1.jsonl.gz'
inventory_path = RAW / 'backlog-audit/pr135-historical-inventory-v1.jsonl.gz'
carry_path = RAW / 'backlog-audit/pr135-carryforward-v1.jsonl.gz'
original_path = RAW / 'backlog-audit/pr135-original-v1.yaml.gz'
summary_path = BASE / 'historical-disposition/disposition-summary-v2.json'
positive_path = BASE / 'historical-disposition/positive-proposals-v4.json'
exclusion_path = BASE / 'historical-disposition/exclusion-proposals-v1.json'
ledger_list = gzrows(ledger_path)
ledger = {r['id']: r for r in ledger_list}
old_ledger = {r['id']: r for r in gzrows(old_ledger_path)}
inventory_list = gzrows(inventory_path)
inventory = {r['id']: r for r in inventory_list}
carry_list = gzrows(carry_path)
carry = {r['id']: r for r in carry_list}
original = yaml.safe_load(gzip.open(original_path, 'rt'))
canonical = {r['id']: r for r in map(json.loads, Path('data/feed/items.jsonl').read_text().splitlines())}
positive = {r['id']: r for r in json.loads(positive_path.read_text())['items']}
exclusion = {r['id']: r for r in json.loads(exclusion_path.read_text())['items']}
actionable = set(positive) | set(exclusion)
summary = json.loads(summary_path.read_text())
owner_path = Path('review/approvals/2026-11-02.yaml')
owner = yaml.safe_load(owner_path.read_text())
catalog = {r['id']: r for r in yaml.safe_load(Path('data/papers.yaml').read_text())['papers']}
checks = []
records = []
cached = {}
reference_files = {}


def check(name, passed, **detail):
    checks.append(dict(check=name, passed=bool(passed), **detail))


def saved_record(ref):
    path = ref['path']
    if path not in cached:
        value = Path(path).read_text()
        cached[path] = list(map(json.loads, value.splitlines())) if path.endswith('.jsonl') else json.loads(value)
        reference_files[path] = dict(path=path, sha256=sha(path))
    container = cached[path]
    if 'index' in ref:
        return (container[ref['collection']] if ref['collection'] else container)[ref['index']]
    return next(r for r in container['items'] if r['id'] == ref['id'])


check('ledger_exact_frozen_hash', sha(ledger_path) == '1e37b9d95567d7ec7fa8616ae5ae7a2564c9dce7987887cac3e5ff18fcc6a004')
check('all_121_unique_ids_preserved', len(ledger_list) == len(ledger) == len(inventory) == len(carry) == 121 and set(ledger) == set(inventory) == set(carry))
check('summary_input_and_ledger_hashes', all(sha(r['path']) == r['sha256'] for r in summary['inputs']) and sha(ledger_path) == summary['ledger']['sha256'] and hashlib.sha256(gzip.decompress(ledger_path.read_bytes())).hexdigest() == summary['ledger']['uncompressed_sha256'])
check('29_actionable_92_keep', len(actionable) == 29 and sum(r['skip_apply_when_no_new_adjudication'] for r in ledger_list) == 92)
check('original_queue123', len(original['items']) + len(original['lab_updates']) == 123)
for item_id, row in ledger.items():
    inv, old, c = inventory[item_id], old_ledger[item_id], canonical[item_id]
    snapshot = inv['canonical_snapshot']
    review = snapshot['review']
    rc = dict(
        original_review_object=row['canonical_review_before'] == review,
        original_review_hash=row['canonical_review_before_sha256'] == jsha(review),
        current_review_unchanged_at_audit=c.get('review') == review,
        source_hash=row['canonical_source_hash_at_archive'] == inv['canonical_source_hash'] == source_hash(c) == source_hash(snapshot),
        first_seen=row['first_seen_preserved'] == c['first_seen'] == snapshot['first_seen'],
        dated='2026-11-18' == row['date_checked'],
        preserve_review_instruction=row['do_not_rewrite_old_review_to_today_defer'] is True,
        no_mutation_claim=row['canonical_writes'] == row['github_writes'] == 0 and row['new_formal_decision_written'] is False and row['new_publication_claimed'] is False,
        recoverable_reason=bool(row['reason_zh']) and bool(row['next_action_zh']) and bool(row['issue_refs']),
        existing_provenance=all(row['existing_formal_review'][key] == review.get(key) for key in ('decision', 'date', 'reviewed_on', 'github_pr', 'owner_login', 'merge_commit', 'source_hash')),
    )
    arc, cf = row['archive_reference'], row['original_carryforward_reference']
    rc['archive_reference'] = sha(arc['path']) == arc['sha256'] and inventory_list[arc['index']] == inv
    rc['carryforward_reference'] = sha(cf['path']) == cf['sha256'] and carry_list[cf['index']] == carry[item_id]
    ref = row['original_queue_reference']
    rc['original_queue_reference'] = hashlib.sha256(gzip.decompress(Path(ref['path']).read_bytes())).hexdigest() == ref['uncompressed_sha256'] and original[ref['field']][ref['index']] == inv['original_queue_row'] and inv['original_queue_row']['id'] == item_id
    preserve_fields = ('owner_scope_receipt', 'post_approval_correction', 'saved_review_evidence', 'catalog_entry', 'issue_refs', 'scope_recommendation', 'historical_rounds_reported', 'reading_levels_reported')
    rc['carryforward_evidence_preserved'] = all(row.get(k) == carry[item_id].get(k) for k in preserve_fields)
    reference_checks = []
    for evidence in row['saved_review_evidence']:
        ref = evidence['reference']
        reference_checks.append(dict(reference=ref, passed=sha(ref['path']) == ref['sha256'] and saved_record(ref) == evidence['saved_review_record']))
    rc['saved_evidence_exact'] = all(r['passed'] for r in reference_checks)
    receipt = row['owner_scope_receipt']
    if receipt:
        rc['owner_receipt_exact'] = sha(receipt['path']) == receipt['sha256'] and owner['items'][receipt['index']] == receipt['receipt'] and receipt['receipt']['id'] == item_id
        rc['owner_hash_match_flag'] = receipt['exact_hash_matches_current'] == (receipt['receipt']['source_hash'] == source_hash(c))
    correction = row['post_approval_correction']
    if correction:
        rc['post_approval_correction_exact'] = sha(correction['path']) == correction['sha256'] and owner['post_approval_corrections'][correction['index']] == correction['correction'] and correction['correction']['id'] == item_id
    ignore = {'ledger_amendment_v2'}
    if item_id in positive:
        ignore.add('proposal_reference')
        ignore.add('previous_proposal_reference')
        previous = row['previous_proposal_reference']
        rc['v2_preserves_old_proposal_reference'] = previous == old['proposal_reference'] and sha(previous['path']) == previous['sha256']
    rc['v2_only_expected_delta'] = {k: v for k, v in row.items() if k not in ignore} == {k: v for k, v in old.items() if k not in ignore}
    if item_id in actionable:
        p = positive.get(item_id) or exclusion[item_id]
        ref = row['proposal_reference']
        rc['actionable_proposal_bound'] = sha(ref['path']) == ref['sha256'] and ref['id'] == item_id and row['source_hash'] == source_hash(c) and row['decision_suggestion'] == p['decision_suggestion'] and row['skip_apply_when_no_new_adjudication'] is False
        rc['await_dated_apply'] = row['canonical_apply_recommendation'] == 'apply_source_bound_suggestion_after_true_dated_merge'
    else:
        rc['no_blanket_new_defer'] = row['skip_apply_when_no_new_adjudication'] is True and row['canonical_apply_recommendation'] == 'keep_canonical_review_unchanged' and row['decision_suggestion'] is None
        if row['current_work_status'] == 'existing_catalog_entry_retained':
            entry = row['catalog_entry']
            cat = catalog[entry['id']]
            rc['catalog_identity_and_classification'] = cat['arxiv'] == item_id.split(':', 1)[1] and all(cat.get(k) == entry.get(k) for k in ('id', 'scope', 'section', 'must_read'))
    records.append(dict(id=item_id, source_hash=row['canonical_source_hash_at_archive'], prior_review_sha256=row['canonical_review_before_sha256'], current_work_status=row['current_work_status'], work_category=row['work_category'], decision_suggestion=row['decision_suggestion'], skip_apply=row['skip_apply_when_no_new_adjudication'], ledger_record_sha256=jsha(row), checks=rc, evidence_reference_checks=reference_checks))
check('all121_row_checks', all(all(r['checks'].values()) for r in records))
actual_categories = dict(Counter(r['work_category'] for r in ledger_list if r['skip_apply_when_no_new_adjudication']))
check('category_counts', actual_categories == summary['non_actionable_work_category_counts'] == {'editorial_not_external_blocker': 56, 'bounded_review_evidence': 14, 'already_cataloged_no_new_publication_claim': 8, 'item_specific_artifact_evidence_gap': 3, 'external_source_access_blocker': 3, 'item_specific_scope_evidence_gap': 7, 'post_approval_counterevidence': 1})
ada = ledger['arxiv:2610.33245']
check('adapra_later_counterevidence_precedence', ada['current_work_status'] == 'post_approval_counterevidence_retained' and ada['post_approval_correction']['correction']['effective_decision'] == 'defer' and '在线 rubric' in ada['classification_precedence_note'] and ada['skip_apply_when_no_new_adjudication'])
rsi = ledger['arxiv:2610.32253']
check('rsihub_current_evaluation_route', rsi['catalog_entry']['scope'] == 'harness_eval' and rsi['catalog_entry']['section'] == 'evaluation' and 'harness_eval/framework' in rsi['classification_precedence_note'])
failures = [r for r in checks if not r['passed']]
bad_rows = [dict(id=r['id'], failed=[k for k, v in r['checks'].items() if not v]) for r in records if not all(r['checks'].values())]
if failures or bad_rows:
    print(json.dumps(dict(failures=failures, rows=bad_rows), ensure_ascii=False))
    raise SystemExit(1)
paths = [ledger_path, old_ledger_path, inventory_path, carry_path, original_path, summary_path, positive_path, exclusion_path, owner_path, Path('data/papers.yaml')]
result = dict(schema='follow-rsi.publication-crosscheck.v1', reviewed_at=datetime.now(timezone.utc).isoformat(), reviewer='nov18_hf17_crossreview', status='pass', scope='All121 recovery-state records checked against exact archived canonical review, current source_hash, original PR135 row, preserved evidence, owner receipts and corrections; this is not a new scientific fulltext audit of the92 retained rows.', canonical_sha256=sha('data/feed/items.jsonl'), inputs=[dict(path=str(p), sha256=sha(p)) for p in paths], evidence_files=list(reference_files.values()), counts=dict(check_groups=len(checks), rows=121, actionable=29, keep_original_review=92, source_paid_requests=0, network_requests=0), remaining_categories=actual_categories, checks=checks, items=records, limitations=['The56 editorial items still need recorded editorial/source-binding work; they are not external access failures.', '14 bounded reviews remain bounded; no new fulltext exclusion is claimed.', '8 existing catalog entries are preserved without a new publication claim.', '10 specific evidence gaps,3 external source failures and1 later counterevidence remain individually recoverable.', 'No canonical edit, GitHub merge or public deployment was performed by this reviewer.'])
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
OUT.with_suffix('.md').write_text('# 历史 121 条可恢复状态独立核对\n\n全部 121 个稳定 ID、原 canonical.review 对象及哈希、first_seen、source_hash、原 PR135 行、旧审核引用与 owner 纠正均核对通过。19 条纳入与 10 条排除可进入真实日期审核应用；其余 92 条必须保留原决定，不能批量重写为今天 defer。\n\n92 条分为：56 条编辑整理、14 条有界初筛、8 条既有目录、10 条具体证据缺口、3 条外部来源失败、1 条后续反证。56 条编辑工作不是外部阻塞，也不称已完成正式处置。AdaPRA 后续纠正优先，RSIHub 保留 harness_eval/evaluation 分类。\n\n这是状态与引用完整性核对，不是对全部 92 篇新增全文审核或实验数字重算，也不是合并或上线凭据。\n')
print(json.dumps(dict(path=str(OUT), sha256=sha(OUT), counts=result['counts']), ensure_ascii=False))
