> 供 owner 复审的笔记快照。分类建议不构成日报 accept；本次打包未修改 canonical 数据或历史审核决定。返回 [审核索引](INDEX.md)。

## 精读笔记：S³Gym

核对日期：2026-10-30。依据独立审查对官方 v1 方法、表格和相关结果逐项核对；未独立复现实验。归为 general_rsi，不计入 Harness 方法数。

### 更新的是什么

在 7 个游戏中测试探索、自评与经验复用，路径包括：

1. History ICL：将带评分的轨迹序列化后放进后续上下文。
2. Summary Memory：把轨迹压缩为可复用的自然语言经验，再供后续决策使用。
3. Training：把探索轨迹和自评转换为 SFT 样本，更新权重。

前两条修改经验内容，第三条修改参数。原文没有证明它改写了摘要器、记忆管理程序、调度器或控制流文件；不能因为经验文字影响行为就直接视为可复用 Harness 程序进化。

### 预算与留出

方法节声明不同路径从相同 base 开始，使用同一组 exploration seeds、同一组 evaluation seeds、相同交互预算与 decoding settings。探索与评估两阶段之间的随机种子不重叠，评价轨迹不会加入 history、memory 或训练数据。

“交互预算相同”不等于总 token、摘要调用、训练算力或美元成本相同。也不是已完成与并行采样、顺序修正的匹配总预算对照。

主上下文实验有 30 个探索 episodes，每 3 个探索 episodes 进行一次检查；每个 checkpoint 评 3 个 strict-mode episodes。这里的 3 指每次评估局数，主实验仍覆盖 7 个游戏；不能当作 3 个独立完整实验。

### 关键数字的正确解释

表 6 的全基准 blockwise ρ(A,g)=−0.010，其中 A 是事件层面正反馈一致率，g 是下一次严格评估的归一化变化。校准指标另为 ρ(−E,g)=−0.018。这不是所有自评指标的统一相关系数，更不是因果证明。

GPT-5.5 在 Chess 的 AUC+ 为 History ICL 0.474 对 Summary Memory 16.840；PvZ 为 History ICL 548.499 对 Summary Memory 33.219。这是两种经验组织路径的比较，不是训练前后准确率、最终游戏得分或胜率。

参数训练路径另用 Qwen3-8B；PvZ 的初始原始分为 23，更新后的各 checkpoint 为 6。不能把这一行与 GPT-5.5 的 AUC+ 混在一张未注明指标的趋势图里。

### 证据字段边界

- 留出集 yes：论文明确两阶段种子分离，评估轨迹不进入后续经验；本轮未审核实现来证明代码严格遵守。
- 不相交演化集 partial：随机种子与 episode 分离，但仍是同组游戏，不能说换了整个下游基准。
- 反馈为模型自评 self_judgment。
- 匹配总预算、完整成本、跨模型程序迁移、独立重复运行和代码/最终产物可用性等未确认项保持 unknown。

S³Gym、Aspire 与 HarnessDev 同属 Self-Developing Agents 项目，但分别研究经验/权重、目标与训练、可运行 Harness，分类不能互相替代。

### 来源与日期

- [arXiv 元数据](https://arxiv.org/abs/2608.31100)：v1 首次提交 2026-08-31 17:05:41 UTC；PDF 封面为 2026-09-01。
- [§4.3](https://arxiv.org/html/2608.31100#S4.SS3)：History 与 Summary Memory。
- [§4.4](https://arxiv.org/html/2608.31100#S4.SS4)：两阶段种子与数据隔离。
- [§4.5](https://arxiv.org/html/2608.31100#S4.SS5)：Training 与交互预算声明。
- [§5.2](https://arxiv.org/html/2608.31100#S5.SS2)：episode 和 checkpoint 设置。
- [§6.2](https://arxiv.org/html/2608.31100#S6.SS2)：自评与增益耦合分析；原表数值应按各自指标解释。
- [官方系列项目](https://self-developing-agents.github.io/)。

机构（PDF 首页）：ByteDance Seed；M-A-P；TokenWave.AI。

正文抓取时间：2026-10-30T03:08:24.723332+00:00。HTML SHA-256：282d079947cd1775c1bc9a8ff91c489a4eb51afb423984eda08edf4da1a454b3。
