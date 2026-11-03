# 候选 issue #16–#30 核查

核查时间：2026-11-02T08:54:12.019515+00:00

15 个 issue 正文及评论均已读取。完成来源初审/复用后的建议为 **6 收录、5 排除、4 待补证**。其中 5 篇新候选完成一手初审（3 收录、2 排除），仍需独立复核。此代理未改 canonical、未发布、未评论或关闭 issue。

公开 feed 核查时的期次为 2026-10-27；以下已准备内容不能当作已上线。

| Issue | 论文 | 范围建议 | 当前动作 |
|---|---|---|---|
| [#16](https://github.com/adongwanai/follow-rsi/issues/16) | TinyAstral | 收录建议 | independent_review_then_historical_supplement_or_catalog |
| [#17](https://github.com/adongwanai/follow-rsi/issues/17) | WeGenEvoStudio / WeGenEditBench | 范围排除 | independent_review_then_archive_scope_exclusion |
| [#18](https://github.com/adongwanai/follow-rsi/issues/18) | Video Generation Meets Agent Harness | 收录建议 | independent_review_then_historical_supplement_or_catalog |
| [#19](https://github.com/adongwanai/follow-rsi/issues/19) | KARMA | 待补证 | keep_open_evidence_required |
| [#20](https://github.com/adongwanai/follow-rsi/issues/20) | MoLRSI | 待补证 | keep_open_evidence_required |
| [#21](https://github.com/adongwanai/follow-rsi/issues/21) | RecRSI | 范围排除 | record_scope_exclusion |
| [#22](https://github.com/adongwanai/follow-rsi/issues/22) | MetaVul | 收录建议 | independent_review_then_historical_supplement_or_catalog |
| [#23](https://github.com/adongwanai/follow-rsi/issues/23) | VEvo-Harness | 待补证 | keep_open_evidence_required |
| [#24](https://github.com/adongwanai/follow-rsi/issues/24) | From Grind to Grasp | 范围排除 | record_scope_exclusion |
| [#25](https://github.com/adongwanai/follow-rsi/issues/25) | SceneEvolve | 收录建议 | historical_supplement_or_catalog |
| [#26](https://github.com/adongwanai/follow-rsi/issues/26) | RuHarness | 收录建议 | historical_supplement_or_catalog |
| [#27](https://github.com/adongwanai/follow-rsi/issues/27) | Training for Alignment | 范围排除 | independent_review_then_archive_scope_exclusion |
| [#28](https://github.com/adongwanai/follow-rsi/issues/28) | The Trinity | 收录建议 | hf_2026_10_28_recovery |
| [#29](https://github.com/adongwanai/follow-rsi/issues/29) | Work Agents | 范围排除 | record_scope_exclusion |
| [#30](https://github.com/adongwanai/follow-rsi/issues/30) | OmniBrain-0 | 待补证 | keep_open_evidence_required |

## 重要校正

- #21 RecRSI、#24 From Grind to Grasp 已有与当前输入一致的排除审查，但最新范围批准回执未覆盖这两个 ID。应补齐追踪；不是重跑付费模型的理由。
- #20 MoLRSI、#23 VEvo-Harness 官方已有 v2，canonical 保留 v1；本次另读 v1，原始版本未消除边界。
- #30 OmniBrain 摘要差异仅为 canonical 的 `teachers'interaction` 缺一个空格，issue 与官方摘要完全相同。不能称为论文改版或科学内容改变。
- #25 SceneEvolve、#26 RuHarness 没有已证实的 HF 推荐日，应进历史补录/目录；#28 Trinity 按 HF 10 月 28 日归期。
- #18 视频 Harness 综述建议计入专项评测/理论，不能增加方法篇数，不能把其引用的全部工作算成 Harness RSI。
- 新候选元数据与原始正文在 `proposed-new-items.json`、`new-source-findings.json` 及 `build/issues-2026-11-02/candidates/sources/`；短双语摘要不新增成绩数字，证据字段均保留 unknown。

## #16 TinyAstral

Stage 1 冻结 teacher 权重，由执行轨迹定位失败并修改工具、返回协议、感知和恢复组件；候选经预注册配对门控后进入可复用主线版本。Stage 2 才训练小模型，不能把后阶段蒸馏误当成第一阶段没有 Harness 演化。

已准备的短摘要：用执行反馈和配对检验演化冻结教师的工具与恢复逻辑，再蒸馏小模型。
Evolves a frozen teacher’s tools and recovery logic with execution feedback and paired tests, then distills a compact model.

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已核对官方 v1 身份及正文。原发表日期为 2026-10-30；issue 创建时间不代表论文首发或 HF 推荐日。初审建议纳入 Harness 方法。Stage 1 冻结 teacher 权重，由执行轨迹定位失败并修改工具、返回协议、感知和恢复组件；候选经预注册配对门控后进入可复用主线版本。Stage 2 才训练小模型，不能把后阶段蒸馏误当成第一阶段没有 Harness 演化。

当前完成的是一手来源初审，待独立复审后记录最终处理；尚未据此声明已发布。原文：https://arxiv.org/abs/2610.41216

关闭条件：Complete independent comparison and record final scope result; for includes, verify real catalog/supplement artifact before claiming published.

## #17 WeGenEvoStudio / WeGenEditBench

改进对象是图像生成/编辑模型的参数与训练数据处方；固定多 Agent Harness 组织诊断、检索、数据合成、LoRA 适配及复评。没有显示反馈修改并保留该 Harness 自身的提示、工具实现或控制流。基准测图像编辑质量，非 Harness 演化专项。

已准备的短摘要：诊断图像编辑失败并生成训练处方，通过监督适配更新图像模型。
Diagnoses image-editing failures and builds targeted supervision to adapt image models.

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已核对官方 v1 身份及正文。原发表日期为 2026-10-30；issue 创建时间不代表论文首发或 HF 推荐日。初审建议排除当前 Harness 专题。改进对象是图像生成/编辑模型的参数与训练数据处方；固定多 Agent Harness 组织诊断、检索、数据合成、LoRA 适配及复评。没有显示反馈修改并保留该 Harness 自身的提示、工具实现或控制流。基准测图像编辑质量，非 Harness 演化专项。

当前完成的是一手来源初审，待独立复审后记录最终处理；尚未据此声明已发布。原文：https://arxiv.org/abs/2610.41210

关闭条件：Complete independent comparison and record final scope result; for includes, verify real catalog/supplement artifact before claiming published.

## #18 Video Generation Meets Agent Harness

以视频模型外的 Harness 为分析单位，§2.3 显式区分产物、持久 Harness 和改进过程，§5.2 系统梳理 Harness 更新，§5.3.2 专门讨论 Harness 演化的预算控制、留出评估及跨轮程序对照。建议计入 Harness 专项综述/理论，绝不计入方法数量。

已准备的短摘要：梳理视频 Harness 演化，并区分产物修复、跨任务保留和改进过程更新。
Surveys video-harness evolution, separating output repair, retained cross-task changes, and updates to the improvement procedure.

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已核对官方 v1 身份及正文。原发表日期为 2026-10-29；issue 创建时间不代表论文首发或 HF 推荐日。初审建议按 Harness 专项综述/理论收录。以视频模型外的 Harness 为分析单位，§2.3 显式区分产物、持久 Harness 和改进过程，§5.2 系统梳理 Harness 更新，§5.3.2 专门讨论 Harness 演化的预算控制、留出评估及跨轮程序对照。建议计入 Harness 专项综述/理论，绝不计入方法数量。

当前完成的是一手来源初审，待独立复审后记录最终处理；尚未据此声明已发布。原文：https://arxiv.org/abs/2610.40191

关闭条件：Complete independent comparison and record final scope result; for includes, verify real catalog/supplement artifact before claiming published.

## #19 KARMA

KARMA 对六类文本模块提供原子编辑，包含 role、output protocol 与 action descriptions，理论上可改执行指令/输出协议。但已展示的 Figure 5 修改集中于经验规则 E17–E19/E06–E07 等商业判断知识，周围执行代码与编辑算法固定。需区分真实协议/行为工件更新与领域规则手册更新。

待补证：提供一条实际接纳的 role、output protocol 或 action-description / 行为指令工件的旧版、补丁、新版、验证反馈及后续任务调用，区分程序性执行策略与广告领域知识规则。

原始 v1 复查：官方 v1 仍能证明六类模块可编辑、验证和回滚；展示的案例修改是经验/商业判断规则，未提供足以消除现有边界的具体协议工件修改。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核官方 v1 正文（Sections 3–4.6, A.3–A.5, B.1, D），继续暂缓，未据此计入 Harness 篇数。官方 v1 仍能证明六类模块可编辑、验证和回滚；展示的案例修改是经验/商业判断规则，未提供足以消除现有边界的具体协议工件修改。

需补证：提供一条实际接纳的 role、output protocol 或 action-description / 行为指令工件的旧版、补丁、新版、验证反馈及后续任务调用，区分程序性执行策略与广告领域知识规则。

原文：https://arxiv.org/html/2610.39884v1

关闭条件：Resolve the specific artifact ambiguity from primary-source implementation or appendix; neither accept nor reject solely to close the issue.

## #20 MoLRSI

MoLRSI 的搜索主循环以分子模型/科研 workflow 为产出，所谓 effective search policy 通过三类经验记忆更新，选择公式本身未改。正文另有资源技能的执行报错修复、验收和保留，不能简单归为只有经验；但尚不清楚这是一次工具构建验证，还是跨任务持续修改研究 Harness 的实际方法。

待补证：提供资源技能在持续使用后的旧版、执行失败、修订、准入和后续任务复用实例，证明其超出一次性的工具包装/依赖修复；科学模型、科研 workflow 和经验选择统计不自动等于研究 Agent 自己的 Harness 演化。

原始 v1 复查：v1 与先前 v2 判据处均描述首次使用验证、错误修复和保留，但主改进循环仍输出分子科研 workflow 并更新经验记忆。原版本未补上持续 Harness 工件演化实例。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核官方 v1 正文（Sections 2.1, 4.1 and S1.1–S1.3），继续暂缓，未据此计入 Harness 篇数。v1 与先前 v2 判据处均描述首次使用验证、错误修复和保留，但主改进循环仍输出分子科研 workflow 并更新经验记忆。原版本未补上持续 Harness 工件演化实例。

需补证：提供资源技能在持续使用后的旧版、执行失败、修订、准入和后续任务复用实例，证明其超出一次性的工具包装/依赖修复；科学模型、科研 workflow 和经验选择统计不自动等于研究 Agent 自己的 Harness 演化。

原文：https://arxiv.org/html/2610.39714v1

关闭条件：Resolve the specific artifact ambiguity from primary-source implementation or appendix; neither accept nor reject solely to close the issue.

## #21 RecRSI

修改推荐模型架构、损失、采样器及训练配方，探针反馈筛选外部训练算法；未修改推荐研究 Agent 自己的可复用推理 Harness。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核并复用与当前输入一致的一手来源范围审查，结论为不纳入当前 Harness 专题。修改推荐模型架构、损失、采样器及训练配方，探针反馈筛选外部训练算法；未修改推荐研究 Agent 自己的可复用推理 Harness。

这不否定它在通用 RSI 或其他方向的价值。仅记录范围排除，不将本项计为已发布 Harness。原文：https://arxiv.org/abs/2610.39352

关闭条件：Record source-backed exclusion and matching approval/adjudication in durable tracking before closing.

## #22 MetaVul

被修改对象是准备输入、引导检测并解析输出的独立 Python Harness；优化器读取先前 Harness、逐例预测、标签和指标后提出新版本，隔离检测器评估，最终保留 Pareto 版本并冻结用于未见数据/模型。符合外部可复用 Harness 的反馈演化。

已准备的短摘要：根据漏洞检测反馈迭代 Python Harness，保留候选并测留出与跨模型迁移。
Refines Python harnesses with vulnerability-detection feedback, retains candidates, and tests held-out data and cross-model transfer.

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已核对官方 v1 身份及正文。原发表日期为 2026-10-29；issue 创建时间不代表论文首发或 HF 推荐日。初审建议纳入 Harness 方法。被修改对象是准备输入、引导检测并解析输出的独立 Python Harness；优化器读取先前 Harness、逐例预测、标签和指标后提出新版本，隔离检测器评估，最终保留 Pareto 版本并冻结用于未见数据/模型。符合外部可复用 Harness 的反馈演化。

当前完成的是一手来源初审，待独立复审后记录最终处理；尚未据此声明已发布。原文：https://arxiv.org/abs/2610.40721

关闭条件：Complete independent comparison and record final scope result; for includes, verify real catalog/supplement artifact before claiming published.

## #23 VEvo-Harness

两位审查者对工件语义仍不同，保留 boundary 并等补证，不能把本人的 include 候选当作已达成共识的正例。

待补证：提供一条 skill 的字段结构、旧版/patch/新版、双臂准入反馈及后续任务调用，核实变化是生成策略指令而不只是成功 prompt、记忆文本、语义嵌入或评分统计。

原始 v1 复查：v1 同样声明可执行技能、因果 patch、跨任务保留，并写明策略嵌入合并及指令片段保护；未展示可消除两位前审分歧的具体技能工件。原始版本不能使 unknown 自动升级为 include。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核官方 v1 正文（Sections 3.1–3.5 and 4.3），继续暂缓，未据此计入 Harness 篇数。v1 同样声明可执行技能、因果 patch、跨任务保留，并写明策略嵌入合并及指令片段保护；未展示可消除两位前审分歧的具体技能工件。原始版本不能使 unknown 自动升级为 include。

需补证：提供一条 skill 的字段结构、旧版/patch/新版、双臂准入反馈及后续任务调用，核实变化是生成策略指令而不只是成功 prompt、记忆文本、语义嵌入或评分统计。

原文：https://arxiv.org/html/2610.39158v1

关闭条件：Resolve the specific artifact ambiguity from primary-source implementation or appendix; neither accept nor reject solely to close the issue.

## #24 From Grind to Grasp

研究工作量、信息、个人与集体递归改进的广义理论，非专门研究 Harness 程序演化。范围排除不以理论论文没有运行闭环为理由。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核并复用与当前输入一致的一手来源范围审查，结论为不纳入当前 Harness 专题。研究工作量、信息、个人与集体递归改进的广义理论，非专门研究 Harness 程序演化。范围排除不以理论论文没有运行闭环为理由。

这不否定它在通用 RSI 或其他方向的价值。仅记录范围排除，不将本项计为已发布 Harness。原文：https://arxiv.org/abs/2610.38728

关闭条件：Record source-backed exclusion and matching approval/adjudication in durable tracking before closing.

## #25 SceneEvolve

围绕冻结学生更新可复用的场景重建 Harness；开发集重建执行/评分反馈决定保留，最终冻结用于未见场景。不是把每个场景的输出代码等同于 Harness。

已准备的短摘要：按重建反馈演化冻结模型外的工具和复用例程，最终 Harness 用于未见场景。
Evolves tools and reusable routines around a frozen model from reconstruction feedback, then applies the final harness to unseen scenes.

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核并复用与当前输入一致的收录意见。围绕冻结学生更新可复用的场景重建 Harness；开发集重建执行/评分反馈决定保留，最终冻结用于未见场景。不是把每个场景的输出代码等同于 Harness。

本项应归入历史来源补录；原发表/版本日期保留，不混作今天的新论文。范围批准已有记录；实际页面发布完成后再附公开链接。原文：https://arxiv.org/abs/2610.37046

关闭条件：Verify a real public catalog/supplement/page before claiming publication.

## #26 RuHarness

冻结模型，对六个外部 Harness 功能坐标进行更新；执行轨迹形成并重估 rubric，候选通过验证阈值后进入下一轮。

已准备的短摘要：从执行轨迹更新评分准则并指导可复用 Harness 修订，验证后保留。
Updates rubrics from execution traces to guide reusable harness revisions retained after validation.

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核并复用与当前输入一致的收录意见。冻结模型，对六个外部 Harness 功能坐标进行更新；执行轨迹形成并重估 rubric，候选通过验证阈值后进入下一轮。

本项应归入历史来源补录；原发表/版本日期保留，不混作今天的新论文。范围批准已有记录；实际页面发布完成后再附公开链接。原文：https://arxiv.org/abs/2610.36826

关闭条件：Verify a real public catalog/supplement/page before claiming publication.

## #27 Training for Alignment

主从博弈中的训练与内生偏好更新理论，研究训练状态、过度/不足纠偏和泛化；AI 后训练及 RSI 只是应用语境。未专门研究外部 Harness 工件的反馈修改与保留，故不计入当前 Harness 专题。

已准备的短摘要：用主从模型分析偏好对齐训练及对未训练状态的泛化。
Analyzes preference-alignment training and generalization to untrained states in a principal-agent model.

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已核对官方 v1 身份及正文。原发表日期为 2026-10-26；issue 创建时间不代表论文首发或 HF 推荐日。初审建议排除当前 Harness 专题。主从博弈中的训练与内生偏好更新理论，研究训练状态、过度/不足纠偏和泛化；AI 后训练及 RSI 只是应用语境。未专门研究外部 Harness 工件的反馈修改与保留，故不计入当前 Harness 专题。

当前完成的是一手来源初审，待独立复审后记录最终处理；尚未据此声明已发布。原文：https://arxiv.org/abs/2610.40684

关闭条件：Complete independent comparison and record final scope result; for includes, verify real catalog/supplement artifact before claiming published.

## #28 The Trinity

冻结模型外六类协议模块根据成功/失败轨迹修订，验证版本继承并合入下一轮 Base Harness；能力树拓扑固定，评测技能另行准备，不宣称局部接纳都要求分数提高。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核并复用与当前输入一致的收录意见。冻结模型外六类协议模块根据成功/失败轨迹修订，验证版本继承并合入下一轮 Base Harness；能力树拓扑固定，评测技能另行准备，不宣称局部接纳都要求分数提高。

本项应归入HF 2026-10-28 推荐日；原发表/版本日期保留，不混作今天的新论文。范围批准已有记录；实际页面发布完成后再附公开链接。原文：https://arxiv.org/abs/2610.36077

关闭条件：Verify a real public catalog/supplement/page before claiming publication.

## #29 Work Agents

工作 Agent 的广义系统分类与综述，同时讨论模型、Harness 及联合优化；其研究对象是工作系统整体，非 Harness 演化专项。复用既有范围裁决，不把原模型的 defer 伪装为模型给过 exclude。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核并复用与当前输入一致的一手来源范围审查，结论为不纳入当前 Harness 专题。工作 Agent 的广义系统分类与综述，同时讨论模型、Harness 及联合优化；其研究对象是工作系统整体，非 Harness 演化专项。复用既有范围裁决，不把原模型的 defer 伪装为模型给过 exclude。

这不否定它在通用 RSI 或其他方向的价值。仅记录范围排除，不将本项计为已发布 Harness。原文：https://arxiv.org/abs/2610.35845

关闭条件：Record source-backed exclusion and matching approval/adjudication in durable tracking before closing.

## #30 OmniBrain-0

Section 5.1–5.2 明确冻结参数验证提醒、反馈修订并跨轮保留，不能用权重为主排除。但当前证据尚不能区分提醒策略工件改写与固定提醒器中的规则内容积累，官方代码仍未公开；两组最终均保留边界。

待补证：提供 reminder policy / rubric 的实际旧版、修订及后续调用，区分可复用执行策略工件更新与固定提醒器中规则/提醒内容积累。存在权重训练不是否定局部 Harness 更新的理由。

原始 v1 复查：v1 正文明示固定参数下验证、反馈修订和跨轮保留提醒；仍未提供可消除现有策略工件/内容边界的实例。摘要差异仅是 canonical 的 teachers’ 后漏一个空格，没有科学内容或版本差异。

建议 issue 回复（当前状态下可用；发布后另补实际链接）：

已复核官方 v1 正文（Sections 5.1–5.2, 6.3, and RSI model configuration），继续暂缓，未据此计入 Harness 篇数。v1 正文明示固定参数下验证、反馈修订和跨轮保留提醒；仍未提供可消除现有策略工件/内容边界的实例。摘要差异仅是 canonical 的 teachers’ 后漏一个空格，没有科学内容或版本差异。

需补证：提供 reminder policy / rubric 的实际旧版、修订及后续调用，区分可复用执行策略工件更新与固定提醒器中规则/提醒内容积累。存在权重训练不是否定局部 Harness 更新的理由。

原文：https://arxiv.org/html/2610.36013v1

关闭条件：Resolve the specific artifact ambiguity from primary-source implementation or appendix; neither accept nor reject solely to close the issue.


## 历史候选条目已备好

`historical-catalog-candidates.yaml` 提供 #25 SceneEvolve 与 #26 RuHarness 的可直接追加目录行；原发表日均为 2026-10-27，`section: candidates`、`status: candidate`、`needs_reading: true`，全部证据值 unknown。短双语摘要不含新增成绩数字，并保留来源审查、输入 hash 和既有批准回执的绑定；未写入 canonical 或日报。两行均通过当前 papers schema 校验。
