"""Freeze ten source-bound historical rejection proposals; no production writes."""
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.feed.review import source_hash
OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/historical-disposition'

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
def gz(path):
    with gzip.open(ROOT / path, 'rt') as f:
        return [json.loads(line) for line in f]
def norm(value):
    return re.sub(r'\s+', ' ', value).strip()

ip = 'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz'
cp = 'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-carryforward-v1.jsonl.gz'
inv = {r['id']: r for r in gz(ip)}
carry = {r['id']: r for r in gz(cp)}
receipts = json.loads((OUT / 'exclusion-source-index.json').read_text())
source_map = {}
for source in receipts:
    assert source['http_status'] == 200
    assert sha(source['source_file']) == source['source_sha256']
    assert sha(source['text_file']) == source['text_sha256']
    source_map.setdefault(source['id'], []).append(source)

DETAILS = {
'arxiv:2610.22990': {
 'reading_scope': 'Official full-source identity and selected method/scope passages, plus prior three-round source review; not an experiment replication.',
 'reason_zh': '固定 74 项任务与 11 个领域，只改变请求者画像及其请求；考察固定 CUA 对不同用户的服务表现，不是可保留 Harness 修改的专项评测。',
 'limitations_zh': ['本次不复算全部任务分数或人口统计差异。', '旧摘要长引句末尾与 HTML 存在直弯引号差异，采用正文中可精确匹配的完整短句。'],
 'fresh_quotes': ['We introduce PersonaCUABench, which holds 74 tasks across 11 domains fixed and varies only who asks.'],
 'raw_source_matches_historical': None,
},
'arxiv:2610.38728': {
 'reading_scope': 'Official full-source identity and selected definitions of recursive gain/improvement, reusing prior three-round theory scope review.',
 'reason_zh': '提出工作量、信息和跨代改进效率的广义 RSI 理论，也讨论个人及集体组织；未以 Harness 程序演化为专门研究对象。范围排除不以理论论文缺执行闭环为理由。',
 'limitations_zh': ['旧 Atom 摘要和 HTML 摘要措辞不同；旧摘要引句仅绑定 canonical 官方摘要，正文判断绑定同 SHA 的 HTML。', '不声称完整重推全部定理或复现其理论结论。'],
 'raw_source_matches_historical': True,
 'old_raw_sha256': 'c7241c4b7011db459b30e07304e337d3f8d3d7d5f2ff50680dd054abdd93a20a',
},
'arxiv:2610.34977': {
 'reading_scope': 'Official method passages on per-memory access state, teacher-mask training and later-query utility, reusing prior independent review/adjudication.',
 'reason_zh': 'AMIE 更新每条记忆的访问权重和抑制状态，宿主管理程序及部署策略固定；teacher-mask 蒸馏与下游效用评价分开。可保留的是记忆项状态而非由任务反馈改写的 Harness 管理程序，依 owner 已确认边界排除。',
 'limitations_zh': ['不把持久状态本身误写成完全没有持久化；排除依据是被修改对象和反馈用途。', '保留原有模型输出与边界讨论，不重新宣称全部实验已核验。'],
 'raw_source_matches_historical': True,
 'old_raw_sha256': '05fe37b67f94ea9560d910186266fdad12a9f62c9ac23b4c976007a1ba43ba0e',
},
's2:c470d4b2c990d73e0b34f5f9e384423fd7c09a14': {
 'reading_scope': 'Complete official three-page IEEE editorial PDF including references.',
 'reason_zh': '编辑短文讨论计算智能、搜索、效率、信任与责任的广义研究议程，没有提出或专项评测可持久修改 Harness 的方法。',
 'limitations_zh': ['期刊月份为 2026 年 11 月，正文 current-version 日期为 2026-10-08，不能将 11 月刊期当成新发表日期。', '正文 DOI 为 10.1109/MCI.2026.3726101；版面另含相邻内容 DOI 3726102，不混同。'],
 'raw_source_matches_historical': True,
 'old_raw_sha256': '8a2d0ac6eb4180ea7f25627ecf509e1c4008faec2039686525827da8f22e7518',
},
's2:c9b9cd5e0b6447a180914049754459b00b3cf264': {
 'reading_scope': 'Author-deposited OSF preprint abstract in Crossref and exact reciprocal preprint/journal DOI relation; no publisher full-text claim.',
 'reason_zh': '明确关联的作者预印本摘要讨论自主目标生成、认知科学和人机共同探索；不是 Harness 程序反馈修改及保留的专项方法或评测。按已批准的摘要范围意见排除。',
 'limitations_zh': ['本次未获取期刊全文，不将摘要排除写成全文或数字审查。', '预印本发表于 2026-09-24；期刊 metadata 为 2026 年 12 月刊期，不改写成当日新论文。'],
 'raw_source_matches_historical': True,
 'old_raw_sha256': '106544eee544f3466136096a408ba1aad68329ee8769fc4bc0e5167c3a73d9dc',
},
'post:/us-midterms-analysis/': {
 'reading_scope': 'Complete official Japanese article.',
 'reason_zh': '多模型对照原文核实选举叙事分析，输出为情报报告；修改对象不是自己的 Harness，保留短 URL 稳定 ID 与既有重复身份信息。',
 'limitations_zh': ['不独立验证报告中的选举预测和全部社会科学结论。', '网页当前 HTML 可能随站点模板变化；仅声明本次原文核验和旧引句仍可匹配，不称历史 HTML 完全相同。'],
 'raw_source_matches_historical': None,
},
'post:https://openai.com/index/openai-servicenow-partnership-expansion': {
 'reading_scope': 'Complete official article, including existing-business-rule and permission sections.',
 'reason_zh': '企业产品合作及集成公告沿用既有业务规则和权限；没有提供自主演化 Harness 的方法或专项评测。',
 'limitations_zh': ['本次审核公开文章范围，不推断未公开内部实现。', '当前网页原始字节不宣称与旧 HTML 相同。'],
 'raw_source_matches_historical': None,
},
'post:https://openai.com/index/the-future-of-the-firm': {
 'reading_scope': 'Official essay introduction and organizational scenarios, checked against the saved source passages.',
 'reason_zh': '文章自称 next-economy 系列 essay，讨论 AI 在企业层级和组织中的位置；不是 Harness 演化方法、专项理论或评测。',
 'limitations_zh': ['范围判断不等于核验全部经济预测。', '当前网页原始字节不宣称与旧 HTML 相同。'],
 'raw_source_matches_historical': None,
},
'post:https://openai.com/index/legora': {
 'reading_scope': 'Official article body, legal-playbook and engineering iteration sections.',
 'reason_zh': '法律团队构建 playbook，人类工程团队利用 coding agents 修改客户产品；文章未提供系统修改并保留自身 Harness 的闭环证据。',
 'limitations_zh': ['产品迭代速度和业务效果不在本次实证核验范围。', '当前网页原始字节不宣称与旧 HTML 相同。'],
 'raw_source_matches_historical': None,
},
'post:https://sakana.ai/symposium-2026/': {
 'reading_scope': 'Official English event report and opening Japanese overview, pre-training announcement and Darwin Godel Machine retrospective passages.',
 'reason_zh': '研讨会报道宣布预训练计划并回顾世界模型、科研和 Physical AI；Darwin Gödel Machine 为既有工作的介绍，没有新 Harness 方法或实证，不能计为新论文或 HF 推荐。',
 'limitations_zh': ['未独立审计讲话中全部科学史或既往论文成绩。', '当前网页原始字节不宣称与旧 HTML 相同。'],
 'raw_source_matches_historical': None,
},
}
items, rows = [], []
for id, detail in DETAILS.items():
    record, hist = inv[id], carry[id]
    c = record['canonical_snapshot']
    assert source_hash(c) == record['canonical_source_hash']
    owner = record['owner_scope_receipt_ref']
    assert owner['exact_hash_matches_current']
    assert owner['receipt']['source_hash'] == record['canonical_source_hash']
    assert owner['receipt']['scope_recommendation'] == 'exclude'
    assert sha(owner['path']) == owner['sha256']
    srcs = source_map[id]
    primary_source = next(s for s in srcs if s['source_kind'] != 'journal-json')
    body = (ROOT / primary_source['text_file']).read_text()
    if detail['raw_source_matches_historical']:
        assert primary_source['source_sha256'] == detail['old_raw_sha256']
    checks = []
    refs = []
    for evidence in hist['saved_review_evidence']:
        ref = evidence['reference']
        assert sha(ref['path']) == ref['sha256']
        old = evidence['saved_review_record']
        refs.append({'reference': ref,
                     'historical_reading_scope': old.get('reading_scope', old.get('review_level')),
                     'independent_round_3': old.get('independent_round_3'),
                     'initial_primary': old.get('initial_primary'),
                     'initial_independent': old.get('initial_independent')})
        quotes = []
        for entry in old.get('source_quotes', old.get('quotes', [])):
            quotes.append(entry if isinstance(entry, dict) else {'quote': entry})
        for key, value in old.get('data', {}).items():
            if key.endswith('_quote') and value:
                quotes.append({'quote': value, 'kind': key})
        for entry in quotes:
            quote = entry['quote']
            found = quote in body
            normalized = norm(quote) in norm(body)
            canonical_abstract = quote in c.get('abstract', '')
            assert found or normalized or canonical_abstract, (id, quote)
            checks.append({'quote': quote, 'legacy_reference': ref,
              'legacy_quote_kind': entry.get('kind', entry.get('location')),
              'exact_in_current_body': found,
              'whitespace_normalized_in_current_body': normalized,
              'canonical_official_abstract_match': canonical_abstract,
              'check_scope': 'official_body' if found or normalized else 'canonical_official_abstract_only',
              'new_text_path':primary_source['text_file'],
              'new_text_sha256':primary_source['text_sha256']})
    for quote in detail.get('fresh_quotes', []):
        assert quote in body
        checks.append({'quote':quote,'exact_in_current_body':True,
                       'check_scope':'official_body_new_complete_short_quote',
                       'new_text_path':primary_source['text_file'],
                       'new_text_sha256':primary_source['text_sha256']})
    identity = None
    if id.startswith('s2:c9b9'):
        preprint = next(s for s in srcs if s['source_kind'] == 'preprint-json')
        journal = next(s for s in srcs if s['source_kind'] == 'journal-json')
        assert preprint['relation']['is-preprint-of'][0]['id'] == journal['doi']
        assert journal['relation']['has-preprint'][0]['id'] == preprint['doi']
        identity = {'preprint_doi':preprint['doi'],'journal_doi':journal['doi'],
                    'reciprocal_relation_verified':True,
                    'read_scope':'linked_preprint_abstract_only',
                    'preprint_published':preprint['published'],
                    'journal_issue':journal['published']}
    note = ('历史积压排除；沿用 2026-11-02 exact-source-hash 范围批准，并于 2026-11-18 恢复官方来源、复核原引句及适用边界。'
            + detail['reason_zh'] + ' 阅读范围：' + detail['reading_scope']
            + ' 不改 first_seen；旧模型错误/质量告警保留；不将此条发布为新论文。')
    row = deepcopy(record['original_queue_row'])
    row.update(decision='reject',note=note,promote_to_repo=False)
    rows.append(row)
    items.append({'id':id,'title':c['title'],'decision_suggestion':'reject',
       'edition_date':'2026-11-17','reviewed_on':'2026-11-18',
       'source_hash':record['canonical_source_hash'],'first_seen_preserved':c['first_seen'],
       'owner_scope_approval':owner,'source_receipts':srcs,
       **detail,'identity_verification':identity,'quote_checks':checks,
       'historical_round_labels_unmodified':hist['historical_rounds_reported'],
       'prior_review_records':refs,
       'round_coverage_note':'Saved source reviews and original primary/independent records are preserved. This date adds identity/source and scope checks; separate current independent crosscheck is pending. Missing old ledger round labels are not fabricated.',
       'pending':['current_independent_source_crosscheck','real_dated_review_PR_merge_and_apply'],
       'numeric_audit_recertified':False,'canonical_writes':0,'github_writes':0,
       'paid_requests':0,'publication_claimed':False})

