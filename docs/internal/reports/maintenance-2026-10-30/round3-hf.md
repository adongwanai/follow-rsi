# 2026-10-30 HF 补充候选独立第三轮复审

未读取 round1 或 round2 结论；逐篇阅读 7 篇原始摘要，对 5 篇方法/评测/理论边界读取官方 arXiv 相关正文。身份与原始日期使用 parent 提供的后验官方 Atom 原始响应，非其他轮审核结论。

**7 篇摘要已逐篇读完；5 篇定向核对官方正文；7 个身份及原始日期已由官方 Atom 验证。0 篇 Harness、4 篇其他方向、3 篇排除。** 所有 owner decision 维持 defer，未对外发布。

Harness 需要反馈驱动地修改外部可复用程序工件并保留复用；评测/理论须专项研究该演化。一般代理能力、安全评测、固定提示实验、训练权重和任务中的反复修正不能据词面纳入。

本批是 10/30 发现的 **10/29 HF 推荐榜补充**，不冒充 10/30 榜。原始日期与 HF 推荐日期分别保留。

| 原始发表时间（arXiv） | ID | 论文 | 建议 |
| --- | --- | --- | --- |
| 2026-09-30T15:16:21Z | 2610.30161 | TauIndianBankBench: Procedure-Aware, Action-Oriented Evaluation of Tool-Using Conversational Agents | other_direction |
| 2026-10-14T19:15:58Z | 2610.20832 | Amortizing Sequential Experimental Design in Reasoning LLMs | exclude |
| 2026-10-15T18:03:13Z | 2610.22507 | RealCLI: Toward a Unified Evaluation of Human-Agent Collaboration for CLI Agents | other_direction |
| 2026-10-21T17:59:14Z | 2610.30132 | LongZero: Enhancing Long-Context Reasoning in LLMs from Zero Data | exclude |
| 2026-10-26T16:14:17Z | 2610.35671 | Evaluating DeepSeek V4.1 Flash-1017 for loss of control and harmful manipulation risks | other_direction |
| 2026-10-26T18:15:26Z | 2610.36095 | Instruction Capacity: Behavior and Degradation of Language Models under Controlled Load | other_direction |
| 2026-10-27T17:50:20Z | 2610.37626 | Know, then Draw: A New Learning Paradigm for Visual Generation | exclude |

## 1. TauIndianBankBench: Procedure-Aware, Action-Oriented Evaluation of Tool-Using Conversational Agents

- 来源：https://arxiv.org/abs/2610.30161
- 原始时间：`2026-09-30T15:16:21Z`；v1；HF 推荐日：10/29；发现日：10/30。
- 范围：`targeted_methods_and_scope_sections`；Owner decision：`defer`。
- 观察到的修改/测量对象：银行工具调用过程与结果评测。

**摘要原句：**

> Besides the final records, it checks that the assistant took every required step and made no unrequested change.

**定向正文证据：**

3.2 Scoring：

> A session is scored deterministically by two pass/fail checks.

4 Evaluation Protocol：

> It is prompted with the task’s persona and scenario and a fixed set of instructions.

已读章节：3.1 Environment and tasks；3.2 Scoring: pass criterion, final-state check, action check, write purity, call order；4 Evaluation Protocol。

原始正文 SHA-256：`a05da33dbfb3d2e1cd8563686dd5bf4392e07fbb1ec7595699b9220735d892f5`。

**建议：other_direction。** 银行规则、金标准工具调用序列及固定用户模拟器用于评估过程合规与最终数据库状态。评估的是任务执行是否漏步骤或产生未授权变更，并非反馈修改代理自身提示、工具或控制流。

边界：procedure-aware 与训练前后比较不自动构成 Harness 演化；每会话从新的固定银行状态开始，未给出跨任务保留的程序更新。

整篇层面可证明 Harness 自动修改及跨任务保留的引文不足，相关字段保持 unknown；不把缺失补成肯定结论。

来源异常：arXiv API 原始 published 为 2026-09-30T15:16:21Z，但编号前缀为 2610；保留来源原值，原因 unknown，不擅自校正。

## 2. Amortizing Sequential Experimental Design in Reasoning LLMs

- 来源：https://arxiv.org/abs/2610.20832
- 原始时间：`2026-10-14T19:15:58Z`；v1；HF 推荐日：10/29；发现日：10/30。
- 范围：`original_abstract_only`；Owner decision：`defer`。
- 观察到的修改/测量对象：用信息增益奖励训练模型策略。

**摘要原句：**

> We study how to amortize sequential Bayesian experimental design (BED) into an LLM by explicitly training the reasoning that guides action selection using information-gain rewards.

> These results suggest that information gathering can be learned as a generalizable reasoning skill in LLMs.

**建议：exclude。** 摘要明确以信息增益奖励训练 LLM 的推理与动作选择策略，泛化承载于模型参数；没有可复用外部程序工件被反馈改写的主张，也未建立多代模型自举闭环。

