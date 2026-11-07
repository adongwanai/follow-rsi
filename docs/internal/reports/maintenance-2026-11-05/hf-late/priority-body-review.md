# HF 晚到重点论文正文范围复核

复核时间：2026-11-05T07:45:32.178868+00:00

仅复核两篇官方 HTML 的方法与边界章节；这是建议，不是正式接收、排除或发布批准。初筛历史文件保持不变。

本次正文读取：2 次免费 arXiv HTML GET，均 HTTP 200；此前完整 HF 榜单 GET 1 次。付费调用 0。官方元数据查询单独记账。

初筛列出的3篇优先正文问题中，本报告只补读 EmoReward 和 SleuthVLM。PyRUA-DataFarm 未由本审阅者补读正文；初筛文件保留原历史状态。

## arxiv:2611.06518 — EmoReward: Self-Evolving Reward Calibration for Emotional Video Generation RL

建议：exclude；对象：data_task；正式状态：defer。

奖励系统确实把完成训练的反馈转成下一次训练复用的数值校准表，不能说没有反馈或没有持久化；但改变对象是训练奖励分配（data_task），所读正文未展示 Agent 自身可复用 Harness 的修改、验收与继承，因此建议排除当前 Harness 发布范围。

来源：https://arxiv.org/html/2611.06518；观察时间：2026-11-05T07:40:05.168157+00:00
HTML SHA256：`2824f46ab835d9543dccc11b9771460f5b817a3bfd484d76e0a54bf91cd55c42`
段落文件：`build/pr39-resolution-2026-11-05/hf-late/bodies/2611.06518.paragraphs.json`
段落 JSON SHA256：`d2594c4cd73f75940a042f7f981da4c42215328b0ae2e2d32db6b03ff78f9111`

已读：第3节 Method（全部提取段落）；附录A Limitations and Future Work（全部提取段落）；附录E Evolve: RewardMemory Construction and Use（全部提取段落）。

- agent_runtime_present：文章以 Plan/Act/Reflect/Evolve 描述奖励系统；该命名本身不足以证明 Agent 自身执行程序被改写。
- changed_object：由完成的参考训练轨迹估计提供者可靠性，形成奖励融合权重/倍率数值表；生成器训练另外更新模型参数。
- feedback：有。参考运行的提供者分数与 VideoAlign outcome 的相关性用于校准奖励分配。
- retention：有。导出的表在后续训练中固定查询和复用。
- own_reusable_harness_modification：未见。所读方法和限制未展示 Agent 改写自己的提示词、工具、控制程序、验证/改进策略并继承接受版本。
- validation_and_inheritance：有参考到校准训练的实验比较与奖励表继承；未展示候选 Harness 修改的验收和跨任务版本谱系。
- co_evolution_check：未因含模型训练而直接排除；另外检查外部工件，实际改变的是训练奖励表，按 taxonomy 属 data_task。
- sustained_rsi：未演示持续多代，附录A明确只有一次 reference-to-calibrated transition。

可核对原文（每项均是已存规范化段落的逐字子串）：

