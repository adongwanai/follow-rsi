# 2026-11-08 独立范围复审

完成时间：2026-11-08T00:23:41.020291+00:00

19 个增量身份逐项留痕：建议纳入 5、当前证据排除 12、边界待补 1、正式身份待补 1。9 篇读正文，9 篇对官方摘要做排除抽查，1 篇仅核 S2 原始元数据。没有把摘要筛查说成正文审核；没有接受、合并或发布。

Beneath the Surface、PromptOps、ReferClaw、Evolver 的首轮正文范围判断由本 agent 完成，root 已独立读取原文核心方法、协议及限制并回传一致的纳入/待定边界。EnvOpt 与 Criteria Exposure 同时有 sources 主审与独立正文复审。

| 条目 | 建议 | 阅读范围 |
| --- | --- | --- |
| Tools Need Not Speak in Text: Latent Context Compression for Agents | exclude_from_harness_rsi | independent_round_3_complete |
| Beneath the Surface: What We Overlook When We Talk About Agent Evolution | include_harness_specialized_evaluation | fulltext_scope_pass_parent_crosscheck_confirmed |
| PromptOps: Iterative Prompt Optimization for LLM-as-a-Judge Systems | include_harness_component | fulltext_scope_pass_parent_crosscheck_confirmed |
| ReferClaw: Disambiguating User Intent for Egocentric Assistance | include_harness_coevolution | fulltext_scope_pass_parent_crosscheck_confirmed |
| Evolver: Turning Agent Exploration into Evolving Capabilities | borderline_defer | fulltext_scope_pass_parent_crosscheck_confirmed |
| Learning the Task or Learning the Verifier? Rethinking Criteria Exposure in Embodied Self-Improvement | include_harness_specialized_evaluation | independent_round_3_scope_complete |
| EnvOpt: Automated Optimization for Agent Environments | include_harness_tool_component | independent_round_3_scope_complete |
| Towards Robust Long-Lived Agents: Benchmarking Experience Lifecycles in Evolving Environments | exclude_from_harness_rsi | independent_round_3_scope_complete |
| WeightLoop: Weight-Space Programming with Experimental Feedback | exclude_from_harness_rsi | independent_round_3_scope_complete |
| Reclassification Is All You Missed: Surfacing Variant Reinterpretation Need in Online Health Communities at Population Scale | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| Agentic Behavior Engineering: A Design-by-Contract Methodology for Specifying, Verifying, and Governing Enterprise AI Agents | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| ControlAnything: Generative UI and On-Demand Device Integration for Mixed-Reality Hand Interaction by a Coding Agent | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| Where Do Reported Long-Video QA Gains Come From? A Controlled Audit of Frame Selection, Evidence Injection, and Expert Routing | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| The Memory Trap: Language Agents Overgeneralize from Benign Interactions | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| ReproBridge: Building Reproducibility into ML Research Artifacts | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| Using Experience Twice: Dynamic Process Rubrics for Privileged Token-Level Credit Assignment | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| Rethinking Self-Repair in Code-as-Policy Agents: What Drives Retry Success? | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| VirtualTrialHarness: Coordinating Agentic Operationalization of Virtual Trial Protocols Across Complex Clinical Schemas | exclude_from_harness_rsi_at_current_evidence | independent_exclusion_sample_official_abstract_only |
| ELLMO at LLMs4OL 2026 Tasks Flagship, Reuse, and Taxonomy: Ontology Learning Across Contexts | defer_official_identity_blocked | independent_metadata_check_identity_blocked |

## 逐项依据

### arxiv:2611.06500 · Tools Need Not Speak in Text: Latent Context Compression for Agents

训练更新的是压缩器的 encoder LoRA 与 latent adapter 神经参数；只有 target agent 冻结。§3.4 是基于下一动作分布对齐及记录动作监督的梯度训练，§3.5 推理时复用训练后的固定压缩器。压缩器参数跨任务复用不等于提示、技能、工具或上下文管理程序被反馈驱动改写并继承。没有足以证明 Harness 共演化或至少两轮模型权重 RSI 的证据。

- §3.4 Action-Preserving Training: “During training, we keep the target agent frozen and update only the LoRA parameters of the context-aware encoder and the parameters of the latent adapter.”
- §3.4 Action-Preserving Training: “Since latent tokens are continuous and differentiable, gradients can propagate through the frozen target agent to optimize the compression model:”
- §3.1 Overview: “During inference, the trained compressor replaces raw tool observations with latent tokens after each tool call, allowing the agent to perform multi-step interactions with a more compact context (Section 3.5 ).”

