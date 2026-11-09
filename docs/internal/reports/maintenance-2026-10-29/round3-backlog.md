# 2026-10-29 第三轮：积压与其他来源独立反向复审

独立检查58篇：10月28日HF原始列表50篇，加主分支来源中不在28日和29日HF列表的8篇。未读其他轮次结论、LLM标签或owner decision。所有结果为建议，没有改decision或发布。

**4篇待人工审核的Harness建议 + 2篇边界项（OmniBrain-0、AdaPRA）。** 12篇做了定向方法正文核查；这不等于完成证据卡的全文审计。

## 优先人工复核

| 论文 | 独立建议 | 关键边界 |
|---|---|---|
| The Trinity | Harness / evolve_main | 冻结模型，修改六类协议模块，验证后继承/保留 |
| RuHarness | Harness / evolve_main | 轨迹诊断、rubric与Harness更新、验证门控 |
| GEPA-Curator | Harness / evidence_selection | 提示变异保留为checkpoint，curator筛优化证据 |
| Skill Dreaming | Harness / component | PR反馈驱动技能版本跨请求改写 |
| OmniBrain-0 | borderline；正文支持coevolution | 正文有独立reminder-policy反馈/保留环，主要贡献仍是模型 |
| AdaPRA | borderline | seed跨任务，但在线store任务隔离，不能混接证据 |

OmniBrain-0的分歧来自口径：owner文档§4.1写明“权重和Harness都被迭代修改，算harness/coevolution”；本地prompt另要求外部Harness为明确主要对象。这里提供正文证据，不替owner裁定，也不将正文引句冒充摘要通过自动闸门。

## 日期

50篇HF属于10月28日积压，不是10月29日推荐。8篇补充保留原来源，缺HF推荐日保持unknown，first_seen不作新闻日期。58篇arXiv首次发表/更新日期均已核验。

| 条目 | 来源published | arXiv首发 | 最新更新 |
|---|---|---|---|
| VibeVideoBench | 2026-10-27 | 2026-10-26 | 2026-10-27 |
| HABIT-Bench | 2026-10-20 | 2026-10-17 | 2026-10-20 |
| SPOT | 2026-10-26 | 2026-10-15 | 2026-10-26 |
| Lexical Imprint | 2026-10-26 | 2026-02-11 | 2026-10-26 |
| QUAN | 2026-10-27 | 2025-09-05 | 2026-10-27 |
| Looped Transformer Scaling | 2026-10-20 | 2026-10-19 | 2026-10-20 |
| MoveBench | 2026-10-26 | 2026-10-19 | 2026-10-26 |

上表仅报告源日期语义，未改论文数据。

## 58篇逐项建议

