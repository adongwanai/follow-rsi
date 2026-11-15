from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from copy import deepcopy
import hashlib
import json
import shutil
import yaml
from scripts.feed.storage import load_items, write_json
from scripts.feed.review import _review_row, source_hash, validate_daily_review
from scripts.feed.window import daily_metadata
from scripts.feed.dates import daily_section
from scripts.feed.guard import check_summary

R = Path.cwd(); B = R / 'build/maintenance-2026-11-15'
D = R / 'docs/internal/reports/maintenance-2026-11-15'
records = {x['id']: x for x in load_items(R)}
source = json.loads((B / 'final-source-adjudication.json').read_text())['items']
draft_path = B / 'summary-draft-v3.json'
draft = json.loads(draft_path.read_text())
summary_review = json.loads((B / 'independent/summary-review-v3.json').read_text())
draft_hash = hashlib.sha256(draft_path.read_bytes()).hexdigest()
assert summary_review['input']['sha256'] == draft_hash
assert {k: summary_review['counts'][k] for k in ['pass', 'fail', 'needs_revision']} == {'pass': 9, 'fail': 0, 'needs_revision': 0}
summaries = {x['id']: x for x in draft['items']}
numeric = []
for ident, x in summaries.items():
    assert source_hash(records[ident]) == x['source_hash_before_summary']
    checked = check_summary(records[ident]['title'], records[ident]['abstract'], **x['summary_override'])
    assert checked['ok']
    numeric.append({'id': ident, 'source_hash': source_hash(records[ident]), 'numeric_guard': checked})

queues = {}; originals = {}; archives = []
for day in ['2026-11-11', '2026-11-12', '2026-11-15']:
    p = R / f'review/daily/{day}.yaml'
    if p.exists():
        queues[day] = yaml.safe_load(p.read_text()); originals[day] = deepcopy(queues[day])
        queues[day]['reviewed_on'] = '2026-11-15'
    else:
        queues[day] = {'date': day, 'reviewed_on': '2026-11-15', 'items': [], 'lab_updates': []}
    for name in [f'review/daily/{day}.yaml', f'data/feed/review-provenance/{day}.json',
                 f'site/daily/{day}.json', f'site/daily/{day}.html', f'daily/{day}.md',
                 f'daily/{day}.en.md', f'data/feed/daily/{day}.json']:
        old = R / name
        if not old.exists():
            continue
        target = D / 'prior-editions' / name; target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.read_bytes() == old.read_bytes()
        else:
            shutil.copyfile(old, target)
        archives.append({'original': name, 'archive': str(target.relative_to(R)),
                         'sha256': hashlib.sha256(old.read_bytes()).hexdigest()})

changes = []
def make(item, day):
    row = _review_row(item); timing = daily_metadata(R, item, day); row.update(timing)
    row['daily_section'] = daily_section({**item, **timing}, day); row['promote_to_repo'] = False
    row['evidence_notice'] = '来源、身份、日期、范围与定性摘要已交叉核验；原文按版本/哈希绑定。未复现实验，未全表重算。'
    return row

def put(day, row, reason, apply=True):
    assert records[row['id']]['kind'] not in ['post', 'release']
    found = next((i for i, x in enumerate(queues[day]['items']) if x['id'] == row['id']), None)
    if found is None:
        queues[day]['items'].append(row)
    else:
        queues[day]['items'][found] = row
    changes.append({'id': row['id'], 'edition_date': day, 'reviewed_on': '2026-11-15',
                    'decision': row['decision'], 'source_hash': row['source_hash'],
                    'reason': reason, 'apply_to_canonical': apply})

for opinion in source:
    item = records[opinion['id']]; assert source_hash(item) == opinion['source_hash']
    day = str(item['published'])[:10] if opinion['suggestion'] == 'include' else '2026-11-15'
    assert day in queues
    row = make(item, day); row['decision'] = {'include': 'accept', 'exclude': 'reject', 'defer': 'defer'}[opinion['suggestion']]
    row['note'] = opinion['reason_zh'] + ' ' + opinion['limits_zh'] + ' 原文与三轮核验见 docs/internal/reports/maintenance-2026-11-15/。'
    if item['id'] == 'arxiv:2611.15700':
        row['note'] = row['note'].replace('部署知识库尚无批准合并/重建索引', '自动生成的知识变更尚未获批合并到已部署语料并重建索引')
    if opinion['suggestion'] == 'include':
        sm = summaries[item['id']]; row['summary_override'] = sm['summary_override']
        row['direction_override'] = {k: sm[k] for k in ['primary', 'secondary', 'harness_sub']}
        row['note'] += ' 无HF推荐日，按官方原发表日补刊；first_seen与实际审核日为11/15，不冒充11/15新发表。'
    put(day, row, 'new_source_adjudication')

# Only this historical row is stale: its real HF date was added on Nov 14 and
# its canonical rejection was already rebound through the Nov 13 review.
stale = []
for day, review in originals.items():
    for row in review['items'] + review['lab_updates']:
        if row['source_hash'] != source_hash(records[row['id']]):
            stale.append((day, row['id']))
assert stale == [('2026-11-12', 'arxiv:2611.14256')], stale
item = records['arxiv:2611.14256']; old = item['review']
assert old['decision'] == 'reject' and old['date'] == '2026-11-13'
assert old['source_hash'] == source_hash(item)
row = make(item, '2026-11-12'); row['decision'] = 'reject'
row['note'] = ('保留排除。11/14已核实真实11/13 HF推荐日并在11/13审核单重绑当前来源；本旧11/12行仅更新来源快照/hash供补刊整单校验。原YAML与原刊已归档；不重新apply此行，不覆盖canonical现行11/13正式排除凭据。')
put('2026-11-12', row, 'historical_queue_source_snapshot_rebind_only', apply=False)