source_hash: `62824809a851912b3fe26ee0897e1e0ba1f08bf29a368f2191a017434ffbe0c5`

### arxiv:2611.07624 · Beneath the Surface: What We Overlook When We Talk About Agent Evolution

统一流程比较提示、技能、配置、编排等外部 Harness 的代际修改，分离搜索/准入的 Train/Validation 与最终 Test，并由 EvoAudit 的算子修订形成 AGE。可纳入 Harness 专项评测；外层/内层可改范围须分别叙述。

- §3.2.1: “Codex 0.143.0 ( OpenAI, 2026 ) is outer-layer-only and permits changes to prompts, skills, configuration, and external orchestration.”
- §3.2.2: “Evolution uses Train/Validation evidence for search and admission, while Test is reserved for Seed and Champion evaluation.”
- §7.2: “Each generation selects a Parent, collects fresh Train trajectories, diagnoses behavior, and proposes one Candidate.”
- §7.2: “The mutation agent receives the selected behavior evidence, Parent workspace, prompt and skill inventory, and editing contract.”
- §7.2: “Outputs retain the patch, changed-file list, surface-check report, agent response, and usage record.”
- §7.1-7.2: “EvoAudit diagnoses archived evolution runs and returns validated operator revisions. Installing its four revisions in A-Evolve gives Audit-Guided Evolution (AGE).”

边界：Scope review and quoted mechanisms, not independent recalculation of every table or experimental reproduction. Do not describe Codex outer-only edits as permission to modify its inner source.

source_hash: `d9782677e50a751330bbe24e6374ad191e58d8f6b768fd15a481446c5f267da8`

### arxiv:2611.07123 · PromptOps: Iterative Prompt Optimization for LLM-as-a-Judge Systems

执行中的 judge prompt 经参考反馈监测，修改评分 rubric 或 demonstrations，择优版本用于后续流式样本；修改对象和持久使用均有正文依据。仅是评审器提示组件的闭环，真实标签成本与延迟没有验证。

- §3: “PromptOps extends an LLM-as-a-Judge system with a continuous feedback loop for monitoring and recalibrating its evaluation behavior.”
- §3.1: “Rubric Synthesis is a lightweight custom optimization method that restricts revisions of the current prompt p t p_{t} to its scoring rubric, while leaving all other prompt components unchanged.”
- §3.1: “The highest-scoring candidate is retained as the updated prompt p t + 1 p_{t+1} .”
- §4.1: “Consequently, during prompt optimization, only observations encountered so far may be accessed, never future ones.”
- §3: “Our experiments therefore study adaptation under oracle-like feedback rather than realistic label acquisition.”
- §4.1: “An optimization pass does not necessarily change the prompt, as an optimizer may retain the current prompt if it does not identify an improvement.”

边界：Immediate oracle-like feedback; real label sparsity, delay, noise, disagreement and cost are not reproduced. FairBotBench stream evaluation is not evidence of invariant cross-domain robustness. No model-weight training or training-free claim is inferred from fixed API backends.

source_hash: `ec0932d3d2d90cca95e98f54954b3bd947d9439b6bef00d498c287c15646cc91`

### arxiv:2611.07683 · ReferClaw: Disambiguating User Intent for Egocentric Assistance

每次核实失败后写入含触发条件、纠正动作、反模式和回归测试的可复用技能，后续交互检索进负责 agent 的 prompt；另有 GRPO 更新其 LoRA 并按固定验证探针准入/回滚。外部技能与权重都持续演化，不能仅因有训练排除。

- §3.3: “Each agent-specific skill records an ambiguity trigger, candidate topology ( e.g. , one object encountered twice), decisive contrast, corrected action, anti-pattern, and two regression tests against unnecessary asking.”
- §3.3: “Up to three skills, retrieved by trigger–topology embedding similarity, immediately enter the responsible agent’s prompt.”
- §3.3: “GRPO ( Shao et al., 2024 ) updates only that agent’s LoRA adapter, with a KL penalty toward frozen Base.”
- §3.3: “Promotion requires improvement on the target failure type without degrading overall accuracy, unnecessary asking, or mean cost on a fixed validation probe; otherwise the update is rolled back (Appendix B.7 ).”
- Appendix D.2: “any resulting skill or parameter update can influence interactions k + 1 k+1 onward but never the current or preceding examples.”
- Appendix D.2: “The model, skill library, and optimization state are initialized identically at the start of each stream order and then carried forward without resets inside that stream.”
- Appendix D.2: “ReferClaw (Skills) additionally enables fast adaptation: after each verified failure, the skill evolver synthesizes a short skill, and the three most relevant skills are retrieved by cosine similarity and inserted into the responsible agent’s prompt.”