| # | 论文 | 建议 | 理由 |
|---|---|---|---|
| 1 | [The Trinity](https://arxiv.org/abs/2610.36077v1) | harness / harness | 比较成功/失败轨迹，修改冻结模型外六类协议模块，验证后版本保留并沿能力树继承。 |
| 2 | [MPO](https://arxiv.org/abs/2610.35013v1) | exclude / model_weights | 优化RL优势估计和token/turn信用分配，改的是模型训练，不是外部Harness。 |
| 3 | [ChronoReplay](https://arxiv.org/abs/2610.34283v1) | exclude / model_weights | 时间回放异构监督训练VLM；冻结模型下的帧选择是既定推理策略，没有Harness版本更新。 |
| 4 | [VibeVideoBench](https://arxiv.org/abs/2610.35864v2) | exclude / evaluation_benchmark | 评测Agent写代码生成成品视频；视频/渲染程序是任务产物，不评测Harness演化。 |
| 5 | [Memory Tax](https://arxiv.org/abs/2610.34073v1) | exclude / evaluation_benchmark | 比较记忆系统相对RAG的收益与信息损失，没有反馈驱动程序演化的研究对象。 |
| 6 | [PDRVLA](https://arxiv.org/abs/2610.37381v1) | exclude / model_weights | 监督训练VLA物理动态表征；冻结辅助世界模型不代表外部Harness更新。 |
| 7 | [TTME](https://arxiv.org/abs/2610.32046v1) | other_direction / experience_world_model | 保留科研框架与验证器，更新经验指南/策略条目来优化科学候选程序，非管理程序改写。 |
| 8 | [Hy-Nomas](https://arxiv.org/abs/2610.36729v1) | exclude / model_weights | 训练交互视频世界模型；Prompt Enhancer处理当前历史，不改写自身提示/控制流。 |
| 9 | [FVQ](https://arxiv.org/abs/2610.37662v1) | exclude / model_weights | 视觉表示量化和多模态模型训练，与Harness演化无关。 |
| 10 | [HABIT-Bench](https://arxiv.org/abs/2610.24520v2) | exclude / evaluation_benchmark | 评测从长期对话推断用户习惯的记忆能力，非Harness工件演化。 |
| 11 | [Rollback](https://arxiv.org/abs/2610.36068v1) | other_direction / embodied | 机器人策略与LoRA世界模型互促，改的是模型；搜索流程无反馈改写自身代码。 |
| 12 | [ThinkWorld](https://arxiv.org/abs/2610.37666v1) | exclude / model_weights | 通过世界想象和RL训练VLA动作推理，改的是参数化模型。 |
| 13 | [CodeCap-Bench](https://arxiv.org/abs/2610.37341v1) | exclude / evaluation_benchmark | 视频代码字幕是外部任务产物，基准评测生成忠实度而非Harness演化。 |
| 14 | [LociArt](https://arxiv.org/abs/2610.36456v1) | exclude / model_weights | 局部视频风格化模型、数据和评测，不涉及Agent Harness更新。 |
| 15 | [ZwZ2 / EvidenceConnect](https://arxiv.org/abs/2610.37037v1) | exclude / model_weights | 合成视觉证据数据再用RLVR训练VLM，不是程序Harness演化。 |
| 16 | [RSI Arena](https://arxiv.org/abs/2610.33624v1) | other_direction / ai4ai | Agent根据人类偏好继续训练模型，研究自主模型研发/后训练，无自身Harness改写证据。 |
| 17 | [EmbeddingGemma 2](https://arxiv.org/abs/2610.37364v1) | exclude / model_weights | 多模态嵌入模型及多阶段训练，不涉及Harness更新。 |
| 18 | [MatAnyone-E](https://arxiv.org/abs/2610.35724v1) | exclude / none | 视频抠图的memory是视觉特征缓存，不是自进化Agent程序。 |
| 19 | [h1](https://arxiv.org/abs/2610.35962v1) | exclude / none | 固定Lean接口/反思循环修改当前证明，保留证明文件和摘要，没有Harness版本迭代。 |
| 20 | [Omni-InteractScope](https://arxiv.org/abs/2610.35439v1) | exclude / evaluation_benchmark | 评测流式助手工具/提醒/连续服务能力，不评测Harness演化。 |
| 21 | [Calibration-Free MoE Channel Selection](https://arxiv.org/abs/2610.37386v1) | exclude / none | 权重读取/稀疏解码优化，非Agent Harness改写。 |
| 22 | [Economics of Reasoning Effort](https://arxiv.org/abs/2610.34491v1) | exclude / evaluation_benchmark | 推理预算反事实评测和固定失败后升级策略，没有修改可复用策略。 |
| 23 | [SPOT](https://arxiv.org/abs/2610.22543v2) | exclude / model_weights | 训练解码草稿器加速扩散模型；token推测/验证不是Harness演化。 |
| 24 | [NLD-Uni](https://arxiv.org/abs/2610.36466v1) | exclude / model_weights | 蒸馏与token渐进精修，self-refining指扩散生成，非Harness演化。 |
| 25 | [Cross-modal Steering](https://arxiv.org/abs/2610.36269v1) | exclude / none | 跨模态激活向量因果控制，不涉及执行反馈驱动程序工件演化。 |
| 26 | [Lexical Imprint](https://arxiv.org/abs/2602.10657v2) | exclude / none | 词汇对齐分析及固定drafter路由，routing不等于Harness自我改写。 |
| 27 | [RynnWorld-Latent](https://arxiv.org/abs/2610.36791v1) | exclude / model_weights | 世界模型预训练及合成训练数据，主对象是模型/数据。 |
| 28 | [OSMA-Bench](https://arxiv.org/abs/2610.34674v1) | exclude / evaluation_benchmark | 导航安全评测与人工设计参数推断步骤，非反馈驱动Harness演化。 |
| 29 | [Your Policy Is Secretly a Harness](https://arxiv.org/abs/2610.37255v1) | exclude / theory_survey | 固定Harness间切换、模型适配与ceiling/mismatch理论；属Harness接口背景，非反馈演化专项理论。 |
| 30 | [SearchHorizonBench](https://arxiv.org/abs/2610.34714v1) | exclude / evaluation_benchmark | 执行历史评测搜索价值，历史校准不是搜索/记忆管理程序的版本改写。 |
| 31 | [LongChang](https://arxiv.org/abs/2610.37649v1) | other_direction / data_task | 反馈修改物理场景/科学探索任务；工具和科学报告是任务产物，无工具库持续演化证据。 |
| 32 | [Timestral](https://arxiv.org/abs/2610.37585v1) | exclude / model_weights | 时序预测基础模型及训练，不涉及Agent Harness。 |
| 33 | [OvisOCR3](https://arxiv.org/abs/2610.33066v1) | exclude / model_weights | OCR模型预训练、蒸馏和RL，改的是权重。 |
| 34 | [HaMo](https://arxiv.org/abs/2610.34724v1) | other_direction / model_weights | 外部变化是experience card累积/检索，另一侧参数更新；管理程序不变，非Harness/权重共进化。 |
| 35 | [CrossProfile](https://arxiv.org/abs/2610.37624v1) | exclude / evaluation_benchmark | 固定记忆筛选启发式与群体证据偏差评测，非Harness工件自动更新。 |
| 36 | [JAM](https://arxiv.org/abs/2610.37219v1) | exclude / model_weights | 机器人策略结构与损失研究，辅助预测头训练后删除，非Harness演化。 |
| 37 | [GeoUG](https://arxiv.org/abs/2610.36022v1) | exclude / model_weights | RL训练何时生成几何证据的决策，改变权重而非外部控制流工件。 |
| 38 | [What Outcome RL Buys](https://arxiv.org/abs/2610.34894v1) | exclude / evaluation_benchmark | 分解模型RL训练收益与知识边界，不是Harness演化专项评测。 |
| 39 | [Fin-SD](https://arxiv.org/abs/2610.36082v1) | exclude / model_weights | 模型生成hindsight提示用于蒸馏权重；提示是训练监督，非Harness新版本。 |
| 40 | [MLE-World](https://arxiv.org/abs/2610.37175v1) | other_direction / ai4ai | 固定实验预测器指导外部ML程序搜索，改研究产物/预测模型，非Agent自身Harness。 |
| 41 | [Buried Interfaces](https://arxiv.org/abs/2610.31924v1) | exclude / none | 分子薄膜界面测量与ML光学模型，非Agent/RSI研究。 |
| 42 | [WiD](https://arxiv.org/abs/2610.36192v1) | exclude / model_weights | 像素生成模型训练结构优化，不涉及Harness。 |
| 43 | [SARL](https://arxiv.org/abs/2610.30435v1) | exclude / model_weights | 奖励训练搜索状态意识，摘要明确独立RL且无推理脚手架。 |
| 44 | [QUAN](https://arxiv.org/abs/2509.05512v2) | exclude / model_weights | 四元数图像分类/检测网络，非Agent Harness演化。 |
| 45 | [AlphaBet](https://arxiv.org/abs/2610.22684v1) | exclude / model_weights | 用proper scoring和GRPO训练事件预测policy，非外部Harness。 |
| 46 | [T-DIG](https://arxiv.org/abs/2610.29003v1) | exclude / model_weights | 生成器冻结但提示生成policy用GRPO训练；用户图像交互是任务内迭代。 |
| 47 | [Looped Transformer Scaling](https://arxiv.org/abs/2610.26030v2) | exclude / model_weights | 共享层循环与BPTT尺度研究，循环网络不是自改进Harness。 |
| 48 | [PhysEvolve](https://arxiv.org/abs/2610.34921v1) | other_direction / data_task | 世界程序是训练环境，验证反馈更新GRPO权重与课程；既定验证器未演化。 |
| 49 | [MoveBench](https://arxiv.org/abs/2610.26185v2) | exclude / evaluation_benchmark | 体育健康问答基准，rubric是固定评测，非演化中的环内验证器。 |
| 50 | [AdaPRA](https://arxiv.org/abs/2610.33245v1) | borderline / harness | 执行检查修改rubric，离线seed跨任务；在线store任务隔离，不能拼接两阶段声称跨任务演化。 |
| 51 | [iPrefBench](https://arxiv.org/abs/2610.34735v1) | exclude / evaluation_benchmark | 个性化手机Agent推断/询问基准，非Harness演化评测。 |
| 52 | [ReGE](https://arxiv.org/abs/2610.33861v1) | exclude / experience_world_model | 同题多次尝试汇总为下次尝试指导，学生从同一初始状态重跑，无跨任务工件保留。 |
| 53 | [AgentDrawBench](https://arxiv.org/abs/2610.19025v1) | exclude / evaluation_benchmark | 代码绘图/视觉理解研究，绘图是任务产物，demo技能未证实反馈持续演化。 |
| 54 | [CRM-Agent-Bench](https://arxiv.org/abs/2610.32004v1) | exclude / evaluation_benchmark | 可执行合约评测企业Agent，环境有状态不表示Harness会演化。 |
| 55 | [RuHarness](https://arxiv.org/abs/2610.36826v1) | harness / harness | 轨迹反馈更新rubric并改写六类Harness坐标，验证集门控后进入下一轮。 |
| 56 | [OmniBrain-0](https://arxiv.org/abs/2610.36013v1) | borderline / harness | 正文独立验证并跨轮保留reminder-policy更新，再训练权重；符合owner双侧迭代条款，但主要贡献仍是模型，需人工确认边界。 |
| 57 | [GEPA-Curator](https://arxiv.org/abs/2610.37651v1) | harness / harness | 执行轨迹驱动提示变异与checkpoint保留，curator筛证据，另有Harness代码优化扩展。 |
| 58 | [Skill Dreaming](https://arxiv.org/abs/2610.36188v1) | harness / harness | PR验证/失败反馈生成修订可复用技能，固定权重Actor后续请求使用新版本。 |

## 定向正文证据

### The Trinity

比较成功/失败轨迹，修改冻结模型外六类协议模块，验证后版本保留并沿能力树继承。

> Evolver compares successful and failed trajectories using public observations, actions, and host-assigned outcomes to identify node-specific improvements.

[原文](https://arxiv.org/html/2610.36077v1#S3.SS4)（feedback）

> It develops reusable modules through host-registered bindings in the six-protocol library

[原文](https://arxiv.org/html/2610.36077v1#S3.SS4)（artifact）

> Explorer retains node modules; Creator uses the same tree structure and consolidates its next Base Harness.

[原文](https://arxiv.org/html/2610.36077v1#S2.SS2)（persistence）

> and a frozen Claude Opus 5 backbone

[原文](https://arxiv.org/html/2610.36077v1#S4.SS1)（frozen_model）

候选仍需owner复核；定向方法阅读不等于证据卡全部字段的全文审计。

### TTME

保留科研框架与验证器，更新经验指南/策略条目来优化科学候选程序，非管理程序改写。

> We preserve each framework’s original parent-selection and archive-update rules.

[原文](https://arxiv.org/html/2610.32046v1#S3.SS1)（fixed_management）

> We retain the underlying discovery framework and task verifier while replacing only TTT with TTME.

[原文](https://arxiv.org/html/2610.32046v1#S3.SS1)（fixed_framework）

> We store the entry, its summary, and the supporting notes with source references.

[原文](https://arxiv.org/html/2610.32046v1#A3.SS2)（experience_data）

已定向确认边界，未审计所有实验与证据字段。

### h1

固定Lean接口/反思循环修改当前证明，保留证明文件和摘要，没有Harness版本迭代。

> h1 keeps a model working on a Lean proof until an external validator accepts it or the budget runs out

[原文](https://arxiv.org/html/2610.35962v1#S2.SS2)（same_task）

> the model then continues from the current file with this summary.

[原文](https://arxiv.org/html/2610.35962v1#S2.SS2)（state_not_harness）

已定向确认边界，未审计所有实验与证据字段。

### Your Policy Is Secretly a Harness

固定Harness间切换、模型适配与ceiling/mismatch理论；属Harness接口背景，非反馈演化专项理论。

> Six harnesses act on three MiniWoB++ task families

[原文](https://arxiv.org/html/2610.37255v1#S2)（fixed_interfaces）

> Harness evaluations should therefore report the ceiling next to the frozen return, evaluate several checkpoints under each harness rather than a single one

[原文](https://arxiv.org/html/2610.37255v1#S7)（theory_scope）

已定向确认边界，未审计所有实验与证据字段。

### LongChang

反馈修改物理场景/科学探索任务；工具和科学报告是任务产物，无工具库持续演化证据。

> Each operation modifies a mechanism involved in the same error to create a scene with altered physics for further exploration.

[原文](https://arxiv.org/html/2610.37649v1#S5)（environment_not_harness）

已定向确认边界，未审计所有实验与证据字段。

### HaMo

外部变化是experience card累积/检索，另一侧参数更新；管理程序不变，非Harness/权重共进化。

> This equation describes accumulation; optional post-training release is applied afterward.

[原文](https://arxiv.org/html/2610.34724v1#S3.SS1)（memory_entries）

> this procedure is used only to curate supervision for model adaptation.

[原文](https://arxiv.org/html/2610.34724v1#S3.SS1)（weights_object）

已定向确认边界，未审计所有实验与证据字段。

### AdaPRA

执行检查修改rubric，离线seed跨任务；在线store任务隔离，不能拼接两阶段声称跨任务演化。

> We discover rubrics offline from past harness-only runs of the base agent, using the leaderboard percentile of each attempt to contrast stronger and weaker attempts

[原文](https://arxiv.org/html/2610.33245v1#S3.SS3)（offline_stage）

> Stores are isolated across tasks, so that results do not depend on the order in which tasks are run.

[原文](https://arxiv.org/html/2610.33245v1#S3.SS5)（no_online_cross_task）

> Add creates a rubric only after the PRA has run and recorded a check for it in the same review, update rewrites a rubric’s specification, and retire deactivates a rubric and records the reason.

[原文](https://arxiv.org/html/2610.33245v1#S3.SS5)（verifier_edit）

> The seed rubrics are discovered only on DSPredict-Easy, whose tasks are mostly tabular, yet they improve DSPredict-Hard, whose tasks span vision, text, audio, time series, and molecular data.

[原文](https://arxiv.org/html/2610.33245v1#S5.SS4)（offline_transfer）

候选仍需owner复核；定向方法阅读不等于证据卡全部字段的全文审计。

### ReGE

同题多次尝试汇总为下次尝试指导，学生从同一初始状态重跑，无跨任务工件保留。

> A single coach call produces the guide, allowing decisions about what to retain and connect to account for information across attempts.

[原文](https://arxiv.org/html/2610.33861v1#S2.SS2)（one_task_guide）

> The student starts from the task’s initial environment state and uses the guidance alongside current observations.

[原文](https://arxiv.org/html/2610.33861v1#S2)（same_task_retry）

已定向确认边界，未审计所有实验与证据字段。

### RuHarness

轨迹反馈更新rubric并改写六类Harness坐标，验证集门控后进入下一轮。

> RuHarness summarizes each failed run into a structured failure report and aggregates these reports to identify recurring cross-task behavioral patterns.

[原文](https://arxiv.org/html/2610.36826v1#S3.SS2)（feedback）

> Each coordinate defines a corresponding set of editable components in the agent system.

[原文](https://arxiv.org/html/2610.36826v1#S3.SS3)（artifact）

> A candidate is advanced to the next evolution round only if its validation improvement exceeds the acceptance threshold, with the current harness retained otherwise.

[原文](https://arxiv.org/html/2610.36826v1#S3.SS3)（persistence）

候选仍需owner复核；定向方法阅读不等于证据卡全部字段的全文审计。

### OmniBrain-0

正文独立验证并跨轮保留reminder-policy更新，再训练权重；符合owner双侧迭代条款，但主要贡献仍是模型，需人工确认边界。

> The update changes the guidance supplied by the harness and retains the tool interfaces in Section 3.2 .

[原文](https://arxiv.org/html/2610.36013v1#S5.SS1)（artifact）

> OmniBrain-0 executes evaluation trajectories under the candidate guidance with its parameters fixed.

[原文](https://arxiv.org/html/2610.36013v1#S5.SS1)（frozen_phase）

> The verifier assesses goal attainment and execution efficiency, and the Meta-Agent uses the resulting evidence to identify valid reminders and revise ineffective guidance.

[原文](https://arxiv.org/html/2610.36013v1#S5.SS1)（feedback）

> Effective reminders are retained across rounds, enabling execution guidance to accumulate from observed interaction outcomes.

[原文](https://arxiv.org/html/2610.36013v1#S5.SS1)（persistence）

> The updated model is redeployed for further collection, so subsequent challenges reflect its current capabilities.

[原文](https://arxiv.org/html/2610.36013v1#S5.SS2)（weights_iteration）

候选仍需owner复核；定向方法阅读不等于证据卡全部字段的全文审计。

### GEPA-Curator

执行轨迹驱动提示变异与checkpoint保留，curator筛证据，另有Harness代码优化扩展。

> It executes the tasks using an actor agent conditioned on the prompt and returns an updated prompt, task-level agent trajectories, and evaluation results

[原文](https://arxiv.org/html/2610.37651v1#S3)（artifact_feedback）

> GEPA-Curator maintains a single lineage in which each mutation becomes the next checkpoint.

[原文](https://arxiv.org/html/2610.37651v1#S4.SS1)（persistence）

> The parent is freshly executed on these tasks, and the optimizer revises it using the resulting feedback and the Curator’s rationale.

[原文](https://arxiv.org/html/2610.37651v1#S5.SS3)（harness_code_extension）

候选仍需owner复核；定向方法阅读不等于证据卡全部字段的全文审计。

### Skill Dreaming

PR验证/失败反馈生成修订可复用技能，固定权重Actor后续请求使用新版本。

> Each skill specifies when it applies, how to implement the change, and how to validate the result.

[原文](https://arxiv.org/html/2610.36188v1#S4.SS2)（artifact）

> Failed implementations and review corrections provide negative constraints and repair strategies.

[原文](https://arxiv.org/html/2610.36188v1#S4.SS2)（feedback）

> Skills can be reused, extended, revised, or replaced as repository requirements evolve, producing an updated skill set that guides subsequent development.

[原文](https://arxiv.org/html/2610.36188v1#S3)（persistence）

> New skills are added, existing skills are revised, and superseded versions are archived with their supporting PR records.

[原文](https://arxiv.org/html/2610.36188v1#S4.SS4)（versioning）

> without updating model weights or guaranteeing global optimality.

[原文](https://arxiv.org/html/2610.36188v1#S3)（frozen_model）

候选仍需owner复核；定向方法阅读不等于证据卡全部字段的全文审计。

## 审计边界

- 引文与归档HTML在统一显示空白后逐字匹配，章节锚点已核对；HTML、Atom、抓取时间及SHA-256在round3-backlog-evidence中。
- TTME改经验条目，HaMo改经验卡和权重，h1解当前证明，ReGE同题重试；memory/Harness/reflection字样不是纳入证据。
- RSI Arena为自主模型研发；Your Policy Is Secretly a Harness为接口理论背景。没有将它们或静态能力基准计为Harness演化专项。
- 未运行付费模型，未改owner决定，未发布候选，未将补录变为今日新闻。

与今日8篇独立复审合计66篇，其中14篇做了定向正文核查；完整证据卡全文审计仍为0。JSON最终建议为harness 4、borderline 2、other_direction 7、exclude 45；OmniBrain-0的正文判读单独保留，未因聚合口径丢失。