边界：sequential experimental design 描述任务中的连续信息选择；不能将动作序列或训练步数算成递归自改进轮次。仅摘要范围判断，未全文核验其训练细节。

整篇层面可证明 Harness 自动修改及跨任务保留的引文不足，相关字段保持 unknown；不把缺失补成肯定结论。

## 3. RealCLI: Toward a Unified Evaluation of Human-Agent Collaboration for CLI Agents

- 来源：https://arxiv.org/abs/2610.22507
- 原始时间：`2026-10-15T18:03:13Z`；v1；HF 推荐日：10/29；发现日：10/30。
- 范围：`targeted_methods_and_scope_sections`；Owner decision：`defer`。
- 观察到的修改/测量对象：评测运行时协作，未改写持久工件。

**摘要原句：**

> REALCLI-COLLAB introduces a scripted user that delivers progressive information, corrections, constraint revisions, and authorization decisions.

**定向正文证据：**

2.3 Script-Driven User Simulation：

> In this way, the timing of user interventions varies with the execution trajectory, while task semantics, key messages, and evaluation criteria remain fixed.

D.1 Details of Agent Harness：

> We evaluate all agents through three mainstream CLI agent scaffolds.

已读章节：2.1 Task Formulation；2.2 Five-Dimensional Collaboration Framework；2.3 Script-Driven User Simulation；2.4 Evaluation Metrics；D.1 Details of Agent Harness。

原始正文 SHA-256：`0af8d8cbacab82c36f8218cefbcae04f2def1fbe4fb6b9bd8e81c62be7e3bf09`。

**建议：other_direction。** 评测人类信息补充、纠正、授权和当前任务状态适应。正文明确任务语义与评测条件固定，比较三个现成 CLI scaffold，没有评测这些工件根据执行反馈演化并跨任务保留的机制。归一般代理协作评测。

边界：使用名为 Harness 的 agent scaffold 和用户纠正反馈，不足以进入 Harness 专项演化评测；跨任务统计一致性也是指标，不是持久更新。

整篇层面可证明 Harness 自动修改及跨任务保留的引文不足，相关字段保持 unknown；不把缺失补成肯定结论。

## 4. LongZero: Enhancing Long-Context Reasoning in LLMs from Zero Data

- 来源：https://arxiv.org/abs/2610.30132
- 原始时间：`2026-10-21T17:59:14Z`；v1；HF 推荐日：10/29；发现日：10/30。
- 范围：`targeted_methods_and_scope_sections`；Owner decision：`defer`。
- 观察到的修改/测量对象：固定自合成数据后的 GRPO 权重训练。

**摘要原句：**

> LongZero combines these self-written multi-hop reasoning tasks with self-written multi-round retrieval tasks and trains the model with GRPO.

**定向正文证据：**

3.1.3 Difficulty Filtering：

> Because the same model generates and filters the data, the difficulty of the kept questions adapts to the model that will be trained on them.

4.1 Settings：

> All methods, including the baselines, share this configuration, and we report the final checkpoint of each run;

5 Conclusion and Future Work：

> Future work includes iterating LongZero so that the trained model regenerates and refilters its own data,

已读章节：3 LongZero；3.1 Data Synthesis (all subsections)；3.2 Reinforcement Learning；4.1 Settings；5 Conclusion and Future Work。

原始正文 SHA-256：`2033f3438ac00dcba9f13fbb3a7a71a1abbe1630d7db87d7b90cb100d172bf39`。

**建议：exclude。** 方法先由基模型生成和筛选一个训练集，再做 GRPO；优化对象是权重。结论将训练后模型再次生成并重筛数据的迭代明确列为 future work。因此不能把当前结果写成已验证的多代模型 RSI，更不属于 Harness。

边界：self-written、zero data 和 multi-round retrieval 是数据生成/任务形式。多步 GRPO 不等于多轮再生成训练数据。此处依据正文澄清单轮训练边界，建议排除当前 RSI 收录。

整篇层面可证明 Harness 自动修改及跨任务保留的引文不足，相关字段保持 unknown；不把缺失补成肯定结论。

## 5. Evaluating DeepSeek V4.1 Flash-1017 for loss of control and harmful manipulation risks

- 来源：https://arxiv.org/abs/2610.35671
- 原始时间：`2026-10-26T16:14:17Z`；v1；HF 推荐日：10/29；发现日：10/30。
- 范围：`targeted_methods_and_scope_sections`；Owner decision：`defer`。
- 观察到的修改/测量对象：综合模型安全评测，包含有界研发任务。

**摘要原句：**

> Drawing on the EU General-Purpose AI Code of Practice, we evaluate the model across 34 benchmarks, including 5 in-house suites, spanning evaluation integrity, loss of control, and harmful manipulation.

**定向正文证据：**

Introduction：

> This report evaluates DeepSeek V4.1 Flash-1017 for such risks in three areas: evaluation integrity, loss of control, and harmful manipulation.

2.4.2 RE-Bench：

> In the Rust workflow task, the agent builds an iterative scaffold that generates candidate Rust solutions, compiles them, and uses test feedback to repair errors;