边界：The source specifies prospective stream updates; no current/past example may benefit from its own update. Source-backed method classification is not a reproduction of reported gains.

source_hash: `1174e82b9e6b41bb37f81a3a3efbb60f71ababac2feaca30f983f5cbb20ea95e`

### arxiv:2611.07595 · Evolver: Turning Agent Exploration into Evolving Capabilities

Gene 可携带程序性策略；固定版本代码也有从成功 Capsule 蒸馏 Gene、轻量验证和持久入库。不能仅因自然语言或内容寻址存储就排除技能。然而论文的比较冻结候选池、优先同任务经验复用，并明确不验证未见任务泛化或长期在线进化；反馈主要改变资产资格，尚不足以把该实验归为已验证的跨任务 Harness 改写。保留边界待补。

- §3.5: “Rejection and provenance revocation are recorded separately from the underlying content-addressed assets, preserving their identity while modifying their subsequent eligibility.”
- §4.1: “candidate assets are frozen before augmented execution.”
- §4.1: “Gene selection prioritizes experience derived from the same task, followed by other matching candidates within the isolated pool, with an injection budget of 12,000 bytes.”
- §4.1: “Both B and G retain the same foundation model and harness configuration and are evaluated using the corresponding native benchmark grader.”
- §4.1: “This protocol assesses historical experience reuse rather than generalization to unseen tasks or long-term online evolution.”

边界：Do not convert frozen same-task reuse into demonstrated cross-task or longitudinal Harness evolution. Selected paired observations and token accounting have evaluation limits; extraction overhead is not established as included. Repository asset repair handles schema/network rejection; it is not by itself task-performance improvement evidence. Presence of procedural content is positive boundary evidence, not proof of effective closed-loop generalization.

source_hash: `f006e6832371d2c17e989273b2d0830b19f76ed6a5f82444c77bf1e9fa35d8da`

### arxiv:2611.08318 · Learning the Task or Learning the Verifier? Rethinking Criteria Exposure in Embodied Self-Improvement

冻结 actor/primitive/perception/scoring，执行反馈驱动多轮可调用技能代码和记忆库修订，并有最优版本回滚；十个源任务库被蒸馏为共享库用于不相交目标任务。它直接评估 Harness 技能库改进的证据边界，不能当作一次性机器人外部产物排除。

- §3.1: “The actor, the primitives, perception and benchmark scoring are frozen and only the library changes; the two settings share the loop and differ in what the learner reads, so differences between them reflect exposure rather than the loop itself.”
- §3.1: “whose skills are callable code that reports what it did and whose memory entries say when to apply what, with the evidence for it; a revision is usually tried first in verification rollouts, and the loop rolls back to the best revision so far when a batch falls clearly below it.”
- §3.4: “To reuse libraries, we distill the libraries of ten source tasks into one shared library and apply it to disjoint target tasks, in RoboDojo and on two further benchmarks with aligned primitives.”

边界：Simulated feedback, author-written criteria, finite held-out layouts and aligned primitives bound the result. Mechanism interpretations are not component ablations or independent experiment replication.

source_hash: `34f983204e18d6a18ec910c1365545b4b1a5148496c0e6ca59fb8ce8bf34b985`

### arxiv:2611.07372 · EnvOpt: Automated Optimization for Agent Environments

仅纳入反馈驱动并跨任务复用的工具访问层/程序：轨迹与成本驱动优化，新工具与程序随优化环境保留，且原环境加演化工具的消融单列此部分。环境文件/目录整理本身不计 Harness。作者固定 target runner 不等于所有工具工件固定。

- §2: “EnvOpt uses disjoint sets of training tasks (without verifiers) at each step to optimize the environment. After each step, the optimized environment is tested on a separate validation set to determine when the whole process should be stopped.”
- §4.1: “a validate_tenacity.py is built to automatically fetch the code change made by the target agent, search for relevant test files, run the tests, and return verdicts.”
- §4.4: “During environment optimization, EnvOpt can also optimize ways to access the new environment, including new tools.”
- §4.4: “Since tool optimization might be covered by harness engineering, this ablation shows that EnvOpt brings significantly more headroom for optimization in addition to harness engineering.”

