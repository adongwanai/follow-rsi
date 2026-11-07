# 11/04 初审A：11/03 HF推荐

20条：4条方法正文范围核查、1条原意见复用、15条摘要初筛。NorthCUA由另一位审查者处理。没有付费模型调用，没有批准或发布。

| ID | 范围建议 | 核查层次 | 理由 |
| --- | --- | --- | --- |
| arxiv:2611.01860 | exclude | hf_original_abstract_screen | 图形学 Agent 与文献系统的一般综述，反馈主要用于生成和修订图形代码产物；摘要未提出 Harness 演化专项方法、理论或评测。 |
| arxiv:2611.00859 | exclude | hf_original_abstract_screen | 联合设计视频生成训练与固定并行运行时，优化视频模型和执行效率；没有提出运行程序经反馈自改并跨任务继承。 |
| arxiv:2611.03126 | exclude | primary_method_sections_scope_review | 方法2.2、2.4、2.5的反馈闭环用于引导下一轮数据采集、合成任务和SFT/RL训练；可复用primitives用于组成训练任务，snapshot回滚保留同一任务的成功轨迹，未展示Agent自身运行Harness经反馈迭代继承。 |
| arxiv:2611.03178 | exclude | primary_method_sections_scope_review | 正文承认模型与Harness共同演化的重要性，但已报告闭环是CoworkOS控制GLM教师与外部Qwen训练目标，依据评测修改数据配方、示范与训练计划；工作区和记忆保持运行连续性，不构成已证实的CoworkOS自身运行规则演化。归通用Agent系统/自动模型研发。 |
| arxiv:2610.40191 | include | reuse_unchanged_abstract_and_prior_primary_review | 本轮仅新增11/03 HF成员身份，原摘要与已存条目一致；复用已核实的Harness专项报告范围意见，当前质量闸门仍阻止正式接受与出版。 |
| arxiv:2611.01560 | exclude | hf_original_abstract_screen | 提出支持开放模型训练的统一机器人Harness并比较模型能力；摘要没有运行Harness根据执行反馈自动修订和跨任务保留的机制。 |
| arxiv:2611.02074 | exclude | primary_method_sections_scope_review | 正文3.1从同一issue的历史编译detectors并做admission检查，固定后服务该issue的采样轮；第6节明确跨轮更新history和跨issue分配仍为未来工作。历史引导训练轨迹采集不能直接记作跨任务Harness自进化。 |
| arxiv:2611.02897 | exclude | hf_original_abstract_screen | 研究图像裁剪、全景取景与解释的学习型评分器，改进对象为视觉模型及图片产物。 |
| arxiv:2610.27954 | exclude | hf_original_abstract_screen | ReTrace评测执行中的故障恢复能力，属于一般Computer-use可靠性评测；摘要没有把Harness版本演化作为研究对象。 |
| arxiv:2611.03424 | exclude | hf_original_abstract_screen | 比较AI科研提案与人类后续研究的选题品味，属于AI研发能力评测，非Harness演化专项。 |
| arxiv:2611.02112 | exclude | hf_original_abstract_screen | 通过教师token排序训练学生模型，直接优化权重与蒸馏目标。 |
| arxiv:2611.03602 | exclude | hf_original_abstract_screen | 验证与教师修订用于生成训练轨迹，GRPO训练观察策略；对当前视频改计划是任务内推理，未展示外部程序反馈修订后跨任务保留。 |
| arxiv:2611.00172 | exclude | hf_original_abstract_screen | 多模态嵌入表征的综述和立场，研究对象是表征覆盖、对齐与组合性。 |
| arxiv:2611.01815 | exclude | hf_original_abstract_screen | 评估视频世界模型表征及预测误差能否测量物理惊讶，非Harness程序演化理论或评测。 |
| arxiv:2611.01484 | exclude | hf_original_abstract_screen | 跨仓协同开发任务基准评估编码Agent的任务能力，未把Harness自进化/版本继承作为评估对象。 |
| arxiv:2610.39419 | exclude | hf_original_abstract_screen | 固定视觉编号等外部参照的配对消融评测；training-free视觉技能并不自动意味着技能按反馈迭代和继承。 |
| arxiv:2611.03344 | exclude | hf_original_abstract_screen | 提出Blackwell注意力训练kernel与量化调度设计，优化对象是模型训练的算子实现。 |
| arxiv:2611.03092 | exclude | primary_method_sections_scope_review | 第4.2节明确提出跨episode的用户情境Rehearsal Engineering，更新记忆、技能选择和决策策略，不能说它没有反馈演化；全文主题仍是个人Agent个性化、授权与监督的一般议程，不是Harness演化专项。建议留为通用RSI相关理论。 |
| arxiv:2610.42128 | exclude | hf_original_abstract_screen | 从生成教师向决策排序模型进行on-policy蒸馏，优化对象是reranker模型权重。 |
| arxiv:2611.02633 | exclude | hf_original_abstract_screen | 评测AI作为团队成员的协作能力，虽有留出任务但不是Harness版本演化的专项基准。 |

正文引句、官方身份/日期、可核验定位与内容哈希见同名JSON。未知证据保持unknown；本报告是范围核查，不是实验复现。
