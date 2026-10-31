# RSIHub 与 HarnessDev 原文审查（2026-10-30）

> 阶段存档：本报告覆盖 RSIHub、HarnessDev；“建议必读”为审查建议，不能当作 owner 接受或发布授权。当前 RSIHub 目录 must_read=false。四篇日期及分类见 [INDEX](INDEX.md)。

范围：官方元数据、正文与表格、公开代码，以及 Sarah Eze《为什么 AI 还不会自我进化》中涉及这两篇的说法。署名保留 Sarah Eze。

结论：可形成有边界的证据卡片；文章有口径需要修正。此报告不是实验复现或跨模型家族的审计 PASS。

## 关键修正

- RSIHub sealed 列分母是全基准题数，不是 sealed 内部题数。
- HarnessDev 的 3/4 回退是四条全程 fixed-Gemini 的独立演化线，不是直接迁移演化完成产物。
- +7.2 / +0.5 是九条线的派生均值，混合 5 self 与 4 fixed，且两列题集不同。
- Banking + Codex 仍有 +4.2 至 +9.3，不能概括为强 Agent 的收益消失。
- 53.1% 不等于随机无异；噪声带内收益不等于真实效应为零。

## 审查方法与边界

1. Official metadata/HTML/PDF/project identity and method reading.
2. Visual PDF cover and table checks (RSIHub p8, HarnessDev p12); numbers, denominators, repetitions, limits.
3. Public code inspection; quote-substring and source-hash validation; derived arithmetic; catalog schema.

- Source-supported is not independently reproduced: no original experimental raw dataset and no LLM evolution rerun.
- Same-family agent review; parent independent review must reconcile before publication.
- Current code HEAD may differ from paper locked experiment commit.
- Must-read is a review recommendation, not an owner decision. Unknown evidence stays unknown.

## 元数据与分类

### RSIHub: A Composable Framework for Agent-Evolution Methods

- arXiv 2610.32253 v1；提交 2026-10-23T07:06:07Z；PDF 封面 2026-10-22。
- 作者：Zimu Wang, Xiaobo Wang, Siyu Ye, Jiaqi Li, Silin Chen, Yuling Shi, Ruobing Wang, Jingjing Zhang, Chaofan Wang, Kai Wu, Mengnan Qi, Kai Cai, Xiaodong Gu, Zilong Zheng。
- 机构：University of California, Berkeley；University of Science and Technology of China；Douyin Group；Shanghai Jiao Tong University；Tongji University；Beijing Institute for General Artificial Intelligence；Simple Agent Lab。
- 建议分类：harness_eval / evaluation / framework；建议必读。
- 中文：用于实现和比较 Harness 演化方法的开源框架：以 recipe 和算子接入 AHE、Hyperagents、A-Evolve、GEPA，保护评估边界并保存候选谱系；在同一底模下比较 MiniSWE 与 Codex，并保留 sealed 任务检验泛化。
- English: An open-source framework for implementing and comparing harness-evolution methods. Recipes compose AHE, Hyperagents, A-Evolve, and GEPA with protected evaluation and candidate lineage; experiments compare MiniSWE and Codex under the same underlying model with separate sealed tasks.
- 结果：TB2 + MiniSWE 中 Hyperagents 与 A-Evolve 从 56.2 到 69.7（+13.5 个百分点）；排名与留出收益随设置变化。效果为单次点估计，split 列按全基准任务数作分母，未确认完整匹配 token 预算。

### HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?

- arXiv 2609.01437 v1；提交 2026-09-01T15:45:33Z；PDF 封面 2026-09-02。
- 作者：Yuhao Wu, Jingyuan Zhang, Jiajun Shi, Xinping Lei, Qingshui Gu, Yuxuan Zhang, Zexuan Wang, Chen He, Chen Huang, Maojia Song, Zhiyuan Zeng, Shaowen Wang, Jinkai Liu, Yunfeng Shi, Jiaheng Liu, Shen Yan, Wenhao Huang, Ge Zhang, Wenxuan Zhang。
- 机构：ByteDance Seed；Singapore University of Technology and Design；Georgia Institute of Technology；M-A-P；TokenWave.AI。
- 建议分类：harness_eval / evaluation / benchmark；建议必读。
- 中文：评测模型在权重固定时创建与迭代修改可复用 Harness 的能力。Creation 覆盖六个模型、五个基准；Evolution 根据反馈集修改代码，再冻结版本评估 630 道 SWE-Pro 留出题，并区分创建者与执行器。
- English: Evaluates creation and iterative revision of reusable harnesses with weights fixed. Creation covers six models and five benchmarks; Evolution uses visible feedback before frozen artifacts are evaluated on 630 held-out SWE-Pro tasks, separating creator and executor roles.
- 结果：五条 self-runtime 轨迹的留出增益为 +1.43 至 +4.44 个百分点（均值 +3.11）；四条全程固定 Gemini 的轨迹中三条退步。每个创建者–执行器组合仅一条演化线，未做匹配搜索预算对照，成本不含完整开发开销。

