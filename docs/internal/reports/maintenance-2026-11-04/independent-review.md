# 2026-11-04 独立第三轮复审

本轮维护核对的是 **2026-11-03 HF 榜单**：11 月 4 日当日榜尚未开放。45 篇原始摘要已逐篇筛查，其中 8 篇新增重点论文核查官方正文，2 篇旧审核按内容哈希复用，其余 35 篇为摘要初筛；不能将 45 篇描述为全文审查。

**建议：4 篇纳入（2 篇新增、2 篇旧记录补榜单），40 篇排除当前专题，1 篇保留分歧。** RSS 的 8 条新记录均建议排除；其中 1 条读了全文、1 条另核官方 RSS 摘要。所有正式 decision 均为 `defer`，本报告不构成接受或发布。

## 新增正例与真实分歧

- **NorthCUA**：仅 §4.3.1 的反馈技能改写支路纳入 Harness 组件。程序指导经过独立验证，失败修订后重测准入，并明确供后续任务使用。子类为 `component`；主审 B 已按独立反馈从初版 `evolve_main` 更正，当前双方一致。全模型训练、milestone 快照以及全模型榜单结果不能一并归为 Harness 演化证据。
- **Can Coding Agents Sustain Continual Evolution without Forgetting?**：纳入 Harness 专项评测。研究冻结模型外围提示、执行逻辑与工具的连续改写和跨数据集遗忘。小样本演化与回测不能自动标记独立留出或同预算控制。
- **Avatar Intelligence**：主审 A 建议排除；独立复审保留 `borderline`。Table 1 明言 rehearsal 会更新 Harness 等工程范式，但全篇是更宽的个人代理议程，是否达到 Harness 专项理论标准须由 owner 裁决。保留分歧，不强行改成正例。

## 容易误判的负例

- **CUA-Master**：确有反馈与 primitive 保留，主要被优化对象是任务/环境规格与模型训练数据。
- **CoworkOS**：固定运行时组织外部模型训练；数据配方、训练策略和任务状态的变化不等于运行时程序自改。
- **SWE-Trail**：确会编译和准入可执行 detector 规则，但限定单一 issue、当轮冻结；跨轮更新和跨 issue 调整仍列作未来工作。
- **TAL**：专门核查了 `G_phi` 反思支路及附录 A.2；其外部状态是题目、教学事件和回答结果，教程章节按失败反馈更新。不能简化为“没有反馈”，但尚未显示通用出题、检索或记忆管理程序版本的持久改写。
- **SIMIT**：固定 synthesizer 生成数据，反馈修复图像/样本；学习结果进入 ICL 或权重，联合改写 synthesizer 是未来工作。

## 来源、日期与复用边界

- 45 条 ID、标题、摘要及顺序与原始 HF `paper.summary` 逐项一致；没有使用 HF 自动 `ai_summary` 当论文原文。
- 8 篇重点论文按官方 abs 核身份、原始发表日期与版本记录。SIMIT（2611.00053）的官方 `citation_date` 和唯一 v1 history 都写 **2026-10-11 15:59:08 UTC**，与编号月份不同；原样记录此异常，不按编号改日期。
- VideoHarness 与 TinyAstral 的当前内容来源哈希与 11 月 2 日有效审查一致，本次只补 11 月 3 日 HF 归属。HF 归属变动仍会改变审批哈希，不自动迁移任何批准。VideoHarness 保持理论/综述，TinyAstral 的冻结教师 Harness 阶段与后续学生蒸馏分开。
- 排除项定向抽查：LeanGuard、DeFT-RAG、Reviso、BYOD、ReTrace、MACR。均明确只核摘要边界；没有假称阅读全文。
- DeepMind cheminformatics 全文中的留出集验证对象是 potency 模型；固定技能帮助生成外部科研产物，不据此列为 Harness 自改。OpenAI physical engineering 只核官方 RSS 摘要。

## 逐篇范围结论

