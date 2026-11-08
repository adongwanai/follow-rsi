# 2026-11-03 两篇论文独立正文范围复审

TSFLab 建议纳入 Harness 方法范围；Operon-S1 建议排除出当前 Harness 专题，保留为决策模型/权重 RSI 相关工作。两项正式决定均保持 defer，本报告不产生人工批准。

已核验四份官方 HTTP 200 回执与哈希、两篇 v1 身份和原日期。使用本地正文，无新增网络、付费调用或 GitHub 写操作。主审仅用于对照；本轮不声称盲审。

## TSFLab: A Self-Improving Agent-Agnostic Workbench for Time Series Forecasting Research

arxiv:2610.40901；官方 v1 原日期：2026-10-29T19:22:33Z；建议：include。这是来源发现，不是已核实的 11 月 3 日 HF 榜单成员。

仅将共享程序性指引、流程和 runner 检查的反馈修订链纳入 Harness 方法范围。§3.5 明确研究会话中的评估问题促使 guidance 与 runner checks 修订，经重检集成后由后续 sessions 继承；§4.4 给出实际 instructions 和 runner 更新。

### 修改、反馈、准入和保留

- model_update：按作者定义，宿主 Agent 模型与内部 harness 保持不变。预测模型训练属于科研任务产物，不是本次判为 Harness 的更新链。
- feedback：研究执行中缺失指引、手动配置、重复轮询、提前访问测试数据等失败推动共享 instructions 和 runner 检查修订。
- admission：Recursive Improver 通过可用性、复杂度、一致性检查接纳；失败必须修订和重新检查。独立只读 Agent 审核实现与来源的一致性。
- retention：接受的 repairs 写入共享 workbench，后续会话继承；Appendix A 的入口 AGENTS.md 与 .agents/skills/ 是外置程序性载体。
- automation_boundary：正文描述 agent-produced outcomes/repairs 的验证集成链，并报告实际修复；本轮没有核验代码 diff 或逐条自动写入日志。

### 可核验原句

