# 11 月 2 日 HF 后补四篇：正文范围初审

审核于 2026-11-03；本轮只读本地保存的官方摘要页和 v1 HTML，新增联网请求与付费模型调用均为 0。建议 **Harness 纳入 2、排除本专题 2、边界 0**，四篇正式决定均为 `defer`。这是正文初审，仍需独立第三轮及 owner 审核；既有质量门 recall 0.8571 < 0.90、付费暂停和发布闸门均保持。

HF 归期 2026-11-02 来自本次后补采集任务，本子任务没有重新查 HF 榜。原发表日期及 v1 时间从官方 arXiv 摘要页逐篇核对；不能把 10 月原发表日改写成 11 月 2 日新发表。

| 论文 | 原发表日（UTC） | 当前专题建议 | 方向 / 边界 |
| --- | --- | --- | --- |
| MemSteer · 2610.39276 | 2026-10-29 · v1 | include；正式 defer | harness / component |
| REA · 2610.42053 | 2026-10-30 · v1 | exclude；正式 defer | embodied |
| SketchDirector · 2610.41260 | 2026-10-30 · v1 | exclude；正式 defer | experience_world_model |
| GEPA-Curator · 2610.37651 | 2026-10-27 · v1 | include；正式 defer | harness / evidence_selection |

## MemSteer

MemSteer-Opt 修改存储、检索与上下文构建的可复用记忆设计；用执行失败诊断提出下一版，以验证集表现决定接受，接受后的设计继续用于下一轮，并有冻结设计迁移到新基准与新用户的直接描述。收录依据是设计优化器，不是单纯生成 QA 或修补记忆条目。

§3.3 明确只在候选验证准确率严格高于当前设计时替换，否则保留当前设计；接受后重新运行训练题形成下一轮反馈。§4.3 将冻结的设计用于其他基准和原来源用户集合外的新用户。这里仅核对准入与复用机制，没有重新计算性能。

合成 QA–证据本身是监督数据，不能单靠它归为 Harness。正文另有 MemSteer-Opt 的存储/检索/上下文机制改写；不是只增加事实记忆。新用户继续优化和跨基准结果有边界，不能从这些段落推广为普遍泛化或同预算优势。

