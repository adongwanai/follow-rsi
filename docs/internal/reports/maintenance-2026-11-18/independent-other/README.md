# 2026-11-18 非 HF 候选及历史 issue：独立第三轮复核

这是子 agent 的逐项范围与来源建议，主审须结合独立反证整合；未直接修改 canonical、正式 review 或生产物，也未创建/合并 PR。

- 全部 51 条：建议纳入 11、排除 36、待补 4。
- 44 条新增非 HF 候选：纳入 9、排除 33、待补 2；7 条历史 issue：纳入 2、排除 3、待补 2。
- 官方全文或网页取得 50 条；S2 survey 原请求和一次重试均 429，保留错误原文与逐项原因。
- 11 条建议纳入均有定性中英摘要，来源正文/抽取文本 SHA 和精确原文片段已经校验；这不是实验复现。
- 付费模型请求 0。所有请求回执与原文已持久保存，未重跑历史模型。

## 必须保留的反证与日期边界

- ESI 的初读共演化建议已撤回：主实验 prompt/skill catalog 固定，具体 guidance 候选未发布。现为 defer。
- ELITE 仅用结构/可操作性反馈，无下游候选任务成绩；RemeshingAgent 工具层无 adoption；Synapse 接受总分改善并非所有旧样例不退化。
- WeVisForensics、RoboCoEvo 有可执行/规则工件与权重双方更新；MetaAct 改的是 executable spec。SAGE-VQA 只纳入程序工具子链，评测期间仍有答后更新。
- SIM 的改进器 planning/search 固定；MULTILOOP 主要提示/工具改动；RSI Tax 的 subsequent use 不是准确率因果收益，tokens 不是账单。
- SPG-Select 排除为经验条目边界建议，需主审整合；其附录示例不是实验演化日志。
- BPMN 官方 PDF 有效，标题和全部作者匹配；无 arXiv 水印的 version_identity_matches 保持 null。
- 历史 issue 的 first_seen 从 canonical 保留；额外 metadata parser 的 11/18 first_seen 只记作本次 refetch，不覆盖历史。
- 所有条目无 HF 推荐日；旧论文首次发现单列，不能顺延为今日新发表。JFinBench RSS 的 UTC 11/16 15:00 对应日本 11/17，保留官方网页日。

## 逐项建议

