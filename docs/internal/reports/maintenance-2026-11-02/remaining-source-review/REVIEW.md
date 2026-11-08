# 2026-11-02：15 项剩余来源与分类边界复核

本文件是主审建议，不是第三轮独立复审或人工批准。所有 formal_decision=defer，未改规范记录、证据等级、论文数字或发布内容。

15/15 留下处理结果：4 项排除建议、4 项边界待裁定、7 项外部来源阻塞；本轮没有新增直接纳入建议。

新增补证：结构软件 Agent 通过 Crossref 的官方补充仓库取得作者介绍；Self-generated goals 通过双向 DOI 关系取得官方预印本摘要。IEEE 三页编辑短文也重新读取全文。

| 条目 | 建议 | 原因 / 待补证 |
| --- | --- | --- |
| SkillMem: Compact External Skill Memory for Latent Multi-Agent Reasoning | exclude | 主要训练对象是潜在技能向量和 reader 投影。4.4/A 将文字技能发现定义为固定校准集的提取、过滤和去重，随后做行为蒸馏；不能把冻结 backbone 视为无权重训练。  |
| A Case Study of a Multi-Agent Kernel-Optimization Loop That Learns a New AI Accelerator | unknown | 主体改进外部 NPU kernel 与编译知识；正文记载 beam 改 single-head，但自动修改 loop 的归因链不清。作者仓库明确不公开编排代码与运行记录。 需要 loop 工件变更、提出者/执行反馈/准入记录及后续复用证据；公开 prompts 和“Agent 写过全部代码”不能替代自主反馈演化证据。 |
| VEvo-Harness: Causally-Guarded Self-Evolving Harness for Agentic Image Generation | unknown | v2 明说持久、可路由可执行技能与因果 patch 准入；但具体操作仍为语义嵌入合并、预防策略/记忆规则、Q 统计，技能工件格式与可执行修改未展示清楚。 需要官方完整附录或实现中的可编辑技能工件格式、一次真实更新/准入及后续执行样例，区分持久策略工件与记忆规则内容。 |
| MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery | unknown | 主循环更新分子科研工作流与三类记忆；MCTS 家族/父节点选择公式读取这些记忆。技能执行修复并保留确有正证，但主对照隔离历史经验，不能把主增益直接归为 Harness 演化。 需要把辅助技能修复与主科研工作流/模型训练贡献分开，并给出被实测的 Agent 自身 Harness 工件变更与复用证据；维持 owner 范围裁定。 |
| KARMA: Training-Free Knowledge-Atomic Harness Evolution for Industrial Advertising Agents | unknown | 六类目录能原子改写 prompt/协议/动作描述并验证保留，固定代码并非排除理由；但 Figure 5 展示的已接纳修改均标 experience 规则，尚未证明实验实际更新了独立 Harness 策略工件。 需要已接纳 role/output_protocol/action_descriptions 变更日志，或对 experience 决策规则是否构成 Harness 策略文件的 owner 裁定；接口支持不等于实测修改。 |
| From observation to generation: A complex-systems perspective on generative Human–AI social systems | unknown | 已核对 DOI/题名身份；Crossref 无摘要，出版社返回元数据而无摘要/正文，ScienceDirect 403。不能按标题判为 Harness 或直接排除。 可公开访问的官方摘要/正文或作者认可的预印本；在此之前分类和证据字段保持 unknown。 |
| Mechanism design meets large language models: Foundations and frontiers | unknown | 已核对 DOI/题名身份；Crossref 无摘要，出版社返回元数据而无摘要/正文，ScienceDirect 403。不能按标题判为 Harness 或直接排除。 可公开访问的官方摘要/正文或作者认可的预印本；在此之前分类和证据字段保持 unknown。 |
| Artificial intelligence design agent for automated operation of structural software using knowledge graphs and numerical models | exclude | Crossref 关联的作者补充仓库介绍的是固定多 Agent 框架把自然语言变成 ETABS 任务操作；作者明确提供的是生成脚本等任务产物，非规划/检索/调试 Agent 的实现。未见以自身 Harness 反馈演化为研究对象。  |
| From world model capability to continued play intention: The mediating role of perceived NPC intelligence and the moderating role of anthropomorphism | unknown | 已核对 DOI/题名身份；Crossref 无摘要，出版社返回元数据而无摘要/正文，ScienceDirect 403。不能按标题判为 Harness 或直接排除。 可公开访问的官方摘要/正文或作者认可的预印本；在此之前分类和证据字段保持 unknown。 |
| Liability for rogue behaviors of agentic AI | unknown | 已核对 DOI/题名身份；Crossref 无摘要，出版社返回元数据而无摘要/正文，ScienceDirect 403。不能按标题判为 Harness 或直接排除。 可公开访问的官方摘要/正文或作者认可的预印本；在此之前分类和证据字段保持 unknown。 |
| Agents Act. Who Decides? [Editor's Remarks] | exclude | 完整三页编辑短文讨论生成模型、搜索/优化、能耗与信任的广义代理研究议程；未专门研究外部 Harness 工件的反馈演化。  |
| Self-generated goals in the age of foundation models: artificial autotelic agents and their implications for cognitive science | exclude | 正式刊文与官方预印本通过 Crossref 双向关系连接；预印本摘要研究自主目标生成及认知科学/人类主体性，不是 Harness 工件反馈演化专项综述。  |
| Agentic AI: Philosophical, Technical, Psychological, and Marketplace Perspectives on Delegated Agency | unknown | 已核对 DOI/题名身份；Crossref 无摘要，出版社返回元数据而无摘要/正文，ScienceDirect 403。不能按标题判为 Harness 或直接排除。 可公开访问的官方摘要/正文或作者认可的预印本；在此之前分类和证据字段保持 unknown。 |
| Musubito: Deterministic Execution Lineage for AI-Enabled Python Workflows | unknown | 已核对 DOI/题名身份；Crossref 无摘要，出版社返回元数据而无摘要/正文，ScienceDirect 403。不能按标题判为 Harness 或直接排除。 可公开访问的官方摘要/正文或作者认可的预印本；在此之前分类和证据字段保持 unknown。 |
| Giving stateless agents a sense of time: A reconsolidating episodic–semantic memory architecture | unknown | 已核对 DOI/题名身份；Crossref 无摘要，出版社返回元数据而无摘要/正文，ScienceDirect 403。不能按标题判为 Harness 或直接排除。 可公开访问的官方摘要/正文或作者认可的预印本；在此之前分类和证据字段保持 unknown。 |

数据问题仅报告：

- VEvo-Harness 和 MoLRSI 官方已为 v2（2026-10-30）；输入规范记录仍为 v1。已读今日 v2 正文，但未改规范日期。
- Publisher 的明确在线日期：Mechanism design 为 10-07、Delegated Agency 为 10-26；IEEE PDF current version 为 10-08。它们不同于目前月首占位式刊期。
- Musubito 官方 Crossref 刊期为 2027-02，三篇仍列 2026-12；刊期不得当成今天 HF 推荐日。
- SkillMem、Kernel、KARMA 正文 raw SHA 与历史相同；既有异议完整保留。KARMA 图 5 实际修改均为 experience，不能用“接口允许编辑协议”冒充实验已修改协议。

验证与边界：逐条原文引句和来源 SHA256 见 validation.json；7 项未知不是仅凭标题排除。读到的作者 README、预印本摘要与出版社全文边界逐条标注。未调用付费模型或 Semantic Scholar，未提交 Git。