原始版本时间：`2026-10-29T03:28:49Z`。来源：[官方摘要](https://arxiv.org/abs/2610.39276) · [v1 正文](https://arxiv.org/html/2610.39276v1)。

正文证据（仅折叠空白，保留原句）：

- [3.3 MemSteer-Opt: evidence-guided memory-design optimization](https://arxiv.org/html/2610.39276v1#S3.SS3) · 改的是存储、检索、上下文构建设计，而不只是记忆数据。

  > Starting from a basic memory system, MemSteer-Opt iteratively optimizes how historical records are organized into memory units and indexed, how relevant records are retrieved, and how retrieved records are assembled into the context supplied to the answerer.

- [3.3 MemSteer-Opt: evidence-guided memory-design optimization](https://arxiv.org/html/2610.39276v1#S3.SS3) · 从回答失败及来源证据诊断管理机制的问题。

  > For each incorrect training-set response, we use its evidence annotations to check whether the required source records and cited passages are fully available in the final answer context.

- [3.3 MemSteer-Opt: evidence-guided memory-design optimization](https://arxiv.org/html/2610.39276v1#S3.SS3) · 接受的设计留到下一轮执行和改进。

  > After accepting a revision, we rerun the updated system on the training set to refresh the failure diagnoses and sampled feedback for the next iteration.

- [4.3 Can Optimized Memory Designs Transfer and Adapt?](https://arxiv.org/html/2610.39276v1#S4.SS3) · 改过的设计跨基准复用，区别于同题反复修答案。

  > We freeze the design optimized with generated ATM-Bench QA and apply it to RHELM records without target-domain optimization.

- [4.3 Can Optimized Memory Designs Transfer and Adapt?](https://arxiv.org/html/2610.39276v1#S4.SS3) · 来源用户集合之外直接复用冻结设计；原文人数不作重新计算。

  > We apply a frozen design optimized on six RHELM users to Martin Keller and David R. Ellis, who are excluded from the source-user pool.

- [3.3 MemSteer-Opt: evidence-guided memory-design optimization](https://arxiv.org/html/2610.39276v1#S3.SS3) · 回答模型和其提示保持固定，搜索对象是记忆设计。

  > We hold the answering model, its instruction prompt, and the final context budget fixed across designs.

- [Abstract](https://arxiv.org/html/2610.39276v1) · 摘要明确不更新模型参数。

  > To study the utility of this supervision, we develop MemSteer-Opt, which combines QA-based design evaluation with evidence-guided failure diagnosis to revise memory store, retrieval, and context construction without updating model parameters.

正文 SHA-256：`0d8cd88205828a71c5b83e69a324683a91ae551a2493f3099326a4010302d988`。

未扩展为代码复现、完整实验/费用复核或证据卡数字更新；相应未知项保留在 JSON 中。

## REA

核心贡献是固定的异步具身 runtime、预先测量的路由表和边界触发恢复机制。执行反馈用于当前 episode 的停止或换策略；开发集成功率用于预先选策略。所核查方法未给出 REA 自身根据执行反馈改写并保留 Harness 工件的闭环。

路由记忆保存开发集成功率和成本，测试分发是查表；正文明确共享的策略代码、路由记忆与 judge 阈值在评测前固定。冻结策略跨 episode 复用存在，但这不等于 Harness 被持续改写。

不能仅因含 VLA 或训练 selector 就排除。已专门核对 ASPIRE Fix/Evo：它们是 System 2 候选程序的外部生成方法和对照来源，不能把其演化能力直接算作 REA runtime 的自演化。论文评价不同具身策略及路由/判断位置，不是专门研究 Harness 工件反馈演化的评测；固定评测框架本身并非排除理由。若后续出现 REA 原生持久改写工具/控制流的新证据，应重审。

原始版本时间：`2026-10-30T17:18:13Z`。来源：[官方摘要](https://arxiv.org/abs/2610.42053) · [v1 正文](https://arxiv.org/html/2610.42053v1)。

正文证据（仅折叠空白，保留原句）：

- [Route memory: dispatch without the brain.](https://arxiv.org/html/2610.42053v1#S3.SS2.SSS0.Px1) · 开发数据形成表，测试时查表，不是在线改写路由器。

  > at test time dispatch is a lookup (the route table of Figure 1 ).

- [3.3 Aligned Evaluation Protocol](https://arxiv.org/html/2610.42053v1#S3.SS3) · 路由记忆和准入阈值在评测前固定。

  > Route memories and judge thresholds are fixed on development episodes before evaluation.

- [REA variants.](https://arxiv.org/html/2610.42053v1#S3.SS0.SSS0.Px1) · 实验变化是选择和恢复机制。

  > REA denotes the shared runtime. Its three variants in experiments differ in policy selection and recovery, see details in Algorithms 1 and B.1 :

- [System 2 policy-generation methods.](https://arxiv.org/html/2610.42053v1#S4.SS1.SSS0.Px2) · 确认论文确实使用外部修复/搜索方法，不能漏读后直接说没有任何演化。

  > ASPIRE Fix loop and Evo search [ 2 ] ; Codex + GPT-6 and Agents SDK + GPT-6, coding-agent pipelines generating one program per task; and zero-shot GPT-6, two samples per task.

- [One interface, different selectors.](https://arxiv.org/html/2610.42053v1#S5.SS0.SSS0.Px2) · 另一个 selector 变体是在当前 episode 固定选择，也未建立持久 Harness 修改。

  > In the RoboTwin 2.0 extension, a learned selector chooses one of seven VLAs or a Python policy from the initial observation and keeps that choice fixed throughout the episode ( Section 4.6 , Section C.1 ).

- [1 Introduction](https://arxiv.org/html/2610.42053v1#S1) · 评测对象涵盖通用具身策略，不能据此认定 Harness RSI 专项评测。

  > REA also provides a unified evaluation framework for any policies including code-as-policies and VLAs.

正文 SHA-256：`a42c5017117a562674ace6f8837fc96a01a984adfbcf9c010d771216b3d95bbf`。

未扩展为代码复现、完整实验/费用复核或证据卡数字更新；相应未知项保留在 JSON 中。

## SketchDirector

短期反思用于修改当前场景的布局程序，长期部分增量保存并检索成功布局经验。跨场景复用明确存在，但保留对象是经验条目/图像任务产物，未证明反馈重写操作库、记忆检索机制或其他 Harness 工件；应放经验与记忆相关方向，不计 Harness。

几何和视觉语义校验决定当前布局是否接受；失败轨迹在当前场景成功后丢弃。长期成功经验按对象集合保存，以既定 Jaccard 相似度检索到新场景，属于数据复用。

不能用 not_persistent 排除整个方法，因为长期经验确实跨场景。也不能把 executable scene program 当成工具实现或技能文件：它由预定义 move/scale/rotate/layer/delete/modify 原语生成，修改目标是画布布局，不是这些操作的实现或长期控制规则。

原始版本时间：`2026-10-30T05:05:12Z`。来源：[官方摘要](https://arxiv.org/abs/2610.41260) · [v1 正文](https://arxiv.org/html/2610.41260v1)。

正文证据（仅折叠空白，保留原句）：

- [3.2 Operating Action Library](https://arxiv.org/html/2610.41260v1#S3.SS2) · 操作库是框架定义的动作空间，生成的是场景动作序列。

  > To support interpretable and executable scene composition, we define a compact set of object-level operation codes that serve as the action space of the reasoning agent.

- [3.3 Agentic Layout Reasoning](https://arxiv.org/html/2610.41260v1#S3.SS3) · 被编辑的是物体属性与场景状态。

  > The generated operations are sequentially executed to update object attributes and scene states, producing an explicit and traceable composition trajectory, as illustrated in Fig. 5 .

- [3.3 Agentic Layout Reasoning](https://arxiv.org/html/2610.41260v1#S3.SS3) · 准入对象是当前布局，反馈进入下一轮场景修正。

  > Only layouts satisfying all verification criteria are accepted. Otherwise, the detected violations and verification feedback are recorded and sent to the self-evolving correction module.

- [3.3 Agentic Layout Reasoning](https://arxiv.org/html/2610.41260v1#S3.SS3) · 短期失败记忆仅服务本场景，成功后丢弃。

  > These records are discarded after successful correction and are only used within the current scene generation process.

- [3.3 Agentic Layout Reasoning](https://arxiv.org/html/2610.41260v1#S3.SS3) · 长期对象是成功经验条目，不是检索/管理策略的代码。

  > The Long-Term Experience Memory stores successful layout experiences indexed by the corresponding object set.

- [3.3 Agentic Layout Reasoning](https://arxiv.org/html/2610.41260v1#S3.SS3) · 确实有跨场景复用；据此分到经验方向而非简单说无持续性。

  > Long-Term Experience Memory transfers successful cross-scene trajectories into reusable experiences, which are incrementally stored and retrieved to improve subsequent layout planning and program generation.

正文 SHA-256：`0ec4979609f2eac3106b405a10f0703c84ca4a051a96bcbd4adf902efcb840a6`。

未扩展为代码复现、完整实验/费用复核或证据卡数字更新；相应未知项保留在 JSON 中。

## GEPA-Curator

任务筛选和历史成功轨迹选择服务于反思式 prompt 演化。执行轨迹与评价驱动新 prompt，修改在单谱系 checkpoint 中持续使用，最终由验证集选取版本；§5.3 还给出同一策展机制接到 Harness 代码改写的具体实现。

正文的 GEPA-Curator 是移除 Pareto 选择的 greedy 变体：每次 mutation 成为下一 checkpoint，并定期在验证集评估、最终选最好版本。不能套用原始 GEPA 的逐步拒绝退化规则。Meta-Harness-Curator 则评估 child 与 parent 以及完整开发集，用开发集最优版本做最终测试。

Curator 自身代码保持不变、轨迹历史只是优化器输入，不足以单独证明改进器自我进化；但其驱动的长期 prompt/Harness 代码演化是明确的，所以不因策展器固定就排除，也不误归 improver。这里的训练任务选择服务于外部程序优化，不是训练模型权重的数据课程。

原始版本时间：`2026-10-27T17:58:11Z`。来源：[官方摘要](https://arxiv.org/abs/2610.37651) · [v1 正文](https://arxiv.org/html/2610.37651v1)。

正文证据（仅折叠空白，保留原句）：

- [3 GEPA-Curator Methodology](https://arxiv.org/html/2610.37651v1#S3) · 执行和评价生成下一版 prompt。

  > It executes the tasks using an actor agent conditioned on the prompt and returns an updated prompt, task-level agent trajectories, and evaluation results (See Figure 1 ).

- [3.2 Prior Success Retrieval](https://arxiv.org/html/2610.37651v1#S3.SS2) · 明确 prompt 修改由失败轨迹和评价驱动。

  > Normally, prompt optimizers reflect on failure examples in the current minibatch and mutate the prompt based only on the failed trajectories and their evaluations.

- [4.1 Experimental Setup](https://arxiv.org/html/2610.37651v1#S4.SS1) · 新 prompt 沉淀到后续优化轮次，而非只修当前答案。

  > Rather than evolving a candidate pool and sampling from the Pareto frontier on validation set, GEPA-Curator maintains a single lineage in which each mutation becomes the next checkpoint.

- [4.1 Experimental Setup](https://arxiv.org/html/2610.37651v1#S4.SS1) · 记录作者的最终版本选择协议，不重算迭代数或实验结果。

  > We evaluate the prompt every 16 iterations unless specified on a held-out validation set and select the final model based on the best validation score at the end.

- [3 GEPA-Curator Methodology](https://arxiv.org/html/2610.37651v1#S3) · 策展器提供上下文，不等于优化器自己改写自己。

  > Note that these trajectories are provided to the prompt optimizer only as additional input metadata, leaving the optimizer itself unchanged.

- [5.3 Meta-Harness-Curator](https://arxiv.org/html/2610.37651v1#S5.SS3) · §5.3 另有具体 Harness 代码父子版本更新。

  > The parent is freshly executed on these tasks, and the optimizer revises it using the resulting feedback and the Curator’s rationale.

- [5.3 Meta-Harness-Curator](https://arxiv.org/html/2610.37651v1#S5.SS3) · 代码候选由开发集选择后用于测试，支持持久程序版本而不是单次产物。

  > Training and development executions count toward the search budget, and the candidate with the highest development score is selected for final test evaluation.

正文 SHA-256：`1ee335bb4ef74898a3e7f518fd05d4c3b51a532de3437cef1000c9e9049af8de`。

未扩展为代码复现、完整实验/费用复核或证据卡数字更新；相应未知项保留在 JSON 中。

四篇共 26 处引句已逐条与指定官方 HTML 章节及保存的文本精确匹配（仅折叠空白）。输入文件、SHA-256、HTTP 200 采集回执、分类边界和待第三轮状态见 [结构化记录](late-hf-primary-review.json)。