repair = json.loads((B / 'backlog-audit/primary-review/harness-repair-v1.json').read_text())
cross = json.loads((B / 'independent/harness-repair-v1-cross-review.json').read_text())
assert cross['current_version_scope_summary_review_complete'] and not cross['blocking_disagreements']
item = records[repair['id']]; assert source_hash(item) == repair['source_hash']
row = make(item, '2026-11-15'); row['decision'] = 'backlog'; sm = summaries[item['id']]
row['summary_override'] = sm['summary_override']
row['direction_override'] = {k: sm[k] for k in ['primary', 'secondary', 'harness_sub']}
row['note'] = ('Harness Repair当前官方v1完成主审与独立交叉，限定纳入Harness专项评测历史backlog。模型冻结，研究GEPA指令搜索的收益归因、基线与评测缺陷；保留当前无数字摘要，不升版、不混入后版数字。公开原文可读，v1未公开原始实验工件；不声称实验复现、未触碰留出集或全部搜索方法无效。旧first_seen、日期、判断与摘要纠正链保留；不是11/15新论文。见本日primary-review/harness-repair-v1与独立交叉回执。')
put('2026-11-15', row, 'historical_current_v1_scope_resolution')

amendment = json.loads((B / 'backlog-audit/primary-review/2610.28914-scope-amendment.json').read_text())
cross = json.loads((B / 'independent/2610.28914-v1-v2-cross-review.json').read_text())
assert cross['scope_agrees_after_amendment'] and cross['conclusion'] == 'include_harness_component'
assert cross['primary_amendment']['sha256'] == hashlib.sha256((B / 'backlog-audit/primary-review/2610.28914-scope-amendment.json').read_bytes()).hexdigest()
item = records[amendment['id']]
assert item['version'] == 1 and source_hash(item) == amendment['source_binding']['current_source_hash']
row = make(item, '2026-11-15'); row['decision'] = 'backlog'; sm = summaries[item['id']]
row['summary_override'] = sm['summary_override']
row['direction_override'] = {k: sm[k] for k in ['primary', 'secondary', 'harness_sub']}
row['note'] = ('D-Skill当前v1按主审纠正与独立交叉列Harness组件历史backlog。固定teacher/student执行轨迹提供反馈，逐批修改可复用的工具调用、验证、停止与重试规则，后续任务加载，学生权重固定。默认流程没有新增环境调用或post-patch评价选择，SkillOpt变体的验证门单列。原初稿误把新的在线评价作为必要条件，初稿与纠正链保留；本次不升版、不改first_seen、不称在线递归自评、不算11/15新论文。原文与独立回执见本日2610.28914 scope-amendment及cross-review。')
put('2026-11-15', row, 'historical_current_v1_scope_amendment')

assert Counter(x['decision'] for x in changes if x['apply_to_canonical']) == {'accept': 7, 'reject': 6, 'defer': 3, 'backlog': 2}
for day, old in originals.items():
    changed = {x['id'] for x in changes if x['edition_date'] == day}
    for group in ['items', 'lab_updates']:
        now = {x['id']: x for x in queues[day][group]}
        for row in old[group]:
            if row['id'] not in changed:
                assert now[row['id']] == row
out = B / 'reviews'; out.mkdir(exist_ok=True); checks = []
for day, review in queues.items():
    p = out / f'{day}.yaml'; p.write_text(yaml.safe_dump(review, allow_unicode=True, sort_keys=False, width=110))
    target = R / f'review/daily/{day}.yaml'; prior = target.read_bytes() if target.exists() else None
    try:
        target.write_bytes(p.read_bytes()); validate_daily_review(R, day)
    finally:
        if prior is None:
            target.unlink()
        else:
            target.write_bytes(prior)
    checks.append({'date': day, 'reviewed_on': '2026-11-15', 'items': len(review['items']),
                   'lab_updates': len(review['lab_updates']),
                   'decisions': dict(Counter(x['decision'] for x in review['items'] + review['lab_updates'])),
                   'changed_ids_only_to_apply': [x['id'] for x in changes if x['edition_date'] == day and x['apply_to_canonical']],
                   'draft_sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'validated': True})
report = {'validated_at': datetime.now(timezone.utc).isoformat(), 'reviews': checks,
          'new_or_changed_decisions': changes, 'new_or_changed_counts': dict(Counter(x['decision'] for x in changes)),
          'canonical_application_counts': dict(Counter(x['decision'] for x in changes if x['apply_to_canonical'])),
          'summaries': numeric, 'prior_archives': archives,
          'application_boundary': 'One date per review PR. Verify exact merged bytes and head CI, then apply only the 18 changed canonical decisions. Preserve all old formal decisions, including World In-Context Learning and the existing Nov 13 rejection.',
          'public_preservation': 'The old Nov 11 paper entry must retain all original public fields, including review_date=2026-11-12; supplement edition reviewed_on is 2026-11-15.',
          'formal_approval': False}
write_json(B / 'review-preflight.json', report); write_json(D / 'review-preflight.json', report)
print({'changed_rows': len(changes), 'canonical_application_counts': report['canonical_application_counts'],
       'dates': [{'date': x['date'], 'changed': len(x['changed_ids_only_to_apply'])} for x in checks]})