| HF 顺序 | ID | 独立建议 | 审核深度 | 依据 |
| --- | --- | --- | --- | --- |
| 1 | arxiv:2611.01860 | 排除当前专题 | 摘要初筛 | 图形学 Agent 和文献系统综述；摘要中的反馈改动是图形代码产物，未显示专门研究持久 Harness 演化。 |
| 2 | arxiv:2611.00859 | 排除当前专题 | 摘要初筛 | 视频生成模型的训练/采样方法，未显示外部 Harness 工件随反馈改写。 |
| 3 | arxiv:2611.03126 | 排除当前专题 | 重点正文 | 世界—数据—模型飞轮更新任务数据和模型权重；primitive 库是合成任务的环境/能力/验证规格，非自身 Harness 版本。 |
| 4 | arxiv:2611.03178 | 排除当前专题 | 重点正文 | 固定 CoworkOS 运行时组织实验，迭代对象是外部模型的数据配方和训练策略；持久任务记忆不等于运行时自改。 |
| 5 | arxiv:2610.40191 | 建议纳入 | 旧审查哈希复用 | 复用既有官方 PDF 审核：专门讨论持久 Harness 修订及评估边界，按理论/综述建议纳入，非新演化方法。 |
| 6 | arxiv:2611.01560 | 排除当前专题 | 摘要初筛 | 统一 robot-use Harness 支持后续训练；摘要没有执行反馈改写框架并保留版本的机制。 |
| 7 | arxiv:2611.02074 | 排除当前专题 | 重点正文 | 确有从历史编译并验证检测规则，但限定单个 issue、collection round 内固定；跨轮历史更新和跨 issue 分配仍是未来工作。 |
| 8 | arxiv:2611.02102 | 建议纳入 | 重点正文 | §4.3.1 技能支路将执行发现写成操作指导，独立验证、失败修订、准入后保留并供后续任务复用；仅此组件建议纳入。 |
| 9 | arxiv:2611.02897 | 排除当前专题 | 摘要初筛 | 照片取景/构图模型，未显示 Harness 工件的持久反馈改写。 |
| 10 | arxiv:2610.27954 | 排除当前专题 | 摘要初筛 | ReTrace 专项研究当前环境状态恢复；是一般代理恢复评测，未专门研究 Harness 版本演化。 |
| 11 | arxiv:2611.03424 | 排除当前专题 | 摘要初筛 | 科研 idea 判断评测，不是 Harness 演化专项评测。 |
| 12 | arxiv:2611.02112 | 排除当前专题 | 摘要初筛 | 训练/蒸馏模型权重，不是外部程序工件演化。 |
| 13 | arxiv:2611.03602 | 排除当前专题 | 摘要初筛 | Reviso 用 GRPO 学习观察和工具策略；当前视频内计划更新不构成跨任务程序版本。 |
| 14 | arxiv:2611.00172 | 排除当前专题 | 摘要初筛 | 全模态 embedding 综述，与 Harness 反馈演化无直接证据。 |
| 15 | arxiv:2611.01815 | 排除当前专题 | 摘要初筛 | 物理意外/世界模型能力评估，不是 Harness 演化专项评测。 |
| 16 | arxiv:2611.01484 | 排除当前专题 | 摘要初筛 | 跨仓库软件工程基准，未展示专门测量 Harness 自改过程。 |
| 17 | arxiv:2610.39419 | 排除当前专题 | 摘要初筛 | 视觉推理的固定 scaffolding，不是执行反馈改写并保留 scaffolding 的方法。 |
| 18 | arxiv:2611.03344 | 排除当前专题 | 摘要初筛 | 注意力计算/内核方法，不是 Agent 自身 Harness 改写。 |
| 19 | arxiv:2611.03092 | 待定/分歧 | 重点正文 | Avatar 的 §4.2 明言 rehearsal 会更新 Harness 等工程范式，但整体仍是广义个性化代理议程；保留理论范围分歧。 |
| 20 | arxiv:2610.42128 | 排除当前专题 | 摘要初筛 | 决策模型的蒸馏/训练，不是外部 Harness 工件修改。 |
| 21 | arxiv:2611.02633 | 排除当前专题 | 摘要初筛 | 协作智能/团队能力评测，未专门研究持久 Harness 演化。 |
| 22 | arxiv:2611.02332 | 排除当前专题 | 摘要初筛 | LeanGuard 在固定证明/策略体系内修复被拒工具调用；修的是当前调用，不是验证策略程序版本。 |
| 23 | arxiv:2610.37826 | 排除当前专题 | 摘要初筛 | DeFT-RAG 跨问题保存并复用 QA 缓存；内容保留与固定检索框架不等于记忆管理机制演化。 |
| 24 | arxiv:2610.41574 | 排除当前专题 | 摘要初筛 | BYOD 冻结基座但训练 LoRA 适配器；仍是模型权重变化，不能只凭 frozen base 纳入。 |
| 25 | arxiv:2611.03526 | 排除当前专题 | 摘要初筛 | 神经网络内部层/路由机制，不是模型外部 Harness 演化。 |
| 26 | arxiv:2610.40293 | 排除当前专题 | 摘要初筛 | 多代理服务/硬件工作负载评测，不是 Harness 反馈改写评测。 |
| 27 | arxiv:2610.38623 | 排除当前专题 | 摘要初筛 | 固定 backbone 上残差网络等模型训练，不是外部 Harness 程序。 |
| 28 | arxiv:2610.35219 | 排除当前专题 | 摘要初筛 | MACR 继承和细化当前推理轨迹；relay 触发与竞价规则作为固定框架，未显示持久改写。 |
| 29 | arxiv:2610.38637 | 排除当前专题 | 摘要初筛 | 教师/学生模型权重训练，不是外部 Harness 程序。 |
| 30 | arxiv:2610.41296 | 排除当前专题 | 摘要初筛 | 辅助 reward 用于训练模型，不是 Agent 自己的环内验证器版本演化。 |
| 31 | arxiv:2611.03097 | 排除当前专题 | 摘要初筛 | 页面检索和加权 SFT 方法；未显示固定模型周围的可复用程序自改。 |
| 32 | arxiv:2611.01460 | 排除当前专题 | 重点正文 | TAL 有反馈和跨问题教程知识保留；A.2 的生成器反思写回题目/事件/答案历史，不是通用生成/检索程序版本。 |
| 33 | arxiv:2611.00053 | 排除当前专题 | 重点正文 | SIMIT 的 synthesizer 固定；反馈修复合成图像/数据，产出进入 ICL 或模型权重，非 rendering skill 自改。 |
| 34 | arxiv:2610.39278 | 排除当前专题 | 摘要初筛 | 世界模型预训练，不是 Harness 演化。 |
| 35 | arxiv:2610.39639 | 排除当前专题 | 摘要初筛 | 3D/空间推理基准，不是 Harness 演化专项评测。 |
| 36 | arxiv:2611.03219 | 建议纳入 | 重点正文 | 冻结基础模型，专门研究提示、执行逻辑和工具的跨数据集连续演化及遗忘；建议纳入 Harness 评测。 |
| 37 | arxiv:2610.27815 | 排除当前专题 | 摘要初筛 | 模型转换/解码机制，未显示外部可复用 Harness 工件的反馈修订。 |
| 38 | arxiv:2611.02782 | 排除当前专题 | 摘要初筛 | 视频模型蒸馏/训练，不是 Harness 演化。 |
| 39 | arxiv:2610.32878 | 排除当前专题 | 摘要初筛 | 压缩与搜索算法，不是 Agent 自身 Harness 持久修改。 |
| 40 | arxiv:2611.02928 | 排除当前专题 | 摘要初筛 | Lab2Sim 用执行验证修订虚拟实验网页这一外部产物；不是生成代理自身 Harness 演化。 |
| 41 | arxiv:2610.41216 | 建议纳入 | 旧审查哈希复用 | 复用旧审核：先冻结教师、反馈修订工具/恢复逻辑并成对检验准入，再冻结 Harness 蒸馏学生；两阶段须区分。 |
| 42 | arxiv:2610.41994 | 排除当前专题 | 摘要初筛 | 循环神经网络内部状态/参数初始化，不是外部 Harness 程序。 |
| 43 | arxiv:2611.03393 | 排除当前专题 | 摘要初筛 | 视频超分辨率/修复模型训练，不是 Harness 演化。 |
| 44 | arxiv:2610.38252 | 排除当前专题 | 摘要初筛 | 音乐生成模型教程/综述，未显示 Harness 演化专项研究。 |
| 45 | arxiv:2611.00074 | 排除当前专题 | 摘要初筛 | 人脸 morph 检测评测，不是 Harness 演化专项评测。 |

