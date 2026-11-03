# 2026-11-03 两篇论文一手来源范围审查

结论建议：**TSFLab include；Operon-S1 exclude**。这是范围审查建议；两项正式 decision 仍为 defer，独立复审待完成，未运行正式质量闸门或发布。

只读取主任务保存的官方 abs 与 v1 HTML。四份 HTTP 200 回执及正文 hash 已核对；本次没有网络请求、付费调用、代码复现或实验数字复算。既有冻结报告没有改动。

| 论文 | 官方 v1 首发/版本时间（UTC） | 范围建议 | 关键对象 |
| --- | --- | --- | --- |
| TSFLab | 2026-10-29T19:22:33Z | include | procedural instructions/guidance and runner checks; AGENTS.md and skills establish the carrier layout, while exact changed-file diffs remain unverified |
| Operon-S1 | 2026-10-30T07:07:09Z | exclude | fast decision model checkpoint and probability calibration |

## TSFLab

建议收录其共享工作流/工具与指令修订机制：执行与评估暴露问题，Recursive Improver 促使 guidance、runner checks 和 instruction 更新，复检后进入共享 workbench，后续任务继承。目录中模型实现、知识卡片、预测结果本身不作为 Harness 纳入依据。

反证与边界：§3.1 明说 workbench 不修改宿主 model/harness；按作者命名，CLI 宿主 harness 不变。Follow RSI 的对象判据还包括宿主外的可复用指令、工具和工作流策略；本例明确报告的 instruction/runner 更新满足这一程序性对象边界。附录 AGENTS.md/skills 用于定位程序性载体，不能据此声称已独立取得它们的逐文件修改 diff。也不能把所有知识资源、模型目录和科研产物维护都算作 Harness。

身份：官方 abs ID、标题及 submission history 已核对；只列 v1，正文 URL 明确为 v1。这里确认的是本次保存来源的版本，不自动改写 canonical 或此前 S2 初筛快照。

### 原文证据

