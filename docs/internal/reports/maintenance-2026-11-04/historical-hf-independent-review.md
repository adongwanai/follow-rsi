# 历史 HF 补录独立抽查（2026-11-04）

对主审从旧 HF 快照找回的 **196 条历史记录**，本轮独立抽查 **9 条完整摘要**：7 条指定的易误判边界项，以及使用固定随机种子选择的 2 条排除项。9 条均支持暂时排除当前 Harness 专题，未新增纳入建议。

这些记录归属 **10 月 14 日至 26 日的历史榜单**；不属于 11 月 4 日新消息。原始论文发表/版本日期未单独核查，仍为 unknown。所有正式 decision 都保持 defer。

| 条目 | HF 榜单日期 | 判断依据 |
| --- | --- | --- |
| ProRubric · arxiv:2609.38847 | 2026-10-14 | ProRubric 改的是训练 reward 的 rubric 聚合规则，且摘要明确仅离线分组一次、优化器不变；没有反馈反复改写代理自身的环内验证程序。 |
| LongR · arxiv:2602.05758 | 2026-10-14 | Think-and-Read 和上下文信息增益 reward 用于 RL 训练。控制文档读取不等于外部控制流程序按反馈演化；摘要没有程序版本保留证据。 |
| MolLean · arxiv:2610.20459 | 2026-10-23 | Lean kernel 校验分子状态和当前推理动作，反馈修复化学推理轨迹；修改对象是分子状态/任务推理产物，摘要未展示校验 kernel 或通用工具程序自身演化。 |
| SCOPE · arxiv:2610.22264 | 2026-10-16 | 冻结的是图像生成器，GRPO 仍训练 prompt rewriter 的模型策略；生成每次请求的 prompt 不是可复用系统提示程序版本。 |
| VLA-Rolling · arxiv:2610.25043 | 2026-10-21 | 冻结 VLA 并复用动作尾部、估计置信度与分配去噪预算，继承对象是连续控制中的中间动作状态；没有方法规则自身持久改写证据。 |
| WORTH · arxiv:2610.27597 | 2026-10-26 | 两篇推理故事的证据发现/判断基准，评的是线索选择和人物判断；不是外部 Harness 反馈演化专项评测。 |
| FocusVLA · arxiv:2610.31423 | 2026-10-26 | 历史动作驱动未来意图预测和视角路由；摘要描述当前动作生成时的状态适应，没有修改并保留路由规则程序的机制。训练细节仅凭摘要保持 unknown。 |
| SAE-IDF · arxiv:2610.19636 | 2026-10-19 | 稀疏编码和频率加权用于跨符号系统匹配；没有代理执行反馈改写 Harness 的研究对象。 |
| AReA · arxiv:2610.17227 | 2026-10-14 | 去噪步骤中按既定机制缩放注意力感受野；不训练且 receptive field evolves 也不等于外部 Harness 工件自改。 |

原文短引句与快照定位：

- **ProRubric**：“Rubric-based reinforcement learning (Rubric-RL) trains language models where no verifier exists.” / “The grouping is done once, offline, and leaves the optimizer unchanged.”
- **LongR**：“Furthermore, LongR consistently enhances performance across diverse RL algorithms (e.g., DAPO, GSPO).”
- **MolLean**：“the model receives feedback to decide its next action, and rejected actions leave the state unchanged.” / “MolLean supports one-pass trace execution, whole-trace refinement, and interactive reasoning through MolLean-MCP.”
- **SCOPE**：“We propose SCOPE, an objective based on Group Relative Policy Optimization (GRPO) that aligns update weighting with this structure.”
- **VLA-Rolling**：“These results show that action tails are not merely discarded predictions, but reusable intermediate states that enable more efficient and accurate VLA inference.”
- **WORTH**：“models read original mystery narratives without clue annotations, autonomously select key clue sentences, identify case participants, and explain their reasoning process.”
- **FocusVLA**：“FocusVLA predicts future interaction intent from historical actions and uses it to guide dynamic view routing during action generation.”
- **SAE-IDF**：“Our method, SAE-IDF, encodes a symbol in its native context into a sparse code with a sparse autoencoder (SAE), re-weights each dimension by its rarity and matches across systems.”
- **AReA**：“We propose AReA, a training-free attention mechanism whose receptive field evolves from coarse to fine, following the denoising progression.”

定向项 ProRubric 的简称只出现在摘要中，已定位并核查完整摘要。随机两项为 SAE-IDF（2610.19636）和 AReA（2610.17227），种子为 `follow-rsi-independent-2026-11-04`。

已核对 11 处旧快照定位的 ID、标题与摘要，验证 11 段连续短引句。JSON 记录来源文件哈希、HF 真实归期和主审比较。

**边界：这是 9/196 的独立摘要抽查，不能称 196 篇完成全文三轮审核。** 未重跑实验、未改规范数据或正式决策、未运行全仓测试与构建。全局 recall 闸门仍未通过；没有接受、合并或发布。

机器可读记录：[historical-hf-independent-review.json](historical-hf-independent-review.json)。