2.4.2 RE-Bench：

> we then freeze the submitted workflow and evaluate its pass rate on 165 held-out problems.

已读章节：Introduction；2.4 Autonomous AI Research and Development；2.4.1 PaperBench Code-Dev；2.4.2 RE-Bench。

原始正文 SHA-256：`572baae6cd6785decdca303ac2889c6cd47c944ea567d71b48bbe6b94b60ed7c`。

**建议：other_direction。** 主问题是综合模型失控、操纵及评测可信度。正文确有 RE-Bench Rust 子任务：产生一个可复用代码生成工作流并冻结后在留出题测试；这一实际 Harness 相关实验应保留说明，但不足以把整篇综合安全报告列为 Harness 演化专项方法或评测。

边界：不能笼统说它完全没有 Harness 相关内容。Rust 子实验与其余 AI 研发/安全任务分别记录；当前仍为 safety_governance/evaluation_benchmark，不自动加 secondary harness，不发布到 Harness 主专题。

整篇层面可证明 Harness 自动修改及跨任务保留的引文不足，相关字段保持 unknown；不把缺失补成肯定结论。

该句证明提交的工作流被复用，不等于证明工作流在每个留出任务中自行演化；当前内容不足以将整篇文章标为 Harness 专项。

## 6. Instruction Capacity: Behavior and Degradation of Language Models under Controlled Load

- 来源：https://arxiv.org/abs/2610.36095
- 原始时间：`2026-10-26T18:15:26Z`；v1；HF 推荐日：10/29；发现日：10/30。
- 范围：`targeted_methods_and_scope_sections`；Owner decision：`defer`。
- 观察到的修改/测量对象：固定提示测量模型指令负载容量。

**摘要原句：**

> The passport of a model serves as the calibration of a future meter of the instruction load of prompts.

**定向正文证据：**

3.3 Construction of a task：

> The template is not a parameter of the experiment: changing the wording means a new version of the protocol, so the wording of the instruction does not act as a factor of the outcome.

6.2 Measuring prompts：

> The validity of this representation is yet to be established experimentally.

已读章节：3 The Instrument: introductory formulation；3.1 The atomic instruction—word replacement；3.3 Construction of a task: fixed-template passage；3.5 What the instrument measures；6.2 Measuring prompts；7 Conclusion。

原始正文 SHA-256：`74ac66097b42e5bf536de5b787d73bea147840b2461c903039bce6bfe2eff9ec`。

**建议：other_direction。** 固定替换规则与固定提示模板测量指令负载和模型响应，未进行反馈提示进化。未来的通用 prompt 负载计量是提出的拓展，正文说明其表示有效性尚待实验。归一般能力计量与理论背景。

边界：研究 prompt 不自动构成 Harness 演化理论。正文主动固定提示措辞以控制实验变量，不能把实验中的负载变化误写成程序工件优化。

整篇层面可证明 Harness 自动修改及跨任务保留的引文不足，相关字段保持 unknown；不把缺失补成肯定结论。

## 7. Know, then Draw: A New Learning Paradigm for Visual Generation

- 来源：https://arxiv.org/abs/2610.37626
- 原始时间：`2026-10-27T17:50:20Z`；v1；HF 推荐日：10/29；发现日：10/30。
- 范围：`original_abstract_only`；Owner decision：`defer`。
- 观察到的修改/测量对象：自回归预训练与扩散后训练权重。

**摘要原句：**

> We propose a learning paradigm that assigns these roles to autoregressive pretraining for knowledge acquisition and diffusion post-training for high-fidelity rendering.

**建议：exclude。** 图像生成中的预训练目标、语义表示、扩散后训练和缩放律研究。摘要没有模型自主改写外部 Harness、跨任务保留程序修改或多代自举的主张。

边界：预训练与后训练是多个训练阶段，不等于递归自改进轮次。仅摘要范围判断，未审查完整视觉生成实验。

整篇层面可证明 Harness 自动修改及跨任务保留的引文不足，相关字段保持 unknown；不把缺失补成肯定结论。

## 核验与限制

- 7 篇均是今天发现的 10/29 HF 榜补充，不是 10/30 榜；保留各自经 arXiv 验证的原始日期。
- LongZero 把训练后再生并重筛训练集列为 future work；当前结果不能按已完成多轮 RSI 处理。
- DeepSeek 安全报告确有冻结 Rust 工作流后留出评测的 Harness 相关子任务；整篇仍是综合安全评测，不据此改成 Harness 专项。
- TauIndianBankBench 的 arXiv 发布时间为 9/30，与 2610 编号月份不一致。只报告来源异常，不修改日期。
- 未声称读完所有论文或完成实验审计；5 篇是定向章节阅读，另 2 篇只作摘要范围判断。
- 所有摘要引文均为原始摘要连续子串；正文引文按空白归一化匹配；5 份 HTML 及身份 Atom 的 SHA-256 已复核。
- 未改共享数据、审核队列、owner 决定或公开内容。
