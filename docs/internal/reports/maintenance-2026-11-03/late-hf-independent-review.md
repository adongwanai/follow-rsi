# 11 月 2 日 HF 晚到条目：独立复审

复审日期：2026-11-03（Asia/Shanghai）。HF 推荐归期：**2026-11-02**。本批正式决定均为 **defer**；以下均为范围建议，不是人工批准、审核闸门通过或发布。

4 篇正文复审：建议纳入 2 篇，排除当前 Harness 专题 2 篇；与主审范围建议 4/4 一致。另有目的抽查 3/18 条摘要排除建议，3/3 支持原建议；其余 15 条不在本轮独立抽查范围。

| 论文 | 官方 v1 原始日期（UTC） | Harness 范围建议 | 关键界线 |
| --- | --- | --- | --- |
| MemSteer · 2610.39276 | 2026-10-29T03:28:49Z | 建议纳入 | 建议纳入 MemSteer-Opt：变化的是存储、检索和上下文构建的记忆管理设计。执行失败诊断驱动设计提案，验证集决定是否替换；接受的设计进入后续轮次，并可冻结后跨基准、跨用户复用。不能只依据合成 QA 或新增记忆条目收录。 |
| REA · 2610.42053 | 2026-10-30T17:18:13Z | 排除当前专题 | 建议排除当前 Harness 自进化专题。论文的核心是异步执行、预先拟合的候选路由表和固定恢复机制；开发反馈确实用于统计和路由，策略也跨 episode 复用，但没有建立 REA 自身自动修订并保留外部程序工件的闭环。 |
| SketchDirector · 2610.41260 | 2026-10-30T05:05:12Z | 排除当前专题 | 建议移到经验记忆相关方向，不计入 Harness。布局程序的反馈修正针对当前画布；跨场景保留的是成功布局经验，按既定 Jaccard 规则检索。未建立操作库、检索机制或其他持久 Harness 程序的修改。 |
| GEPA-Curator · 2610.37651 | 2026-10-27T17:58:11Z | 建议纳入 | 建议纳入任务与证据选择方向：策展器选择任务和历史成功轨迹，为反思式 prompt 修改提供证据；新 prompt 进入后续 checkpoint。§5.3 还明确把这一机制接入 Harness 代码优化。策展器固定不妨碍其所优化的外部工件演化，但不能宣称改进器自身演化。 |

## 来源与日期核验

验证了 8 份已保存官方响应的 HTTP 200 回执、SHA-256 和字节数；4 篇标题、稳定 ID、v1 submission history 均相符。HF 原始响应包含 38 个唯一成员，本批 4 篇及 3 篇抽查项均在 11 月 2 日榜单中。11 月 3 日只是本次补采与复审日。

- HF 原始响应：`build/maintenance-primary-2026-11-03/hf-2026-11-02.json`，SHA-256 `07edcacf5b2600542e81b8545732780aad9dcf3e4b333185dc9c5100a734b094`。
- 官方回执清单：`build/maintenance-primary-2026-11-03/late-primary-attempts.json`；抓取时间与每个响应哈希见 JSON。
- 3 篇摘要抽查仅使用 HF 返回的原始 `paper.summary`；没有读取其官方全文，不把 HF 的 `publishedAt` 提升为已独立验证的原始发表/版本日期。
- 先读来源形成结论再比对主审；共享工作区材料可见，不声称盲审。

## MemSteer：建议纳入

建议纳入 MemSteer-Opt：变化的是存储、检索和上下文构建的记忆管理设计。执行失败诊断驱动设计提案，验证集决定是否替换；接受的设计进入后续轮次，并可冻结后跨基准、跨用户复用。不能只依据合成 QA 或新增记忆条目收录。

