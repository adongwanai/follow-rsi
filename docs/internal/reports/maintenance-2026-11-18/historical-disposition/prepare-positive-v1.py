"""Freeze selected historical backlog proposals without changing production data."""
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.feed.guard import check_summary, unknown_evidence
from scripts.feed.review import source_hash

OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/historical-disposition'
def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
def gz(path):
    with gzip.open(ROOT / path, 'rt') as f:
        return [json.loads(line) for line in f]
inventory_path = 'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz'
carry_path = 'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-carryforward-v1.jsonl.gz'
inventory = {r['id']:r for r in gz(inventory_path)}
carry = {r['id']:r for r in gz(carry_path)}
sources = json.loads((OUT / 'restored-source-index.json').read_text())
oldprov_path = 'docs/internal/reports/maintenance-2026-10-30/independent/source-provenance.json'
oldprov = {r['id']:r for r in json.loads((ROOT / oldprov_path).read_text())['items']}
old31_path = 'docs/internal/reports/maintenance-2026-10-31/primary/review-reconciled.json'
old31 = {r['id']:r for r in json.loads((ROOT / old31_path).read_text())['items']}

# These are current editorial proposals, not saved paid-model outputs.
overrides = {
 '2610.37905': (
  'FilingLoop 用已评分批次的要求级反馈改写 Reviewer 与 Filer 的程序性技能，供后续未尝试的案例使用，模型权重保持不变；这是在线历史反馈适应，不能视为独立留出集验证。',
  'FilingLoop revises procedural Reviewer and Filer skills from requirement-level feedback on scored batches and applies them to later unattempted cases with fixed model weights. This is online adaptation from historical feedback, not an independent held-out evaluation.'),
 '2610.38392': (
  'Masked Erosion 研究固定模型外部的文本 Harness 在接受闸门下如何逐步丢失冗余安全约束：被接受的修改成为后续父代。主要实验人为施加删除压力，用于隔离闸门行为，不能概括为部署中的普遍失效率。',
  'Masked Erosion studies how acceptance gates can erode redundant safeguards in a textual harness around a fixed model, with accepted edits becoming later parents. Most experiments deliberately impose deletion pressure to isolate gate behavior, rather than estimate general deployment failure rates.'),
 '2610.39122': (
  '该安全评测研究用户赞许如何影响个人代理面对间接提示注入时的授权判断。MetaClaw 把会话反馈写成可复用技能并用于后续会话；技能演化和强化学习权重更新是分别测试的分支，不能当成同一代理的协同演化。',
  'This safety evaluation studies how user appreciation affects personal agents’ authorization judgments under indirect prompt injection. MetaClaw turns session feedback into reusable skills for later conversations; skill evolution and reinforcement-learning weight updates are separately tested branches, not joint co-evolution in one agent.'),
 '2610.39358': (
  '研究在策略权重更新后诊断技能效用变化，并用 readout 和失败轨迹指导技能编辑。在闭环实验中，编辑器修改文本技能库，配对验证决定是否保留到后续窗口；独立诊断实验则固定技能库。',
  'The study diagnoses changes in skill utility after policy-weight updates and uses readouts and failed trajectories to guide skill edits. In closed-loop experiments, an editor revises the textual skill bank and paired validation decides retention for later windows; the separate diagnostic experiments keep the skill bank fixed.'),
 '2610.39508': (
  '该方法把技能执行中的不确定操作编译为程序，利用执行错误和检查差异修订技能与代码，并保存验证后的程序资产供后续技能复用。开发时曾查看留出失败案例，测试期冻结资产库并不意味着完全独立的留出验证。',
  'The method compiles uncertain skill operations into programs, repairs skills and code using execution errors and check discrepancies, and retains validated program assets for later skills. Development inspected held-out failures, so a frozen asset bank at test time does not establish fully independent held-out validation.'),
 '2610.25568': (
  '该 Harness 将原始目标、可修改计划与执行记录分离，由 planner、worker、reviewer 协作；setup agent 根据试运行轨迹和工具反馈修订可复用指令。在 Terminal-Bench 2.1 上通过 89 个实例中的 83 个（93.26%）；结果针对完整配置，未隔离指令演化的单独贡献。',
  'The harness separates the original objective from mutable plans and execution records, with planner, worker, and reviewer roles; a setup agent revises reusable instructions from trial trajectories and tool feedback. It passes 83 of 89 Terminal-Bench 2.1 instances (93.26%); these results concern the complete configuration, without isolating instruction evolution.'),
 '2610.27889': (
  '借鉴 RL 的 pass@k 分析，对比优化前后的 Harness，区分增益来自已有能力更可靠地发挥还是可解任务范围扩大。所测设置中，pass@1 优势可能在更大尝试预算下反转，属于 Harness 专项诊断评测。',
  'Drawing on RL pass@k analysis, the study compares harnesses before and after optimization to distinguish more reliable elicitation from broader task coverage. In the evaluated settings, pass@1 advantages can reverse at larger attempt budgets; this is a focused diagnostic evaluation of harness optimization.'),
 '2610.34938': (
  '研究让 retro 回顾 Claude Code 在 30 个 SWE-bench Verified 问题上的会话并提出 Harness 修改，由研究者选择实施 24 个提案、评估 12 个变更。后续任务中，多数遇到目标问题的评估未减少重复工作；这是含人工选择的专项评测。',
  'The study uses retro to review Claude Code sessions on 30 SWE-bench Verified issues and propose harness changes; researchers select 24 proposals for implementation and evaluate 12 changes. Most evaluations that encounter the targeted problem show no reduction in repeated work on later tasks; selection involves humans.'),
 '2610.32813': (
  'HarnessMM 在 actor 权重固定时复用已有决策，减少后续推理调用；另用训练反馈和验证选择迭代改进配套 Harness 配置。DeepSeek Harness 的完整配置报告成功率上升、Tokens/task 下降，不能把全部收益归因于单一 RSI 或替换组件。',
  'HarnessMM reuses resolved decisions to reduce later reasoning calls with fixed actor weights, while training feedback and validation selection iteratively refine companion harness configurations. The full DeepSeek Harness configuration reports higher success and lower Tokens/task; the entire gain cannot be attributed to RSI or callback substitution alone.'),
 '2610.32026': (
  'RSI-Opt 的 meta-agent 根据历史运行证据改写可复用的提示、playbook、优化器代码库和决策节奏，并归档策略供后续运行继承。模型训练是应用任务；递归继承的独立增益缺少匹配预算对照，且曾发生留出任务描述被读取的情况。',
  'RSI-Opt uses historical run evidence to revise a reusable prompt, playbook, optimizer-code library, and decision cadence, archiving policies for later runs. Model training is the application task; the isolated benefit of recursive inheritance lacks a matched-budget control, and a held-out task description was accessed during development.'),
 '2610.29121': (
  '该方法用拟合后冻结的线性 readout 在执行前给脚手架代码修改打分，再依据 steering-split 反馈选择并保留候选。GPT-4o 实验返回节点在留出 HumanEval+ 上的得分为 87.0%，parent-rate 消融为 84.2%；这些百分比是得分，不是返回节点的比例。',
  'A linear readout, frozen after fitting, scores scaffold-code edits before execution, followed by candidate selection and retention using steering-split feedback. In the GPT-4o experiment, returned nodes score 87.0% on held-out HumanEval+, versus 84.2% for the parent-rate ablation; these percentages are scores, not proportions of nodes returned.'),
 '2610.35051': (
  'VISTA 用 Harness graph 保留版本与证据，元代理主动生成 rollout、探测失败并修订指令、可执行技能及协调逻辑。仿真实验中相对静态反思报告更高成功率和更少 rollout；效率优势本身不能证明预算完全匹配。',
  'VISTA retains harness versions and evidence in a graph while a meta-agent actively generates rollouts, probes failures, and revises instructions, executable skills, and coordination logic. Simulation experiments report higher success with fewer rollouts than static reflection; efficiency alone does not establish fully matched budgets.'),
 '2610.35316': (
  'RSIV-Harness 固定语言模型权重，依据失败轨迹修订外部 Harness，并用 anchor 与 memory 检查决定保留或回滚。在 ODAC-Vis 的原骨干设置中，一轮改进提高全部六项指标，可执行性变化为 +28.02 点、图表结构为 +34.01 点；跨骨干结果并非所有指标都提升。',
  'RSIV-Harness fixes language-model weights, revises the surrounding harness from failure traces, and uses anchor and memory checks for retention or rollback. In the original backbone setting on ODAC-Vis, one round improves all six metrics, including +28.02 points in executability and +34.01 in chart structure; transfer does not improve every metric.'),
}