## 重点正文原文凭证

### CUA-Master: Scaling Computer-use Agents through Open-World Recursive Improvements (arxiv:2611.03126)

原始/当前 v1 日期：`2026-11-02T13:41:14Z`。建议：排除当前专题；方向边界：`data_task/model_weights`。

> Semantically equivalent primitives are canonicalized and deduplicated, while variants with distinct preconditions, environment requirements, or verification logic are retained.

[S2.SS4.SSS1.p1.2](https://arxiv.org/html/2611.03126#S2.SS4.SSS1.p1.2) — 反证：确有持久 primitive 库，但对象为任务/环境规格。

> each iteration of SFT is trained starting from the same base checkpoint, with the updated data from each iteration added to the original training set.

[S2.SS5.SSS2.p1.1](https://arxiv.org/html/2611.03126#S2.SS5.SSS2.p1.1) — 主要优化对象仍是模型及训练数据。

限制：确有数据反馈、primitive 保留和快照重试；排除依据是被优化对象，不是声称没有反馈。；不把 retained successful prefix / verified training trajectories 误作跨任务 Harness 改写。

### CoworkOS:Scaling Agent Coworkers for Real-world Automation (arxiv:2611.03178)

原始/当前 v1 日期：`2026-11-02T14:15:11Z`。建议：排除当前专题；方向边界：`ai4ai/data_task/model_weights`。

> GLM-5.3 primarily serves as the controller and data teacher, while Qwen3.6-35B-A3B is the model trained and evaluated.

[S4.SS3.SSS2.Px1.p1.1](https://arxiv.org/html/2611.03178#S4.SS3.SSS2.Px1.p1.1) — 控制器与被训练模型区分。

> Across five rounds, CoworkOS continually uses evaluation feedback to identify capabilities to strengthen, revise the data recipe, and update the training strategy.

[S4.SS3.SSS4.p1.1](https://arxiv.org/html/2611.03178#S4.SS3.SSS4.p1.1) — 有反馈，但修改对象是数据配方和训练计划。

> Main maintains a memory document with the objective, completed work, next actions, and important information or constraints.

[S3.SS3.SSS3.Px1.p1.1](https://arxiv.org/html/2611.03178#S3.SS3.SSS3.Px1.p1.1) — 反证：有持久任务记忆，但未证明运行时程序自改。

限制：导言中的 models/harnesses need to coevolve 是动机，不代表实验已改写 CoworkOS。；项目技能被加载与技能自动演化不同；不能把任务状态持久化当程序持久修订。

### SWE-Trail: History-Guided Trajectory Collection for Coding Agent Training (arxiv:2611.02074)

原始/当前 v1 日期：`2026-11-01T17:26:42Z`。建议：排除当前专题；方向边界：`data_task`。

> Before collection begins, the compiler validates each proposed detector state against its supporting evidence and replays its rules on the recorded attempts.

[S3.SS1.p3.1](https://arxiv.org/html/2611.02074#S3.SS1.p3.1) — 反证：生成可执行规则并做 replay/admission，不能说没有规则生成。

> SWE-Trail applies a narrower form of adaptive allocation within one issue.

[A9.SS6.p2.1](https://arxiv.org/html/2611.02074#A9.SS6.p2.1) — 程序规则保留范围限定在单个 issue。

> The history of that issue is compiled before the new collection round, and the resulting rules remain fixed during the rollout.

[A9.SS6.p2.1](https://arxiv.org/html/2611.02074#A9.SS6.p2.1) — 当轮规则固定。

> Future work could update history across rounds and allocate effort differently across issues.

[S6.p2.1](https://arxiv.org/html/2611.02074#S6.p2.1) — 跨轮/跨 issue 更新为未来工作，不能补推。

限制：这是最强排除反例之一：确有可执行 detector 生成与重放准入，但方法目的及保留范围不足以算当前专题。；未来若展示跨轮生成规则版本或跨任务复用，可重新审查。

### NorthCUA Technical Report: Turbocharging Computer-Use Agents through Experience at Scale (arxiv:2611.02102)

原始/当前 v1 日期：`2026-11-01T18:16:47Z`。建议：建议纳入；方向边界：`harness/component_only; model_weights_for_overall_report`。

> The creator turns the resulting findings into textual guidance that states when the procedure applies, which actions to take, and how to check its intended effect

[S4.SS3.SSS1.Px2.p1](https://arxiv.org/html/2611.02102#S4.SS3.SSS1.Px2.p1) — 保留对象是可操作技能指导。

> The revised candidate is tested again before admission for reuse.

[S4.SS3.SSS1.Px3.p2](https://arxiv.org/html/2611.02102#S4.SS3.SSS1.Px3.p2) — 反馈修订并再次验证后准入。

> The skill library also makes a tested procedure available to later tasks that meet its applicability conditions.

[S4.SS3.SSS1.Px4.p2](https://arxiv.org/html/2611.02102#S4.SS3.SSS1.Px4.p2) — 明确跨任务程序复用。

> Skill v2 records Vertical=False as the setting for vertical columns and adds explicit series-color assignment through chart2 , followed by property readback and visual inspection.

[S4.SS3.SSS3.Px1.p3](https://arxiv.org/html/2611.02102#S4.SS3.SSS3.Px1.p3) — 实际 v1→v2 操作规则案例，未复现其实验。

> Task-specific assistance, reuse within a family, and transfer to a new application remain distinct uses of the record.

[A3.SS2.p2](https://arxiv.org/html/2611.02102#A3.SS2.p2) — 必须保留泛化层级边界。

限制：只纳入 §4.3.1 的技能组件；全篇主要仍含模型训练，不能宣称整个模型冻结。；子类为 component；主审 B 已据独立反馈更正，双方当前一致。milestone 快照搜索本身不是 Harness 自改。；明确程序跨任务可用性；不推断已经独立量化跨任务泛化或该组件对全模型成绩的因果收益。

### Avatar Intelligence: Amplifying Human Agency Through Persistent Personal Agents (arxiv:2611.03092)

原始/当前 v1 日期：`2026-11-02T13:11:57Z`。建议：待定/分歧；方向边界：`theory_survey; harness_specificity_unresolved`。

> harness engineering injects executable rules and control policies

[S4.SS2.p1.1](https://arxiv.org/html/2611.03092#S4.SS2.p1.1) — Harness 定义指向可执行规则，非仅关键词。

> Rehearsal provides an adaptation process that draws on, and updates, the other three forms of engineering.

[S4.T1](https://arxiv.org/html/2611.03092#S4.T1) — 实质反证：理论明言 rehearsal 更新包括 Harness 的工程范式。

> updating the avatar's memory, skill selection, and decision policy under bounded autonomy.

[S4.SS2.p3.1](https://arxiv.org/html/2611.03092#S4.SS2.p3.1) — 广义个性化/决策适应，未给出专门 Harness 方法或实验。

限制：主审 A 建议 exclude/general theory；独立 reviewer 建议 borderline，分歧真实保留。；不能写成已实现的 Harness 方法或经实验验证的 RSI；是否属于专门理论交 owner 判断。

### Can Large Language Model Agents Learn by Watching Tutorial Videos? (arxiv:2611.01460)

原始/当前 v1 日期：`2026-11-01T02:48:09Z`。建议：排除当前专题；方向边界：`experience_world_model/data_task`。

> the Write operator first proposes a candidate via an LLM-based editor that rewrites the chapters relevant to each failure.

[S3.SS2.SSS2.p2](https://arxiv.org/html/2611.01460#S3.SS2.SSS2.p2) — 主要持久对象是教程章节知识。

> containing previously generated questions, their teaching events, and the frozen answer model’s outcomes.

[A1.SS2.SSS0.Px1.p1](https://arxiv.org/html/2611.01460#A1.SS2.SSS0.Px1.p1) — 题目生成器外部状态的具体内容。

> Thus, reflective revision updates the generator’s external state and prompt context across rounds rather than its parameters.

[A1.SS2.SSS0.Px1.p1](https://arxiv.org/html/2611.01460#A1.SS2.SSS0.Px1.p1) — 必须保留的反证：存在跨轮上下文更新。

> Given this index, the question, and its options, the frozen LLM selects up to three relevant chapter IDs in JSON.

[A1.SS2.SSS0.Px3.p1](https://arxiv.org/html/2611.01460#A1.SS2.SSS0.Px3.p1) — TOC 检索步骤保持固定；未展示检索程序改写。

限制：不是见到 memory 就排除；核查了 G_phi reflective revision、A.2 的固定 Hard rewrite mode 和 TOC。；当前证据支持题目/事件/答案 history 与教程知识迭代；未见通用出题或记忆管理程序的可保留改写。；不把跨轮上下文更新说成不存在，也不把整个系统说成没有反馈。

### SIMIT: Self-Improving Vision-Language Models via Imagination at Test-Time (arxiv:2611.00053)

原始/当前 v1 日期：`2026-10-11T15:59:08Z`。建议：排除当前专题；方向边界：`data_task/model_weights/context`。

> Failures trigger repair or regeneration with explicit error feedback and bounded retries.

[S3.SS2.p7](https://arxiv.org/html/2611.00053#S3.SS2.p7) — 有反馈，但修复对象是合成样本。

> The self-generated data can be used for in-context learning (SIMIT-ICL), fine-tuning (SIMIT-FT), or both.

[S3.SS3.p1](https://arxiv.org/html/2611.00053#S3.SS3.p1) — 保留在上下文样本或权重。

> Future work could explore jointly updating the solver and synthesizer.

[A15.I1.i5.p1](https://arxiv.org/html/2611.00053#A15.I1.i5.p1) — 联合更新为未来方向。

> We keep the synthesizer fixed to preserve broad applicability and enable rigorous controlled ablations of the proposed design choices.

[A15.I1.i5.p1](https://arxiv.org/html/2611.00053#A15.I1.i5.p1) — 明确说明 synthesizer 固定。

限制：可扩展 rendering skill 接口不是自动 skill 演化。；Single-Query FT 重置权重，Test-Set FT 保留模型权重；均非 Harness 版本。；官方日期与 ID 月份不一致，记录来源原值不自行纠正。

### Can Coding Agents Sustain Continual Evolution without Forgetting? (arxiv:2611.03219)

原始/当前 v1 日期：`2026-11-02T14:43:37Z`。建议：建议纳入；方向边界：`evaluation_benchmark/harness_eval`。

> which improves agent capabilities by modifying the harness based on execution experience while keeping the foundation model parameters fixed

[S2.p1](https://arxiv.org/html/2611.03219#S2.p1) — 专门研究 Harness 反馈演化。

> we restrict the scope of self-evolution to several aspects: modifying the system prompt, modifying the agent execution logic, and adding or modifying tools.

[S3.SS2.p1](https://arxiv.org/html/2611.03219#S3.SS2.p1) — 被研究演化方法的可改工件。

> Finally, the Evolve Agent uses the evidence produced by the Agent Debugger to modify the harness code, preparing the updated harness for the next round of evolution.

[S3.SS3.p2](https://arxiv.org/html/2611.03219#S3.SS3.p2) — 演化与版本延续。

> In each round, the same batch of tasks is executed twice, and the resulting trajectories are analyzed to guide the evolution.

[S3.SS4.p1](https://arxiv.org/html/2611.03219#S3.SS4.p1) — 限制：重复的是同批任务，不是独立留出证据。

限制：论文是 Harness 专项评测，不是新方法。；50/50/30 小样本演化与旧任务回测不等于独立留出集；heldout、同预算控制与可复现标记仍 unknown。；未重跑实验、未复算全表；不把子集分数写成完整 SWE-bench Verified 成绩，不混用相对下降与百分点。

## 校验与未通过的闸门

已核 45 条 HF 原始摘要映射、8 篇官方身份日期、29 段正文短引句、6 段摘要抽查引句、3 段 RSS 全文引句及 2 条旧记录内容哈希；JSON 中保留逐条路径、原文定位、SHA-256 和意见分歧。主审与独立建议 44/45 一致，NorthCUA 的初版子类差异已更正为 component，主审文件哈希已刷新。

本 reviewer 未重跑原论文实验、未运行全仓测试与构建，也未修改规范数据或正式决策。全局 recall 上次报告为 0.8571，低于 0.90；本次独立复审不消除该闸门。没有新增正式 accept、合并或发布。

机器可读报告：[independent-review.json](independent-review.json)。四篇独立 abs 请求凭证：`build/maintenance-independent-2026-11-04/abs-receipts.json`。