## 逐项核对与替换句

### RH-01 · supported

RSIHub 与 Harness RSI 有关。

固定模型配置，反馈驱动持久的外部软件修改，候选形成可复用谱系。框架支持 core 演化机制；本仓库按 owner 要求定位 harness_eval（评测基础设施），不等于权重训练或其他大类别 RSI。报告结果只测固定 recipe，未实证外层 agent 递归修改改进过程。

> each iteration selects a candidate to extend, gathers evidence from its behavior, proposes and evaluates a revision, and retains the outcome for later search.
> — [§1](https://arxiv.org/html/2610.32253#S1.p1.1)，PDF p. 1, 2；RH-loop。

> The surface block declares the resources a candidate may change, allowing the same operator interfaces to support prompt-only and whole-harness studies.
> — [§3.1](https://arxiv.org/html/2610.32253#S3.SS1.p3.1)，PDF p. 4；RH-surface。

> All experiments use GPT-5.4 with high reasoning effort as the target model for both MiniSWE and Codex. Every recipe uses a Codex mutation agent backed by GPT-5.4 with xhigh reasoning effort.
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p3.1)，PDF p. 7；RH-models。

> The target, evaluator, runtime, data splits, and allowed mutable surface remain fixed; sealed tasks are excluded from adaptation feedback. Our experiments evaluate fixed recipes.
> — [§3.2](https://arxiv.org/html/2610.32253#S3.SS2.p3.1)，PDF p. 5；RH-fixed。

### RH-02 · supported

统一实例化 AHE、Hyperagents、A-Evolve、GEPA。

属于同一框架上的接口适配，不等于完全复现各原始工作的配置和结果。

> Exact correspondence with a source implementation also depends on its prompts, models, budgets, dependencies, and runtime adapters.
> — [§4.1](https://arxiv.org/html/2610.32253#S4.SS1.p3.1)，PDF p. 7；RH-adaptation。

> All experiments use GPT-5.4 with high reasoning effort as the target model for both MiniSWE and Codex. Every recipe uses a Codex mutation agent backed by GPT-5.4 with xhigh reasoning effort.
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p3.1)，PDF p. 7；RH-models。

### RH-03 · supported

TB2 + MiniSWE 最大 +13.5 个百分点。

表 1：56.2 → 69.7，Hyperagents 与 A-Evolve 并列，不是只由 Hyperagents 达到，也未建立重复运行后的稳定性。

> On Terminal Bench 2, every method improves the MiniSWE baseline by 7.8–13.5 percentage points; Hyperagents and A-Evolve reach the highest overall score of 69.7.
> — [§4.3 / Table 1](https://arxiv.org/html/2610.32253#S4.SS3.p2.1)，PDF p. 8；RH-tb2。

> These descriptive point estimates do not establish the stability of close differences without repeated runs.
> — [§4.3](https://arxiv.org/html/2610.32253#S4.SS3.p4.1)，PDF p. 8；RH-stability。

### RH-04 · supported

TB2 + Codex 增益 +0 至 +2.2。

限定 Terminal-Bench 2；MiniSWE 和 Codex 两者底模都为 GPT-5.4，不是跨底模测试。

> Gains are smaller from the stronger Codex baseline: AHE reaches 71.9 ( + 2.2 +2.2 points), Hyperagents and A-Evolve each add 1.1 points, and GEPA preserves the baseline.
> — [§4.3 / Table 1](https://arxiv.org/html/2610.32253#S4.SS3.p2.1)，PDF p. 8；RH-codex-tb2。

> All experiments use GPT-5.4 with high reasoning effort as the target model for both MiniSWE and Codex. Every recipe uses a Codex mutation agent backed by GPT-5.4 with xhigh reasoning effort.
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p3.1)，PDF p. 7；RH-models。

### RH-05 · corrected

MiniSWE 上 Hyperagents 第一，Codex 上 AHE 第一。

须限定基准，并列不能省略。

建议替换：在 Terminal-Bench 2 + MiniSWE 上，Hyperagents 与 A-Evolve 并列第一；在 τ³ Banking + MiniSWE 上，Hyperagents 最高。两个基准的 Codex 设置中，AHE 的总分最高。

> On Terminal Bench 2, every method improves the MiniSWE baseline by 7.8–13.5 percentage points; Hyperagents and A-Evolve reach the highest overall score of 69.7.
> — [§4.3 / Table 1](https://arxiv.org/html/2610.32253#S4.SS3.p2.1)，PDF p. 8；RH-tb2。

> Hyperagents gives the largest MiniSWE improvement, from 27.8 to 33.0, whereas AHE performs best with Codex, raising the overall score from 24.7 to 34.0. GEPA is close behind at 33.0.
> — [§4.3 / Table 1](https://arxiv.org/html/2610.32253#S4.SS3.p2.1)，PDF p. 8；RH-banking。

### RH-06 · corrected

Banking + MiniSWE 留出成功率下降 4.1 / 2.1 / 2.1。

数值正确，分母口径需修正；split 列用全 97 题作分母。

建议替换：在 τ³ Banking + MiniSWE 设置中，AHE、Hyperagents 和 GEPA 的 sealed 列分别下降 4.1、2.1、2.1 个百分点。表 1 这一列按全部 97 道任务作分母，表示留出任务对全基准 pass@1 的贡献；它不是 27 道留出任务内部的成功率。

> Terminal Bench 2 contains 89 tasks split into 50 train, 19 gate, and 20 sealed tasks; τ 3 \tau^{3} Banking contains 97 tasks split into 50 train, 20 gate, and 27 sealed tasks.
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p2.1)，PDF p. 7；RH-counts。

> each split column in Table 1 is its contribution to the full-benchmark score
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p2.1)，PDF p. 7；RH-denominator。

> On τ 3 \tau^{3} Banking, Hyperagents produces the largest overall gain from MiniSWE despite a 2.1-point sealed regression; AHE and GEPA also lose 4.1 and 2.1 points on sealed tasks.
> — [§4.3 / Table 1](https://arxiv.org/html/2610.32253#S4.SS3.p3.1)，PDF p. 8；RH-sealed。

### RH-07 · corrected

执行 Agent 越强，演化收益越小并几乎消失。

Banking + Codex 的 +4.2 至 +9.3 是反例，不能跨基准作因果概括。

建议替换：收益取决于基准、起始 Harness 和方法：Terminal-Bench 2 中 Codex 的增益较小，但 τ³ Banking 中 Codex 仍有 +4.2 至 +9.3 个百分点的提升，不能概括为执行 Agent 越强，演化收益越小。

> Hyperagents gives the largest MiniSWE improvement, from 27.8 to 33.0, whereas AHE performs best with Codex, raising the overall score from 24.7 to 34.0. GEPA is close behind at 33.0.
> — [§4.3 / Table 1](https://arxiv.org/html/2610.32253#S4.SS3.p2.1)，PDF p. 8；RH-banking。

> Gains are smaller from the stronger Codex baseline: AHE reaches 71.9 ( + 2.2 +2.2 points), Hyperagents and A-Evolve each add 1.1 points, and GEPA preserves the baseline.
> — [§4.3 / Table 1](https://arxiv.org/html/2610.32253#S4.SS3.p2.1)，PDF p. 8；RH-codex-tb2。

### RH-08 · corrected

各方法花的 token 没对齐。

可核实的是未报告完整匹配总 token 的对照；不能从报告缺失断言实际预算一定不相等。附录开销是框架时延，非完整 LLM 成本。

建议替换：论文固定了模型配置和最多 10 代等设置，但没有报告完整的匹配总 token 预算对照，也未给出包括演化在内的完整 LLM 成本。

> All recipes propose one child per generation, and evolution runs continue for at most 10 generations. The evolution results use static task sampling and one evaluation per task, while the capability-preservation controls use three independent repetitions.
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p4.1)，PDF p. 7；RH-repeats。

> instrumenting workspace initialization, candidate snapshotting, mutable-surface validation, evaluation recording, integrity verification, and recovery separately from model inference, benchmark execution, and mutation.
> — [Appendix B.2 / Table 5](https://arxiv.org/html/2610.32253#A2.SS2.p1.1)，PDF p. 16；RH-cost。

### RH-09 · supported

效果表单次运行；三次重复只用于执行保真控制。

控制实验不能证明演化增益显著或执行完全等价。

> All recipes propose one child per generation, and evolution runs continue for at most 10 generations. The evolution results use static task sampling and one evaluation per task, while the capability-preservation controls use three independent repetitions.
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p4.1)，PDF p. 7；RH-repeats。

> These controls characterize execution variability; they do not establish execution-mode equivalence or the statistical significance of the single-run evolution gains.
> — [§4.4](https://arxiv.org/html/2610.32253#S4.SS4.p2.1)，PDF p. 9；RH-controls。

### RH-10 · supported

评估边界与封存集受保护。

论文和当前公开代码支持冻结 evaluator 与非选择性 sealed anchor；不等于敌意代码隔离或完整安全审计。

> The target, evaluator, runtime, data splits, and allowed mutable surface remain fixed; sealed tasks are excluded from adaptation feedback. Our experiments evaluate fixed recipes.
> — [§3.2](https://arxiv.org/html/2610.32253#S3.SS2.p3.1)，PDF p. 5；RH-fixed。

> Sealed evaluation runs as a separate, non-selectable anchor.
> — [Appendix D.2](https://arxiv.org/html/2610.32253#A4.SS2.p2.1)，PDF p. 19；RH-anchor。

> RSIHub does not contain hostile code, so stronger deployments require independent attestation, isolation, and containment.
> — [§6](https://arxiv.org/html/2610.32253#S6.p1.1)，PDF p. 10；RH-security。

### RH-11 · corrected

框架中搜索、选择、最终评估永远三个不重叠集合。

论文实验有三个分区；通用框架允许 gate 与 train 重合。

建议替换：RSIHub 本次实验使用 train、gate、sealed 三个分区，并把 sealed 排除在修改反馈之外；框架本身允许 gate 与 train 重合，不能把三者分离当作所有配置的强制保证。

> Terminal Bench 2 contains 89 tasks split into 50 train, 19 gate, and 20 sealed tasks; τ 3 \tau^{3} Banking contains 97 tasks split into 50 train, 20 gate, and 27 sealed tasks.
> — [§4.2](https://arxiv.org/html/2610.32253#S4.SS2.p2.1)，PDF p. 7；RH-counts。

> Gate tasks may coincide with training tasks; sealed tasks are reserved for held-out reporting.
> — [§3.2 Evaluate](https://arxiv.org/html/2610.32253#S3.I1.i6.p1.1)，PDF p. 5；RH-gate。

### RH-12 · unverified

公开代码足以复现 Table 1 数字。

公开 Apache-2.0 仓库已检查，但默认 AHE 是 30-task demo。未找到与 Table 1 对应的最终候选及每任务原始结果；未运行付费演化，不声称数值复现。

> We release RSIHub through Simple Agent Lab under Apache-2.0, with runnable recipes, reusable operators, documentation
> — [§1 Release](https://arxiv.org/html/2610.32253#S1.SS0.SSS0.Px1.p1.1)，PDF p. 3；RH-code。

> Exact correspondence with a source implementation also depends on its prompts, models, budgets, dependencies, and runtime adapters.
> — [§4.1](https://arxiv.org/html/2610.32253#S4.SS1.p3.1)，PDF p. 7；RH-adaptation。

### HD-01 · supported

HarnessDev 是 Harness 自进化评测。

权重固定，修改可运行外部 Harness 并跨任务复用；开发环境 D 固定，其递归自进化仍为未来工作。

> Changing this harness while holding model weights fixed can substantially alter task performance.
> — [Abstract](https://arxiv.org/html/2609.01437#abstract1.1)，PDF p. 1；HD-weights。

> The submitted artifact is a runnable harness that is frozen and then reused across downstream tasks.
> — [§3.1](https://arxiv.org/html/2609.01437#S3.SS1.p1.1)，PDF p. 4；HD-persistent。

> The development environment D D is held fixed across both stages;
> — [§6.1](https://arxiv.org/html/2609.01437#S6.SS1.p1.1)，PDF p. 15；HD-dev-fixed。

### HD-02 · corrected

从空壳开始，然后进行 10 轮评测。

起点弱但可运行，不是空仓库；10 是 H0 后完整双基准评估对的预算上限，未必跑满。

建议替换：从弱但可运行的 seed 搭建 Harness，再以最多 10 次 H0 后完整评估对为预算，依据 100 道 SWE-Pro 与 89 道 Terminal-Bench 的反馈修改；冻结后用未向开发者返回结果的 630 道 SWE-Pro 留出题评估。

> from a weak but runnable seed
> — [Figure 1](https://arxiv.org/html/2609.01437#S1.F1)，PDF p. 2；HD-seed。

> The controller provides a budget of ten post- H 0 H_{0} full-evaluation pairs.
> — [§3.2](https://arxiv.org/html/2609.01437#S3.SS2.SSS0.Px3.p2.1)，PDF p. 5；HD-budget。

> During development, it receives results from a fixed 100-task SWE-Pro feedback set and all 89 Terminal-Bench tasks.
> — [§3.2](https://arxiv.org/html/2609.01437#S3.SS2.SSS0.Px3.p1.1)，PDF p. 5；HD-feedback。

### HD-03 · corrected

平均反馈 +7.2，留出 +0.5。

表 6 报告 delta 无权平均得到 +7.1889 / +0.4933。须注明混合 5 self + 4 fixed 轨迹，两个分数用不同任务集，且无总体不确定性估计。

建议替换：按 HarnessDev 表 6 的 9 条演化线报告的增量作无权平均，反馈分约涨 7.2 个百分点，留出分约涨 0.5 个百分点。该统计混合了 5 条 self-runtime 和 4 条全程固定 Gemini 执行的轨迹；反馈分是 SWE-Pro-100 与 Terminal-Bench-89 的均值，留出分只来自 SWE-Pro-630。

> We run five self-runtime trajectories and four fixed-Gemini ablations, using the same creator, development environment, and starting harness.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px2.p2.1)，PDF p. 11, 12；HD-lineages。

> The feedback pair is the unweighted mean of the SWE-Pro-100 and Terminal-Bench-89 percentage scores; the held-out columns use only the SWE-Pro-630 tasks run afterwards.
> — [Table 6 caption](https://arxiv.org/html/2609.01437#S4.T6)，PDF p. 12；HD-table6-metrics。

> Evolution currently has one trajectory per creator–runtime cell and one unfinished main-runtime cell, and its post-freeze held-out evaluation covers SWE-Pro only, so the trajectories do not support uncertainty estimates or population-level comparisons.
> — [§6.1](https://arxiv.org/html/2609.01437#S6.SS1.p1.1)，PDF p. 15；HD-limitations。

### HD-04 · supported

64 次切换：2 次明确正向、27 次噪声带内增益、8 次双基准倒退。

分类总和 8+16+3+7+27+2+1=64；约 ±4.75 是反馈 pair-score 点数，不是任意单基准或通用置信区间。

> The nine lineages produce 73 official versions and 64 adjacent version switches;
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px2.p2.1)，PDF p. 12；HD-switchcount。

> Of the 64 official switches, eight regress on both benchmarks, 16 show a single-benchmark regression, three show a cross-benchmark trade-off, seven produce no measurable change, 27 report gains that remain inside the repeated-run noise band, two have clear positive evidence beyond the noise band, and one contains no executable code change.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p1.1)，PDF p. 13；HD-switch-types。

> The same commit can vary by about ± 4.75 \pm 4.75 pair-score points, so small gains cannot be attributed to code changes from score alone.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p1.1)，PDF p. 13；HD-noise。

### HD-05 · corrected

53.1% 与抛硬币差不多。

34/64=53.125%，四舍五入成立；未报告对随机水平的显著性或等价检验。

建议替换：64 次可比切换中，反馈与留出同向变化只有 34 次（53.1%），接近一半；这不能直接推出与随机选择没有差别。

> feedback and held-out scores move in the same direction only 34 times ( 53.1 % 53.1\% ), and only 2/9 declared versions are held-out optimal.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p2.1)，PDF p. 13；HD-agreement。

> Evolution currently has one trajectory per creator–runtime cell and one unfinished main-runtime cell, and its post-freeze held-out evaluation covers SWE-Pro only, so the trajectories do not support uncertainty estimates or population-level comparisons.
> — [§6.1](https://arxiv.org/html/2609.01437#S6.SS1.p1.1)，PDF p. 15；HD-limitations。

### HD-06 · supported

只有 2/9 声明最终版本为各线留出最优。

表 6 两个 final gap=0；留出分未参与编辑、停止和最终选择。

> feedback and held-out scores move in the same direction only 34 times ( 53.1 % 53.1\% ), and only 2/9 declared versions are held-out optimal.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p2.1)，PDF p. 13；HD-agreement。

> The final gap is the best held-out score of a lineage minus the score of its declared version.
> — [Table 6 caption](https://arxiv.org/html/2609.01437#S4.T6)，PDF p. 12；HD-table6-gap。

> These scores are never shown to the creator and cannot affect editing, stopping, or final version selection.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px2.p3.1)，PDF p. 12；HD-no-selection-leak。

### HD-07 · corrected

生成最好均分 67.8 对人类 86.2。

数值正确；平均排除 MLE；人工参考是 Harness+各自底模系统，不是人的能力或统一执行器受控对照。

建议替换：Creation 表中，Opus 4.8 生成 Harness 的四基准平均分为 67.8，所选人工工程系统参考为 86.2；均值不包含 MLE-bench，参考系统也使用各自配套模型，因此不能把差值全归因于 Harness。

> Avg. is the unweighted mean over SWE-Pro, Terminal-Bench, EQ-Bench3, and BrowseComp.
> — [Table 3 caption](https://arxiv.org/html/2609.01437#S4.T3)，PDF p. 8；HD-average。

> Human-reference results are verified public system results rather than paired controls under one executor;
> — [§4.1](https://arxiv.org/html/2609.01437#S4.SS1.p2.1)，PDF p. 7；HD-human-reference。

### HD-08 · corrected

84.6 对 83.7，32.9 对 24.0，52.4 对 92.2。

表 3 Opus vs 选定系统参考正确；BrowseComp 的 52.4 非所有模型最高，GPT-5.5 为 52.6。

建议替换：以 Opus 4.8 生成的 Harness 为例，EQ-Bench3 为 84.6 对参考系统 83.7，MLE-bench 为 32.9 对 24.0，BrowseComp 为 52.4 对 92.2。GPT-5.5 的 BrowseComp 为 52.6，略高于 Opus。

> Avg. is the unweighted mean over SWE-Pro, Terminal-Bench, EQ-Bench3, and BrowseComp.
> — [Table 3 caption](https://arxiv.org/html/2609.01437#S4.T3)，PDF p. 8；HD-average。

> Human-reference results are verified public system results rather than paired controls under one executor;
> — [§4.1](https://arxiv.org/html/2609.01437#S4.SS1.p2.1)，PDF p. 7；HD-human-reference。

### HD-09 · corrected

换成 Gemini 后 3/4 倒退说明演化产物跨模型迁移失败。

三退一进来自从 H0 开始便全程 fixed-Gemini 的独立演化；RQ1 frozen re-execution 才是直接迁移对照。

建议替换：另四条从头到尾固定 Gemini 执行的独立演化线中，只有 Opus 的声明版本相对各自 H0 在留出集上提高，其余三条退步，GPT-5.5 下降 10.32 个百分点。这不是将 self-runtime 最终演化产物直接换模型的实验。

> We run five self-runtime trajectories and four fixed-Gemini ablations, using the same creator, development environment, and starting harness.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px2.p2.1)，PDF p. 11, 12；HD-lineages。

> Under fixed Gemini, however, only Opus improves and the other three regress.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p2.1)，PDF p. 13；HD-fixed-gains。

> Every creator harness is executed by Gemini 3.1 Pro.
> — [Table 4 caption](https://arxiv.org/html/2609.01437#S4.T4)，PDF p. 8；HD-frozen-transfer。

> its Self-Eval SWE-Pro score falls from 69.3 to 33.0 under Gemini, and its Writing score falls from 84.6 to 74.2.
> — [§4.2](https://arxiv.org/html/2609.01437#S4.SS2.SSS0.Px4.p1.1)，PDF p. 11；HD-transfer-example。

### HD-10 · corrected

模型几乎不看失败轨迹，接口仅两次。

专用接口两次和显式检查 0.5%–40.2% 正确；同段还说使用自定义脚本与 probes，不能等同于没有其他诊断。

建议替换：专用轨迹接口只调用两次，不同演化线显式检查的案例占 189 道反馈题的 0.5%–40.2%；模型也使用自定义脚本和小规模探测，这个接口计数不能代表全部诊断活动。

> the dedicated trajectory interface is called only twice, and explicitly inspected cases cover just 0.5 % 0.5\% – 40.2 % 40.2\% of the 189 feedback tasks, depending on the lineage.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px3.p2.1)，PDF p. 12；HD-diagnostic。

> Creators instead rely on custom scripts and small probes, both of which can disagree with the full evaluation;
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px3.p2.1)，PDF p. 12；HD-custom-probes。

### HD-11 · supported

成本未算全。

只报告执行 token；创建/修改开销排除，RQ2 还明确排除 creator/judge/probe。

> Execution cost is reported as both the total and the mean per task; tokens used by the creator to build or modify the harness are excluded.
> — [§3.5](https://arxiv.org/html/2609.01437#S3.SS5.p1.1)，PDF p. 7；HD-cost。

> Creator, judge, and probe tokens are excluded.
> — [Appendix B / Figure 10](https://arxiv.org/html/2609.01437#A2.F10)，PDF p. 24；HD-token-exclusions。

### HD-12 · corrected

小于噪声的提升等于没有。

无法可靠归因不等于真实效应为零。

建议替换：落在重复运行噪声带内的提升，不能仅凭单次分数确认来自代码修改；这不等于证明真实收益为零。

> The same commit can vary by about ± 4.75 \pm 4.75 pair-score points, so small gains cannot be attributed to code changes from score alone.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p1.1)，PDF p. 13；HD-noise。

### HD-13 · corrected

换题后都基本不涨。

五条 self-runtime 留出全正（+1.43 至 +4.44，均值 +3.11），不能用混合均值掩盖分组差异。

建议替换：五条 self-runtime 轨迹的留出增益均为正（+1.43 至 +4.44，平均 +3.11），四条全程固定 Gemini 的轨迹中三条退步；每格仅一条轨迹，尚不能证明总体稳定增益。

> All five self-runtime declarations improve over H 0 H_{0} on held-out tasks, with gains of + 1.43 +1.43 to + 4.44 +4.44 points and a mean gain of + 3.11 +3.11 .
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p2.1)，PDF p. 13；HD-self-gains。

> Under fixed Gemini, however, only Opus improves and the other three regress.
> — [§4.3](https://arxiv.org/html/2609.01437#S4.SS3.SSS0.Px4.p2.1)，PDF p. 13；HD-fixed-gains。

> Evolution currently has one trajectory per creator–runtime cell and one unfinished main-runtime cell, and its post-freeze held-out evaluation covers SWE-Pro only, so the trajectories do not support uncertainty estimates or population-level comparisons.
> — [§6.1](https://arxiv.org/html/2609.01437#S6.SS1.p1.1)，PDF p. 15；HD-limitations。

### HD-14 · supported

缺匹配搜索预算的朴素基线。

原文明确留为未来工作。每任务步骤/时间上限不等于对照多采样或顺序修正。

> matched-search evaluation remains future work.
> — [§5](https://arxiv.org/html/2609.01437#S5.SS0.SSS0.Px3.p1.1)，PDF p. 15；HD-matched。

### HD-15 · unverified

基准与最终演化 Harness 已公开。

官网仅有论文，官方 GitHub 账号列表只见网站仓库；附录仍说 will be released。不能把网站源码当基准代码。

> The reference seed implementation, the audit script, and the held-out task splits will be released with the benchmark.
> — [Appendix C](https://arxiv.org/html/2609.01437#A3.p3.1)，PDF p. 25；HD-code-status。

## HarnessDev 表 6 九行数据

增量单位为百分点；保留原表 delta，不用四舍五入端点相减替换。CSV / JSON 均已生成。

| 设置 | 创建者 | 反馈 H0→最终 | Δ | 留出 H0→最终 | Δ | 最终 gap |
|---|---|---:|---:|---:|---:|---:|
| self | Gemini 3.1 Pro | 59.9 → 68.7 | 8.8 | 48.89 → 51.59 | 2.70 | 0.00 |
| self | Opus 4.8 | 71.1 → 74.1 | 3.0 | 63.02 → 67.46 | 4.44 | 1.59 |
| self | Qwen 3.7 Max | 41.8 → 55.7 | 13.9 | 42.22 → 43.65 | 1.43 | 3.17 |
| self | DeepSeek V4 Pro | 47.2 → 60.6 | 13.4 | 47.30 → 50.48 | 3.17 | 1.75 |
| self | GPT-5.5 | 59.2 → 65.1 | 5.9 | 48.25 → 52.06 | 3.81 | 0.00 |
| fixed_gemini | Opus 4.8 | 58.8 → 68.6 | 9.7 | 48.10 → 50.79 | 2.70 | 2.54 |
| fixed_gemini | Qwen 3.7 Max | 62.1 → 63.2 | 1.1 | 49.52 → 48.41 | -1.11 | 1.11 |
| fixed_gemini | DeepSeek V4 Pro | 47.3 → 53.8 | 6.5 | 43.02 → 40.63 | -2.38 | 3.02 |
| fixed_gemini | GPT-5.5 | 56.6 → 59.1 | 2.4 | 42.22 → 31.90 | -10.32 | 16.51 |

- all_nine_feedback_delta: 7.188888888888888888888888889
- all_nine_heldout_delta: 0.4933333333333333333333333333
- self_five_feedback_delta: 9.0
- self_five_heldout_delta: 3.11
- fixed_four_feedback_delta: 4.925
- fixed_four_heldout_delta: -2.7775

## 证据字段建议

yes 表示该测试存在，不等于所有结果为正。

| 字段 | RSIHub | HarnessDev |
|---|---|---|
| held_out | yes | yes |
| matched_budget_baseline | unknown | no |
| cross_model_transfer | no | yes |
| cost_reported | unknown | partial |
| disjoint_evolution_set | partial | partial |
| reliability_metric | partial | partial |
| code_released | yes | unknown |
| evolved_harness_released | unknown | unknown |
| who_edits | external | external |
| feedback | ground_truth | ground_truth |
| timing | offline | offline |
| topology | unknown | chain |

### rsihub 字段说明

- held_out=yes: Sealed excluded from mutation feedback. (RH-counts, RH-fixed)
- matched_budget_baseline=unknown: No verified full compute/token-matched comparison with parallel sampling or sequential revision; unknown, not a claim actual budgets differ. (RH-repeats, RH-cost)
- cross_model_transfer=no: All target models GPT-5.4; MiniSWE/Codex are harnesses. (RH-models)
- cost_reported=unknown: Framework latency reported; full LLM inference/evolution cost not verified. (RH-cost)
- disjoint_evolution_set=partial: Sealed is separate, but overall headline includes train/gate. (RH-counts, RH-denominator)
- reliability_metric=partial: Three-repeat execution controls; evolution single-run. (RH-repeats, RH-controls)
- code_released=yes: Official Apache-2.0 repository inspected at recorded HEAD. (RH-code)
- evolved_harness_released=unknown: No paired final experiment artifacts located. (RH-adaptation)
- who_edits=external: Separate Codex mutation agent edits target; underlying same model is not same process. (RH-models)
- feedback=ground_truth: Experiment benchmark outcomes and trajectories. (RH-counts)
- timing=offline: Development before sealed evaluation. (RH-fixed, RH-anchor)
- topology=unknown: Framework policies vary, no single topology verified. (RH-loop)

### harnessdev 字段说明

- held_out=yes: SWE630 withheld from editing/stopping/selection. (HD-heldout, HD-no-selection-leak)
- matched_budget_baseline=no: Explicitly future work. (HD-matched)
- cross_model_transfer=yes: RQ1 directly reruns frozen harnesses under Gemini; yes denotes existence, not successful transfer. RQ2 fixed trajectories are separate. (HD-frozen-transfer, HD-transfer-example, HD-lineages)
- cost_reported=partial: Executor only; excludes creator/judge/probes. (HD-cost, HD-token-exclusions)
- disjoint_evolution_set=partial: SWE holdout disjoint; feedback trajectory scores reuse development benchmarks. (HD-feedback, HD-heldout)
- reliability_metric=partial: RQ1 avg@3 and noise check; RQ2 one trajectory/cell. (HD-creation-repeats, HD-noise, HD-limitations)
- code_released=unknown: No benchmark code verified in official project/repo list. (HD-code-status)
- evolved_harness_released=unknown: No final frozen artifact release verified. (HD-code-status)
- who_edits=external: Creator in fixed D edits later executor artifact; self-runtime means model identity. (HD-persistent, HD-dev-fixed)
- feedback=ground_truth: RQ2 external benchmark outcomes; Creation signals vary. (HD-feedback)
- timing=offline: Revision during development before frozen holdout. (HD-persistent, HD-heldout)
- topology=chain: Individual linear official-version trajectories. (HD-switchcount)

## 代码与数据限制

RSIHub inspected HEAD: d6554299c58bf0fe2db04ddda0277f9db67ea680

- Frozen evaluator / clean checkout / sealed anchor have implementation support.
- AHE artifact-valid and parent-eligible gates do not require strict score gain; admission is not proof every version improves.
- Current default AHE uses terminal-bench-2-30-v1 demo, not the 89-task paper configuration.
- No Table 1 final candidate/raw per-task artifacts verified; no numerical reproduction or security audit performed.

- Official project links papers but no benchmark implementation.
- Official account API lists only Self-Developing-Agents/Self-Developing-Agents.github.io.
- Appendix says seed/audit/splits will be released; code and evolved artifacts unknown.

仅报告，不擅自修改：

- RSIHub submission 2026-10-23 vs PDF cover 2026-10-22; preserve both.
- HarnessDev submission 2026-09-01 vs PDF cover 2026-09-02; preserve both.
- HarnessDev public SWE count 731 vs feedback100+holdout630=730. Invalid-instance exclusion is mentioned but missing instance/reason not verified from a released manifest; no invented explanation.
- Table 6 displayed delta and subtraction of rounded endpoints sometimes differ. Preserve printed deltas.

## 来源与验证

已验证 11 个源文件 SHA-256、50 处原文子串、2 个 catalog proposal 的 schema、9 行表 6 和派生均值。文章未修改，SHA-256: 28a9b76793a45cd2c72a947de981332449240dacd9752a86359f3ba82dbc07e8。

| 来源 | 抓取 UTC | SHA-256 |
|---|---|---|
| [rsihub abstract.html](https://arxiv.org/abs/2610.32253) | 2026-10-30T03:08:37.484865+00:00 | 0287585ac81380d73d456cd68a457fb3eb20a3b0f19ee9bdeea440e6ab2e8cad |
| [rsihub html.html](https://arxiv.org/html/2610.32253) | 2026-10-30T03:08:42.299414+00:00 | bd8cdbd8bc3af4bb5f4b48e3a715c175163e56f6f83d667851a3675d78600d8c |
| [rsihub pdf.pdf](https://arxiv.org/pdf/2610.32253) | 2026-10-30T03:08:48.754021+00:00 | d16b71c14a1276b6faac00a307a6e7f2ce81ae93a5a7490b6a661879889d072d |
| [rsihub project.html](https://simpleagentlab.com/rsihub/) | 2026-10-30T03:17:48.045236+00:00 | 9cf3181305f8675671c666595f0428f730adf105aa5607be5c6c4ca42a610dce |
| [rsihub github-repository.json](https://api.github.com/repos/simple-agent-lab/RSIHub) | 2026-10-30T03:13:29.421722+00:00 | e95ad7b65bbbb9e246226f4d54cd5ff9e6226423c8aa734c1ab9262646effe25 |
| [rsihub github-releases.json](https://api.github.com/repos/simple-agent-lab/RSIHub/releases) | 2026-10-30T03:13:31.018065+00:00 | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| [harnessdev abstract.html](https://arxiv.org/abs/2609.01437) | 2026-10-30T03:08:37.484866+00:00 | 440e13e74e8a6d69f939942f45f344b3a98a211e54bd3417395ab74845535c44 |
| [harnessdev html.html](https://arxiv.org/html/2609.01437) | 2026-10-30T03:08:42.304528+00:00 | 0bbc8ed36a571a31bea861747c91722946b67c5fa352eb4bd39bb9aa94c73f93 |
| [harnessdev pdf.pdf](https://arxiv.org/pdf/2609.01437) | 2026-10-30T03:08:49.874594+00:00 | 1231454f0ae5ccffdb3d031dc8f42eae0cbbaeb61dcd25dddb1855074697dfc0 |
| [harnessdev project.html](https://self-developing-agents.github.io/) | 2026-10-30T03:10:36.944415+00:00 | d1a9ce04eabd64fce85e28a7bbf00b4a3334010c90dfe31abb65a767f504e51b |
| [harnessdev github-public-repositories.json](https://api.github.com/users/self-developing-agents/repos?per_page=100) | 2026-10-30T03:13:29.421716+00:00 | 3fc36924f8ddbb9e8e1d171deda21a94fa69130640774aae6e8e0426ba8f011a |

完整数据见 [结构化报告](rsihub-harnessdev-report.json)；表格输入见 [JSON](harnessdev-table6.json) / [CSV](harnessdev-table6.csv)。