- **修改对象**：模型外的存储组织、索引、检索与上下文构建流程；不是历史记录内容本身。
- **执行反馈**：用训练题执行结果和来源证据定位存储、检索、回答阶段的失败，提供给设计 proposer。
- **接受机制**：§3.3 的 A(d′)>A(d_t) 决定是否替换；不提高则保留当前设计。这里未重算准确率。
- **跨轮次/任务保留**：接受后重跑训练集形成下一轮诊断；§4.3 明确冻结 ATM-Bench 设计后用于 RHELM，且有来源用户之外的迁移。

**可核验引文**

- [S3.SS3.SSS0.Px1.p1.1](https://arxiv.org/html/2610.39276v1#S3.SS3.SSS0.Px1.p1.1)："MemSteer-Opt iteratively optimizes how historical records are organized into memory units and indexed" — 改管理流程而非仅填充历史内容。
- [S3.SS3.SSS0.Px1.p2.3](https://arxiv.org/html/2610.39276v1#S3.SS3.SSS0.Px1.p2.3)："We hold the answering model, its instruction prompt, and the final context budget fixed across designs." — 回答模型、提示和最终上下文预算固定。
- [S3.SS3.SSS0.Px3.p1.1](https://arxiv.org/html/2610.39276v1#S3.SS3.SSS0.Px3.p1.1)："using the diagnosed failures to guide changes to storage, retrieval, or context construction." — 失败诊断指导外部设计修改。
- [S3.SS3.SSS0.Px3.p1.1](https://arxiv.org/html/2610.39276v1#S3.SS3.SSS0.Px3.p1.1)："We rebuild the memory under each valid candidate and evaluate its accuracy on the fixed validation set." — 候选重新构建并接受固定验证集评价。
- [S3.SS3.SSS0.Px3.p1.1](https://arxiv.org/html/2610.39276v1#S3.SS3.SSS0.Px3.p1.1)："After accepting a revision, we rerun the updated system on the training set to refresh the failure diagnoses and sampled feedback for the next iteration." — 保留修改并形成下一轮反馈。
- [S4.SS3.p2.1](https://arxiv.org/html/2610.39276v1#S4.SS3.p2.1)："We freeze the design optimized with generated ATM-Bench QA and apply it to RHELM records without target-domain optimization." — 明确有冻结设计跨基准复用。
- [abstract1.1](https://arxiv.org/html/2610.39276v1#abstract1.1)："without updating model parameters" — 作者明确不更新模型参数。

**反证与边界**

- 监督 QA 是 LLM 生成的，不等于人工认证；论文限制部分承认共享错误和可搜索设计空间的限制。
- 纳入依据是管理机制优化。没有检查发布代码或重跑实验，也未验证所有改动的因果贡献、成本公平性或普遍泛化。

下一步：人工确认范围；若制作完整证据卡，再核对代码中的设计差异、验证/测试隔离与成本设置。

## REA：排除当前 Harness 专题

建议排除当前 Harness 自进化专题。论文的核心是异步执行、预先拟合的候选路由表和固定恢复机制；开发反馈确实用于统计和路由，策略也跨 episode 复用，但没有建立 REA 自身自动修订并保留外部程序工件的闭环。

- **修改对象**：LIBERO 中候选是冻结的 Python 控制程序；按开发成功率/成本生成路由表，测试阶段查表。RoboTwin 的扩展主要是成功率预测 head。
- **执行反馈**：开发执行反馈用于候选排序；运行时 judge/exception 用于本 episode 的停止或切换。存在反馈，不能写成没有反馈。
- **接受机制**：路由表与恢复 ladder 评测前确定。最终 verdict 只记录；不是候选 Harness 改版的接受门。
- **跨轮次/任务保留**：策略库和路由统计保留复用，但所核查方法没有将任务执行失败转成新的可复用路由/验证程序版本。

**可核验引文**

- [S3.SS1.SSS0.Px1.p1.1](https://arxiv.org/html/2610.42053v1#S3.SS1.SSS0.Px1.p1.1)："On LIBERO-Pro they are frozen Python programs written by coding agents" — 控制程序在该实验中冻结。
- [S3.SS2.SSS0.Px1.p1.1](https://arxiv.org/html/2610.42053v1#S3.SS2.SSS0.Px1.p1.1)："Before evaluation, the router runs each candidate" — 承认开发阶段真实执行反馈。
- [S3.SS2.SSS0.Px1.p1.1](https://arxiv.org/html/2610.42053v1#S3.SS2.SSS0.Px1.p1.1)："at test time dispatch is a lookup" — 测试路由是查表。
- [A2.SS1.p1.1](https://arxiv.org/html/2610.42053v1#A2.SS1.p1.1)："Route memory fixes the ladder before the reset." — 恢复顺序在 episode 前确定。
- [A2.SS1](https://arxiv.org/html/2610.42053v1#A2.SS1)："the verdict after the last run is only logged." — 最终反馈不被写成新 Harness 版本。
- [S4.SS1.SSS0.Px2](https://arxiv.org/html/2610.42053v1#S4.SS1.SSS0.Px2)："ASPIRE Fix loop and Evo search" — 外部候选生成含演化方法，未漏读该反证。
- [A3.SS1.SSS0.Px2.p1.1](https://arxiv.org/html/2610.42053v1#A3.SS1.SSS0.Px2.p1.1)："The mixed configuration adds a linear code-policy head, trained with binary cross-entropy on execution success/failure labels" — 区分预测 head 的权重训练。
- [A3.SS1.SSS0.Px2.p1.1](https://arxiv.org/html/2610.42053v1#A3.SS1.SSS0.Px2.p1.1)："Later completed calibration scenes are not used to refit this checkpoint." — 报告 checkpoint 未随之后校准场景继续更新。
- [A3.SS1.SSS0.Px2.p1.1](https://arxiv.org/html/2610.42053v1#A3.SS1.SSS0.Px2.p1.1)："caches that choice for the entire episode" — 这一扩展在当前 episode 固定所选策略。

**反证与边界**

- 已核对外部 ASPIRE Fix/Evo 的程序生成/演化来源。这说明候选来源可能演化，不能据此把 REA runtime 本身认作自演化。
- 开发统计形成持久 route memory 是正面反证；排除依据是工件修改闭环未建立，不是必须在线改进，也不是否认离线优化。
- RoboTwin 有 selector/head 训练，不能仅因有权重训练而排除；正文未建立外部 Harness 与权重的共同反馈迭代。
- 固定评测框架并非天然排除，但本文主要比较具身控制和路由位置，未证明是 Harness 工件演化的专项评测。

下一步：若后续版本或代码展示 REA 根据反馈修订长期控制流、验证器或技能文件，并在后续任务沿用，应重审；本次不据此设想补全。

## SketchDirector：排除当前 Harness 专题

建议移到经验记忆相关方向，不计入 Harness。布局程序的反馈修正针对当前画布；跨场景保留的是成功布局经验，按既定 Jaccard 规则检索。未建立操作库、检索机制或其他持久 Harness 程序的修改。

- **修改对象**：执行六种预设操作生成/修订外部场景布局，另外积累成功场景经验条目。
- **执行反馈**：几何和视觉语义检查触发当前布局重写；失败记录引导该场景下一次规划。
- **接受机制**：验证条件接受的是布局产物，短期失败记录在成功后丢弃。
- **跨轮次/任务保留**：长期成功经验明确跨场景复用；因此不能给整个方法贴 not_persistent。保留的是内容经验，尚非管理机制的新版本。

**可核验引文**

- [S3.SS2.p1.1](https://arxiv.org/html/2610.41260v1#S3.SS2.p1.1)："An action is selected from six primitive operations:" — 动作库预先定义。
- [S3.SS3.SSSx2.p12.1](https://arxiv.org/html/2610.41260v1#S3.SS3.SSSx2.p12.1)："Only layouts satisfying all verification criteria are accepted." — 接受门作用于布局。
- [S3.SS3.SSSx3.p2.1](https://arxiv.org/html/2610.41260v1#S3.SS3.SSSx3.p2.1)："These records are discarded after successful correction and are only used within the current scene generation process." — 短期失败轨迹仅用于当前场景。
- [S3.SS3.SSSx3.p3.1](https://arxiv.org/html/2610.41260v1#S3.SS3.SSSx3.p3.1)："The Long-Term Experience Memory stores successful layout experiences indexed by the corresponding object set." — 明确承认成功经验长期存储。
- [S3.SS3.SSSx3.p3.1](https://arxiv.org/html/2610.41260v1#S3.SS3.SSSx3.p3.1)："relevant experiences are retrieved by measuring the Jaccard similarity between the current object set and historical object sets" — 检索采用既定对象集合相似度。
- [S3.SS3.SSSx3.p5.1](https://arxiv.org/html/2610.41260v1#S3.SS3.SSSx3.p5.1)："this experience is retrieved and provided to the agent as a reference for subsequent layout planning." — 跨场景复用的是参考经验。

**反证与边界**

- 作者使用 self-evolving correction 的措辞，而且确有跨场景经验，已作为反证核查；名称和持久记忆本身不足以构成 Harness。
- 可执行 scene program 是绘图任务产物，不能未经证据当成长期可调用工具或技能文件。
- 所读段落未明确冻结所有模型参数，保留 unknown；排除结论不依赖推断冻结状态。

下一步：如要纳入 Harness，需提供反馈改写动作实现、记忆管理程序或可复用技能，并作为后续版本保留的正文/代码证据。

## GEPA-Curator：建议纳入

建议纳入任务与证据选择方向：策展器选择任务和历史成功轨迹，为反思式 prompt 修改提供证据；新 prompt 进入后续 checkpoint。§5.3 还明确把这一机制接入 Harness 代码优化。策展器固定不妨碍其所优化的外部工件演化，但不能宣称改进器自身演化。

- **修改对象**：主实验修改外部 prompt；Meta-Harness-Curator 扩展修改父 Harness 的代码。
- **执行反馈**：actor 执行任务并产生评价/轨迹，反思器结合失败与成功参考改写 prompt；代码扩展重新执行父版本后据反馈修订。
- **接受机制**：greedy 变体每次 mutation 都成为下一 checkpoint；定期验证并最终选验证集最佳。不能套用每步只接受上涨的规则。
- **跨轮次/任务保留**：同一 lineage 的更新进入后续步骤；代码扩展保留父子及历史，最终按开发集选版本用于测试。

**可核验引文**

- [S3.p1.1](https://arxiv.org/html/2610.37651v1#S3.p1.1)："returns an updated prompt, task-level agent trajectories, and evaluation results" — 直接修改外部 prompt。
- [S3.p2.1](https://arxiv.org/html/2610.37651v1#S3.p2.1)："leaving the optimizer itself unchanged." — 不能宣称固定策展包装使优化器自身改写。
- [S4.SS1.p1.1](https://arxiv.org/html/2610.37651v1#S4.SS1.p1.1)："maintains a single lineage in which each mutation becomes the next checkpoint." — 新 prompt 在后续 checkpoint 复用。
- [S4.SS1.p1.1](https://arxiv.org/html/2610.37651v1#S4.SS1.p1.1)："select the final model based on the best validation score at the end." — 最终按验证集选，不是每步上涨准入。
- [S5.SS3.SSS0.Px1.p1.1](https://arxiv.org/html/2610.37651v1#S5.SS3.SSS0.Px1.p1.1)："the optimizer revises it using the resulting feedback and the Curator’s rationale." — Harness 代码扩展据新执行反馈修改。
- [S5.SS3.SSS0.Px1.p1.1](https://arxiv.org/html/2610.37651v1#S5.SS3.SSS0.Px1.p1.1)："Each child is evaluated on the same tasks as its parent and on the full development set, regardless of whether its training score improves." — 代码子版本不因训练涨跌免除开发集评价。
- [S5.SS3.SSS0.Px1.p1.1](https://arxiv.org/html/2610.37651v1#S5.SS3.SSS0.Px1.p1.1)："the candidate with the highest development score is selected for final test evaluation." — 按开发表现选后续测试版本。

**反证与边界**

- Curator 的任务历史和成功轨迹检索是固定的外层机制；不能仅凭它有记忆称为 improver 自进化。
- 材料明确优化 prompt/代码，但所选段落没有声明所有模型参数冻结；保留 unknown，不将固定部署模型名当作冻结证明。
- 正文接受机制与原始 GEPA 不同。代码扩展对 child 同时评任务与开发集，并非训练分上涨才评测。
- 未检查实现、重跑实验或复算费用；本文搜索结果不能在此被升级为稳健/同预算优势结论。

下一步：人工确认任务与证据选择分类；完整证据卡需另核对实验重复、成本及开发集反复使用的边界。

## 摘要排除项抽查

这 3 项均为摘要级范围建议，正式决定保持 defer，原始日期和版本保持 unknown。

### QCP · arxiv:2610.37393

有真实反馈迭代，但摘要指向轨迹重标注和机器人策略微调。不能因出现 iterative、online rollouts 就列作 Harness；当前摘要未建立外部程序工件共同演化。

- 抽样目的：抽查有多轮反馈的负例，防止把存在反馈直接等同于 Harness。
- 原文："relabels the accumulated trajectories in hindsight according to their measured quality, and fine-tunes the policy."
- 定位：`build/maintenance-primary-2026-11-03/hf-2026-11-02.json` 的 `/34/paper/summary`，逐字匹配。
- 结论：支持原摘要排除建议；不声称已排除全文可能存在的协同演化或专项评测证据。

### rTaste · arxiv:2610.40488

研究对象是科研实验的提出、预测和排序判断。摘要提到 evaluation harness，但没有把外部 Harness 的反馈改写作为被测变量；一般研究能力评测不等于 Harness 专项评测。

- 抽样目的：抽查含 evaluation harness 术语的负例，防止名词匹配和泛评测误收。
- 原文："Each model, working as a research agent alone or as a team, proposes minimum viable experiments (MVEs), forecasts whether each will pass a threshold it sets and ranks them."
- 定位：`build/maintenance-primary-2026-11-03/hf-2026-11-02.json` 的 `/32/paper/summary`，逐字匹配。
- 结论：支持原摘要排除建议；不声称已排除全文可能存在的协同演化或专项评测证据。

### LARC · arxiv:2610.42149

self-evolves latent reasoning 指向 SFT/RL 训练模型内部表示。摘要未给外部提示、工具、技能或控制流改写证据；不把测试时扩展直接解释成程序性自进化。

- 抽样目的：抽查含 self-evolves 的权重研究，防止把关键词当作范围证据。
- 原文："the training framework consists of two stages: (i) curriculum supervised fine-tuning (SFT), and (ii) information-gain reinforcement learning (RL)."
- 定位：`build/maintenance-primary-2026-11-03/hf-2026-11-02.json` 的 `/6/paper/summary`，逐字匹配。
- 结论：支持原摘要排除建议；不声称已排除全文可能存在的协同演化或专项评测证据。

## 验证边界

本轮校验 29 条正文引句与 3 条摘要引句，4 份官方身份/版本记录、8 份官方响应完整性和 HF 原始成员归期。没有修改主数据、人工决定、网站发布或既有冻结报告；没有新网络/付费请求、实验复现或测试套件运行。

主审报告：`docs/internal/reports/maintenance-2026-11-03/late-hf-primary-review.json`。摘要筛查：`docs/internal/reports/maintenance-2026-11-03/late-hf-screen.json`。逐条来源、反证与 SHA-256 见同名 JSON。
