# 2026-11-05 S2 新发现候选：摘要、关键正文与续跑

本批 82 个唯一 ID 来自今日 S2 的 30 日窗口，是新发现候选；不要计为昨日旧来源的漏抓。规范库比对冻结在 `fa7a628a1a1c720c130159943249979e08e0c0c9`。

完整阅读 76 条提供的 S2 摘要，初判 18 include、43 exclude、15 borderline 原样保留。补读全部 33 个正例/边界的关键正文后，76 项当前为 28 include、47 exclude、1 borderline。另 6 项复用今日 HF 已有主审和独立意见（3 include、3 exclude），82 项合计 31 include、50 exclude、1 borderline。所有词均是范围建议，正式决定保持 defer，新增批准、付费调用、生产写入和发布均为 0。

主审本人完成 33 项官方正文关键章节选读，记录 174 条精确原文摘句、段落上下文、位置与来源哈希，未声称通篇阅读、数值审计或实验复现。其余 43 个新增排除项仍为完整摘要阅读。个人正文记录先写，再与独立冻结证据逐 ID 对照，33 项中 32 项建议一致、1 项分歧保留。独立报告另含 6 个摘要排除抽查；其余 37 项没有独立初筛，不能把抽查写成全量独立复审。

身份及日期：75 个独立 S2 arXiv 候选与 6 个 HF 重叠项均有官方身份、v1 和版本历史证据；PRISM 的 DOI、题名和 2026-10-31 发表日由出版社核验，原提交日、论文版本和修订日仍未知。网页 modified time 不是论文修订日。

7 条 S2/官方摘要差异均已逐项比较，仅为空格差异，未发现范围影响。6 项 HF 复用中 2 条摘要字节完全相同；4 条分别为 textbf/emph、货币符号、乘号 LaTeX 格式差异，当前 S2 文本与官方摘要完全一致。两套哈希均保留，不把旧回执重绑到新文本。

范围按工件、反馈、后续保留判断，程序性指令/技能文档不必是独立可执行源码。WASP-Mem依据认证、分页/错误恢复程序页修订及下一轮消费证据由个人正文初判 borderline 调整为 include；初判和解释仍保留，未声称审计过原始wiki补丁。ModelBlaster保留主审 exclude / 独立 borderline：争点是条件化优化claims是否已是Agent自身程序策略。CogniLife双方均 borderline：概念相关，但实现的staging-to-active路径未闭合。

模型训练为主要贡献不会自动排除真实 Harness 演化。CARE排除基于正文明确Harness由业务owner/工程师修改且不属于循环步骤；RSI-Env已确认真实交替更新。RSI-Dojo仍只有官方摘要证据，不能把“improved harness”直接视作完成闭环，也不能声称已做正文排除审查。

[逐项机器报告](backlog-s2-review.json) · [33 项正文证据](backlog-s2-body-evidence.md) · [逐 ID 续跑清单](backlog-s2-resume.json)