边界：Only the feedback-edited tool component belongs to Harness; do not relabel all environmental reorganization as Harness. Training tasks omit verifiers; proxy reliability, validation and the reported failures limit the conclusions.

source_hash: `8db313ff433b0571c1a75731e46dfa96b1ee2c68b886c889050ff94338601dd9`

### arxiv:2611.05450 · Towards Robust Long-Lived Agents: Benchmarking Experience Lifecycles in Evolving Environments

比较固定 Hermes 接口中结构/规则经验的保存、失效和修订；memory/skills 是内容载体，当前证据未显示经验管理程序或 Harness 政策被演化。保留跨任务经验评测定位，不仅凭 skills 字样纳入 Harness。

- §2.4.1: “Agents are instructed to store structural experience in memory and rule experience in skills.”
- §2.4.1: “The with-experience condition retains these assets and retrievable history across tasks. The without-experience condition clears them between tasks.”
- Appendix B.1: “The Hermes memory and skill interfaces are pinned to revision 345cd2b057a45 .”

边界：This exclusion concerns the present Harness topic, not whether persistent experience is useful or self-improvement in a broader taxonomy. Natural-language skills can qualify elsewhere when behavioral-policy modification is evidenced; the filename is not decisive.

source_hash: `5435049b16f931063090678d6a7ef24a691684bc53e22c3f27bdfd35c9fc90fe`

### arxiv:2611.07319 · WeightLoop: Weight-Space Programming with Experimental Feedback

LLM 一次写出的 editor 固定；后续实验反馈更新科学预测器的数值权重/系数/叶值，持久对象是模型参数。未证实 editor 或其它外部 Harness 同步反馈改写，不能归为 Harness 共演化。

- Introduction: “The editor code and LLM remain fixed during this loop.”
- Introduction: “New measured outcomes determine the parameter changes, without another LLM call or gradient retraining.”
- Introduction: “The scientific predictor is the object of this improvement loop.”

边界：Repeated predictor updates are not recursive rewriting of the editor. No independent recomputation of reported ranking/discovery metrics.

source_hash: `6e79c531101abd2c3c0a35d6cbfdb5adcc117d44ce83cb49758c1b8f0462b631`

### arxiv:2611.07054 · Reclassification Is All You Missed: Surfacing Variant Reinterpretation Need in Online Health Communities at Population Scale

PRISM 临床变异重解释工作流与 no-contact dry run；无反馈改写持久 Harness 的证据。

- Official abstract: “We built PRISM, an agentic large-language-model pipeline that screens these posts, checks whether the variant was later reclassified, and drafts a disclaimer-bearing outreach message, in a no-contact dry run.”

source_hash: `30e7e29a9fd59ad4237be303f72888fe9dbbe381984f4ead9e7b149887a6b953`

### arxiv:2611.05454 · Agentic Behavior Engineering: A Design-by-Contract Methodology for Specifying, Verifying, and Governing Enterprise AI Agents

工程方法论和契约/回归职责分工，描述应改何种资产；摘要未展示 agent 基于反馈自动改写并继承 Harness 的执行闭环。

- Official abstract: “We illustrate the method with an executable capacity-allocation boundary suite and a constructed worked example of a product-review approval workflow.”

source_hash: `6cfb1e9f90b8f83a83591ff73ea7a2899708e87d5ad4d4fc497504be858309b3`

### arxiv:2611.08321 · ControlAnything: Generative UI and On-Demand Device Integration for Mixed-Reality Hand Interaction by a Coding Agent

设备连接程序是当前用户任务产物；摘要把 connector reuse 明列后续工作，未证明跨任务 Harness 保留与演化。

- Official abstract: “These findings point to connector reuse and the observation of effects through the headset's own sensors as next steps for on-demand device integration in MR.”

source_hash: `98ea4cb52ae24fef7a7a872002f695be2244ef25db8f482149ebad163d029a5b`

### arxiv:2611.07329 · Where Do Reported Long-Video QA Gains Come From? A Controlled Audit of Frame Selection, Evidence Injection, and Expert Routing

固定骨干/提示/预算的 frame selection 与 evidence/model-swap 消融；不是反馈驱动 Harness 演化的专项评测。