def wspace(text):
    return ' '.join(text.split())

results = []
queue = []
for s in sources:
    id = s['id']; inv = inventory[id]; c = inv['canonical_snapshot']; hist = carry[id]
    assert source_hash(c) == inv['canonical_source_hash']
    assert s['canonical_source_hash'] == inv['canonical_source_hash']
    assert s['status'] == 'ok' and sha(s['source_file']) == s['source_sha256']
    assert sha(s['text_file']) == s['text_sha256']
    raw_old = []
    if id in oldprov:
        br = oldprov[id].get('body_receipt')
        if isinstance(br, dict):
            raw_old += [a['sha256'] for a in br.get('attempts', []) if a.get('sha256')]
    if id in old31:
        raw_old += [q['sha256'] for q in old31[id]['source_quotes'] if q['kind'] == 'official_full_text']
    assert s['source_sha256'] in raw_old, (id, 'restored official bytes changed')
    aid = c['arxiv_id']; text = (ROOT / s['text_file']).read_text(); ntext = wspace(text)
    abstracts = [c.get('abstract', '')]
    quote_checks = []
    old_refs = []
    reasons = []; limits = []
    for e in hist['saved_review_evidence']:
        ref = e['reference']; d = e['saved_review_record']; old_refs.append(ref)
        assert sha(ref['path']) == ref['sha256']
        datum = d.get('data') or d
        reasons += [datum.get('reason_zh')] if datum.get('reason_zh') else []
        limits += [datum.get('limitations_zh')] if datum.get('limitations_zh') else []
        quotes = [(key, value) for key, value in (d.get('data') or {}).items() if key.endswith('_quote') and value]
        quotes += [('saved_quote', q) for q in d.get('quotes', [])]
        quotes += [(q['kind'], q['quote']) for q in d.get('source_quotes', [])]
        for kind, quote in quotes:
            in_body = wspace(quote) in ntext
            in_abstract = any(wspace(quote) in wspace(a) for a in abstracts)
            assert in_body or in_abstract, (id, kind, quote)
            quote_checks.append({'kind':kind, 'quote':quote,
              'match':'whitespace_normalized_substring_in_restored_body' if in_body else 'exact_canonical_official_abstract_wording_on_unchanged_owner_hash',
              'source_file':s['text_file'] if in_body else inventory_path,
              'source_sha256':s['text_sha256'] if in_body else sha(inventory_path)})
    if id in old31:
        d = old31[id]
        assert d['identity_verified'] and d['independent_round_3']['status'] == 'completed_independently_before_comparison'
        direction = {'primary': d['topic_primary'], 'harness_sub': d['harness_sub']}
        rounds = [1,2,3]
        limits += [d['boundary_note_zh']] if d.get('boundary_note_zh') else []
    else:
        direction = {'primary':c['primary'], 'harness_sub':c.get('harness_sub')}
        rounds = hist['historical_rounds_reported']
        assert rounds == [1,2,3]
    if aid in overrides:
        zh,en = overrides[aid]
    else:
        zh,en = c['summary_zh'],c['summary_en']
    guard = check_summary(c['title'],c['abstract'],zh,en)
    assert guard['ok'], (id, guard)
    evidence = unknown_evidence()
    evidence_changes = []
    # Only carry specific abstract-supported evidence, never infer transfer from multiple model runs.
    keep = {
      '2610.33487':['held_out','matched_budget'],
      '2610.36826':['held_out'],
      '2610.35616':['cross_model'],
      '2610.32026':['cross_model'],
      '2610.29121':['held_out'],
    }.get(aid, [])
    for key in keep:
        evidence[key] = deepcopy(c['evidence_quick'][key])
    for key, prior in c.get('evidence_quick', {}).items():
        if evidence.get(key) != prior:
            evidence_changes.append({'field':key,'before':prior,'after':evidence[key],
              'reason':'Only item-specific supported evidence is retained: multiple model runs do not prove transfer; fewer calls do not prove matched budgets; an unverified repository link is not a fresh code-release audit. RSI-Opt held-out description access is separately disclosed.'})
    owner = inv.get('owner_scope_receipt_ref')
    if owner:
        assert owner['exact_hash_matches_current'] and owner['receipt']['source_hash'] == inv['canonical_source_hash']
        assert sha(owner['path']) == owner['sha256']
    note = ('历史积压补录；复用旧独立三轮范围审查，并于2026-11-18恢复与旧SHA完全相同的官方正文、复核引句和双语摘要。'
            '不改first_seen；非当日新发现或HF新推荐；旧模型错误/质量评测告警保留。')
    if limits:
        note += ' 限制：' + '；'.join(dict.fromkeys(limits))
    row = deepcopy(inv['original_queue_row'])
    row.update(decision='backlog',direction_override=direction,
               summary_override={'summary_zh':zh,'summary_en':en},
               evidence_quick=evidence, promote_to_repo=False, note=note)
    queue.append(row)
    results.append({'id':id,'title':c['title'],'decision_suggestion':'backlog',
      'reviewed_on':'2026-11-18','edition_date':'2026-11-17','first_seen_preserved':c['first_seen'],
      'source_hash':inv['canonical_source_hash'],'source':s,
      'restored_raw_source_matches_historical_sha256':True,
      'old_original_source_sha256':sorted(set(raw_old)),
      'owner_scope_approval':owner,
      'authorization_when_no_item_scope_receipt':'Current standing user authorization; requires real dated review PR merge before application.' if not owner else None,
      'old_three_rounds':rounds,'prior_review_records':old_refs,
      'mechanism_reasons_zh':list(dict.fromkeys(reasons)),
      'limitations_zh':list(dict.fromkeys(limits)), 'quote_checks':quote_checks,
      'summary_provenance':'Codex editorial source check; saved paid outputs remain unchanged; no new paid-model claim.',
      'summary_before':{'summary_zh':c.get('summary_zh'),'summary_en':c.get('summary_en')},
      'summary_override':row['summary_override'], 'summary_numeric_guard':guard,
      'summary_semantic_review':'Checked against unchanged official source and the recorded scope limitations. Numeric guard alone is not semantic validation.',
      'direction_override':direction, 'evidence_quick':evidence,'evidence_changes':evidence_changes,
      'catalog_entry_preserved':hist.get('catalog_entry'), 'promote_to_repo':False,
      'pending':['independent_current_summary_crosscheck','real_dated_review_PR_merge_and_apply','build_and_live_publication_verification'],
      'canonical_writes':0,'github_writes':0,'publication_claimed':False})

payload = {'created_at':datetime.now(timezone.utc).isoformat(),'date':'2026-11-18',
  'input_inventory':{'path':inventory_path,'sha256':sha(inventory_path)},
  'input_carryforward':{'path':carry_path,'sha256':sha(carry_path)},
  'scope':'Nineteen targeted historical proposals, not whole-backlog approval or publication.',
  'reviewer':'/root/nov18_independent_recovery','paid_requests':0,
  'counts':{'backlog_suggestions':len(results),'current_summary_independent_pending':len(results)},
  'items':results}
(OUT / 'positive-proposals-v1.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(OUT / 'positive-review-rows-v1.yaml').write_text(yaml.safe_dump({'items':queue},allow_unicode=True,sort_keys=False,width=110))
(OUT / 'positive-proposals-v1.sha256').write_text(sha(OUT.relative_to(ROOT) / 'positive-proposals-v1.json')+'\n')
print(json.dumps({'items':len(results),'quote_checks':sum(len(r['quote_checks']) for r in results),
  'json_sha256':sha(OUT.relative_to(ROOT) / 'positive-proposals-v1.json'),
  'yaml_sha256':sha(OUT.relative_to(ROOT) / 'positive-review-rows-v1.yaml')},indent=2))
