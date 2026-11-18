"""Freeze this reviewer's source-bound judgments; never applies publication decisions."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[5]
REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/independent-hf16'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/independent-hf16'
INTAKE = ROOT / 'build/maintenance-2026-11-18/source-intake'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(ROOT))


def norm(text):
    return ' '.join(text.split())


hf_path = INTAKE / 'source-results/hf-daily.json'
hf = json.loads(hf_path.read_text())
board = [r for r in hf['records'] if '2026-11-16' in r.get('hf_daily_dates', [])]
assert len(board) == 40 and len({r['id'] for r in board}) == 40
official_path = INTAKE / 'official-metadata/records.json'
official = {r['id']: r for r in json.loads(official_path.read_text())['records']}
baseline_path = INTAKE / 'canonical-baseline.jsonl'
baseline = {r['id']: r for r in map(json.loads, baseline_path.read_text().splitlines())}
index_path = REPORT / 'fulltext-index.json'
index = json.loads(index_path.read_text())
fulltexts = {r['arxiv_id']: r for r in index['items']}
assert len(fulltexts) == 13
assert all(r['fulltext_status'] == 'version_verified' for r in fulltexts.values())

requests = [json.loads(line) for line in (INTAKE / 'network/hf-daily/attempts.jsonl').read_text().splitlines()]
board_request = next(r for r in requests if r['params']['date'] == '2026-11-16')
board_body = ROOT / board_request['body_path']
assert sha(board_body) == board_request['body_sha256']
shutil.copyfile(board_body, RAW / 'hf-2026-11-16.body.json')
shutil.copyfile(official_path, RAW / 'official-metadata-records.json')

# Each excerpt was selected from a read abstract. All matches are checked below.
# The direction is descriptive for a rejected item, not an endorsement as RSI.
judgments = {
    '2611.18359': ('reject', 'theory_survey', 'off_topic',
        '通用具身 S2 架构、能力评测与路线综述；第 6.2.4 节确实讨论保留的工具、技能和 Harness 变更及验证标准，但它是广义路线的一个未来方向，主体并非 Harness 反馈演化专项。保留该正向证据，不误称全文完全没有演化研究。',
        'we propose an evaluation framework that measures both model capabilities and closed-loop system performance.'),
    '2611.18397': ('reject', 'model_weights', 'single_round_training',
        'Gamer 的持久学习对象是经过预训练、指令微调和多轮交互 RL 训练的 VLA 模型；摘要未给出反馈改写外部程序工件并保留的机制。多轮 rollout 不能单独证明 Harness 共演化。',
        'We train the policy for long-horizon interaction with a stable multi-turn reinforcement learning method'),
    '2611.15789': ('reject', 'evaluation_benchmark', 'off_topic',
        '评估 Agent 交付的 Blender 4D 场景及渲染视频；反馈修订的是外部创作产物，非 Agent 自身可复用 Harness。',
        'an agent turns a brief into an executable 4D scene and renders its proxy video.'),
    '2611.18482': ('reject', 'model_weights', 'single_round_training',
        '训练视觉依赖 token 的 speculative drafter 并做稀疏注意力加速；自适应加权不构成持久修改 Agent 工件。',
        'a simple and effective framework that adaptively upweights visually dependent tokens that the drafter predicts poorly.'),
    '2611.12901': ('reject', 'model_weights', 'not_persistent',
        'StepRefine 在一次生成内按熵峰切换解码与潜变量精炼；controller 固定，修改不作为后续任务的程序版本保留。',
        'a step-aware switch between discrete denoising and latent refinement.'),
    '2611.17831': ('reject', 'model_weights', 'single_round_training',
        '通过反事实监督训练视频语言模型读取冻结编码器里的动态信息，未见外部 Harness 反馈演化。',
        'we then build counterfactual supervision'),
    '2611.07226': ('reject', 'model_weights', 'off_topic',
        '研究 Transformer 残差与共享块的深度记忆结构；所谓 loop 是网络计算结构，不是 Agent 自改程序工件。',
        'Looped Transformers reduce parameter count by repeatedly applying shared blocks'),
    '2611.17878': ('reject', 'ai4ai', 'off_topic',
        '生成城市卫星影像及动态能源地图，是领域生成模型与外部数据产物，不是 Harness 演化。',
        'synthesizes static urban satellite imagery together with spatially aligned, dynamic monthly building energy consumption maps.'),
    '2611.17814': ('reject', 'data_task', 'off_topic',
        'G-CAST 确有循环更新和保留的 executable reward，但 §4 明确它用于训练路由与模型适应。新工具、技能及 SOP 的 capability contract expansion 是输入条件，未展示反馈编辑这些执行工件的循环。按训练奖励/权重方向排除，不是因权重训练而排除。',
        'reward-routed, entropy-prioritized training data and governed reward evolution.'),
    '2611.18338': ('reject', 'experience_world_model', 'static_framework',
        'MEM-SQL 的三层记忆来自已验证问题-SQL 历史，全文明确评估期间固定；SQL 修复针对当前任务查询，未改写管理策略或可复用 Harness。',
        'MEM-SQL'),
    '2611.17955': ('reject', 'evaluation_benchmark', 'off_topic',
        '通用多模态网页任务执行基准，逐任务隔离状态并比较固定配置；未专门研究反馈改写并跨任务保留的 Harness。',
        'WebArena-Pro runs each task in isolation and supports reproducible, parallel evaluation.'),
    '2611.18549': ('reject', 'model_weights', 'off_topic',
        '像素空间视频扩散模型结构与训练设计，没有 Agent 程序工件演化。',
        'a simple large-patch DiT-style Transformer for pixel-space video diffusion'),
    '2611.06866': ('reject', 'evaluation_benchmark', 'off_topic',
        'GH-AWTrace 主体是普通 Agent 工作流日志数据与失败/工具/单次协调分析。引言存在反馈改 Copilot instructions 的有效案例，但并非论文的 Harness 演化专项评测；不能据一个动机案例把全数据集标为演化研究。',
        'These observations enable research on execution failures, tool use, and the relationship between reported run outcomes and visible task progress.'),
    '2611.17194': ('reject', 'model_weights', 'single_round_training',
        'eDMD 改蒸馏学生/评分模型的分布匹配训练目标，未展示外部 Harness 经反馈保留修改。',
        "trains a single shared fake model exclusively on the student's final outputs"),
    '2611.17440': ('reject', 'evaluation_benchmark', 'off_topic',
        '比较模型、scaffold 与 reasoning effort 对轨迹行为的影响，固定配置的跨仓检索并非反馈演化的专项评测。',
        'scaffold'),
    '2611.02822': ('reject', 'model_weights', 'single_round_training',
        '在视频扩散蒸馏中区分语义锚定与运动注意力；保持初始帧上下文不等于长期程序性 Harness 更新。',
        'a distillation-time plug-in for AR-VDMs'),
    '2611.17820': ('reject', 'safety_governance', 'static_framework',
        '研究固定多 Agent 角色/通信/安全提示干预；协调者产出的安全规格面向当前开发任务，无反馈驱动地修订并跨任务保留 Harness 的证据。',
        'having a designated safety lead agent ensure system-level safety'),
    '2611.14487': ('reject', 'evaluation_benchmark', 'off_topic',
        '问题游戏依据 oracle 反馈修改科研想法这一外部产物；固定游戏框架不因此形成 Agent 自身 Harness 演化。',
        "Re-Search tracks how a model's idea evolves as it asks questions and receives binary oracle feedback"),
    '2611.14505': ('accept', 'evaluation_benchmark', None,
        '专项评估外部程序/技能持久化的学习收益：最终判定在存储前返回，程序经验证保存，后续新会话加载工件；有清空状态对照和冻结后的已见/未见任务测试。纳入为 Harness 专项基准，非声称基准本身会自改。',
        'We run an agent harness with frozen weights, with and without persistence'),
    '2611.18442': ('reject', 'evaluation_benchmark', 'off_topic',
        'CAN 轨迹恢复与隐私攻击基准，LLM 只从已有候选重建路线中选择；模型设置及预算经验证 pilot 后固定，未演化自身 Harness。',
        'an LLM harness that selects among candidate routes'),
    '2611.17811': ('reject', 'evaluation_benchmark', 'off_topic',
        '研究 AI 论文审稿批评的附录偏差；无 Harness 工件反馈改写或跨任务接受机制。',
        'we know little about which parts of a paper these models actually criticize.'),
    '2611.14504': ('reject', 'model_weights', 'off_topic',
        '蛋白-配体基础模型预训练与生物能力涌现，持久对象为模型权重，不是 Agent 工件自改。',
        'Bonbon was trained on protein-ligand sequences alone'),
    '2611.16439': ('reject', 'embodied', 'off_topic',
        '人机对齐示范采集界面、部署数据校准与机器人策略学习；人类物理反馈不是 Harness 自主修订。',
        'a human-aligned data collection system for whole-body mobile manipulation.'),
    '2611.18529': ('reject', 'experience_world_model', 'static_framework',
        '固定 e-means 配方执行说话人聚类与窗口内标签修订；变更的是聚类状态/身份，不是管理工件。',
        're-clustering is confined to a bounded window, labels are revised for a few seconds'),
    '2611.18130': ('reject', 'evaluation_benchmark', 'off_topic',
        '人工反馈改考试 PDF 转换代码用于构建金融题库；该代码是外部数据产物，基准评估金融知识而非 Harness 演化。',
        'a coding agent writes exam-specific conversion code and a review page, while a human verifies every example and feeds corrections back to the agent.'),
    '2611.18429': ('reject', 'evaluation_benchmark', 'off_topic',
        '研究水下图像质量指标、人类偏好与生成编辑漂移；被测试的是外部图像及指标，不是 Agent 程序演化。',
        'whether these metrics agree with human judgments.'),
    '2611.18550': ('reject', 'model_weights', 'single_round_training',
        '蒸馏生成器的 adapter 微调或固定主方向激活引导，非跨任务保留的 Harness 修订。',
        'ReDiverse-FT fine-tunes a lightweight adapter'),
    '2611.17169': ('reject', 'evaluation_benchmark', 'off_topic',
        '对输出编码格式做预定 LoRA 微调对照；当前话语内自我纠正不构成 Harness 长期修改。',
        'we fine-tune two sub-billion models'),
    '2611.16661': ('reject', 'harness', 'static_framework',
        '固定调度规则根据观测进度调整当前批次资源和队列；没有根据效果改写调度程序并跨任务采纳新版本。',
        'Chain-Advancing Action Scheduling (CAAS), which prioritizes long chains using observed progress'),
    '2611.16500': ('reject', 'model_weights', 'single_round_training',
        'Even 语言数据集、tokenizer 扩展与 LoRA 适配，不含外部 Harness 反馈演化。',
        'Using LoRA fine-tuning of Qwen3-VL-4B'),
    '2611.17780': ('reject', 'model_weights', 'static_framework',
        '训练好的 SQL 模型及 validator 参与预注册置信度级联，当前查询候选选择不会持续改写级联策略。',
        'a pre-registered confidence cascade'),
    '2610.41354': ('reject', 'embodied', 'not_persistent',
        '冻结控制器的测试时输入噪声优化及后续策略定向微调，目标是当前运动或模型权重，未修改外部可复用 Harness。',
        "differentiable task costs guide optimization of the generator's input noise with frozen weights"),
    '2611.16010': ('reject', 'model_weights', 'off_topic',
        '图像/深度联合生成的统一骨干模型与尺度研究，无 Agent 反馈工件更新。',
        'Iris-Z is a general image generator that produces appearance and geometry together.'),
    '2611.17321': ('reject', 'model_weights', 'not_persistent',
        '训练 flow 并在测试时以连接约束修正 LEGO 姿态；改进的是外部组装结果，不是 Agent Harness。',
        'an analytic connectivity-field guidance to pull predictions toward connected assemblies at test time.'),
    '2611.05843': ('reject', 'model_weights', 'not_persistent',
        '固定联合 flow 在图像/测量状态上做反问题求解；连续状态迭代不是可复用程序更新。',
        'image and measurement states are jointly updated based on their current values.'),
    '2611.15640': ('reject', 'evaluation_benchmark', 'off_topic',
        '流式视频记忆能力评测，区分记忆必要性和视觉理解；没有专门研究管理代码/技能文件的反馈演化。',
        'a benchmark dedicated to evaluating memory capabilities in streaming video understanding.'),
    '2611.16312': ('reject', 'embodied', 'static_framework',
        '多材料物理引擎虽提供 Agent 文档、错误修复提示和 MCP 工具，但这是固定能力接口；Agent 训练外部机器人策略不等于修改自身 Harness。',
        'the engine is exposed as tools over the Model Context Protocol.'),
}


def fulltext_quote(arxiv_id, locator, quote, purpose):
    item = fulltexts[arxiv_id]
    p = ROOT / item['body_path']
    assert sha(p) == item['body_sha256']
    if p.suffix == '.html':
        soup = BeautifulSoup(p.read_text(), 'html.parser')
        element = soup.find(id=locator)
        assert element is not None, (arxiv_id, locator)
        text = norm(element.get_text(' ', strip=True))
    else:
        text = norm((ROOT / item['text_path']).read_text())
    assert norm(quote) in text, (arxiv_id, locator, quote)
    return {
        'purpose': purpose, 'locator': locator, 'quote': norm(quote),
        'source_url': item['fulltext_url'] + (('#' + locator) if p.suffix == '.html' else ''),
        'body_path': item['body_path'], 'body_sha256': item['body_sha256'],
        'match': 'exact_contiguous_after_whitespace_normalization',
    }


quotes = {
    '2611.14505': [
        ('S2.SS1.p1', 'We deliver the verdict on the final submission before any storage step, such that storage decisions can reflect the outcome.', 'feedback'),
        ('S3.SS0.SSS0.Px3.p1', 'We run prime-agent ( Karten et al., 2026 ) with its tools and automatic refinement, opening a fresh conversation per instance.', 'tested_artifact_context'),
        ('S3.SS0.SSS0.Px3.p1', 'It may store learnings after the final verdict, in hindsight, and only its written state carries over.', 'feedback_and_persistence'),
        ('S4.SS0.SSS0.Px4.p1', 'explicitly told the harness to write Python programs to solve the tasks, verify each program against the demonstrations, save it for its task and reuse it.', 'program_artifact'),
        ('A4.SS1.p1', 'Nothing carries from one instance to the next except what the harness persisted itself, which is the global harness store, skills and workspace files for prime-agent, the memory and skill files for hermes-agent, and the memory notes, skills and dream diary for openclaw.', 'concrete_external_artifacts'),
        ('S2.SS3.p1', 'We start every test instance from the learner’s state at the end of the stream, and nothing learned on one test instance reaches another.', 'frozen_evaluation'),
        ('S2.SS3.p1', 'The seen test consists of four fresh instances of each of the stream’s 25 tasks, at instance seeds the stream did not use, and measures memorization.', 'seen_test_definition_not_cross_task_generalization'),
        ('S2.SS3.p1', 'In the held-out test, which measures generalization, 100 evaluation tasks never seen on the stream are served once each.', 'held_out_definition'),
        ('S2.SS4.p1', 'the same learner on the same stream and the same tests, with its state wiped before each instance.', 'reset_control'),
        ('S1.p5', 'harness-based methods gain little or nothing on the unseen tasks.', 'result_qualification'),
        ('S3.SS0.SSS0.Px4.p1', 'The teacher’s play receives uncharged feedback, so these are upper-bound experiments for what GLM can teach Qwen through the harness.', 'matched_budget_limitation'),
        ('A12.SS0.SSS0.Px1.p1', 'QDE excludes training compute and teacher labels.', 'cost_comparison_limitation'),
    ],
    '2611.17814': [
        ('S4.SS0.SSS0.Px2.p2', 'Reward update proposal then specifies the executable rule change needed to correct that mismatch.', 'positive_update_evidence'),
        ('S4.SS0.SSS0.Px2.p2', 'Trial adaptation uses the candidate reward to control routing and training on an audit batch.', 'training_reward_object'),
        ('S4.SS0.SSS0.Px2.p3', 'Within this loop, the executable reward is a versioned bundle of components.', 'positive_persistence_evidence'),
        ('S4.SS0.SSS0.Px4.p1', 'The training reward evolves with the capability contract during the loop, but all results reported in this paper are measured with one common frozen evaluation reward: the final contract-complete version.', 'training_vs_evaluation_boundary'),
        ('S5.SSx1.p3', 'all methods within an experiment use the same parent model, harness version, candidate universe, teacher targets, and decoding configuration.', 'harness_is_input_to_comparison'),
    ],
    '2611.18338': [
        ('S4.SS1.p1', 'and keep it fixed throughout evaluation.', 'fixed_memory'),
        ('S7.p3', 'MEM-SQL is also evaluated with static memory, so how adding, updating and retiring memory affects performance in dynamic settings remains open.', 'explicit_static_limit'),
    ],
    '2611.06866': [
        ('S1.p2', 'a weekly workflow reads feedback on merged pull requests and turns recurring reviewer requests into proposed updates to the repository’s Copilot instructions', 'positive_motivating_example_preserved'),
        ('S1.p4', 'illustrative use cases showing how the data can support studies of failures, tool interactions, and within-run agent coordination.', 'actual_research_scope'),
        ('S4.SS3.p1', 'It shows within-run delegation and synthesis, while providing no evidence of memory shared across runs.', 'example_scope_limit'),
    ],
    '2611.18359': [
        ('S1.p5', 'The roadmap connects this progression to four research directions, including continual improvement from physical experience.', 'broad_scope'),
        ('S6.SS2.SSS4.p1', 'Continual improvement retains a change to memory, tools, skills, the harness, or a policy, and verifies that it improves later work.', 'positive_definition_preserved'),
        ('S6.SS2.SSS4.p2', 'Others change tools, skills, and harness code around a frozen model', 'positive_harness_discussion_preserved'),
        ('S6.SS2.SSS4.p4', 'A credible claim of improvement should therefore report gains on held-out tasks and show no regression on earlier tasks.', 'positive_validation_criteria_preserved'),
        ('A1.SS8.SSS0.Px1.p1', 'Such a claim should pass the three-part test of Section 6.2.4 : gains on held-out tasks, no regression, and separate contributions of the S2 foundation model, the harness, and S1.', 'survey_specificity_boundary'),
    ],
    '2611.17820': [
        ('S3.p2', 'Collaborative artifacts (e.g., a Python module the team is jointly building, or a system-level safety document the manager produces) accumulate in this workspace.', 'current_task_workspace'),
        ('S4.SS1.SSS0.Px3.p6', 'The PM is instructed to write an explicit system-level safety specifications document before decomposing the task; the document is shared with all coders alongside their module subtasks.', 'static_intervention'),
    ],
    '2611.17440': [
        ('S1.p4', 'Finally, we examine frontier models and agent scaffolds to show how scaffold choice and reasoning effort systematically shift patterns of exploration, modification, and verification.', 'fixed_configuration_comparison'),
        ('S3.p3', 'Deploying the same base model under different scaffolds is treated as a distinct stack.', 'research_unit'),
    ],
    '2611.17955': [
        ('S1.p3', 'WebArena-Pro runs each task in isolation against per-task seeded container state, supporting reproducible parallel evaluation that avoids drift between runs.', 'independent_task_execution'),
    ],
    '2611.15789': [
        ('S1.p1', 'Coding agents can build it instead: from a script, photos, a continuation or real footage, they write Blender code, render previews, inspect their frames and revise', 'external_task_artifact'),
    ],
    '2611.18442': [
        ('PDF Section VI.2 LLM-based candidate selection', 'Model settings and budgets are fixed after a validation pilot', 'fixed_selector'),
    ],
    '2611.18130': [
        ('S1.p3', 'a coding agent generates exam-specific conversion code and a review page, while a human verifies every example and feeds corrections back to the agent.', 'external_benchmark_construction'),
    ],
    '2611.16661': [
        ('S2.p5', 'CAAS uses observed trajectory progress to advance long execution chains and shorten the batch tail without changing individual job service times.', 'fixed_dispatch_rule'),
    ],
    '2611.14487': [
        ('S1.p2', 'Given only the research problem of a published paper, an inquisitor model must rediscover the paper’s idea by asking up to 100 yes-or-no questions', 'external_idea_search'),
    ],
}

records = []
for r in board:
    rid, aid = r['id'], r['arxiv_id']
    saved = baseline.get(rid)
    if saved is not None:
        assert aid in {'2611.12068', '2611.13509', '2611.16378'}
        records.append({
            'id': rid, 'arxiv_id': aid, 'title': r['title'],
            'recommendation': 'reuse_existing',
            'hf_daily_date_observed': '2026-11-16',
            'hf_observed_at': r['first_seen'],
            'existing_first_seen': saved['first_seen'],
            'existing_review_decision': saved['review']['decision'],
            'existing_review': saved['review'],
            'note_zh': '只增补实际观察的 HF 推荐日；保留已有 first_seen、审核决定、事实正文和刊期，不重复计为新纳入。旧论文范围不在本次重新评判。',
            'canonical_baseline_path': rel(baseline_path),
            'canonical_baseline_sha256': sha(baseline_path),
        })
        continue

    decision, primary, reason, why, excerpt = judgments[aid]
    # A case-insensitive check is used only to locate source capitalization;
    # the stored excerpt always retains the actual source's exact characters.
    pos = r['abstract'].lower().find(excerpt.lower())
    assert pos >= 0, (aid, excerpt)
    source_quote = r['abstract'][pos:pos + len(excerpt)]
    assert source_quote in r['abstract']
    meta = official[rid]
    assert norm(meta['title']).casefold() == norm(r['title']).casefold(), (aid, meta['title'], r['title'])
    rec = {
        'id': rid, 'arxiv_id': aid, 'title': meta['title'],
        'recommendation': decision, 'suggested_primary': primary,
        'suggested_secondary': ['harness'] if decision == 'accept' else [],
        'harness_sub': None, 'exclude_reason': reason,
        'reason_zh': why,
        'reviewed_on': '2026-11-18', 'recommended_edition': '2026-11-16',
        'hf_daily_dates': ['2026-11-16'], 'actual_new_first_seen': r['first_seen'],
        'published': meta['published'], 'updated': meta['updated'], 'version': meta['version'],
        'identity_check': 'HF stable arXiv ID and normalized title match official arXiv metadata',
        'source_abstract_quote': source_quote,
        'source_abstract': r['abstract'],
        'official_abstract': meta['abstract'],
        'official_abstract_sha256': hashlib.sha256(meta['abstract'].encode()).hexdigest(),
        'hf_official_abstract_same': norm(meta['abstract']) == norm(r['abstract']),
        'review_basis': 'official_versioned_fulltext_and_both_abstracts' if aid in fulltexts else 'HF_abstract_and_official_metadata_abstract',
        'fulltext_evidence': [fulltext_quote(aid, *q) for q in quotes.get(aid, [])],
        'scope_only': True,
        'experimental_replication': False,
        'source_numbers_recomputed': False,
    }
    if aid in fulltexts:
        rec['fulltext'] = {k: v for k, v in fulltexts[aid].items() if k != 'official_metadata'}
    if aid in {'2611.17814', '2611.06866', '2611.18359', '2611.18338'}:
        rec['boundary_item'] = True
    if aid == '2611.18359':
        rec['scope_confidence'] = 'medium'
        rec['counterevidence_zh'] = '全文有实质 Harness 改进讨论，争点是是否达到专门研究的范围门；若主审相反，保留分歧，不可单凭此稿自动接受。'
    if aid == '2611.14505':
        rec['summary_proposal'] = {
            'summary_zh': 'Continual-ARC 用反复出现且实例更新的 ARC 任务流，比较可保留程序和技能文件的 Agent Harness 与清空状态的对照；流结束后冻结系统，分别测试已见任务的新实例和未见任务。论文观察到，持久化本身的记忆收益有限，明确的程序编写、验证与复用指导能改善已见任务表现，而未见任务的泛化收益仍很小或没有。纳入为 Harness 专项评测；反馈预算可比不代表模型训练与教师成本完全匹配。',
            'summary_en': 'Continual-ARC evaluates persistent agent harnesses on a stream of recurring ARC tasks with fresh instances, using reset controls and frozen seen-task and held-out tests. The tested systems retain programs and skill files across sessions. Persistence alone generally gives limited memorization gains; explicit guidance to write, verify and reuse programs helps on returning tasks, while gains on unseen tasks remain small or absent. This is a harness-focused evaluation, not evidence that feedback-budget comparisons match training and teacher costs.',
        }
        rec['numeric_check'] = {
            'proposed_summary_quantitative_results': [],
            'status': 'no_quantitative_result_claims_in_proposed_summary',
            'checked': 'Qualitative results checked against official v3; source numeric strings in evidence are unmodified.',
            'warning': 'HF says "No harness-based method gains"; official v3 says "gain little or nothing". Use the latter qualified wording.',
        }
        rec['evidence_boundaries'] = {
            'matched_total_compute_budget': 'unknown',
            'cross_model_artifact_transfer': 'unknown',
            'all_reported_experimental_numbers_recomputed': False,
            'interpretation': 'Seen-task gains are memorization; frozen held-out tasks test generalization. Multiple tested models alone do not prove artifact transfer.',
        }
    records.append(rec)

counts = dict(Counter(r['recommendation'] for r in records))
assert counts == {'reject': 36, 'reuse_existing': 3, 'accept': 1}, counts
payload = {
    'schema': 'follow_rsi_independent_scope_review_v1',
    'reviewer': '/root/nov18_hf16_crossreview',
    'review_round': 3,
    'frozen_at': datetime.now(timezone.utc).isoformat(),
    'independence': 'Judgments made from source records and scope rules without reading the parent reviewer\'s per-item draft. Not a claim of double-blind review.',
    'status': 'independent_first_draft_frozen',
    'scope': 'Complete HF 2026-11-16 board observed on 2026-11-18; new-item scope review and metadata-only reconciliation of three existing IDs.',
    'counts': {**counts, 'raw_board_members': 40, 'new_ids': 37, 'version_verified_fulltexts': 13},
    'source_observation': {
        **board_request,
        'preserved_body_path': rel(RAW / 'hf-2026-11-16.body.json'),
        'normalized_source_path': rel(hf_path), 'normalized_source_sha256': sha(hf_path),
        'official_metadata_path': rel(RAW / 'official-metadata-records.json'),
        'official_metadata_sha256': sha(official_path),
        'fulltext_index_path': rel(index_path), 'fulltext_index_sha256': sha(index_path),
    },
    'rules': [
        {'path': 'feed/taxonomy.yaml', 'sha256': sha(ROOT / 'feed/taxonomy.yaml')},
        {'path': 'feed/prompts/harness_gate.md', 'sha256': sha(ROOT / 'feed/prompts/harness_gate.md')},
    ],
    'limitations': [
        'This is source-bound scope review, not replication or recomputation of all experimental numbers.',
        'No paid requests, no publication decisions, no canonical or review YAML edits.',
        'Evidence-Governed Adoption, MIRIX-2.0 and Mobile AI Factory reuse earlier decisions; no fresh acceptance is asserted.',
        'Broad-scope Envisioning Agentic Robotics has positive Harness-improvement discussion; scope disagreement must be preserved if the lead review differs.',
        'The parent must finish round reconciliation, exact source/content checks and approval provenance before publication.',
    ],
    'paid_requests': 0,
    'items': records,
}
target = REPORT / 'independent-review-v1.json'
assert not target.exists(), 'Frozen review already exists; use an amendment for later changes.'
target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
receipt = {
    'path': rel(target), 'sha256': sha(target), 'counts': payload['counts'],
    'all_source_quotes_matched': True,
    'fulltext_quotes_checked': sum(len(x.get('fulltext_evidence', [])) for x in records),
    'abstract_quotes_checked': 37,
    'numeric_claims_added_to_summary': 0,
    'paid_requests': 0,
}
(REPORT / 'independent-review-v1-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
