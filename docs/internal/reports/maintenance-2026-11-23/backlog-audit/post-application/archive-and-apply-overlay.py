from pathlib import Path
from collections import Counter
from copy import deepcopy
from datetime import datetime,timezone
import json,gzip,shutil,hashlib
from scripts.feed.storage import load_items,write_json
from scripts.feed.review import source_hash
R=Path.cwd(); D=R/'docs/internal/reports/maintenance-2026-11-23'; B=R/'build/maintenance-2026-11-23'; F=D/'publication-final'
assert (F/'generation-receipt.json').is_file()
source=Path('/private/tmp/follow-rsi-2026-11-23-backlog-final'); pre=D/'backlog-audit/pre-application'; pre.mkdir(parents=True,exist_ok=True)
for p in source.iterdir():
    if p.is_file():shutil.copyfile(p,pre/p.name)
rows=[json.loads(l) for l in gzip.open(pre/'backlog-ledger.jsonl.gz','rt')]; items={x['id']:x for x in load_items(R)}
adjud=json.loads((D/'primary-review/final-adjudication.json').read_text()); decisions={x['id']:x for x in adjud['items']}
plan=json.loads((B/'created-review-prs.json').read_text()); verified={x['date']:json.loads((F/f'verified-review-{x["number"]}.json').read_text()) for x in plan}
post=D/'backlog-audit/post-application';post.mkdir(exist_ok=True)
changed=[]; stamp=datetime.now(timezone.utc).isoformat()
for r in rows:
    key=r['id']
    if key not in decisions:continue
    a=decisions[key]; item=items[key]; receipt=verified[a['edition_date']]
    r['pre_application_status']={k:deepcopy(r.get(k)) for k in ('status','processing_bucket','next_actions')}
    r.update(audit_stage='post_application_exact_merged_reviews_not_yet_live',formal_github_head_verified_by_this_audit=True,current_dated_review_receipt=receipt,canonical_source_hash=source_hash(item),first_seen=item['first_seen'],canonical_hf_daily_dates=item.get('hf_daily_dates',[]),canonical_version=item.get('version'),live_publication_verified_by_this_audit=False)
    if a['application']=='apply':
        review=item['review'];assert review['source_hash']==source_hash(item) and review['github_pr']==receipt['github_pr'] and review['merge_commit']==receipt['merge_commit']
        r.update(formal_review=deepcopy(review),formal_review_source_hash_matches=True,formal_content_equivalence_verified=True,formal_hash_rebound_by_this_audit=False,reason_zh=[a['reason']])
        if a['decision']=='reject':
            r.update(status='formally_reviewed_scope_exclusion',processing_bucket='formal_scope_exclusion',next_actions=['仅在来源内容或可核验证据变化时重开逐项范围审核；保留本次来源哈希、排除理由及独立历史意见。'])
        elif a['decision']=='defer':
            r.update(status='formally_reviewed_specific_evidence_pending',processing_bucket='pending_evidence',next_actions=[a['reason']],issue_refs=sorted(set([60]+[x for x in (r.get('issue_refs') or []) if isinstance(x,int)])))
        else:
            path='site/recaps/2026-11-23--2026-11-23.json' if a['decision']=='backlog' else f'site/daily/{a["edition_date"]}.json'
            manifest=json.loads((R/path).read_text());assert key in {x['id'] for x in manifest['items']}
            r.update(status='formally_approved_local_publication_pending_deployment',processing_bucket='formal_or_catalog_record',local_publication_artifacts=[path],next_actions=['出版 PR 经 CI 合并后，核对 Pages 及本条所属公开刊物的精确字节；未完成前不称已上线。'])
    else:
        r['metadata_only_receipts']=deepcopy(item.get('metadata_review_receipts',[]));r['scientific_review_preserved']=True;r['scientific_content_reapproved']=False
        if key in ('arxiv:2611.18856','arxiv:2611.21373'):
            r.update(status='hf_date_metadata_receipted_existing_scientific_review_preserved',formal_review=deepcopy(item.get('review')),formal_review_source_hash_matches=item.get('review',{}).get('source_hash')==source_hash(item),next_actions=['保留旧科学审核和已出版快照；HF 日期元数据回执不构成重新批准或新增出版。'])
        else:
            r.update(status='v2_catalog_wording_correction_merged_pending_live_check',processing_bucket='formal_or_catalog_record',next_actions=['核对现行公开证据卡片的文字和数字与 pinned v2；后续完整版本数值/证明审核另留任务，不声称实验复现。'])
    changed.append(key)