payload = {'created_at':datetime.now(timezone.utc).isoformat(),'date':'2026-11-18',
 'reviewer':'/root/nov18_independent_recovery',
 'input_inventory':{'path':ip,'sha256':sha(ip)},
 'input_carryforward':{'path':cp,'sha256':sha(cp)},
 'counts':{'reject_suggestions':len(items),'independent_crosscheck_pending':len(items),
           'free_source_GETs':len(receipts),'paid_requests':0},
 'authorization_limit':'Exact source-hash owner receipts are scope authorizations, not fabricated historical dated merges or model success. Parent must obtain real dated review provenance before applying.',
 'items':items}
for name in ['exclusion-proposals-v1.json','exclusion-review-rows-v1.yaml']:
    assert not (OUT / name).exists(), name
(OUT / 'exclusion-proposals-v1.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(OUT / 'exclusion-review-rows-v1.yaml').write_text(yaml.safe_dump({'items':rows},allow_unicode=True,sort_keys=False,width=110))
(OUT / 'exclusion-proposals-v1.sha256').write_text(sha(OUT.relative_to(ROOT) / 'exclusion-proposals-v1.json')+'\n')
print(json.dumps({'items':len(items),'quotes_checked':sum(len(r['quote_checks']) for r in items),
 'json_sha256':sha(OUT.relative_to(ROOT) / 'exclusion-proposals-v1.json'),
 'yaml_sha256':sha(OUT.relative_to(ROOT) / 'exclusion-review-rows-v1.yaml')},indent=2))
