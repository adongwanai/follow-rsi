# 2026-11-11 独立范围复审（初稿）

No root primary-scope-review or other agents conclusions were read before this initial report. Author/source text and local taxonomy only.

此稿只完成范围/来源核对，不是人工批准或实验复现。

共 64 条：{'exclude': 54, 'include': 8, 'borderline': 2}

| ID | 建议 | 类型 | 理由 |
|---|---|---|---|
| arxiv:2611.12063 | exclude | outside_harness | 优化外部数据系统及其规格/验证的研究愿景；没有Agent自身可复用Harness的反馈更新证据。 |
| arxiv:2611.12552 | include | harness_method_task_local | SciMARS 明确改变角色规程、协调契约和可选记忆管理策略，执行候选后选择并保留下一轮 Harness；按现行定义“后续任务或改进轮次”，其任务内跨改进轮次的 Harness 更新可收。 |
| arxiv:2611.10884 | exclude | outside_harness | 固定FSM执行控制改善long-horizon指令遵循；FSM结构/规程不随反馈演化。 |
| arxiv:2611.12041 | exclude | outside_harness | SMO由既有skill语料进行结构化编译；§3.3明确“Agent execution does not feed back”。schema/novelty/connectivity检查带来库版本，缺执行或任务评估反馈驱动的自改闭环。 |
| arxiv:2611.11499 | include | harness_coevolution | JoMoHa 不仅训练两个模型：Engineer 根据历史反馈生成可执行 Harness，程序与 Solver 均跨轮保存；不同保存程序在固定 Solver 下被交叉评估，部署选择保存程序。符合权重与外部 Harness 双方反馈更新和保留。 |
| arxiv:2611.12068 | include | harness_method_subsection | 仅 AutoDream 的procedural refinement可纳：它根据带原文引用的session outcome创建、编辑或删除可复用skill，改变actor可用的操作指令。语义记录与图索引合并本身不算Harness演化。 |
| arxiv:2611.12120 | exclude | outside_harness | SCALE内化concept到神经表示并整理经验数据；没有修改外部Harness代码/管理机制。 |
| arxiv:2611.12885 | include | harness_method_subsection | RoboScript 的§4.1有独立Harness证据：coding agent为动作接口缺口写可复用skills，driver执行原场景与其他布局验证，循环到coverage停止提升后冻结，供Agent后续任务学习与部署调用。Task Memory及反思仍须另标经验内容，不将整篇所有记忆都算Harness。 |
| arxiv:2611.11509 | exclude | outside_harness | SimplEvo直接重写关于任务过程、完成/恢复的working-memory经验文本；未改memory管理工具、runtime流程或可执行skills，按当前区分记忆内容与Harness机制的规则归经验方向。 |
| arxiv:2611.11565 | exclude | outside_harness | EARN更新动作credit和存储route并条件replay；固定记忆更新/选择规则不被改写，属于经验引导test-time adaptation。 |
| arxiv:2611.10501 | exclude | outside_harness | 好奇心论述要求可在线更新环境预测结构，不是专项Harness RSI方法或理论。 |
| arxiv:2611.10542 | include | harness_specific_safety_evaluation | BadEvolve 直接评测执行经验如何经trusted evolver变成持久skills后门；evolution、attack validation和test分离，目标就是Harness技能演化，属于专项安全评测。 |
| arxiv:2611.10748 | include | harness_method_domain_limited | REINS 的在线memory-miss路径让LLM生成带触发条件/谓词/动作的可执行规则，经过世界模型rollout验证后写回，之后直接参与runtime planning；这是持续Agent中的操作规则更新，超出仅保存历史经历。 |
| arxiv:2611.10510 | exclude | outside_harness | ReSkill用development coding agent优化外部机器人task programs/skill library；部署保留policy独立执行且不再调用agent，不能把外部任务产物当开发Agent自身Harness。 |
| arxiv:2611.10477 | exclude | outside_harness | PatternBloom高reward轨迹一次蒸馏成GPM，Stage II及inference全程冻结；更新主要为RL policy，不能把一次经验库构建当Harness迭代共演化。 |
| arxiv:2611.10787 | include | harness_specific_method_and_theory | TRUST研究Harness更新的统计准入：迭代候选从reasoning/routing/memory/workflow操作产生，检验决定替换incumbent，保持跨轮历史；可收准入方法与专项理论。 |
| arxiv:2611.10022 | include | harness_method | SkillCache 把执行轨迹编译成模型外可复用capsule程序和步骤，执行replay失败后反馈给compiler修复（最多三轮），通过才用于后续warm调用；不是单纯缓存原答案。 |
| s2:6bd9ff9c3957cf1faac67fbce8b42650d82a52fc | borderline | source_blocked | DOI、Crossref 与 OpenAlex 对齐题名/作者/刊物 Originality；Crossref 发表字段仅到 2026-11，S2 和 OpenAlex 报 2026-11-01，不能把后者当作已核实的确切出版日。Crossref 无摘要，OpenAlex 提供重建摘要，但 ScienceDirect 页面返回403且 Elsevier text-mining API 返回401，未取得可核验正文。只凭标题/摘要不能判断是否符合 Harness RSI，保留为新来源阻塞，不能排除或纳入。 |
| arxiv:2611.12806 | exclude | outside_harness | 异构触觉表示预训练/机器人policy整合，无Harness自改。 |
| arxiv:2611.10771 | exclude | outside_harness | WorldFoundry为世界模型推理/评测的固定基础设施，目录和artifact contracts不是Harness RSI。 |
| arxiv:2611.12762 | borderline | harness_mechanism_not_demonstrated | Sage-Taiyi §2.3.4描述根据成功/失败精炼可复用方法，可能满足Harness方法条件；但演示/算法主要更新当前Cognitive State、想法与研究目标，结论把通过经验精炼和跨域复用repertoire列为future work。缺少实际改动工件/跨轮保留实例，暂缓。 |
| arxiv:2611.12886 | exclude | outside_harness | Reframe训练视觉agent的RL/OPD权重；工具动作修补发生在训练rollout，不留作外部Harness工件。 |
| arxiv:2610.42148 | exclude | outside_harness | Flide是精确state forking推理引擎优化，无自改环路。 |
| arxiv:2611.10304 | exclude | outside_harness | Longtail-SWE修订的是benchmark任务描述/测试，非Agent自身Harness。 |
| arxiv:2611.11558 | exclude | outside_harness | InfraRSI改训练系统launch knobs/kernel/code patches，并保存基础设施经验；固定任务契约和workflow未自改，属于外部AI基础设施研发。 |
| arxiv:2611.10329 | exclude | outside_harness | SIRIS测模型如何判断模拟器推荐可靠性，非Harness演化专项评测。 |
| arxiv:2611.11450 | exclude | outside_harness | OPD训练推理mismatch分析和rollout配置准入，非Agent外部Harness自改。 |
| arxiv:2611.10592 | exclude | outside_harness | MotionGraphicsBench是动画生成benchmark，构建verification programs作为评测数据，不是Harness RSI专项。 |
| arxiv:2611.02810 | exclude | outside_harness | TRIO通过reward分别训练query/judge/answer agents；缺反馈更新外部Harness工件。 |
| arxiv:2611.08240 | exclude | outside_harness | FewStepRL为diffusion RL目标与训练算法，无Agent Harness更新。 |
| arxiv:2610.36980 | exclude | outside_harness | AutoVend评价长期售货业务决策，库存/商业policy在task内变化不是Harness RSI。 |
| arxiv:2611.10123 | exclude | outside_harness | 模型pain-state内省实验，非Harness演化。 |
| arxiv:2611.01112 | exclude | outside_harness | Auriga为固定执行Harness，文中13次development升级未给自主修改者/自动改码闭环，部署仅单episode状态调整；结论把automated cross-task tool synthesis列未来工作，当前不能证成RSI。 |
| arxiv:2611.11890 | exclude | outside_harness | ViT关注区域loss/表示学习，非RSI Harness。 |
| arxiv:2611.12324 | exclude | outside_harness | WARC test-time训练世界模型所有参数，配fixed graph explorer；外部Harness不迭代。 |
| arxiv:2611.05791 | exclude | outside_harness | FlyHash固定hash检索方案用于agent memory，没有反馈更新memory管理算法。 |
| arxiv:2611.10556 | exclude | outside_harness | onóna为embedding/output-head架构与语言模型训练，非Harness RSI。 |
| arxiv:2611.08935 | exclude | outside_harness | SkinMind固定图检索工具构建query-specific evidence subgraph，没有跨任务Harness改写。 |
| arxiv:2611.10690 | exclude | outside_harness | JoVox是voxel生成flow模型，非Harness RSI。 |
| arxiv:2611.12167 | exclude | outside_harness | FraudBench评价欺骗倾向和静态prompt intervention，非Harness自进化专项。 |
| arxiv:2611.09709 | exclude | outside_harness | RidgeFill闭式拟合cache map与推理优化，非Agent反馈自改。 |
| arxiv:2611.11740 | exclude | outside_harness | Creative Priming用GRPO训练primer生成模型；primer按请求产生，无保存并迭代外部prompt工件证据。 |
| arxiv:2610.37570 | exclude | outside_harness | LCM-Promo是商业uplift finetuned模型，非Harness RSI。 |
| arxiv:2611.12870 | exclude | outside_harness | SWAM研究world-action模型数据/监督/架构训练，无Harness自改。 |
| arxiv:2611.09195 | exclude | outside_harness | InstantHMR移动人体mesh恢复模型，非RSI。 |
| arxiv:2611.11344 | exclude | outside_harness | Spatial Harness执行physics反馈来校正当前世界状态/推理，框架本身固定。 |
| arxiv:2611.09987 | exclude | outside_harness | 人脸识别early-exit深监督模型，无Harness RSI。 |
| arxiv:2611.08969 | exclude | outside_harness | PhysioWave-T生理信号foundation model预训练/融合，非RSI。 |
| arxiv:2611.11995 | exclude | outside_harness | Infrathon是外部AI基础设施优化任务benchmark；长时间改外部代码不等于自身Harness。 |
| arxiv:2611.09501 | exclude | outside_harness | e-means聚类优化算法，无Agent自改。 |
| arxiv:2611.12875 | exclude | outside_harness | Click3R用人类点击修正当前3D重建，非自主跨任务Harness。 |
| arxiv:2501.08686 | exclude | outside_harness | KG-RAG4SM固定KG检索/重排用于schema matching，无反馈驱动Harness更新。 |
| arxiv:2512.23818 | exclude | outside_harness | Energy-Tweedie为噪声/score理论，无Harness RSI。 |
| arxiv:2611.10987 | exclude | outside_harness | HQL为offline Q-function学习方法，非外部Harness演化。 |
| arxiv:2611.09124 | exclude | outside_harness | A2-MEAS的correction code训练adapter/policy，部署fresh codes修当前行为；未显示外部Harness代码/规则被迭代保留。 |
| arxiv:2611.10404 | exclude | outside_harness | Coding or Cheating使用同一固定harness研究模型reward hacking，不是Harness RSI专项。 |
| arxiv:2611.01729 | exclude | outside_harness | ODE Policy学动作动力学模型，无Harness RSI。 |
| post:https://openai.com/index/helping-caregivers-use-ai-in-everyday-life | exclude | outside_harness | 照护者AI技能线下活动，非系统自改研究。 |
| post:https://openai.com/index/introducing-businesses-chatgpt | exclude | outside_harness | Business Hub/Agents产品发布，商家资料更新非Harness演化。 |
| post:https://openai.com/index/closing-ai-guidance-gap-education | exclude | outside_harness | 教育AI使用与培训研究，非Harness RSI。 |
| post:https://openai.com/index/ai-effect-on-freelance-work | exclude | outside_harness | AI与自由职业市场研究，非Harness RSI。 |
| post:https://deepmind.google/blog/gemini-4-carbon-is-now-available/ | exclude | outside_harness | 模型及swarm产品发布，未给自修改Harness闭环。 |
| post:https://deepmind.google/blog/introducing-alphaproof-code/ | exclude | outside_harness | 多Agent生成/检查Lean证明，优化的是外部形式证明产物，没有自身Harness更新。 |
| post:https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/ | exclude | outside_harness | VLA模型能力发布，未给外部Harness反馈更新证据。 |
