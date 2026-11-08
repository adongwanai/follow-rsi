# 2026-10-30 HF 第一轮独立来源审核

**10-30 HF 榜单当前不可用；不能写成成功抓取或 0 篇。**

检查时间：2026-10-30T00:03:25.556075+00:00（北京时间约 08:03）。

- API：HTTP 400，原文错误明确要求 date ≤ 2026-10-29T00:00:00.000Z。
- 网页：请求 `/papers/date/2026-10-30` 得到 HTTP 200，但页面显示 Oct 29，嵌入的 `DailyPapers.dateString=2026-10-29`，返回同一份 14 篇旧日榜单。
- 结论：请求日期尚未由 HF 提供；不猜测具体开放时间，不把前一日内容冒充当天。

## 10-29 榜单变化

昨天最终快照 8 篇 → 当前 14 篇：**新增 7、消失 1、标题/摘要变化 0、原样保留 7**。消失条目是 DTCA（2610.35201）；这只是榜单变化，不表示论文撤稿。

新条目是“10-30 发现的 10-29 榜单补充”。摘要审查：Harness 0、边界候选 0、模型/数据其他方向 1、排除 6。全部保持 defer。

| 新增条目 | HF 推荐日 | 权威首发/更新 | 建议 | 原因 |
| --- | --- | --- | --- | --- |
| [RealCLI: Toward a Unified Evaluation of Human-Agent Collaboration for CLI Agents](https://huggingface.co/papers/2610.22507) | 2026-10-29 | unknown（arXiv 429） | exclude | 评测 Agent 对渐进信息、纠错和授权的响应；变化的是当前任务要求，不是跨任务演化的 Harness。 |
| [TauIndianBankBench: Procedure-Aware, Action-Oriented Evaluation of Tool-Using Conversational Agents](https://huggingface.co/papers/2610.30161) | 2026-10-29 | unknown（arXiv 429） | exclude | 检查银行任务的操作步骤和终态，是流程执行评测，不是 Harness 自演化专项评测。 |
| [Amortizing Sequential Experimental Design in Reasoning LLMs](https://huggingface.co/papers/2610.20832) | 2026-10-29 | unknown（arXiv 429） | exclude | 把序贯实验设计能力训练进 LLM，改进对象是模型权重，不是外部 Harness。 |
| [LongZero: Enhancing Long-Context Reasoning in LLMs from Zero Data](https://huggingface.co/papers/2610.30132) | 2026-10-29 | unknown（arXiv 429） | other_direction | 自写训练任务后用 GRPO 更新模型；这是模型/数据改进方向，非 Harness 工件自修改。 |
| [Evaluating DeepSeek V4.1 Flash-1017 for loss of control and harmful manipulation risks](https://huggingface.co/papers/2610.35671) | 2026-10-29 | unknown（arXiv 429） | exclude | 比较模型版本的失控和操纵风险；没有专门研究外部 Harness 演化。 |
| [Instruction Capacity: Behavior and Degradation of Language Models under Controlled Load](https://huggingface.co/papers/2610.36095) | 2026-10-29 | unknown（arXiv 429） | exclude | 测量模型在指令负载下的能力极限，不是反馈驱动的提示程序优化或 Harness 演化。 |
| [Know, then Draw: A New Learning Paradigm for Visual Generation](https://huggingface.co/papers/2610.37626) | 2026-10-29 | unknown（arXiv 429） | exclude | 视觉生成模型的训练范式与缩放律，不研究 Agent RSI 或 Harness。 |

## 逐篇证据

### RealCLI: Toward a Unified Evaluation of Human-Agent Collaboration for CLI Agents

- ID：arxiv:2610.22507；对象：CLI 人机协作能力基准。
- 原文引句：a paired benchmark that unifies the evaluation of task execution and human-agent collaboration quality on realistic CLI tasks.
- 理由：REALCLI-EXEC/COLLAB 比较固定系统的任务表现与协作质量。脚本用户修改约束和代理适应任务，不等于反馈使代理修改可复用程序并保留新版本。
- 不确定性：本轮依据 HF 原始摘要；没有读论文正文。；arXiv 身份/首发/更新核对请求返回 HTTP 429，权威日期与独立身份核验保持 unknown；不以 HF publishedAt 替代。

### TauIndianBankBench: Procedure-Aware, Action-Oriented Evaluation of Tool-Using Conversational Agents

- ID：arxiv:2610.30161；对象：银行业务流程执行基准。
- 原文引句：an action-oriented benchmark of 1,000 Indian retail-banking tasks where an assistant helps a simulated customer.
- 理由：摘要只报告程序合规与操作结果的评估差异；固定流程检查和训练前后评价没有建立外部工具/工作流自动修订的反馈闭环。
- 不确定性：本轮依据 HF 原始摘要；没有读论文正文。；arXiv 身份/首发/更新核对请求返回 HTTP 429，权威日期与独立身份核验保持 unknown；不以 HF publishedAt 替代。；HF paper.publishedAt=2026-09-30 与 2610 编号月份不一致，须后续权威核对；未擅自修改。

### Amortizing Sequential Experimental Design in Reasoning LLMs

- ID：arxiv:2610.20832；对象：LLM 实验设计策略权重。
- 原文引句：explicitly training the reasoning that guides action selection using information-gain rewards.
- 理由：信息增益奖励用于训练 action-selection reasoning；摘要没有外部程序版本更新，也没有明确多代自生成/再训练闭环。跨任务泛化的训练技能不能等同可执行技能文件演化。
- 不确定性：本轮依据 HF 原始摘要；没有读论文正文。；arXiv 身份/首发/更新核对请求返回 HTTP 429，权威日期与独立身份核验保持 unknown；不以 HF publishedAt 替代。

### LongZero: Enhancing Long-Context Reasoning in LLMs from Zero Data

- ID：arxiv:2610.30132；对象：自合成任务与 LLM 推理权重。
- 原文引句：LongZero combines these self-written multi-hop reasoning tasks with self-written multi-round retrieval tasks and trains the model with GRPO.
- 理由：主要持续对象是模型参数与合成训练样本。摘要没有提示/工具/技能或控制流文件被反馈改写并保留的机制。广义模型 RSI 是否具备明确多代闭环仍需正文，不能因为 self-written、multi-round 或 zero data 就推断完整循环。
- 不确定性：本轮依据 HF 原始摘要；没有读论文正文。；arXiv 身份/首发/更新核对请求返回 HTTP 429，权威日期与独立身份核验保持 unknown；不以 HF publishedAt 替代。

### Evaluating DeepSeek V4.1 Flash-1017 for loss of control and harmful manipulation risks

- ID：arxiv:2610.35671；对象：模型系统性安全评测。
- 原文引句：an independent safety evaluation of DeepSeek V4.1 Flash-1017
- 理由：建议发布前安全评测、过程可观测性与私有基准属于模型治理；这些建议不是 Agent 自修改工具、工作流或验证器的已实现方法。
- 不确定性：本轮依据 HF 原始摘要；没有读论文正文。；arXiv 身份/首发/更新核对请求返回 HTTP 429，权威日期与独立身份核验保持 unknown；不以 HF publishedAt 替代。

### Instruction Capacity: Behavior and Degradation of Language Models under Controlled Load

- ID：arxiv:2610.36095；对象：固定规则负载下的指令容量测量。
- 原文引句：the instruction capacity - the number of rules held at a given share of right replacements - with an uncertainty.
- 理由：实验操纵替换规则数量与位置并统计成功率；未来 prompt-load meter 的用途不等于已实现持续更新 Harness 的机制。
- 不确定性：本轮依据 HF 原始摘要；没有读论文正文。；arXiv 身份/首发/更新核对请求返回 HTTP 429，权威日期与独立身份核验保持 unknown；不以 HF publishedAt 替代。

### Know, then Draw: A New Learning Paradigm for Visual Generation

- ID：arxiv:2610.37626；对象：视觉生成模型预训练与后训练。
- 原文引句：autoregressive pretraining for knowledge acquisition and diffusion post-training for high-fidelity rendering.
- 理由：AR 知识预训练、扩散渲染后训练和语义 tokenizer 都是模型训练设计；没有外部可复用程序的反馈迭代。
- 不确定性：本轮依据 HF 原始摘要；没有读论文正文。；arXiv 身份/首发/更新核对请求返回 HTTP 429，权威日期与独立身份核验保持 unknown；不以 HF publishedAt 替代。

## 复核产物

- `hf-source-evidence/manifest.json`：API 和网页请求 URL、HTTP 状态、抓取时间、响应正文路径与 SHA256。
- `hf-source-evidence/comparison.json`：精确新增/移除/未变列表，两个日期页内嵌实际日期。
- `hf-source-evidence/new-ids-arxiv-metadata.json`：权威身份请求的 429 状态及原始响应哈希；原日期不被猜测。
- `new-hf-input.json`：只含新增 7 条原始摘要及来源元数据，不含本轮审核判断，供第二模型独立处理。
- 全部短引句经校验为 HF 摘要原文连续子串，且 ≤200 字符。
- 仅读摘要；全文审读 0 篇。没有修改共享数据、队列、代码或发布内容。