assert len(changed)==238 and len(rows)==9292
payload=''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows).encode()
(post/'backlog-ledger.jsonl.gz').write_bytes(gzip.compress(payload,mtime=0))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary={'stage':'post_application_exact_merged_reviews_not_yet_live','generated_at':stamp,'all_ids':len(rows),'canonical_ids':len(items),'updated_ledger_ids':len(changed),'formal_new_canonical_decisions':dict(Counter(a['decision'] for a in decisions.values() if a['application']=='apply')),'metadata_only_receipts':4,'all_id_buckets':dict(Counter(r['processing_bucket'] for r in rows)),'all_ids_have_specific_recoverable_status':all(r.get('status') and r.get('reason_zh') for r in rows),'old_version_tasks_preserved_exactly':sha(pre/'version-review-tasks.jsonl.gz')==sha(source/'version-review-tasks.jsonl.gz'),'old_historical_model_errors_preserved_exactly':sha(pre/'historical-model-errors.json')==sha(source/'historical-model-errors.json'),'online_verified':False,'ledger_sha256':sha(post/'backlog-ledger.jsonl.gz'),'pre_application_summary_sha256':sha(pre/'summary.json'),'boundaries':['238 rows receive exact merged review receipts; other historical opinions and recoverable work are preserved.','Version-task count is a separate dimension, not a count of unreviewed papers.','No paid-model rerun or experimental replication.','A later live-publication overlay must prove deployment separately.']}
write_json(post/'summary.json',summary)
for p in (B/'pr-audit').glob('pr-*.json'):shutil.copyfile(p,F/p.name)
shutil.copyfile(Path('/private/tmp/follow-rsi-publish-20261123.py'),F/'generate-publication.py')
shutil.copyfile(Path(__file__),post/'archive-and-apply-overlay.py')
(D/'README.md').write_text('''# Follow RSI 2026-11-23 maintenance

All 12 enabled sources were attempted at 15:53–15:58 Asia/Shanghai on November 23. Six complete HF boards contain 152 unique papers: 39/50/50/0/0/13 for November 18–23. The saved source snapshot contains 4,684 occurrences, 4,416 stable IDs, 520 window occurrences and 471 window IDs. Canonical records grew from 2,222 to 2,456 (213 papers and 21 posts). Semantic Scholar traversal is partial after rate limits; unvisited coverage is unknown.

Three-round source-bound review yields 25 delayed daily inclusions (November 18: 7; November 19: 10; November 20: 8), four historical additions, 202 exclusions and three specific evidence deferrals. November 21–23 have substantive status bulletins. The review date is November 23; original publication, version, HF recommendation and first_seen dates are retained. Two existing HF-date metadata receipts and two v2 catalog corrections are separate from new discoveries. The initial November 18 not_ready bulletin and October 27 withdrawal remain recoverable.

The independent pre-application ledger and post-application overlay cover all 9,292 historical stable IDs. All 2,096 saved version tasks and 41 historical model errors are preserved; internal editorial work is not mislabeled as an external blocker. Six older issues retain their individual artifact/evidence gaps, alongside EVA-RSI, DailyBrick and the S2-only truncated survey. Current formal decisions are bound to actual date PRs, exact heads, successful checks, owner identity and merge commits. Standing owner authorization is not a claim of manual owner reading.

W47 contains 32 daily papers, with 33 already-published historical entries separately projected from the hash-bound prior recap. W48 historical additions are separately listed in the November 23 recap. Old scientific approvals are not rebound merely because HF-date metadata changed.

Historical model evaluation remains incomplete: recall 0.892857 versus threshold 0.90. No threshold or pass claim was changed. This maintenance uses zero paid model requests and zero generation tokens; source requests and account-balance checks are different operations. Scope review is not experimental replication.

The generation receipt intentionally says online_verified=false. Successful publication requires the subsequent publication PR, Pages deployment and live-verification receipt. The later final live overlay records this transition without rewriting the earlier evidence boundary.
''')
print(json.dumps(summary,ensure_ascii=False))
