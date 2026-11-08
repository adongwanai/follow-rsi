# Coca-Cola 主审：arxiv:2611.06500

建议排除 Harness RSI 核心；正式 decision 仍 defer，等待独立第三轮复审。

学习对象是神经压缩器的 LoRA 与 latent adapter 权重。正文给出冻结 target agent 下的梯度训练，推理期使用固定已训练压缩器；没有执行或评估反馈驱动地改写并跨轮保留提示、工具代码、技能或上下文管理机制的 Harness 演化证据。压缩器在后续任务复用不等于外部 Harness 工件被迭代修改。也不足以认定两轮模型权重 RSI。

官方 v1：2026-11-04T13:32:36Z；HF 推荐日 2026-11-06；实际发现 2026-11-08T00:04:20.207518+00:00。不得归为 11/08 HF 新论文。

§3.4 Action-Preserving Training
> During training, we keep the target agent frozen and update only the LoRA parameters of the context-aware encoder and the parameters of the latent adapter.

§3.4 Action-Preserving Training
> Since latent tokens are continuous and differentiable, gradients can propagate through the frozen target agent to optimize the compression model:

§3.1 Overview
> During inference, the trained compressor replaces raw tool observations with latent tokens after each tool call, allowing the agent to perform multi-step interactions with a more compact context (Section 3.5 ).

原始官方 abs 与全文、请求回执、sha256 和规范记录 source_hash 均见 primary-review.json。该审核核实范围与日期，不声称复算实验数字。
0 付费调用；未改生产数据。