- Official abstract: “It holds the backbone, frame budget, decoding, prompt and grader fixed while varying one decision at a time.”

source_hash: `02b4e4d7c73c38a1c0429fdeae3181f5659ef5fcf053a75df18857748665ebd0`

### arxiv:2611.07554 · The Memory Trap: Language Agents Overgeneralize from Benign Interactions

研究持久记忆内容导致的跨任务过度泛化；未见记忆管理程序/策略被闭环修改，应归经验/记忆安全评测。

- Official abstract: “These findings demonstrate that even benign interactions can lead to serious risks from memory systems, and thus motivate the need for new research into ensuring that agents preserve the scope of their memories.”

source_hash: `13a6584fdfcdb0770b1ebb8c68a6991188704d7a5cfaf140120b1ef2ce507669`

### arxiv:2611.08452 · ReproBridge: Building Reproducibility into ML Research Artifacts

优化后的代码/环境/launcher/复现说明是研究任务产物与可复现知识包；摘要未展示反馈改写通用 agent Harness 的代际闭环。

- Official abstract: “We define a standardized artifact design comprising a refined codebase, environment setup, experiment launchers, and a reproduction guide, and introduce ReproBridge, an agent workflow for constructing these refined reproducible artifacts.”

source_hash: `da8df1e27f131ccb8d7e931108fe9a421796181bf431e2f7fb187a504fa5f90a`

### arxiv:2611.06543 · Using Experience Twice: Dynamic Process Rubrics for Privileged Token-Level Credit Assignment

动态 rubric 是训练期 privileged supervision，服务 GRPO 权重学习；未显示推理时保留的外部 Harness 组件同步演化。

- Official abstract: “ORSD treats the selected rubric bundle as privileged information during training, then compares the log-likelihoods of the original tokens with and without the rubric.”

source_hash: `6798c7fe1a86f71290b54abce67e2c191e41270be009c5066d3d8452cfdd7460`

### arxiv:2611.06863 · Rethinking Self-Repair in Code-as-Policy Agents: What Drives Retry Success?

固定反馈模板与冻结代码模型反复生成当前场景程序；实验针对任务内 retry，不证明跨任务 Harness 演化。

- Official abstract: “A fixed lookup selects feedback templates using failure labels and the API variant. A frozen code model generates a fresh program after each scene reset.”

source_hash: `3174ae0fefe76fc7f76ff8c29948231732cf3b1c03d63d748001553ca3040cc6`

### arxiv:2611.05551 · VirtualTrialHarness: Coordinating Agentic Operationalization of Virtual Trial Protocols Across Complex Clinical Schemas

静态框架选择可复用 procedural skills 并维持跨阶段契约；摘要未说明工具/技能库本身如何根据执行反馈迭代保留，不能仅因标题 Harness 纳入 RSI。

- Official abstract: “Here we introduce VirtualTrialHarness (VTHarness), an agent framework that coordinates virtual-trial operationalization by selecting reusable procedural skills for each workflow stage and uses explicit contracts to maintain consistent study decisions across stages.”

source_hash: `78bfe381314565446b431b51f3eab3a4d9de302fcaeaf48bc20d62a5954f3f87`

### s2:563e7283598c54f4ade87b809f84eb885f8e18ed · ELLMO at LLMs4OL 2026 Tasks Flagship, Reuse, and Taxonomy: Ontology Learning Across Contexts

已核 S2 原始引用响应的 paperId/title/abstract 匹配，但未取得作者或出版社可核验的身份与日期来源。不能把元数据排除建议写成三轮完成。

- S2 摘要（官方身份未核）：“Across these tasks, we develop task-specific methods that combine LLM prompting, NLP-based extraction, ontology context, cross-domain classification, and embedding-based downselection.”

source_hash: `b59e4827505c535fbd70b8077d2be5edfb43f51cf4d3d0e1499eda0b9689952f`

## 日期与数字边界

Coca-Cola 在实际查询的 2026-11-06 HF 榜单中，首次发现仍为 2026-11-08；论文原始/版本时间取官方 2026-11-04T13:32:36Z。其他本轮 S2 条目未观察到 HF 推荐日，不能补造。Evolver 与 ELLMO 的待补原因逐项保留。

本报告未改论文摘要或实验数字；引用严格绑定缓存 HTML/原始响应及 SHA-256，详细字符位置见 JSON。没有实验复现或全部表格数值复算。付费调用 0，生产数据修改 0，GitHub 写入 0。
