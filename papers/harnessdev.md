# HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?

<!-- AUTO:CARD:START -->

[arXiv](https://arxiv.org/abs/2609.01437) · [HF](https://huggingface.co/papers/2609.01437)

2026-09-01 · ByteDance Seed · Singapore University of Technology and Design · Georgia Institute of Technology · M-A-P · TokenWave.AI · 五、评测、归因与可信度

**必读 / MUST READ**

| 证据字段 | 记录 |
| --- | --- |
| 留出集 | ✅ 有 |
| 同预算对照 | ❌ 没有 |
| 跨模型迁移 | ✅ 有 |
| 报告成本 | ◐ 部分 |
| 不相交演化集 | ◐ 部分 |
| 可靠性指标 | ◐ 部分 |
| 开源代码 | ❔ 未审 |
| 公开演化出的 Harness | ❔ 未审 |
| 谁来改 |  外部改进器 |
| 反馈来源 |  标准答案 |
| 改进时机 |  离线 |
| 演化结构 |  链 |

**一句话**：评测模型在权重固定时创建与迭代修改可复用 Harness 的能力。Creation 覆盖六个模型、五个基准；Evolution 根据反馈集修改代码，再冻结版本评估 630 道 SWE-Pro 留出题，并区分创建者与执行器。

**关键结果**：五条 self-runtime 轨迹的留出增益为 +1.43 至 +4.44 个百分点（均值 +3.11）；四条全程固定 Gemini 的轨迹中三条退步。每个创建者–执行器组合仅一条演化线，未做匹配搜索预算对照，成本不含完整开发开销。

<details><summary>English</summary>

| Evidence field | Record |
| --- | --- |
| Held-out evaluation | ✅ yes |
| Matched-budget baseline | ❌ no |
| Cross-model transfer | ✅ yes |
| Cost reported | ◐ partial |
| Disjoint evolution set | ◐ partial |
| Reliability metric | ◐ partial |
| Code released | ❔ not yet reviewed |
| Evolved harness released | ❔ not yet reviewed |
| Who edits |  external |
| Feedback |  ground_truth |
| Timing |  offline |
| Topology |  chain |

**Summary**: Evaluates creation and iterative revision of reusable harnesses with weights fixed. Creation covers six models and five benchmarks; Evolution uses visible feedback before frozen artifacts are evaluated on 630 held-out SWE-Pro tasks, separating creator and executor roles.

**Key result**: All five self-runtime trajectories improve on held-out tasks by +1.43 to +4.44 points (mean +3.11), while three of four separate fixed-Gemini trajectories regress. There is one evolution trajectory per creator–executor cell, no matched-search baseline, and incomplete development-cost accounting.

</details>

<!-- AUTO:CARD:END -->

<!-- AUTO:NOTES:START -->

## 精读笔记：HarnessDev

核对日期：2026-10-30。核对官方 v1 正文、表格、项目页和公开代码可用性；未独立复现实验。分类为 Harness 专项评测（harness_eval），在“实验设计”路线中接在 Harness-Delta Attribution 之后。

### 改进对象与协议

Creation 从弱但可运行的 seed 创建完整 Harness；Evolution 从它自己的冻结 H0 出发，用执行反馈修改可复用程序。每个版本冻结后再执行任务；模型权重固定，开发环境 D 也保持固定。不能把一次创建或固定 D 内的修改，扩写成已验证开发环境本身的递归进化。

Creation 覆盖 6 个创建者模型、4 个领域、5 个基准，合计 2,207 个独立下游实例；每个创建者–基准组合独立创建并评估 3 个 Harness，报告 avg@3。

Evolution 的可见反馈为 SWE-Pro-100 和 Terminal-Bench-89。H0 之后最多 10 次完整双基准评估对；小规模 probes 只供诊断，不是官方分数。全部轨迹结束后，对每个官方版本评估 630 道 SWE-Pro 留出题；结果不返回给创建者，不参与修改、停止或最终版本选择。

### 读表 6 时必须分开两类实验

- self-runtime：创建者模型也充当执行器，共 5 条轨迹。
- fixed-Gemini：从同一 H0 起点另开独立轨迹，全程由 Gemini 执行，共 4 条轨迹。
- 这 4 条 fixed-Gemini 轨迹不是把 self-runtime 演化完成的最终 Harness 直接换模型。

每个创建者–执行器组合只有一条演化轨迹。反馈分是 SWE-Pro-100 与 Terminal-Bench-89 百分数的无权均值；留出分仅为 SWE-Pro-630。下表增量单位是百分点，保持表 6 原始 delta；final gap 是该轨迹最高留出分减去声明最终版本的留出分。

| 运行设置 | 创建者 | 反馈 Δ | 留出 Δ | 最终 gap |
|---|---|---:|---:|---:|
| self | Gemini 3.1 Pro | 8.8 | 2.70 | 0.00 |
| self | Opus 4.8 | 3.0 | 4.44 | 1.59 |
| self | Qwen 3.7 Max | 13.9 | 1.43 | 3.17 |
| self | DeepSeek V4 Pro | 13.4 | 3.17 | 1.75 |
| self | GPT-5.5 | 5.9 | 3.81 | 0.00 |
| fixed_gemini | Opus 4.8 | 9.7 | 2.70 | 2.54 |
| fixed_gemini | Qwen 3.7 Max | 1.1 | -1.11 | 1.11 |
| fixed_gemini | DeepSeek V4 Pro | 6.5 | -2.38 | 3.02 |
| fixed_gemini | GPT-5.5 | 2.4 | -10.32 | 16.51 |

按 9 条线的报告增量无权平均，可得到反馈约 +7.2、留出约 +0.5。这是混合两种运行设置且比较不同题集的派生统计，不是稳定性估计。分别看时，5 条 self-runtime 的留出全部为正，均值 +3.11；4 条 fixed-Gemini 的留出均值为 −2.7775。

### 版本选择与噪声

共 73 个官方版本、64 次相邻切换：8 次双基准退步、16 次单基准退步、3 次跨基准权衡、7 次没有可测变化、27 次增益位于重复运行噪声带内、2 次有超出噪声带的明确正向证据、1 次没有可执行代码变更。

同一 commit 的反馈 pair-score 可相差约 ±4.75 点。带内增益不能仅凭单次分数归因于代码修改；这不等于证明真实效应为零。64 次切换只有 34 次反馈与留出同向（53.1%）；论文没有据此检验“与随机无异”。声明版本只有 2/9 是各线留出最优。

专用轨迹接口只调用 2 次，显式查看的案例覆盖 189 道反馈题的 0.5%–40.2%；但创建者也使用自定义脚本和小 probes，接口计数不等于全部诊断活动。

### 创建能力与直接跨模型测试

Creation 表 3 中 Opus 的四基准平均为 67.8，人工工程系统参考为 86.2；平均不含 MLE-bench。参考行是不同公开 Harness 与各自底模的组合，不能把差值只归因于 Harness，更不是与人的做题能力相比。

以 Opus 为例：EQ-Bench3 为 84.6 对参考 83.7，MLE-bench 为 32.9 对 24.0，BrowseComp 为 52.4 对 92.2。52.4 不是所有生成 Harness 的 BrowseComp 最高值，GPT-5.5 为 52.6。

RQ1 的 Unified-Eval 将同一个已经冻结的 Harness 交给 Gemini 执行，才是“不重新演化”的跨模型测试。例如 Opus 的 SWE-Pro 为 69.3 → 33.0、写作为 84.6 → 74.2。证据卡的跨模型 yes 表示做过这种测试，不表示所有收益都成功迁移。

### 证据字段与尚未知项

- 留出集有；反馈轨迹本身仍在反复使用开发题，所以不相交演化集标 partial。
- 同预算对照标 no：正文明确“matched-search evaluation remains future work”。
- 成本标 partial：报告执行 token，创建/修改、judge、probe token 不计入完整成本。
- 可靠性标 partial：Creation 有 avg@3 和相同 commit 噪声检查，但 Evolution 每格一条线，不支持总体不确定性估计。
- 代码与最终演化产物均为 unknown。官网有论文链接，公开账号只核到网站仓库；附录 C 仍写 seed、audit script、splits “will be released”。

数据口径疑点仅报告：公开 SWE-Pro 为 731 题，但 100 feedback + 630 held-out = 730。论文协议提到排除 invalid instances，本次没有核到可确认所缺实例及原因的公开 split manifest，不擅自补解释。表 6 部分 delta 与四舍五入后的端点相减略有差别，保留原表 delta。

### 来源与日期

- [arXiv 元数据](https://arxiv.org/abs/2609.01437)：v1 提交 2026-09-01 15:45:33 UTC；PDF 封面写 2026-09-02，目录采用前者。
- [§3.2](https://arxiv.org/html/2609.01437#S3.SS2)：反馈、冻结与留出协议。
- [表 3](https://arxiv.org/html/2609.01437#S4.T3)、[表 4](https://arxiv.org/html/2609.01437#S4.T4)：Creation 与直接跨模型实验，PDF p. 8。
- [表 6](https://arxiv.org/html/2609.01437#S4.T6)、[§4.3](https://arxiv.org/html/2609.01437#S4.SS3)：九条线、噪声与版本选择，PDF pp. 12–13。
- [§6.1](https://arxiv.org/html/2609.01437#S6.SS1)：局限；[图 10](https://arxiv.org/html/2609.01437#A2.F10)：成本排除项。
- [Self-Developing Agents 项目](https://self-developing-agents.github.io/)。

作者（arXiv 顺序）：Yuhao Wu, Jingyuan Zhang, Jiajun Shi, Xinping Lei, Qingshui Gu, Yuxuan Zhang, Zexuan Wang, Chen He, Chen Huang, Maojia Song, Zhiyuan Zeng, Shaowen Wang, Jinkai Liu, Yunfeng Shi, Jiaheng Liu, Shen Yan, Wenhao Huang, Ge Zhang, Wenxuan Zhang。

机构（PDF 首页）：ByteDance Seed; Singapore University of Technology and Design; Georgia Institute of Technology; M-A-P; TokenWave.AI。

正文抓取时间：2026-10-30T03:08:42.304528+00:00。HTML SHA-256：0bbc8ed36a571a31bea861747c91722946b67c5fa352eb4bd39bb9aa94c73f93。

<!-- AUTO:NOTES:END -->

<!-- AUTO:RELATED:START -->

## 相关论文

- [EvoHarnessBench](evoharnessbench.md)
- [REUSE](reuse.md)
- [Reflections on Trusting Trust, Revisited](trusting-trust-revisited.md)
- [Aspire: Can Models Self-Evolve from Vague Goals?](aspire.md)
- [Rethinking the Evaluation of Harness Evolution for Agents](rethinking-evaluation.md)
- [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](hda.md)
- [RSIHub: A Composable Framework for Agent-Evolution Methods](rsihub.md)
- [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](harnessopt-bench.md)
- [Auditing the Product, Not the Recursion](auditing-product.md)

<!-- AUTO:RELATED:END -->