| ID | 建议 | 分类 | 原因 |
| --- | --- | --- | --- |
| arxiv:2611.11273 | 排除 | experience_world_model | CASA 存 anonymisation configs/results 和 coarse lessons，当前任务根据隐私/效用反馈重规划；工具与管理机制无持久修改证明。 |
| arxiv:2611.12288 | 待补 | ai4ai | ForgeSystem 声称反馈修改 context/tool/exploration/testing，实际主要验证 kernel/engine 外部产物；具体可接受并保留 Harness 修改实例及多轮收益仍缺。 |
| arxiv:2611.13524 | 纳入建议 | evaluation_benchmark | RSI Tax 的对象包含 Meta-Harness、RRSI 等持久 Harness 更新，明确 task-before-update 协议并审计改进调用 tokens，属于 Harness 专项评测。 |
| arxiv:2611.13818 | 排除 | model_weights | WAM 原文明确该实现不使用 RSI 或 agentic harness；LoRA/进度/路由为固定方案，RSI 是讨论中的未来方向。 |
| arxiv:2611.15754 | 纳入建议 | harness/evolve_main | MULTILOOP 将每个 Harness 版本、训练分数和 rollouts 记入历史，coding agent 据此改代码并选择训练表现最佳版本；有可核验 download_file 新工具修改。 |
| arxiv:2611.17790 | 排除 | ai4ai | AutoRL 确有热/冷修改训练 code/reward/loss 的闭环，但对象是被管理的 RL 训练过程，不是 AutoRL 自己的控制器或工具机制。 |
| arxiv:2611.18006 | 待补 | model_weights | RecurIR 的 estimator、task generator、revision operator/gate 由学习更新，存在独立 transfer/retention 检查；目前未明确可复用外部 Harness 工件如何被修改并部署。 |
| arxiv:2505.23836 | 排除 | evaluation_benchmark | 检测 eval/deployment awareness 的一般评测；未检验持久 Harness 自改闭环。 |
| arxiv:2603.08640 | 排除 | ai4ai | Agent 的交付物是外部 post-trained model，CLI scaffold 对比未提供自身 Harness 演化证据。 |
| arxiv:2609.04298 | 排除 | evaluation_benchmark | 统一适配和一般 Agent benchmark/静态 Harness 对比，不是反馈驱动 Harness evolution 专项。 |
| arxiv:2611.17821 | 排除 | experience_world_model | 扩展布局/场景经验与产物库，正文明确不改 skill representation/retrieval/update protocol；缺少程序化 Harness 修改。 |
| arxiv:2611.18140 | 排除 | model_weights | SFT/GRPO 训练充电 policy，物理反馈驱动动作，外部 safety layer 明确 non-learned；未呈现 Harness 更新。 |
| arxiv:2611.18157 | 排除 | ai4ai | BPMN pipeline 的 prompt-demo 筛选优化分类准确率，后续固定校验生成 XML/ontology 产物；缺少自身 Agent 控制程序反馈改写的保留链。 |
| arxiv:2611.18176 | 待补 | embodied | 撤回初读时按 prompt/skill/policy 设计描述作 coevolution 的建议。主三轮实验证明 prompt 和 skill catalog 固定；唯一具体 guidance 修改候选被 reviewer 拒绝，未发布。 |
| arxiv:2611.18723 | 纳入建议 | harness/component | ViCoR 通过 set_reflex 改写 Python visual reflex guide，依据跨 episode 分数 checkpoint/restore library，存在可执行工件保留。 |
| arxiv:2611.18818 | 排除 | experience_world_model | SPG-Select 保留 SkillBank/ExpeL/Shared Reflexion 的经验条目；schema 为 principle/when_to_apply，与执行工件或管理策略改写证据仍有区别。 |
| arxiv:2611.18856 | 纳入建议 | harness/generalize | 被持续修改并继承的是 executable Harness H；SIM 记录反馈与代码修改历史，帮助跨模型或数据集后的继续优化。不是改进器自身代码进化。 |
| arxiv:2611.19081 | 纳入建议 | harness/coevolution | VLA 权重与可执行 failure detectors/recovery FSM 都随轮次反馈修改，恢复程序经 held-out recovery gate 并跨实例复用。 |
| arxiv:2611.19700 | 排除 | model_weights | 研究 ICL episode retention 与权重更新；FIFO/Prefix/All/Successful 为固定策略，不是反馈改写的 Harness。 |
| arxiv:2611.19764 | 排除 | safety_governance | CompGuard 是固定 runtime 能力/taint 防御，契约声明为 immutable；非反馈驱动 Harness 进化方法或其专项评测。 |
| arxiv:2611.19933 | 纳入建议 | harness/component | 仅 procedural tool 子链纳入：存有 executable code，试运行失效驱动修订，合法版本按 ID 替换并供后题调用。普通 declarative/semantic memories 不自动算 Harness。 |
| arxiv:2611.20049 | 排除 | model_weights | 反馈用于生成训练 frontier 并训练 fresh LoRA，跨轮状态是数据集；没有被修改并保留的 Agent Harness。 |
| arxiv:2611.20230 | 排除 | experience_world_model | 存储和检索有序步骤/经验，使用既定 consolidation/promotion 规则；未展示运行中改写管理机制。 |
| arxiv:2611.20533 | 纳入建议 | harness/component | 可执行 pipeline template/skill document 根据成功失败轨迹进行文本修改，独立 selection gate 严格提升才替换 deployed skill。 |
| arxiv:2611.20605 | 排除 | experience_world_model | 更新文本记忆及每条 utility；noisy-OR、检索、merge/evict 为既定管理规则，没有反馈改写管理代码或策略工件。 |
| arxiv:2611.20655 | 纳入建议 | harness/component | 编译器固定，但被反馈修改并持续部署的是可执行 typed GEAR constraints；不是单纯检索经验条目。 |
| arxiv:2611.20856 | 纳入建议 | harness/component | 将自然语言 skill 编译到 SkIR，执行轨迹定位失效指令并生成 typed patches；验证选中的修改成为下一轮 skill。 |
| arxiv:2611.20927 | 排除 | experience_world_model | LEDGER 保留事实、时效、审计记录与 tombstones；写入/信任/删除规则固定，没有外部 Harness 的反馈更新。 |
| arxiv:2611.20976 | 排除 | experience_world_model | 更新业务语义和图经验；正文明确 Harness、LLM stack 与 prompts 固定。 |
| arxiv:2611.21056 | 纳入建议 | harness/evolve_main | ELITE 修改并跨代继承可执行 coding-agent scaffold；验收是实际编译、导入和执行协议 smoke checks。纳入边界必须注明没有下游任务成绩或候选任务轨迹反馈。 |
| arxiv:2611.21373 | 纳入建议 | harness/coevolution | 视觉 inspector 的 LoRA 与 Report/Ignore role-instruction skill cards 均有反馈更新；card 经 held-out recent calls 验收并在同步点发布，满足权重与 Harness 共演化。 |
| post:https://metr.org/notes/2026-11-16-measuring-alignment-eval-tells/ | 排除 | evaluation_benchmark | alignment-eval tells 的一般研究，不是 Harness 演化专项；不把模型识别测试环境等同自改。 |
| post:https://openai.com/ads/blog/chatgpt-ads-increases-its-market-presence | 排除 | off_topic | 广告 reseller 市场扩展公告，非 Harness/RSI 方法。 |
| post:https://openai.com/ads/customers/vistaprint | 排除 | off_topic | 广告投放客户案例，非 Harness/RSI 方法。 |
| post:https://openai.com/business/customer-stories/holiday-extras-dots | 排除 | off_topic | 主动报告和助手使用案例，不足以证明反馈改写自己的 Harness 工件。 |
| post:https://openai.com/business/customer-stories/revolut | 排除 | off_topic | 企业使用 Codex/ChatGPT 的案例，无自身 Harness 修改的验收及跨任务保留证据。 |
| post:https://openai.com/index/advancing-computer-use-for-healthcare-teams | 排除 | evaluation_benchmark | 医疗 computer-use 的一般表现、安全与成本评测，不是 Harness 演化专项。 |
| post:https://openai.com/index/astra-law-6-2 | 排除 | off_topic | research team 根据 practitioner feedback 调整设置/指令与索引，属于人类研发改进，不是已验证自主 Harness 演化。 |
| post:https://openai.com/index/expanding-chatgpt-for-academic-researchers | 排除 | off_topic | 研究人员访问资助计划，非 Harness 自改方法。 |
| post:https://openai.com/index/introducing-chatgpt-for-sales | 排除 | off_topic | 销售插件和 ready-to-use workflows 产品发布，无执行反馈改写自身流程并保留的证据。 |
| post:https://openai.com/index/introducing-gpt-6-2-astra-sol | 排除 | model_weights | 模型发布及通用职业任务 benchmark，无反馈改写并保留自身 Harness 的实证链。 |
| post:https://openai.com/index/introducing-openai-for-chile | 排除 | off_topic | 公共部门 AI 采用、人才与创业支持合作公告，非 RSI/Harness 方法。 |
| post:https://openai.com/index/lvmh-media-division-partnership | 排除 | off_topic | 媒体合作和企业 AI 部署公告，非 RSI/Harness 方法。 |
| post:https://openai.com/index/more-ways-to-move-care-forward-with-chatgpt-for-healthcare | 排除 | off_topic | 医疗产品、clinical search 与 plugins 更新，无自身 Harness 反馈演化证据。 |
| post:https://openai.com/index/our-first-phase-of-embedded-assessments | 排除 | safety_governance | 第三方 alignment/safeguards 评估计划，未针对 Harness 演化展开专项方法。 |
| post:https://openai.com/index/science-at-the-frontier | 排除 | evaluation_benchmark | 科研用户使用分析和问卷，不是系统根据反馈持久改写 Harness 的研究。 |
| post:https://openai.com/index/strengthening-nato-allied-cyber-defences-ai | 排除 | safety_governance | 网络防御模型部署、授权使用与人员培训案例，未报告 Harness 自改闭环。 |
| post:https://openai.com/index/strengthening-online-child-safety | 排除 | safety_governance | 安全检测分类器、支持与合作发布，无 Harness 演化链。 |
| post:https://openai.com/index/the-kings-trust-and-openai | 排除 | off_topic | 捐赠与年轻人技能培训计划，非 Harness/RSI 方法。 |
| post:https://sakana.ai/jfinbench/ | 排除 | ai4ai | 试验特定转换代码生成金融 benchmark 数据，是外部数据构建产物；共用转录脚本固定，不是自身 Harness 演化。 |
| s2:4fe67f25512c1f8580168b21b26c921b42b22a94 | 待补 | theory_survey | Semantic Scholar metadata 两次实际请求均 429；未取得 DOI/官方全文，不能由摘要确认身份和 Harness 专题范围。 |

## 可恢复文件

- `review-findings.json`：51 条来源、日期、分类、反馈与持久性、反证、摘要与逐项待补。
- `input-records.json`：冻结输入与原始文件哈希；`canonical-existing-bindings.json`：历史日期绑定。
- `source-index.json`、`source-supplement-receipt.json`：实际免费请求及补充验证回执。
- `file-manifest.json`：本子任务全部原文与报告文件的可恢复 SHA。
- `validation-receipt.json`：唯一 ID、正文/文本哈希、所有引句、双语数字守卫检查。