- [#S3.SS4.p1](https://arxiv.org/html/2611.06518#S3.SS4.p1)，段落索引 16，SHA256 `fde919a98b188c061b14c89ec195c72972422ea2c562a786116057e806e1f4b7`
  > These controls are computed, not learned (Appendix D ).
  当前证据门控为预设计算规则。

- [#S3.SS4.SSS0.Px2.p1](https://arxiv.org/html/2611.06518#S3.SS4.SSS0.Px2.p1)，段落索引 18，SHA256 `02e2a06ae37955c52fb8b9bbc733ed90f138c46504d8f20ba5bdb0b7895128b8`
  > EmoReward uses the fixed table produced by Evolve.
  跨训练运行复用的是奖励分配表。

- [#S3.SS5.p1](https://arxiv.org/html/2611.06518#S3.SS5.p1)，段落索引 19，SHA256 `d4178c59df6487cd74e987c048479e7bc16677182fa4253c03c93a182fc950f4`
  > The table is fixed throughout the next training run: only the generator receives gradient updates, and runtime lookup neither re-estimates reliability nor writes back to the table.
  下一次训练期间表固定，只有生成器接受梯度更新。

- [#A1.SS0.SSS0.Px1.p1](https://arxiv.org/html/2611.06518#A1.SS0.SSS0.Px1.p1)，段落索引 34，SHA256 `adaa16d5fe721432f8edefec3a447f24723afbc1bd719e9640907dbf809484d8`
  > EmoReward studies a training-adaptive reward system that transfers evidence about provider reliability between generator-training runs without updating reward-model parameters.
  确有跨运行反馈转移，但对象为生成器训练奖励分配。

- [#A1.SS0.SSS0.Px2.p1](https://arxiv.org/html/2611.06518#A1.SS0.SSS0.Px2.p1)，段落索引 35，SHA256 `f8e8cdd8a85d9c88c5b31f3addc4230dfb3133243d28b983ba1f31f1e9fd8a7e`
  > Our experiments evaluate a reference-to-calibrated transition, not sustained improvement across many generations.
  实验证据只覆盖一次参考运行到校准运行的转移。

- [#A1.SS0.SSS0.Px3.p1](https://arxiv.org/html/2611.06518#A1.SS0.SSS0.Px3.p1)，段落索引 36，SHA256 `1854d672484cd73f1fb4fe2db9edd046e6ffcb10a8946ee60bd5568dd576240d`
  > The ordinal study reported here evaluates outputs; it does not implement this proposed feedback mechanism.
  模型层人工反馈是未来方案，当前输出评价未实现。

- [#A5.SS0.SSS0.Px3.p1](https://arxiv.org/html/2611.06518#A5.SS0.SSS0.Px3.p1)，段落索引 59，SHA256 `3204a8ed7809535ad8638a559432ff347326d026f62109bbd295470eac4a5086`
  > Panel C illustrates this multiply-and-normalize step using recorded scores and illustrative starting weights: it is a controlled replay, not an additional training run.
  图7C的受控回放不能计为额外训练或演化代次。

Official unversioned HTML URL was observed at the recorded time. No v1 date or version is inferred from the HTML URL; official metadata is tracked separately.

## arxiv:2611.06083 — SleuthVLM: Do We Really Need Audio-in-Video for Omni Video Understanding?

建议：exclude；对象：static_framework；正式状态：defer。

文章有真实 Agent Harness，但正文明确系统提示词中的作用域和指南在各 benchmark 固定，守卫规则固定，每题单独 sandbox。动态证据查找、工具反馈和增长的历史属于任务执行状态，未见 Agent 修改可复用 Harness 并验收继承，建议按 static_framework 排除。

来源：https://arxiv.org/html/2611.06083；观察时间：2026-11-05T07:40:09.179513+00:00
HTML SHA256：`68b72ab0dd5fa0b8330cf5e42053c780e94fee899a48eb75d035bef5d67a9a90`
段落文件：`build/pr39-resolution-2026-11-05/hf-late/bodies/2611.06083.paragraphs.json`
段落 JSON SHA256：`f5c4d20a64091dde239cb3b13e54bf94f57defd1ab0affd9054449fb9a1c01d3`

已读：第3节 Method（全部提取段落）；第4.1节 Implementation details 段落；第6节 Conclusion；第9节 Implementation details（全部提取段落）；第13节 Sandbox rules and trajectory audit（全部提取段落）。

- agent_runtime_present：有。VLM 通过工具动态查找视频证据，并决定本题何时回答。
- changed_object：单题的对话历史、检索窗口、采样间隔、工具输出和轨迹；系统提示词、操作指南及守卫规则固定。
- feedback：有任务内工具返回与拒绝原因；未见候选 Harness 工件的评估反馈驱动后续程序修订。
- retention：日志和本题上下文保留；每题独立内存 sandbox。所读正文未展示修改后的 Harness 版本跨题继承。
- own_reusable_harness_modification：未见。正文明确作用域和操作指南在每个 benchmark 相同。
- validation_and_inheritance：报告性能评测和 sandbox 审计，但未展示自动生成 Harness 候选、验收并部署为继承版本的闭环。
- co_evolution_check：本判断基于固定 Harness 与任务态变化的区分，不依赖是否训练模型。
- sustained_rsi：未展示。动态推理/工具执行不等同持续程序演化。

可核对原文（每项均是已存规范化段落的逐字子串）：

- [#S3.SS3.p1](https://arxiv.org/html/2611.06083#S3.SS3.p1)，段落索引 17，SHA256 `50f971d555e8e0a710fb8456cc064341b529e1f31b825b3d446bbb1c4577130e`
  > The harness consists of a scope definition, which fixes what the model can access and do, and an operating guide, which suggests how to gather evidence; both are part of the system prompt and are the same on every benchmark.
  同一固定系统提示词包括作用域和操作指南。

- [#S3.SS3.SSS0.Px2.p1](https://arxiv.org/html/2611.06083#S3.SS3.SSS0.Px2.p1)，段落索引 19，SHA256 `ff121fceab4fe490daba06c9069e04ff81445fdd896aca74df18861549953fbe`
  > The model decides which steps a question needs.
  Agent 自主选择本题的证据收集动作。

- [#S3.SS4.p1](https://arxiv.org/html/2611.06083#S3.SS4.p1)，段落索引 21，SHA256 `548163f4b489873fe7694d4cf2e3040b6b039fa6d99d8b57b39a02831e428ae3`
  > The model takes these steps on its own; the harness prescribes no window or interval.
  本题窗口/间隔调整是执行时选择，不等同改写 Harness。

- [#S9.SS0.SSS0.Px1.p1](https://arxiv.org/html/2611.06083#S9.SS0.SSS0.Px1.p1)，段落索引 44，SHA256 `e84566c1354aa5475906699a5b75f95c18aeb1bdf52d54c8284754c9117ecf8b`
  > Earlier reasoning stays in the history, so prompts only grow and the prefix cache is reused; when a prompt exceeds 110k tokens, the oldest images are dropped from it.
  历史和固定裁剪规则是运行状态与既定策略。

- [#S9.SS0.SSS0.Px2.p1](https://arxiv.org/html/2611.06083#S9.SS0.SSS0.Px2.p1)，段落索引 45，SHA256 `7d793ad4b6b4e5b9e7559181bc809f4accbc2a3b4afdd0fcf58db381b732576e`
  > Each question gets its own sandbox in memory, with a muted copy of the video, and every command is logged.
  sandbox 的边界是单个问题。

- [#S13.SS0.SSS0.Px1.p1](https://arxiv.org/html/2611.06083#S13.SS0.SSS0.Px1.p1)，段落索引 64，SHA256 `3beab5a15940dba3917eb076e86f200cf0605e1a194e99081fc832a75c125f6a`
  > Before a command runs, a guard checks it against fixed rules
  安全守卫执行固定规则。

- [#S13.SS0.SSS0.Px2.p1](https://arxiv.org/html/2611.06083#S13.SS0.SSS0.Px2.p1)，段落索引 65，SHA256 `ae81cbcf50841520dc7816488e065ed2f821c935fb17b8bad8fe759e06fa21c9`
  > Every bash command and its output are written to the result file, and every refused command is kept with its reason.
  轨迹与拒绝原因会保存，但未展示由其驱动 Harness 修改与继承。

Official unversioned HTML URL was observed at the recorded time. No v1 date or version is inferred from the HTML URL; official metadata is tracked separately.

