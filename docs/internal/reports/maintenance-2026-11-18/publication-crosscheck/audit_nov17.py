"""Bind the exact final Nov17 review to independent source and disposition receipts."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import gzip
import hashlib
import json
import yaml
from bs4 import BeautifulSoup

from scripts.feed.review import source_hash, _review_row
from scripts.feed.guard import normalized_whitespace

BASE = Path('docs/internal/reports/maintenance-2026-11-18')
OUT = BASE / 'publication-crosscheck/nov17-formal-review-v1.json'
REVIEW = Path('review/daily/2026-11-17.yaml')
assert not OUT.exists()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def jsha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


doc = yaml.safe_load(REVIEW.read_text())
rows_list = doc['items'] + doc['lab_updates']
rows = {r['id']: r for r in rows_list}
canonical = {r['id']: r for r in map(json.loads, Path('data/feed/items.jsonl').read_text().splitlines())}
preflight_path = BASE / 'primary-review/review-2026-11-17-final-preflight.json'
preflight = json.loads(preflight_path.read_text())
ledger_path = Path('data/feed/raw/maintenance-2026-11-18/historical-disposition/disposition-ledger-v2.jsonl.gz')
ledger = {r['id']: r for r in map(json.loads, gzip.open(ledger_path, 'rt'))}
old_path = Path('data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-original-v1.yaml.gz')
old_doc = yaml.safe_load(gzip.open(old_path, 'rt'))
old = {r['id']: r for r in old_doc['items'] + old_doc['lab_updates']}
hf_path = BASE / 'independent-hf17/final-scope-review.json'
hf = {r['id']: r for r in json.loads(hf_path.read_text())['records']}
adjudication_path = BASE / 'primary-review/final-adjudication.json'
adjudication_doc = json.loads(adjudication_path.read_text())
adjudication = {r['id']: r for r in adjudication_doc['items'] if r['edition_date'] == '2026-11-17'}
hist = BASE / 'historical-disposition'
positive_rows = yaml.safe_load((hist / 'positive-review-rows-v4.yaml').read_text())['items']
exclusion_rows = yaml.safe_load((hist / 'exclusion-review-rows-v1.yaml').read_text())['items']
proposed = {r['id']: r for r in positive_rows + exclusion_rows}
apply_ids = set(preflight['apply_ids'])
keep_ids = {i for i, r in ledger.items() if r['skip_apply_when_no_new_adjudication']}
post_ids = {'post:https://openai.com/index/step-toward-defining-the-standard-model', 'post:https://openai.com/index/our-new-blog-for-science'}
checks, row_checks, post_checks = [], [], []


def check(name, passed, **detail):
    checks.append(dict(check=name, passed=bool(passed), **detail))


check('exact_final_yaml', sha(REVIEW) == preflight['sha256'] == '712e78839a8defa5fece54961a323ce4a11bb3d0c02d6ae3642fc4efabd44e06')
check('date_and_actual_review_date', doc['date'] == preflight['date'] == '2026-11-17' and doc['reviewed_on'] == preflight['reviewed_on'] == '2026-11-18')
check('164_distinct_115papers49posts', len(rows_list) == len(rows) == 164 and len(doc['items']) == 115 and len(doc['lab_updates']) == 49)
check('decision_counts', dict(Counter(r['decision'] for r in rows_list)) == preflight['counts'] == {'backlog': 19, 'reject': 53, 'defer': 92})
check('original123_plus_new41', len(old) == 123 and set(old) <= set(rows) and set(rows) - set(old) == set(hf) and len(hf) == 41)
check('all121_history_retained', set(ledger) == set(old) - post_ids and set(ledger) <= set(rows))
check('apply72_only_precise_set', len(apply_ids) == 72 and apply_ids == set(hf) | set(proposed) | post_ids and apply_ids.isdisjoint(keep_ids))
check('skip92_preserve_original', set(preflight['skip_existing_review_ids']) == keep_ids and keep_ids == {r['id'] for r in rows_list if r['decision'] == 'defer'})
check('29_exact_final_suggestions', all(rows[i] == row for i, row in proposed.items()))
check('frozen_historical_receipts', sha(BASE / 'publication-crosscheck/historical-actionable-v1.json') == 'bb1a776e3463c6c648f9852a508d758d1885d71f83c5e87a7881ebcaef0a880d' and sha(BASE / 'publication-crosscheck/historical-ledger-v1.json') == 'c9b38f5c853e756a8f30b48dcda0b2237d0c105e453887335b7a3c958fbf2c84')
check('hf_frozen_independent_review', sha(hf_path) == 'd58b93b6ea646f2867ea744c58bb9db1163002e395d161b6daf125f32d4de25b' and set(adjudication) == set(hf))
for item_id, row in rows.items():
    c = canonical[item_id]
    baseline = _review_row(c)
    fields = ('id', 'title', 'published', 'updated', 'links', 'hf_daily_dates')
    rc = dict(source_hash=row['source_hash'] == source_hash(c), visible_identity_dates=all(row.get(k) == baseline.get(k) for k in fields))
    for k in ('arxiv_id', 'version', 'abstract', 'summary_zh', 'summary_en'):
        if k in row:
            rc[k] = row[k] == baseline[k]
    if item_id in keep_ids:
        state = ledger[item_id]
        rc.update(
            prior_canonical_review_unchanged=c['review'] == state['canonical_review_before'],
            first_seen=c['first_seen'] == state['first_seen_preserved'],
            no_apply='本行不重新apply' in row['note'] and item_id not in apply_ids,
            reasons_preserved=all(r in row['note'] for r in state['reason_zh']),
            next_step_and_issue=state['next_action_zh'] in row['note'] and all(i['url'] in row['note'] for i in state['issue_refs']),
            remains_historical=row['daily_section'] == 'historical',
        )
    elif item_id in hf:
        evidence = hf[item_id]
        final = adjudication[item_id]
        rc.update(
            exact_independent_evidence=final['evidence'] == evidence,
            decision_agreement=row['decision'] == final['decision'] == evidence['suggestion'] == 'reject',
            reason_preserved=final['reason'] == evidence['reason_zh'] and evidence['reason_zh'] in row['note'],
            source_binding=final['source_hash'] == row['source_hash'],
            observed_hf_date='2026-11-17' in row['hf_daily_dates'] and row['news_date'] == evidence['hf_date'] == '2026-11-17',
            original_and_version_dates=row['published'] == evidence['published_original'] and row['updated'] == evidence['version_updated'],
            actual_review_date=final['reviewed_on'] == evidence['reviewed_on'] == '2026-11-18',
            no_publishable_positive_summary=row['summary_override'] is None,
        )
    row_checks.append(dict(id=item_id, decision=row['decision'], apply=item_id in apply_ids, row_json_sha256=jsha(row), checks=rc))
check('all164_source_date_and_disposition_bindings', all(all(r['checks'].values()) for r in row_checks))

source_index_path = Path('docs/internal/reports/maintenance-2026-11-16/source-evidence-index.json')
source_index = {r['id']: r for r in json.loads(source_index_path.read_text())['records']}
earlier_post_path = BASE / 'independent-recovery/review-findings-final.json'
earlier_posts = {r['id']: r for r in json.loads(earlier_post_path.read_text())['items'] if r['id'] in post_ids}
quotations = {
    'step-toward-defining-the-standard-model': [
        'In an October preprint',
        'I proposed a candidate definition on a lattice—a grid representing spacetime.',
        'Developing this refinement strategy into a proof required several rounds of work with Astra and discussions with outside experts.',
        'The method that Astra and I proposed is far more an answer in principle than an answer in practice; much work lies ahead to make it useful for realistic lattice simulations.',
    ],
    'our-new-blog-for-science': [
        'We’re starting the OpenAI science blog to give scientists and academic researchers a place to share what they’re discovering with AI and how they’re doing the work.',
        'Methods and practical guidance: Examples of how scientists use our models for tasks such as scientific computing, data analysis, exploring literature, and planning experiments.',
    ],
}
for item_id in sorted(post_ids):
    row, c, source = rows[item_id], canonical[item_id], source_index[item_id]
    text_path = Path(source['text_path'])
    raw_path = Path(source['fulltext_body_path'])
    text = normalized_whitespace(text_path.read_text())
    slug = item_id.rsplit('/', 1)[1]
    spans = [dict(quote=q, normalized_start=text.find(normalized_whitespace(q)), exact_normalized_match=normalized_whitespace(q) in text) for q in quotations[slug]]
    raw = BeautifulSoup(raw_path.read_text(), 'html.parser')
    h1 = raw.find('h1')
    rc = dict(
        raw_hash=sha(raw_path) == source['fulltext_body_sha256'],
        text_hash=sha(text_path) == source['text_sha256'],
        h1_identity=h1 is not None and normalized_whitespace(h1.get_text(' ', strip=True)) == c['title'],
        source_hash=source['source_hash_of_proposed_record'] == source_hash(c) == row['source_hash'],
        publish_date=c['published'] == source['published_as_proposed'] and 'November 15, 2026' in text,
        version_unknown=c['version'] == 0 and c['updated'] == source['updated_as_proposed'] == '',
        first_seen=c['first_seen'] == source['first_seen'] == '2026-11-16T00:03:29.529056+00:00',
        reject_unchanged=row == old[item_id] and row['decision'] == 'reject',
        previous_independent_review=earlier_posts[item_id]['canonical_source_hash'] == source_hash(c) and earlier_posts[item_id]['scope_agrees'] is True,
        exact_source_spans=all(s['exact_normalized_match'] for s in spans),
        no_hf_redating=row['hf_daily_dates'] == [] and row['daily_section'] == 'historical',
    )
    interpretation = '正文多轮讨论与改进的是候选粒子物理构造和证明。没有给出反馈编辑并跨任务继承 Agent 自身 Harness 的机制；原排除成立。不核验物理证明，也不把引用的10月预印本或背景结果当新论文。' if slug.startswith('step-') else '全文为科学博客开栏及既有科学案例汇总。没有提出或测试反馈驱动的可复用 Harness 修改；原排除成立。不将背景研究数字及链接转成新论文或重新验证的科学结论。'
    post_checks.append(dict(id=item_id, decision='reject', review_scope='Saved complete official article text independently read for source identity and Harness scope; no linked-paper proof or experimental-number audit.', interpretation_zh=interpretation, source=dict(raw_path=str(raw_path), raw_sha256=sha(raw_path), text_path=str(text_path), text_sha256=sha(text_path)), spans=spans, checks=rc))
check('two_original_post_rejects_source_scope', all(all(r['checks'].values()) for r in post_checks))
check('quality_warning_not_recast_as_pass', adjudication_doc['global_quality_warning'] == {'date': '2026-11-05', 'complete': False, 'recall': 0.892857, 'threshold': 0.9} and adjudication_doc['model_quality_evaluation_not_rerun'] is True and adjudication_doc['paid_model_calls'] == 0)
check('adapra_and_rsihub_corrections_preserved', rows['arxiv:2610.33245']['decision'] == 'defer' and '后续反证优先' in rows['arxiv:2610.33245']['note'] and rows['arxiv:2610.32253']['decision'] == 'defer' and 'harness_eval' in rows['arxiv:2610.32253']['note'] and {'arxiv:2610.33245', 'arxiv:2610.32253'} <= keep_ids)
check('source_conflicts_retained_in_hf_notes', all(not r['source_conflicts'] or r['reason_zh'] in rows[i]['note'] for i, r in hf.items()))
failures = [c for c in checks if not c['passed']]
failed_rows = [dict(id=r['id'], failed=[k for k, v in r['checks'].items() if not v]) for r in row_checks + post_checks if not all(r['checks'].values())]
if failures or failed_rows:
    print(json.dumps(dict(failures=failures, rows=failed_rows), ensure_ascii=False))
    raise SystemExit(1)
inputs = [REVIEW, preflight_path, old_path, ledger_path, hist / 'positive-proposals-v4.json', hist / 'positive-review-rows-v4.yaml', hist / 'exclusion-proposals-v1.json', hist / 'exclusion-review-rows-v1.yaml', hf_path, adjudication_path, source_index_path, earlier_post_path, BASE / 'publication-crosscheck/historical-actionable-v1.json', BASE / 'publication-crosscheck/historical-ledger-v1.json']
result = dict(schema='follow-rsi.publication-crosscheck.v1', reviewed_at=datetime.now(timezone.utc).isoformat(), reviewer='nov18_hf17_crossreview', status='pass', review_file=dict(path=str(REVIEW), sha256=sha(REVIEW), date=doc['date'], reviewed_on=doc['reviewed_on']), canonical_sha256=sha('data/feed/items.jsonl'), counts=dict(check_groups=len(checks), rows=164, papers=115, posts=49, apply=72, backlog=19, reject=53, preserve_existing_review=92, hf_nov17_exclusions=41, historical_inclusions=19, historical_exclusions=10, original_post_exclusions=2), inputs=[dict(path=str(p), sha256=sha(p)) for p in inputs], checks=checks, row_checks=row_checks, original_post_crossreview=post_checks, apply_ids=sorted(apply_ids), keep_original_review_ids=sorted(keep_ids), quality_warning=adjudication_doc['global_quality_warning'], evidence_boundaries=dict(network_requests=0, paid_requests=0, full_experimental_number_recalculation=False, physics_proof_validation=False, github_ci_verified_by_this_receipt=False, exact_github_head_verified_by_this_receipt=False, merge_verified_by_this_receipt=False, deployment_verified_by_this_receipt=False), limitations=['This receipt binds the exact saved review YAML and source evidence, not a future GitHub head or CI run.', 'Only72 IDs are eligible for the planned apply after a real dated review merge; all92 carryforward rows must remain unapplied.', 'The121 historical inventory is separate from the129 new-intake reconciliation; historical recoveries are not today\'s new discoveries.', '29 actionable historical decisions are newly adjudicated from saved or restored sources;92 other states retain bounded evidence and prior decisions without a new fulltext audit.'])
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
OUT.with_suffix('.md').write_text('# 11 月 17 日正式审核稿精确复核\n\n绑定 review/daily/2026-11-17.yaml SHA `'+sha(REVIEW)+'`，实际复核日 2026-11-18。164 行为 115 篇论文、49 篇公告；19 backlog、53 reject、92 defer。原 PR135 的 123 行按稳定 ID 全部保留，新加入 41 条真实 HF 11 月 17 日条目。\n\n仅应用 72 条：19 历史纳入、10 历史排除、41 HF 排除、2 原公告排除。92 条不重新 apply，保留原 canonical.review。19 条 v4 摘要/分类与 10 条排除逐字段一致，四项交叉分类和 HSE 改进器纠正有效。两条原公告正文独立读完，分别为外部物理构造/证明与博客开栏，排除成立；不复核物理证明或背景实验数字。\n\n旧质量分数 0.892857 / 阈值 0.90、不完整的告警保留；本次未跑质量模型。此回执不代替真实 PR head、CI、合并和 Pages 上线验证。\n')
print(json.dumps(dict(path=str(OUT), sha256=sha(OUT), counts=result['counts']), ensure_ascii=False))
