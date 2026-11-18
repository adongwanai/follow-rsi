"""Preserve every original PR135 item, with separate actionable and carryforward states."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT/'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
RAW = ROOT/'data/feed/raw/maintenance-2026-11-18/historical-disposition'
def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def readgz(path):
    with gzip.open(ROOT/path,'rt') as f:
        return list(map(json.loads,f))
ip='data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz'
cp='data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-carryforward-v1.jsonl.gz'
inv={r['id']:r for r in readgz(ip)}
carry=readgz(cp)
positive_name=sys.argv[1]
pp=OUT/positive_name
ep=OUT/'exclusion-proposals-v1.json'
positive={r['id']:r for r in json.loads(pp.read_text())['items']}
exclusion={r['id']:r for r in json.loads(ep.read_text())['items']}
assert len(carry)==len(inv)==121
assert len(positive)==19 and len(exclusion)==10 and not (positive.keys() & exclusion.keys())

worklabels={
 'reusable_inclusion_scope_editorial_preparation':('范围纳入建议已完成，逐篇摘要/原文绑定待整理','editorial_not_external_blocker',
    '复用已保存范围意见；核对该版本的来源、双语摘要、数字语义和证据后，另走真实日期审核，不重跑全量付费模型。'),
 'reusable_exclusion_scope_dated_disposition_pending':('范围排除建议已完成，当前内容绑定/正式处置待整理','editorial_not_external_blocker',
    '复用已保存的排除理由；检查当前源内容与旧引句/独立审核的绑定，补日期处置，勿将 scope receipt 写成已合并决定。'),
 'bounded_source_screen_not_fulltext_exclusion':('有界范围初筛完成，不能称全文排除','bounded_review_evidence',
    '保留该条实际阅读层级与具体不支持理由；若需正式排除，补足当前官方内容和独立复核，不按标题或摘要宣称全文无相关内容。'),
 'existing_catalog_entry_retained':('既有目录条目原样保留','already_cataloged_no_new_publication_claim',
    '保留目录已有分类与阅读路线；目录存在不是本次新审核或日报出版，不重复生成 defer 改写。'),
 'specific_scope_boundary_retained':('已完成边界意见，缺具体可核验实证','item_specific_scope_evidence_gap',
    '按本条具体缺口补版本、反馈或后续消费证据；保留正证与反证，不能将推测写成运行事实。'),
 'specific_harness_evidence_gap_retained':('已完成边界意见，缺工件版本/准入/消费链','item_specific_artifact_evidence_gap',
    '在已有专项 issue 补可执行工件旧版—编辑—准入—后续调用链；源码接口存在不能代替论文实际发生的更新。'),
 'external_source_blocker_retained':('来源身份已知，所需官方内容仍缺','external_source_access_blocker',
    '等待官方可公开摘要/方法全文或作者工件，复用既有身份绑定；metadata HTTP 200 不等于恢复正文。'),
 'post_approval_counterevidence_retained':('后续反证优先，保留暂缓','post_approval_counterevidence',
    '保留后续纠正优先于旧纳入批准；需要新证据解除该条跨任务继承缺口。'),
}
ledger=[]
for index, hist in enumerate(carry):
    id=hist['id']; archived=inv[id]; canonical=archived['canonical_snapshot']
    review=deepcopy(canonical.get('review',{}))
    proposal=positive.get(id) or exclusion.get(id)
    output=deepcopy(hist)
    output['date_checked']='2026-11-18'
    output['original_carryforward_reference']={'path':cp,'sha256':sha(cp),'index':index}
    output['canonical_review_before']=review
    output['canonical_review_before_sha256']=hashlib.sha256(json.dumps(review,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    output['existing_formal_review']={
      'present':bool(review),'decision':review.get('decision'),'date':review.get('date'),
      'reviewed_on':review.get('reviewed_on'),'github_pr':review.get('github_pr'),
      'owner_login':review.get('owner_login'),'merge_commit':review.get('merge_commit'),
      'source_hash':review.get('source_hash'),
      'source_hash_matches_archived_canonical':review.get('source_hash')==archived['canonical_source_hash'],
      'provenance_scope':'Read from the frozen canonical snapshot; this subtask makes no fresh GitHub merge claim.'}
    output['first_seen_preserved']=canonical['first_seen']
    output['canonical_apply_recommendation']='apply_source_bound_suggestion_after_true_dated_merge' if proposal else 'keep_canonical_review_unchanged'
    output['skip_apply_when_no_new_adjudication']=not bool(proposal)
    output['do_not_rewrite_old_review_to_today_defer']=True
    output['canonical_writes']=0
    output['github_writes']=0
    output['new_publication_claimed']=False
    assert output['issue_refs']
    if proposal:
        is_positive=id in positive
        path=pp if is_positive else ep
        suggestion='backlog' if is_positive else 'reject'
        output['current_work_status']='source_bound_backlog_suggestion' if is_positive else 'source_bound_reject_suggestion'
        output['work_category']='actionable_after_independent_check_and_dated_merge'
        output['work_status_zh']='历史纳入建议已备齐，等待精确稿独立复核及日期合并' if is_positive else '历史排除建议已备齐，等待精确稿独立复核及日期合并'
        output['decision_suggestion']=suggestion
        output['proposal_reference']={'path':str(path.relative_to(ROOT)),'sha256':sha(path.relative_to(ROOT)),'id':id}
        output['source_hash']=proposal['source_hash']
        output['next_action_zh']='父任务取得最终独立核验回执，合并同仓真实日期审核 PR 后应用。'
        output['pending_evidence_or_editorial_checks']=deepcopy(proposal['pending'])
        output['new_source_checks_completed']=True
        output['source_checks_scope']='Exact original source bytes/quotes and editorial scope, not experiment replication.'
    else:
        status=hist['status'];label,category,action=worklabels[status]
        output['current_work_status']=status
        output['work_status_zh']=label
        output['work_category']=category
        output['decision_suggestion']=None
        output['next_action_zh']=action
        output['new_source_checks_completed']=False
        output['reason_zh']=list(dict.fromkeys(hist['reason_zh']))
        assert output['reason_zh']
        if status=='existing_catalog_entry_retained':
            output['new_formal_disposition_required']=False
            if id=='arxiv:2610.32253':
                output['classification_precedence_note']='RSIHub 保留最新 harness_eval/framework 分类；旧模型 harness_method 理由仅作为历史意见，不恢复。'
        if hist.get('owner_scope_receipt') and not hist['owner_scope_receipt']['exact_hash_matches_current']:
            output['source_delta_requires_explicit_binding']=True
        if id=='arxiv:2610.33245':
            output['classification_precedence_note']='AdaPRA 后续独立正文纠正优先：在线 rubric 按任务隔离，固定种子迁移不是反馈修改产物跨任务继承。'
    ledger.append(output)

assert len({r['id'] for r in ledger})==121
assert sum(not r['skip_apply_when_no_new_adjudication'] for r in ledger)==29
assert sum(r['skip_apply_when_no_new_adjudication'] for r in ledger)==92
assert all(r['canonical_review_before']==inv[r['id']]['canonical_snapshot']['review'] for r in ledger)
encoded=''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in ledger).encode()
outpath=RAW/'disposition-ledger-v1.jsonl.gz'
assert not outpath.exists()
outpath.write_bytes(gzip.compress(encoded,mtime=0))
summary={
 'date':'2026-11-18','created_at':datetime.now(timezone.utc).isoformat(),
 'reviewer':'/root/nov18_independent_recovery',
 'inputs':[{'path':p,'sha256':sha(p)} for p in [ip,cp,str(pp.relative_to(ROOT)),str(ep.relative_to(ROOT))]],
 'ledger':{'path':str(outpath.relative_to(ROOT)),'sha256':sha(outpath.relative_to(ROOT)),'uncompressed_sha256':hashlib.sha256(encoded).hexdigest()},
 'counts':{'original_PR135_defer_rows':121,'proposed_backlog':19,'proposed_reject':10,
           'keep_existing_canonical_review':92,'canonical_writes':0,'github_writes':0,
           'all_prior_formal_review_preserved':121,'source_free_GETs':30,'paid_requests':0},
 'work_status_counts':dict(Counter(r['current_work_status'] for r in ledger)),
 'non_actionable_work_category_counts':dict(Counter(r['work_category'] for r in ledger if r['skip_apply_when_no_new_adjudication'])),
 'boundaries':['Not all 92 carryforward items are external blockers: editorial preparation, scoped screens, preserved catalog records, specific evidence gaps and publisher access failures are distinguished.',
              'The original 121 canonical decisions are all existing defer receipts. Do not overwrite those receipts with a fresh blanket defer.',
              'Only the 29 source-bound suggestions are candidates for current application, subject to final independent review and true dated merge.',
              'No new model result, source experiment replication, GitHub merge, or online publication is claimed by this subtask.'],
}
(OUT/'disposition-summary-v1.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')

def esc(value): return str(value).replace('|','\\|').replace('\n',' ')
lines=['# PR #135 原 121 条历史待审逐项状态','',
 '19 条建议 backlog、10 条建议 reject；其余 92 条保留原 canonical.review 及精确来源绑定。此表是建议与恢复入口，不是已合并或上线证明。',
 '', '原始 source-hash scope receipt 不等于日期 PR 合并；后续反证优先。保留 first_seen、全部旧审核原件与纠正；不重跑付费模型。','',
 '| 稳定 ID | 当前工作状态 | 具体理由 / 缺口 | 下一步 | issue |','| --- | --- | --- | --- | --- |']
for r in ledger:
    reasons=r.get('reason_zh',[])
    reason=reasons[0] if reasons else ''
    pending=r.get('pending_evidence_or_editorial_checks',[])
    if r['skip_apply_when_no_new_adjudication'] and pending:
        reason+=' 待补：'+'；'.join(pending)
    issues=' '.join(f"[#{i['number']}]({i['url']})" for i in r['issue_refs'])
    lines.append('| '+ ' | '.join([esc(r['id']),esc(r['work_status_zh']),esc(reason),esc(r['next_action_zh']),issues])+' |')
(OUT/'disposition-table-v1.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'ledger':summary['ledger'],'counts':summary['counts'],'category_counts':summary['non_actionable_work_category_counts']},ensure_ascii=False,indent=2))