- **author-boundary** · §3.1 Problem Statement · [S3.SS1.p1.1](https://arxiv.org/html/2610.40901v1#S3.SS1.p1.1)

  > without changing the model or harness

  作者将宿主 Agent 内部 harness 与共享 workbench 分开命名，不能忽略这个限定。

- **feedback-retention** · §3.5 Recursive Improver · [S3.SS5.p1.1](https://arxiv.org/html/2610.40901v1#S3.SS5.p1.1)

  > evaluation problems found during research sessions lead to revised guidance and runner checks; later sessions inherit these repairs.

  执行/评估问题导致程序性指引与 runner 检查修订，后续会话继承修复。

- **admission** · §3.5 Recursive Improver · [S3.SS5.p2.1](https://arxiv.org/html/2610.40901v1#S3.SS5.p2.1)

  > Failed checks prompt revision and rechecking before integration, supporting workbench maintenance.

  失败修改重检后才能集成，存在准入过程。

- **verification-agent** · §3.5 Recursive Improver, Consistency · [S3.SS5.p5.1](https://arxiv.org/html/2610.40901v1#S3.SS5.p5.1)

  > An independent read-only review agent checks whether cards describe implementations

  独立只读审核是验证集成的一部分，不能单独当作更新的效果证明。

- **actual-workflow-fixes** · §4.4 Further Analysis, Maintenance through reuse · [S4.SS4.p3.1](https://arxiv.org/html/2610.40901v1#S4.SS4.p3.1)

  > Missing guidance, manual configuration, repeated log polling, and premature test access led to instruction and runner updates

  观察到的更新对象包括 instructions 和 runner，而非仅预测模型或科研产物。

- **repair-count** · §4.4 Further Analysis, Maintenance through reuse · [S4.SS4.p3.1](https://arxiv.org/html/2610.40901v1#S4.SS4.p3.1)

  > all 17 initial usability failures were repaired before integration.

  原文报告的 17 项失败在集成前修复；未复算此数字。

- **entrypoint** · Appendix A.2 Entry Instructions and Skills · [A1.SS2.p1.1](https://arxiv.org/html/2610.40901v1#A1.SS2.p1.1)

  > Every session starts from one harness-neutral entry file, AGENTS.md

  共享入口为后续会话加载程序性指导提供载体。

- **causal-limit** · §4.4 Further Analysis, Maintenance through reuse · [S4.SS4.p3.1](https://arxiv.org/html/2610.40901v1#S4.SS4.p3.1)

  > although they do not isolate the effect of individual checks.

  作者明确没有隔离各项检查效果。

### 反例与结论边界

- §3.1 与结论称不改宿主模型或 harness。仓库按实际工件而非作者组件命名划界：外置共享的 instructions、工作流和执行检查属于可复用运行层；不能据此把整个 workbench 资源都算作 Harness。
- 预测模型、数据、RevIN 等神经网络组件、知识卡内容和科研结果的增补或重构都不是本次 include 的依据。
- §4.3 不含 Recursive Improver 的独立消融，§4.4 明确未隔离各检查效应。整体完成率/token 对比不能直接归因为递归更新的独立收益。
- 正文支持 TSF 域内后续会话继承，不证明跨研究领域、长期开放运行或改进器自身递归改写。

共演化判断：不需要权重共演化例外；实际纳入依据是共享外部程序工件的反馈修订，而非预测模型训练。

后续补证：

- 提高证据强度需核对 guidance/runner 的前后版本、验收日志及后续会话加载记录。
- 需冻结工作台与持续更新工作台的对照，才能隔离更新链收益。

## Operon-S1: a fast decision controller for long-horizon biomedical agents

arxiv:2610.41350；官方 v1 原日期：2026-10-30T07:07:09Z；建议：exclude。这是来源发现，不是已核实的 11 月 3 日 HF 榜单成员。

建议排除出当前 Harness RSI 专题，保留为决策模型/权重 RSI 相关工作。已报告的错误采样、训练、校准、晋级和继承闭环作用于 LAYA 检查点；共享 policy/thresholds/messages 固定。技能和 profile 修订是实际反例，但正文未把它们接入自动外部工件自改与模型共演化回路。

### 修改、反馈、准入和保留

- feedback：父版本错误与可验证执行/构造标签驱动难例挖掘和训练分配，存在模型自改进反馈，不能说是没有反馈的固定系统。
- admission：promotion gate 对模型决策准确率、置信区间、校准、基线、样本量和退化约束作判断，候选及 verdict 进入追加注册表。
- retention：晋级检查点供后续任务/轮次控制 Agent，并成为下一轮错误来源；持久对象是模型而非已证实自动改写的外部 Harness 工件。
- automation_boundary：正文支持模型训练回路，外部 policy/thresholds/messages 固定。skill release 和 profile 是另行开发与评估的变化，未见由该系统自动生成、准入及继承它们的闭环。

### 可核验原句

- **fixed-policy** · Methods, Control policy · [Sx4.SSx9.SSSx4.p1.1](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx4.p1.1)

  > All controllers share the policy, thresholds and messages below

  训练/对比中共享外部 policy、thresholds 和 messages。

- **trained-object** · Methods, Training and calibration · [Sx4.SSx9.SSSx13.p1.1](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx13.p1.1)

  > Models were fine-tuned from the public checkpoint

  被训练对象是模型检查点。

- **feedback** · Results, Gated retraining couples a data-synthesis pipeline with a promotion gate · [Sx2.SSx5.p1.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx5.p1.1)

  > mines hard examples from the parent version’s errors, trains a candidate

  父模型错误驱动难例选择和新候选训练，确有反馈。

- **retention** · Results, Gated retraining couples a data-synthesis pipeline with a promotion gate · [Sx2.SSx5.p1.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx5.p1.1)

  > A promoted version controls the agent and is the parent whose errors the next round mines

  晋级模型在后续轮次继续控制 Agent 并提供错误，确有持久继承。

- **certified-target** · Results, Training raised accuracy on every decision question · [Sx2.SSx6.p3.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx6.p3.1)

  > The quantity that training targets and the gate certifies is decision accuracy.

  被 gate 认证的是决策准确率，不是外部工件演化或整体任务净收益。

- **model-only** · Results, Training raised accuracy on every decision question · [Sx2.SSx6.p3.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx6.p3.1)

  > Because only the decision model changes

  该训练比较中变化的是决策模型。

- **skill-change** · Results, The seqqa2 baseline gain comes from a convention skill layer · [Sx2.SSx7.p1.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx7.p1.1)

  > r04b adds a general sequence-computation layer and a separately named convention layer for LAB-Bench to r03

  同文确实存在可复用技能版本变化，不能说完全没有外部工件变化。

- **skill-development** · Results, The seqqa2 baseline gain comes from a convention skill layer · [Sx2.SSx7.p1.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx7.p1.1)

  > Skills were developed only on the development half of seqqa2

  存在技能开发/留出安排；这不证明系统自动提议、晋级和继承技能修订。

- **profile-change** · Results, A domain profile extends the same harness to laboratory-protocol troubleshooting · [Sx2.SSx8.p2.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx8.p2.1)

  > We therefore built a protocol profile of the harness.

  承认实际外部 Harness profile 扩展。

- **profile-after-results** · Results, A domain profile extends the same harness to laboratory-protocol troubleshooting · [Sx2.SSx8.p3.1](https://arxiv.org/html/2610.41350v1#Sx2.SSx8.p3.1)

  > The profile was designed after the protocolqa2 results of the main run were seen

  profile 是主实验结果后设计的探索性开发，未描述其由模型晋级循环自动修订。

- **gate-audit-order** · Methods, Promotion gate · [Sx4.SSx9.SSSx14.p1.4](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx14.p1.4)

  > before that version judged any candidate.

  gate-rules@2 在旧 gate 尚未判断候选时由开发审计修订，不能称运行中改进器自演化。

- **main-arm** · Methods, Cross-fitting · [Sx4.SSx9.SSSx15.p1.2](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx15.p1.2)

  > In the main run every task is answered by version 0.

  主任务实验使用 version 0，不能把离线决策训练收益泛化为多轮任务收益。

### 反例与结论边界

- 不以存在权重训练作为自动排除理由。若外部 Harness 工件和权重明确联合迭代，应按共演化处理。
- r03→r04b 增加序列计算与 convention 技能、修补 protocol-audit，并有开发/留出测试；这证明技能变化，未证明系统自动迭代技能。
- protocol profile 确实是在观察诊断失败后设计的外部 Harness 扩展。作者标为结果后设计、开发集调试的探索性部分，没有把 profile 作为 LAYA promotion 的可改候选。
- gate-rules@2 来源于开发审计，旧版尚未判断任何候选，不能把该修订描述成运行改进回路中的 gate 自演化。
- 训练的 gate certifies decision accuracy，主实验使用 version 0；不能声称训练后的多轮整体系任务增益已经被主实验验证。
- 它评测固定 Harness 上不同决策控制器及模型训练，而非外部程序工件反馈演化的专项基准或理论；不能借 harness study 路径绕过范围边界。

共演化判断：已检查技能版本、protocol profile、gate 规则三个反例。尚无外部工件与模型权重联合提议、准入和继承的已报告自动机制，因此当前不适用共演化例外；不是断言未来或未展示实现绝不可能存在该机制。

后续补证：

- 若后续来源提供系统按执行反馈生成的 skill/profile/policy 差异、自动准入和跨任务加载证据，应重新评估。
- 模型侧反馈和持久化正文已经支持，无需重复以缺少它们为排除理由；待补的是外部 Harness 工件自改链。

## 复审边界

主审与独立正文范围建议一致：1 include、1 exclude。JSON 保存四份源回执、20 段逐字引句、段落定位与主审报告哈希。exclude 仅指当前 Harness 专题，并非否定 Operon-S1 的反馈训练或研究价值。

未修改 canonical、已有批准或公开内容；未复算实验、复跑测试、调用付费质量门，也未宣称整个三轮审核流水线已通过。全部正式 decision 仍为 defer。