| ID | 建议 | 阅读层级 | 判断与后续 |
|---|---|---|---|
| arxiv:2610.40663 | include | 完整摘要+正文关键章节 | 正文明确唯一可改对象为空白起始的临床技能文档；失败咨询与专家分析驱动增删改，双集合接受门保留编辑并供后续轮次和封存测试病例使用。 |
| arxiv:2610.40747 | include | 复用同日 HF | 教师权重固定，authoring agent 按任务成功率、token成本和执行反馈修订完整教师 Harness；选定后固定，用于多轮数据生成与学生训练。 |
| arxiv:2610.40751 | exclude | 完整 S2 摘要 | 安全循环主要训练模型、持久安全状态及可移除专家；形式推理Harness是配套推理结构，摘要未将其作为演化对象。 |
| arxiv:2610.40758 | include | 完整摘要+正文关键章节 | 专项评测持久策略/技能自演化如何跨课程继承：GEPA明确演化policy提示，EvoSkill维护技能库，practice反馈更新状态后供test及后续level使用。负结果显示状态多记忆实例，不取消对程序优化机制的评测属性。 |
| arxiv:2610.41143 | exclude | 完整 S2 摘要 | 主要通过SFT与RL训练模型选择talent并路由技能，改进对象是模型策略参数，不是反馈改写外部技能或路由程序。 |
| arxiv:2610.41157 | include | 完整摘要+正文关键章节 | 直接比较自然语言系统提示/函数候选的父代继承和反馈披露；当前best按严格改进保留到下轮，并用独立holdout评估。纳入依据包括持久提示优化的专项分析。 |
| arxiv:2610.41183 | exclude | 完整 S2 摘要 | 反馈与演化改进的是量子纠错码构造程序和数学家族，属于外部科研产物，并未改写发现Agent自身Harness。 |
| arxiv:2610.41245 | exclude | 完整 S2 摘要 | 通过索引、量化效应和相互作用累积抗体优化经验，更新对象是测量记忆内容，不能视为改写记忆管理机制。 |
| arxiv:2610.41320 | exclude | 完整 S2 摘要 | LEXP保留带条件的经验教训并用于后续动作，摘要描述的是经验内容复用，未显示对规划或记忆管理代码/策略文件的演化。 |
| arxiv:2610.41378 | exclude | 完整 S2 摘要 | 固定按需通信流程配合成对延续数据训练轻量触发gate，优化对象是学习到的门控策略，不是外部通信工件的持续改写。 |
| arxiv:2610.41809 | exclude | 完整 S2 摘要 | 讨论持续强化学习十项能力与持久世界基准，没有针对模型外可复用Harness工件反馈演化的专项分析。 |
| arxiv:2611.00180 | include | 完整摘要+正文关键章节 | EDM蒸馏阶段依据执行反馈修订工具与技能指令，Mount把验证后能力注册到执行环境，冻结能力用于后续问题及held-out episodes；不仅新增记忆事实。 |
| arxiv:2611.00384 | exclude | 完整 S2 摘要 | 两条循环生成/修复外部训练模型和训练流水线，调优架构与训练配置；共享Agent运行时本身没有被演化。 |
| arxiv:2611.00463 | include | 完整摘要+正文关键章节 | 执行器策略源代码可读写，包括工具、上下文和进一步自改程序；运行记录/成本支持修订，独立guardian激活后继策略且保留历史，重复目标新账号实验继承自修改。 |
| arxiv:2611.00504 | exclude | 完整 S2 摘要 | CVaR反馈优化GPU准入、VM装箱和放置等外部系统启发式，生成物不是优化Agent自己的推理Harness。 |
| arxiv:2611.00518 | exclude | 完整 S2 摘要 | 固定分析器审核并重建当前对话上下文，修复的是会话状态污染；没有跨任务保留的新Harness程序版本。 |
| arxiv:2611.00580 | exclude | 完整 S2 摘要 | 提出跨实验室科研记忆、假说与评估器修订蓝图，主要对象是科研过程及产物，没有专门研究Agent自身Harness演化。 |
| arxiv:2611.00643 | include | 完整摘要+正文关键章节 | 评测对象包含角色、检索、自质疑、选择规则和策略提示组成的Harness；Opus读评分历史提3轮候选并以严格胜出替换incumbent，论文直接分析judge目标与真值精度失配。 |
| arxiv:2611.00752 | exclude | 完整摘要+正文关键章节 | 正文说明每次修改由作者依据AI判分和人工分析提出，AI编码助手实施，作者复核后保留；这是有真实程序迭代的人工研发，未展示系统自主提出并演化自身Harness的闭环。 |
| arxiv:2611.00960 | include | 完整摘要+正文关键章节 | Refiner依据失败SQL和judge解释生成完整替换提示；候选通过目标及抽样回归检查后继承到下轮，最终提示冻结供跨schema和Generator复用。 |
| arxiv:2611.01113 | include | 完整摘要+正文关键章节 | 保留至多五条When条件规则作为reader原则槽，失败问题触发增改删及候选比较，后续库迁移至独立BigToM-U；同时专项审计演化规则语义有效性。 |
| arxiv:2611.01334 | exclude | 完整 S2 摘要 | 固定轨迹、验证器和阈值，仅测试单轮选择数值摘要的奖励博弈；没有专门评测Harness工件的持续反馈演化。 |
| arxiv:2611.01351 | exclude | 完整摘要+正文关键章节 | 正文将Playbook条目明确为第三人称UI action-effect陈述事实，按固定流程插入、去重和更新计数；跨episode保留的是界面知识，不是被反馈改写的执行程序或策略文件。 |
| arxiv:2611.01377 | exclude | 完整 S2 摘要 | 按当前上下文动态选择retrieve/reason/code/test操作以生成边缘应用，描述的是单任务自适应执行，不是保留的新工作流工件。 |
| arxiv:2611.01386 | include | 完整摘要+正文关键章节 | Reflector/Curator依据验证执行trace、失败对照和旧提案结果增改合并程序性Skill，准入后创建不可变版本，后续run检索并执行该程序。 |
| arxiv:2611.01402 | exclude | 完整 S2 摘要 | Max-k-Cut近似困难性的数学证明与归约，不涉及Agent或Harness自改进。 |
| arxiv:2611.01415 | exclude | 完整 S2 摘要 | 主要把外部条件蒸馏成模型内部激活shift参数并控制注入；主改进对象并非提示/工具等外部可复用程序工件。 |
| arxiv:2611.01572 | exclude | 完整 S2 摘要 | 重放一般代码输出judge对GRPO训练损坏的敏感性，评测的是模型输出和训练，不是Harness工件反馈演化专项。 |
| arxiv:2611.01695 | include | 完整摘要+正文关键章节 | 外环明确区别于商户episodic memory；以交互结果因果归因为门，对跨商户共享策略playbook执行Update/Condition/Add/Merge/Deprecate等修改，后续会话选择非废弃策略。 |
| arxiv:2611.01736 | include | 完整摘要+正文关键章节 | 环境允许目标模型与可执行Harness修订，保留运行记录及后继版本；Knowledge Self案例明确H0/M0→H1/M0，再由该后继系统训练M1，形成真实Harness与目标模型共同演进。 |
| arxiv:2611.01747 | exclude | 完整 S2 摘要 | 在线更新记忆库与contextual-bandit数值路由策略；摘要未描述改写外部控制代码或策略文件，不能把评分器学习当Harness演化。 |
| arxiv:2611.01834 | exclude | 完整 S2 摘要 | 反馈改进的是供SFT/RL使用的训练环境atoms和verifiers，属于环境/奖励侧，不是执行Agent自身推理Harness。 |
| arxiv:2611.01840 | include | 完整摘要+正文关键章节 | 代码工作流在每次交互固定，执行记录和结果驱动编码agent修改分解、分支与求解过程；被保留候选成为下一轮W并继续收集反馈，符合程序工作流演化。 |
| arxiv:2611.01870 | include | 完整摘要+正文关键章节 | Architect读取既有架构及performance history，演化专家identity/directive提示和多Agent图；创建/交叉后按性能多样性保留池，架构可留给后续任务。纳入来自这些外部工件，不只specialist记忆。 |
| arxiv:2611.01908 | exclude | 完整 S2 摘要 | 反思反馈的对象为外部生物预测器模型编辑与测量选择，分析递归反馈增益未成立，非Agent自身Harness专项。 |
| arxiv:2611.02017 | exclude | 复用同日 HF | Switch-SWE 评测未完成任务切换并提出固定context管理模块；摘要无模块自身反馈改写/持久继承，属于一般代理评测。 |
| arxiv:2611.02075 | exclude | 完整 S2 摘要 | 固定预训练条件预测器读取增长的历史证据再映射成决策，经验增加不等于改变Harness程序或提示策略。 |
| arxiv:2611.02079 | include | 复用同日 HF | 固定执行模型，以执行轨迹和质量/成本反馈修改提示、工具、中间件及控制流；获准候选保留到档案并继续迭代。 |
| arxiv:2611.02353 | exclude | 完整 S2 摘要 | 比较一般文本到可视化系统的执行/图表质量，虽分析系统设计差异，但未专门评测持续Harness反馈演化。 |
| arxiv:2611.02391 | exclude | 完整 S2 摘要 | 编码Agent按吞吐评分优化外部仓库多机器人规划器；累积patch属于被设计的业务算法，不是研究Agent自身Harness。 |
| arxiv:2611.02487 | exclude | 完整 S2 摘要 | 机制假说与实验反馈持续改进外部推荐算法，研究流程承载历史证据，本身未被明确改写为新Harness。 |
| arxiv:2611.02501 | exclude | 复用同日 HF | 反馈优化的是外部 speculative decoding 算法和服务系统；保存可重放的优化代码与记忆不等于 Agent 自身 Harness 被迭代修改。 |
| arxiv:2611.02516 | include | 完整摘要+正文关键章节 | 生成Python guardrail工具，复用时融合旧逻辑，依据独立审计的漏洞报告最多三轮修复，只有通过者进入持久工具库供后续防御。 |
| arxiv:2611.02698 | exclude | 完整 S2 摘要 | 评测一般视觉定位/探索能力，附带固定Planner-Worker-Compressor压缩历史；没有Harness演化的专门变量。 |
| arxiv:2611.02752 | exclude | 完整 S2 摘要 | 评测LLM优化外部HPC计算内核的正确性和性能，不是其自身Harness工件的持续改进能力。 |
| arxiv:2611.02779 | exclude | 完整 S2 摘要 | Agent合成并验证外部数据库引擎和证明，反馈服务数据库性能/正确性，合成物不属于Agent自己的推理Harness。 |
| arxiv:2611.02797 | include | 完整摘要+正文关键章节 | 固定backbone下，benchmark执行候选Harness并返回当前任务分数，由各方法选择保留版本再进入下一任务；AHE与HyperAgents明确改prompt/tools/代码及improver，专项测G0–G4泛化和改动过程。 |
| arxiv:2611.02830 | exclude | 完整 S2 摘要 | 用SFT与GRPO训练推理模型为当前任务生成伪代码计划，改进对象是模型参数，任务计划不是跨任务演化Harness。 |
| arxiv:2611.02839 | exclude | 完整摘要+正文关键章节 | 正文明确外部Harness变更确实存在，但由业务owner/工程师按各自日程修订，且3.3写明context change不是CARE循环一步；其自动递归更新对象是模型，未证实Agent生成并保留Harness修订。 |
| arxiv:2611.02950 | exclude | 完整 S2 摘要 | 固定反驳式验证过程在每次动作前寻找反证，修正当前动作，不产生被后续任务保留的新验证器工件。 |
| arxiv:2611.02989 | exclude | 完整 S2 摘要 | 在开发集选择情感分类器升级路由政策并留出评测，属于一次策略选择及预测复核，没有持续自改进外部Harness链。 |
| arxiv:2611.03157 | exclude | 完整 S2 摘要 | 主张跨Agent的显式知识层持续概念化和修订，改进对象是知识表征/内容及知识模型，非Harness程序反馈演化专项。 |
| arxiv:2611.03434 | include | 完整摘要+正文关键章节 | 正文明确supervisor自动propose–test–keep，评分改进加通用/精简性检查决定保留，接受的工具、guardrail、compaction和memory policy引发下一轮错误分析。 |
| arxiv:2611.03517 | exclude | 完整 S2 摘要 | 主要以人工/固定问题库引导Agent优化外部CUDA内核；最小Harness用于目标约束，没有证据表明问题库或Harness本身演化。 |
| arxiv:2611.03534 | exclude | 完整 S2 摘要 | 系统积累规章/工程知识并生成外部电网设计，变化对象是知识内容与业务产物，未显示Agent自身控制程序的演化。 |
| arxiv:2611.03601 | exclude | 完整 S2 摘要 | 框架根据观测调整当下治疗动作和个人经验，配合模拟器/基准，没有跨任务修改Harness程序工件的链条。 |
| arxiv:2611.03618 | include | 完整摘要+正文关键章节 | Python blueprint指定模型调用/推理控制流程，真实样本的trace与分数驱动后续提案；每轮把去除任务特定提示的结构与测量卡写入共享库，支持后续任务组合复用。 |
| arxiv:2611.03674 | include | 完整摘要+正文关键章节 | 外环依据跨小说production trace与修订archive改版本化editor prompt/config及meta-policy；固定kernel选中后成为下一代，meta-policy按其产生的editor在held-out小说的效用评估。 |
| arxiv:2611.03685 | exclude | 复用同日 HF | LOLPlay 测实时视觉Agent能力和reasoning effort，未评测Harness自进化机制。 |
| arxiv:2611.03698 | exclude | 完整 S2 摘要 | 摘要只说明使用 improved harness 采集训练轨迹，没有给出该 Harness 依据执行反馈修改并跨轮保留的证据；暂排除并优先正文抽查，不能仅因模型训练是主贡献而排除实际共演化。 |
| arxiv:2611.03765 | exclude | 完整 S2 摘要 | 评测一般具身Agent对上下文信息缺失的鲁棒性，没有测试外部Harness工件的反馈修改与继承。 |
| arxiv:2611.03868 | include | 完整摘要+正文关键章节 | 官方correctness与置信度筛选交互轨迹，逐例和跨类诊断指导Evolve Agent修改operation实现、intervention和policy；演化后Harness冻结迁移GroupMemBench。 |
| arxiv:2611.03935 | exclude | 完整 S2 摘要 | 人为选择实验室结构与通信配置的系统说明，作者明确未做benchmark结论；可配置研究空间不等于反馈驱动Harness持续自改。 |
| arxiv:2611.04003 | include | 完整摘要+正文关键章节 | 反馈驱动wiki认证程序、分页/错误恢复步骤及代码细节的修订，构成模型外可复用操作指令；更新后的store由下一轮执行读取。自然语言程序性技能也符合工件规则，不因底层执行/检索机制固定而排除。 |
| arxiv:2611.04032 | exclude | 完整 S2 摘要 | 模拟与测量帮助搜索外部LLM serving部署配置，调整引擎/硬件/调度参数，不是优化Agent自身Harness程序。 |
| arxiv:2611.04035 | include | 复用同日 HF | 运行反馈驱动指令和程序技能的诊断、编辑与验证，通过回归检查后保留到后续任务；属于可复用 Harness 组件。 |
| arxiv:2611.04104 | exclude | 完整摘要+正文关键章节 | 实际改写的可执行程序是外部kernel；持续更新的是硬件/算子优化技巧、状态、假说及证据claims，供固定actor/critic和检索机制取用。称其为mutable policy parameters未提供Agent自身控制程序或可复用操作机制被修改的证据。 独立意见为 borderline，待裁定。 |
| arxiv:2611.04277 | include | 完整摘要+正文关键章节 | 冻结policy后运行父Harness分析失败根因，编辑prompt/skill/context/hooks等工件，以validation互补覆盖选父代并归档有效后代；多代形成的池供后续模型训练长期复用。 |
| arxiv:2611.04356 | exclude | 完整 S2 摘要 | 搜索生成触发FEM求解器资源放大的外部对抗输入程序，研究产物不属于Agent自身推理Harness。 |
| arxiv:2611.04431 | exclude | 完整 S2 摘要 | 语言模型辅助优化外部量子定价电路算术，报告电路资源与正确性，不是自改Agent Harness。 |
| arxiv:2611.04437 | include | 完整摘要+正文关键章节 | LLM根据无线执行失败、动作轨迹和任务统计重写Agent自身solve(env,task)程序；共同任务批评估后保留候选为下一代父程序，演化导航/感知/通信控制结构。 |
| arxiv:2611.04439 | include | 完整摘要+正文关键章节 | 外环根据实验过程trace评分提出新增/退休/合并Harness与Skill规则，并用下一轮反馈更新选择；规则指导后续研究轮次且可冻结迁移。内层改推荐模型代码属于外部研究产物。 |
| arxiv:2611.04466 | include | 完整摘要+正文关键章节 | 根据执行trace和用户纠错抽取Context/Decision/Strategy，生成Create/Revise/Merge/Remove技能patch，评分后更新持久技能池并冻结在后续任务评估。 |
| arxiv:2611.04483 | borderline | 完整摘要+正文关键章节 | 提出从交互证据修订决策规则/程序性skills并服务后续调用的生命周期；现有实现将capability failure转为候选并保留staging，但配对评估到active promotion尚未贯通。可作Harness架构/理论讨论候选，不能作为已实现持续技能闭环主方法批准。 |
| arxiv:2611.04772 | include | 完整摘要+正文关键章节 | 反馈触发诊断并提出版本化策略条件与依赖执行规则修订，系统规定held-out release checks和回滚；两轮实际revision的回放专项审计检验修复增益是否可复现。 |
| arxiv:2611.04952 | include | 完整摘要+正文关键章节 | 专门诊断持久工件到能力的反馈演化链：同一base model下演化Reflexion记忆、Voyager技能/调用程序、DGM代码谱系，再冻结并按状态、整局、版本谱系检验作用、冲突和保留。 |
| arxiv:2611.05139 | include | 完整摘要+正文关键章节 | 离线以A/B/C轨迹和verifier终局反馈反复增改删版本化Meta-Skill中的act/hold/avoid干预规则，跨任务聚合后冻结供evolver后续调用；保留的是改进器决策规则而非在线临时Harness补丁。 |
| arxiv:2611.05251 | include | 完整摘要+正文关键章节 | Agent发现缺失能力后编写自身可调用工具的lib与skill包装，测试和独立co-lead反馈触发限次修订，通过两类检查才原子提交到持久toolkit，供后续分析复用；主编排代码受保护。 |
| arxiv:2611.05313 | exclude | 完整 S2 摘要 | OPSD把多视图skill经验内化到共享模型policy，动态筛选技能是训练数据组织，主要更新对象是模型参数。 |
| arxiv:2611.05319 | exclude | 完整 S2 摘要 | 固定三算子更新用户/物品profile并改善检索，变化对象是画像内容及匹配信号，非可复用Harness程序改写。 |
| arxiv:2611.05320 | exclude | 完整 S2 摘要 | Agent为每个数据请求生成仿真场景、专家控制器和成功judge，再采样机器人训练数据；这是数据/环境产物演化。 |
| s2:73abbf7ebfcddc9eaa9d9efeecee1e71ba1d5f2b | exclude | 完整 S2 摘要 | 固定推理前middleware校验当次证据、补检索并升级处理，不形成后续任务保留的新上下文管理程序。 |