- **§3.1 Problem Statement** — [`S3.SS1.p1.1`](https://arxiv.org/html/2610.40901v1#S3.SS1.p1.1)

> without changing the model or harness

作者把宿主 Agent harness 与外部 workbench 分开命名；不能忽略该限定，也不能只靠标题决定范围。

- **§3.5 Recursive Improver** — [`S3.SS5.p1.1`](https://arxiv.org/html/2610.40901v1#S3.SS5.p1.1)

> Here, self-improvement means incorporating verified research outputs and fixes into the workbench’s shared resources and workflows so later agents can reuse them.

范围应只取程序性 guidance/workflow/runner 修订，科研方法实现和知识资源本身不能都算 Harness。

- **§3.5 Recursive Improver** — [`S3.SS5.p1.1`](https://arxiv.org/html/2610.40901v1#S3.SS5.p1.1)

> evaluation problems found during research sessions lead to revised guidance and runner checks; later sessions inherit these repairs.

直接支持执行/评估反馈、可复用程序性工件修改和后续会话继承。

- **§3.5 Recursive Improver** — [`S3.SS5.p2.1`](https://arxiv.org/html/2610.40901v1#S3.SS5.p2.1)

> Failed checks prompt revision and rechecking before integration, supporting workbench maintenance.

修订必须通过复检再集成，不能把未经验证的输出等同于已保留工件。

- **§3.5 Recursive Improver / Usability** — [`S3.SS5.p3.1`](https://arxiv.org/html/2610.40901v1#S3.SS5.p3.1)

> Continuous integration (CI) checks basic operations.

可用性检查的实现；详细段落还说明运行、协议、配置一致性检查。

- **§3.5 Recursive Improver / Consistency** — [`S3.SS5.p5.1`](https://arxiv.org/html/2610.40901v1#S3.SS5.p5.1)

> An independent read-only review agent checks whether cards describe implementations and whether implementations preserve the defining mechanisms in papers and pinned official code, using papers alone when code is unavailable.

独立只读复核是资源一致性检查；不把它自动解释为所有指令修订都获得提升检验。

- **§3.5 Recursive Improver** — [`S3.SS5.p6.1`](https://arxiv.org/html/2610.40901v1#S3.SS5.p6.1)

> Additions and fixes from these tasks undergo the same checks, forming a shared update cycle that reduces repeated collection, implementation, and setup.

说明跨后续研究任务反复维护的共享更新周期。

- **§4.4 Further Analysis / Maintenance through reuse** — [`S4.SS4.p3.1`](https://arxiv.org/html/2610.40901v1#S4.SS4.p3.1)

> Missing guidance, manual configuration, repeated log polling, and premature test access led to instruction and runner updates; all 17 initial usability failures were repaired before integration.

正文报告实际 instruction 与 runner 更新；17 为原文数字，本审查未复算。

- **§4.4 Further Analysis / Maintenance through reuse** — [`S4.SS4.p3.1`](https://arxiv.org/html/2610.40901v1#S4.SS4.p3.1)

> although they do not isolate the effect of individual checks.

不能把聚合性能或所有检查的作用独立归因到 Harness 演化。

- **Appendix A.1 Framework Structure** — [`A1.SS1.p1.2`](https://arxiv.org/html/2610.40901v1#A1.SS1.p1.2)

> and workflows in .agents/skills/

定位工作流工件；论文模型和单元所在目录另列，说明二者不可混淆。

- **Appendix A.2 Entry Instructions and Skills** — [`A1.SS2.p1.1`](https://arxiv.org/html/2610.40901v1#A1.SS2.p1.1)

> It states the workbench conventions, module interactions, resource access, and verification requirements.

AGENTS.md 的内容是流程/验证约束，不只是外部问题答案或领域知识卡片。

- **Appendix A.2 Entry Instructions and Skills** — [`A1.SS2.p1.1`](https://arxiv.org/html/2610.40901v1#A1.SS2.p1.1)

> Task-specific skills provide the steps, checks, and common pitfalls of each workflow and are loaded as needed.

可复用任务步骤和检查属于程序性策略载体。

### 证据限制

- 这是原文支持的范围建议，不是对主表所有性能/费用提升归因到 Harness 自进化。
- §4.4 直接承认未隔离各检查的影响；没有逐个修订版本的留出泛化或多代累计收益复算。
- 论文同时维护 TSF 模型代码、知识资源和科研产物；这些不全部属于 Harness。
- 只核验本次方法范围，不设置证据卡的 held_out/matched_budget/cross_model/cost 等正式字段。
- 当前未请求代码仓库或重跑 CI；程序性修改的具体文件 diff 未独立复现。

后续：交独立审查核对 §3.5、§4.4 与附录 A 的程序性更新边界；即使意见一致也需保留正式审核和质量闸门，不能由本报告直接 accept。


## Operon-S1

建议不纳入当前 Harness RSI 专题。论文的反馈、hard-example mining、晋级与跨轮继承闭环都作用于 LAYA 决策模型检查点及校准；policy、thresholds 和 messages 固定。即使慢模型不变，更新外部小决策模型的权重也不等同于可复用 Harness 工件自改。

反证与边界：r03→r04b 确实新增/修订技能并有留出测试，应承认这部分外部工件变化。论文把技能版本效应和决策层训练分开测量，正文未把技能的系统自动生成、验收、反馈修订与 LAYA gated rounds 联成共演化机制；不能因为同文出现技能修订就推定已验证 Harness RSI。gate-rules@2 也是开发审计后的修订，正文明确发生在该版本判断任何候选之前。

身份：官方 abs ID、标题及 submission history 已核对；只列 v1，正文 URL 明确为 v1。这里确认的是本次保存来源的版本，不自动改写 canonical 或此前 S2 初筛快照。

### 原文证据

- **Results / Operon-S1 lifts the agent’s judgements into a separate decision layer** — [`Sx2.SSx1.p2.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx1.p2.1)

> All controllers share this policy and these messages and differ only in the distributions they return

控制器对比固定 policy/messages，变化主要在决策模型输出分布。

- **Results / Operon-S1 lifts the agent’s judgements into a separate decision layer** — [`Sx2.SSx1.p2.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx1.p2.1)

> a message written in advance that may name a convention, a file or a quantity to verify.

提示模板预先写好，未显示它在 gated rounds 中被自动改写。

- **Results / Gated retraining couples a data-synthesis pipeline with a promotion gate** — [`Sx2.SSx5.p1.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx5.p1.1)

> Each round runs the data-synthesis pipeline, which turns an executable curriculum into decisions with verifiable labels, mines hard examples from the parent version’s errors, trains a candidate, fits a temperature-scaling calibration

明确反馈闭环存在；被训练和校准的是决策模型。

- **Results / Gated retraining couples a data-synthesis pipeline with a promotion gate** — [`Sx2.SSx5.p1.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx5.p1.1)

> A promoted version controls the agent and is the parent whose errors the next round mines, so each round starts from the last promoted version.

版本保留与下一轮继承真实存在，但对象是模型检查点，不能混为 Harness 工件。

- **Results / Training raised accuracy on every decision question, and the gains carried over to the agent’s own states** — [`Sx2.SSx6.p3.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx6.p3.1)

> Because only the decision model changes, a trained version can be scored on the agent’s own decision states from the held-out halves, whose items training never drew on

作者直接限定该训练评估中只有决策模型变化。

- **Results / Training raised accuracy on every decision question, and the gains carried over to the agent’s own states** — [`Sx2.SSx6.p3.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx6.p3.1)

> The quantity that training targets and the gate certifies is decision accuracy.

发布 gate 认证决策准确率；不是 Harness 程序修改的验证。

- **Results / The seqqa2 baseline gain comes from a convention skill layer, measured apart from the decision layer** — [`Sx2.SSx7.p1.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx7.p1.1)

> r04b adds a general sequence-computation layer and a separately named convention layer for LAB-Bench to r03, together with a patch to the protocol-audit skill.

必须承认外部技能版本有变化，不能声称全文完全没有 Harness 改动。

- **Results / The seqqa2 baseline gain comes from a convention skill layer, measured apart from the decision layer** — [`Sx2.SSx7.p1.1`](https://arxiv.org/html/2610.41350v1#Sx2.SSx7.p1.1)

> Skills were developed only on the development half of seqqa2, split by a hash of the item identifier, and the held-out half was tested once per release.

技能开发与留出测试另行存在，但该段没有把它描述为本方法的系统自动生成/接纳/反馈迭代工件闭环。

- **Methods / Control policy** — [`Sx4.SSx9.SSSx4.p1.1`](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx4.p1.1)

> All controllers share the policy, thresholds and messages below

控制策略、阈值和消息保持一致是实验设计；不能由变更推理输出推定它们也在自改。

- **Methods / Training and calibration** — [`Sx4.SSx9.SSSx13.p1.1`](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx13.p1.1)

> Models were fine-tuned from the public checkpoint with the vendor training tool

确认候选更新涉及模型权重，不只是冻结模型外提示的改写。

- **Methods / Training and calibration** — [`Sx4.SSx9.SSSx13.p1.2`](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx13.p1.2)

> thresholds are not refitted.

校准候选也不等于控制阈值自进化。

- **Methods / Promotion gate** — [`Sx4.SSx9.SSSx14.p1.4`](https://arxiv.org/html/2610.41350v1#Sx4.SSx9.SSSx14.p1.4)

> An audit found that the first version of the gate could pass a candidate that learned only the label prior, before that version judged any candidate.

gate-rules@2 的修订发生在它评价候选前；不能据此补写为被评测的自动 Harness 元改进回路。

### 证据限制

- 排除依据是已报告自动改进回路的对象，不是“有权重训练就一律排除”；若原始新证据支持权重与外部工件联合迭代，可重判共演化。
- 没有声称全文不存在外部技能变更，相关 r03/r04b 证据已单列。
- 不把固定决策 Harness 的静态控制器对比重新命名为 Harness 自进化专项评测。
- 论文所述决策准确率与最终任务结果分开；本审查未复算任何实验数字或统计显著性。
- 未核查仓库代码、技能提交者或完整版本 diff；对于未描述的技能自动更新机制保持未确认。

后续：独立复审重点检查 r03/r04b 技能开发和 gated training 是否有原文未覆盖的联动自动闭环；若无，可记录范围排除，保留一般模型 RSI/决策控制研究线索。

## 校验

24 条引句已逐条验证为对应段落的空白规范化子串；每条附 section、段落锚点、源文件及 SHA256。已核对两份 abs 和两份全文的官方请求回执。

范围审核不会自动填论文证据卡、不把论文中的晋级 gate 当作 Follow RSI 的正式质量闸门、不把原文 reported 数字称作独立复算。

保留 new-source-screen.json/.md 的历史摘要初筛。本报告是主任务随后取得官方 abs 与正文后形成的范围纠正/确认，不回写此前初筛，不改变正式 defer，也不表示 Follow RSI 质量闸门已过。
