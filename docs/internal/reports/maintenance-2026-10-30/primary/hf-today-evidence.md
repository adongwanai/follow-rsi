# HF 2026-10-30：逐篇证据摘录

范围：16 篇官方摘要；6 篇另核正文相关方法、评测与限制章节。这里仅复制已核实的短引文，不含论文全文。所有建议保持 `defer`，与 owner 最终决定分开。

主结论见 [前两轮报告](hf-today-report.md)，机器可读记录见 [manifest](hf-today-manifest.json)。

## CoSTA: Compressed Speech Token Adaptation for Efficient Spoken Dialogue Models

[官方论文](https://arxiv.org/abs/2610.21143) · [HF 条目](https://huggingface.co/papers/2610.21143)

HF 榜日：2026-10-30；首次发表：2026-10-15T03:00:10Z；版本更新：2026-10-15T03:00:10Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

语音 token 压缩与 post-hoc 适配训练，不是反馈驱动的 Harness 或多轮 RSI。

> CoSTA extends the generation token space with compressed representations via mean-initialized vocabulary extension, pronunciation adaptation, and dialogue adaptation

来源：[官方摘要](https://arxiv.org/abs/2610.21143)；核验缓存 SHA-256 `ad0e6ff11b5810034c15b1ff90269b991ee585c546bda2b9d0766a0ef19ac031`；严格连续子串匹配已通过。

## Your Benchmark Is an Empirical Measure Over Difficulty

[官方论文](https://arxiv.org/abs/2610.29927) · [HF 条目](https://huggingface.co/papers/2610.29927)

HF 榜日：2026-10-30；首次发表：2026-10-21T16:02:37Z；版本更新：2026-10-21T16:02:37Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

一般基准难度分布与题目重写，不是自进化系统或 Harness 演化专项评测。

> We propose two diagnostic metrics that capture these two failure modes and provide rigorous theoretical guarantees.

来源：[官方摘要](https://arxiv.org/abs/2610.29927)；核验缓存 SHA-256 `46f1aebde377ae6303edc67158ade6ac7dfec49107afdde018dc349b9a74bf14`；严格连续子串匹配已通过。

> a simple difficulty-targeted item rewriting algorithm that effectively reduces local coverage gaps.

来源：[官方摘要](https://arxiv.org/abs/2610.29927)；核验缓存 SHA-256 `46f1aebde377ae6303edc67158ade6ac7dfec49107afdde018dc349b9a74bf14`；严格连续子串匹配已通过。

## VibeGame: Prompt-to-Game Development with AI-Native Engine and Self-Evolving Adversarial Agent Team

[官方论文](https://arxiv.org/abs/2610.33106) · [HF 条目](https://huggingface.co/papers/2610.33106)

HF 榜日：2026-10-30；首次发表：2026-10-22T18:03:17Z；版本更新：2026-10-22T18:03:17Z。

Harness 建议：`harness`；广义 RSI 建议：`include`；owner decision：`defer`。

接受项目经无训练蒸馏产生协作 contracts；新项目读取并重新验证，属于可复用 Harness 工作流规则更新。

> For each conducted and accepted project, we further introduce a training-free self-evolution mechanism

来源：[官方摘要](https://arxiv.org/abs/2610.33106)；核验缓存 SHA-256 `db8de5afe0227deb6b126c83a3bf87cd3831257ce3e4de9d629a12736f72432f`；严格连续子串匹配已通过。

> distill it into reusable skeletons, modules, and collaboration contracts for future development.

来源：[官方摘要](https://arxiv.org/abs/2610.33106)；核验缓存 SHA-256 `db8de5afe0227deb6b126c83a3bf87cd3831257ce3e4de9d629a12736f72432f`；严格连续子串匹配已通过。

> VibeGame distills reusable experience from these validated projects with a training-free self-evolution mechanism and uses it to initialize future development runs, preserving implicit development knowledge that general-purpose agents lose across independent runs.

来源：[S3.SS3.p1](https://arxiv.org/html/2610.33106v1#S3.SS3.p1)；核验缓存 SHA-256 `a4c7bab131239dca5e5ee28d8bd3b4604ab75c93e8c50b93928c52629cb6b64a`；严格连续子串匹配已通过。

> A contract is a document that adapts the general AAT workflow to a recurring feature or development pattern.

来源：[S3.SS3.p4](https://arxiv.org/html/2610.33106v1#S3.SS3.p4)；核验缓存 SHA-256 `a4c7bab131239dca5e5ee28d8bd3b4604ab75c93e8c50b93928c52629cb6b64a`；严格连续子串匹配已通过。

> It specifies the role-specific inputs, outputs, dependencies, and verification criteria required to implement that feature, enabling agents to coordinate through a validated procedure rather than relying only on the generic build-and-review loop.

来源：[S3.SS3.p4](https://arxiv.org/html/2610.33106v1#S3.SS3.p4)；核验缓存 SHA-256 `a4c7bab131239dca5e5ee28d8bd3b4604ab75c93e8c50b93928c52629cb6b64a`；严格连续子串匹配已通过。

> The orchestrator first decomposes the game into parallel components, retrieves relevant skeletons, modules, and contracts from the self-evolution repository (Section 3.3 ) as project priors

来源：[S3.SS2.SSS2.p1](https://arxiv.org/html/2610.33106v1#S3.SS2.SSS2.p1)；核验缓存 SHA-256 `a4c7bab131239dca5e5ee28d8bd3b4604ab75c93e8c50b93928c52629cb6b64a`；严格连续子串匹配已通过。

> For w/ Experience, we let VibeGame with GPT-6.1-Sol build and self-evolve on 5 tasks randomly sampled from outside the ablation set, using the task rubrics and the vision-language model (VLM) judge scores in place of user feedback.

来源：[S8.SS1.p2](https://arxiv.org/html/2610.33106v1#S8.SS1.p2)；核验缓存 SHA-256 `a4c7bab131239dca5e5ee28d8bd3b4604ab75c93e8c50b93928c52629cb6b64a`；严格连续子串匹配已通过。

> We observe that when VibeGame continuously develops games of different types, the experience accumulated by self-evolution can instead lower agent performance.

来源：[S13.p1](https://arxiv.org/html/2610.33106v1#S13.p1)；核验缓存 SHA-256 `a4c7bab131239dca5e5ee28d8bd3b4604ab75c93e8c50b93928c52629cb6b64a`；严格连续子串匹配已通过。

> the main experiments use VibeGame without any accumulated experience, and we evaluate self-evolution separately in the ablation study.

来源：[S13.p1](https://arxiv.org/html/2610.33106v1#S13.p1)；核验缓存 SHA-256 `a4c7bab131239dca5e5ee28d8bd3b4604ab75c93e8c50b93928c52629cb6b64a`；严格连续子串匹配已通过。

## A Broader Look into MLLM's Retrieval Heads

[官方论文](https://arxiv.org/abs/2610.32411) · [HF 条目](https://huggingface.co/papers/2610.32411)

HF 榜日：2026-10-30；首次发表：2026-10-23T09:37:28Z；版本更新：2026-10-23T09:37:28Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

优化的是多模态模型 attention heads，属于模型训练；未描述多轮自生成数据/自训练或外部 Harness 修改。

> we turn retrieval heads into a target of optimization by training their attention with a ranking objective.

来源：[官方摘要](https://arxiv.org/abs/2610.32411)；核验缓存 SHA-256 `432719984143f535fb6273db073062b5ef0278c67b071d2e920bb2c803016359`；严格连续子串匹配已通过。

## After One-Click Video: The Inflow of Service-Type Content, the Failure of the Recommendation Pool Mechanism, and the BoLe System

[官方论文](https://arxiv.org/abs/2610.37695) · [HF 条目](https://huggingface.co/papers/2610.37695)

HF 榜日：2026-10-30；首次发表：2026-10-24T09:02:54Z；版本更新：2026-10-24T09:02:54Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

讨论内容供给与推荐机制的产业/平台理论，不是 AI 递归自改进系统。

> Machines and entry rules judge whether service-type content passes the bar. Trusted people judge work-type content. We call this the BoLe system.

来源：[官方摘要](https://arxiv.org/abs/2610.37695)；核验缓存 SHA-256 `c52bef74fb6444a343d32aaabd017b3c4bbcde789eb5d570f96725f5055a5121`；严格连续子串匹配已通过。

## Co-Design Bench: Multimodal Collaborative Coding Evaluation for Agentic Models

[官方论文](https://arxiv.org/abs/2610.35138) · [HF 条目](https://huggingface.co/papers/2610.35138)

HF 榜日：2026-10-30；首次发表：2026-10-26T10:10:21Z；版本更新：2026-10-26T10:10:21Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

评测真实用户应用修改能力，在共享固定 harness 下比较模型；不专门研究 Harness 反馈演化。

> Under a shared agentic harness, the strongest of ten model endpoints passes an average of 69.9% of criteria per task but fully satisfies only 26.4% of tasks.

来源：[官方摘要](https://arxiv.org/abs/2610.35138)；核验缓存 SHA-256 `67127e249364ee9ad158945fa7f260038020273bd069f21ac86fe7b1f6a6c564`；严格连续子串匹配已通过。

## SO-101 Bench: Accessible Spatial Manipulation

[官方论文](https://arxiv.org/abs/2610.36420) · [HF 条目](https://huggingface.co/papers/2610.36420)

HF 榜日：2026-10-30；首次发表：2026-10-27T00:02:28Z；版本更新：2026-10-27T00:02:28Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

机器人操控评测并比较固定 Harness/模型选择；当前任务中写控制代码与恢复，不构成跨任务 Harness 演化。

> An LLM agent that writes code and hands grasping to a learned policy scores 83.2%, and an ablation shows that this lead comes from the choice of harness and the choice of language model.

来源：[官方摘要](https://arxiv.org/abs/2610.36420)；核验缓存 SHA-256 `f78d6ceebe90ad5ee80a5d923b9cea2f73b6f1aaa4ba2396f37309544565a7c0`；严格连续子串匹配已通过。

> We ask what drives this: the harness that
> connects the language model to the robot, or the language model itself.

来源：[S7.p1](https://arxiv.org/html/2610.36420v1#S7.p1)；核验缓存 SHA-256 `0d52253f5dc8c78edf88517efb235b182d489ca1701baa33f0bbfd7bfcce691f`；严格连续子串匹配已通过。

> Holding the PyRUA-Lean + Galaxea 0.5 harness fixed, we compare four language models
> on the same 60 episodes

来源：[S7.SS0.SSS0.Px4.p1](https://arxiv.org/html/2610.36420v1#S7.SS0.SSS0.Px4.p1)；核验缓存 SHA-256 `0d52253f5dc8c78edf88517efb235b182d489ca1701baa33f0bbfd7bfcce691f`；严格连续子串匹配已通过。

## WorkFactory: Turning Professional Intents into Executable Work for Scalable Agent Training

[官方论文](https://arxiv.org/abs/2610.37161) · [HF 条目](https://huggingface.co/papers/2610.37161)

HF 榜日：2026-10-30；首次发表：2026-10-27T12:54:16Z；版本更新：2026-10-27T12:54:16Z。

Harness 建议：`other_direction`；广义 RSI 建议：`borderline`；owner decision：`defer`。

探测执行反馈修订任务说明/参考文件，最终生成训练语料；不是 Agent 自身 Harness。是否满足更广义 RSI 的跨任务继承标准仍需第三轮判定。

> Probe executions then identify support failures and guide repairs while preserving the intended work.

来源：[官方摘要](https://arxiv.org/abs/2610.37161)；核验缓存 SHA-256 `4ee99b03f3212efe65279ad7ae0a073b9d5bf851e91ae9180e961b0c9feb566e`；严格连续子串匹配已通过。

> We construct 112,686 tasks spanning 612 occupations and use the collected teacher trajectories to fine-tune Qwen models at 4B, 27B, and 35B-A3B scales

来源：[官方摘要](https://arxiv.org/abs/2610.37161)；核验缓存 SHA-256 `4ee99b03f3212efe65279ad7ae0a073b9d5bf851e91ae9180e961b0c9feb566e`；严格连续子串匹配已通过。

> A refiner uses the diagnoses to edit the request and existing reference files while preserving the files’ number, types, and dependency structure

来源：[S3.SS4.SSS0.Px2.p1](https://arxiv.org/html/2610.37161v1#S3.SS4.SSS0.Px2.p1)；核验缓存 SHA-256 `7e852a8d3a2580c207a07ee8a01137f5096b4d6567709bf658effe3f44ae9753`；严格连续子串匹配已通过。

> The loop stops when no blocker remains or the repair budget is exhausted, with unresolved tasks discarded.

来源：[S3.SS4.SSS0.Px2.p1](https://arxiv.org/html/2610.37161v1#S3.SS4.SSS0.Px2.p1)；核验缓存 SHA-256 `7e852a8d3a2580c207a07ee8a01137f5096b4d6567709bf658effe3f44ae9753`；严格连续子串匹配已通过。

> All fine-tuned models, including those used in the controlled studies, use the shared supervised fine-tuning configuration reported in Appendix D.3 (Table 9 ).

来源：[S4.SS1.SSS0.Px3.p1](https://arxiv.org/html/2610.37161v1#S4.SS1.SSS0.Px3.p1)；核验缓存 SHA-256 `7e852a8d3a2580c207a07ee8a01137f5096b4d6567709bf658effe3f44ae9753`；严格连续子串匹配已通过。

## WebAnything: From the Wild Web to Scalable Agent Environments

[官方论文](https://arxiv.org/abs/2610.37786) · [HF 条目](https://huggingface.co/papers/2610.37786)

HF 榜日：2026-10-30；首次发表：2026-10-27T18:06:58Z；版本更新：2026-10-27T18:06:58Z。

Harness 建议：`other_direction`；广义 RSI 建议：`borderline`；owner decision：`defer`。

反馈修补的是可发布网站训练环境；采样与下游评测仍使用固定 Agent harness。环境构建循环是否算广义 RSI 待第三轮确认，不能算 Harness。

> an independent verifier checks frozen candidates and guides local repair or targeted source recapture.

来源：[官方摘要](https://arxiv.org/abs/2610.37786)；核验缓存 SHA-256 `15e4185e349dc247140dd90e4d038367a3200f357dddc87e6e9b3f5d1556970b`；严格连续子串匹配已通过。

> Fine-tuning Qwen3.5-9B on 5,856 interaction trajectories improves REAL success by 9.9 percentage points

来源：[官方摘要](https://arxiv.org/abs/2610.37786)；核验缓存 SHA-256 `15e4185e349dc247140dd90e4d038367a3200f357dddc87e6e9b3f5d1556970b`；严格连续子串匹配已通过。

> Our feedback targets frozen website implementations and missing source evidence.

来源：[S2.SS0.SSS0.Px3.p1](https://arxiv.org/html/2610.37786v1#S2.SS0.SSS0.Px3.p1)；核验缓存 SHA-256 `860a1504014af3fad16cd36bc4c2343bb17da1c5acbfefcfa598d8cf638b22ec`；严格连续子串匹配已通过。

> WebAnything supplies executable environments and collects interaction data with the fixed agent harness and a unified task/evaluator pipeline, measuring utility on external benchmarks.

来源：[S2.SS0.SSS0.Px3.p1](https://arxiv.org/html/2610.37786v1#S2.SS0.SSS0.Px3.p1)；核验缓存 SHA-256 `860a1504014af3fad16cd36bc4c2343bb17da1c5acbfefcfa598d8cf638b22ec`；严格连续子串匹配已通过。

> After either path updates the candidate, the controller freezes it again and the Verifier repeats affected checks and applicable regression tests.

来源：[S3.SS3.SSS0.Px2.p3](https://arxiv.org/html/2610.37786v1#S3.SS3.SSS0.Px2.p3)；核验缓存 SHA-256 `860a1504014af3fad16cd36bc4c2343bb17da1c5acbfefcfa598d8cf638b22ec`；严格连续子串匹配已通过。

## WeVisCut: The Whole Editing Room in One Agent From Narration to Long-Form Video

[官方论文](https://arxiv.org/abs/2610.38352) · [HF 条目](https://huggingface.co/papers/2610.38352)

HF 榜日：2026-10-30；首次发表：2026-10-28T06:51:40Z；版本更新：2026-10-28T06:51:40Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

固定指令/工具/runtime 下训练 9B policy，执行反馈修当前视频状态；多阶段 post-training 不是 Harness 程序自更新，也未证明多轮外层 RSI。

> We use this supervision to train a single 9B policy that coordinates production and recovers from failures within the same harness.

来源：[官方摘要](https://arxiv.org/abs/2610.38352)；核验缓存 SHA-256 `0ca55d8ff0944b9d8f7a093e87c149d7edb557bf9aa7adec10d5bc4f94fc2d99`；严格连续子串匹配已通过。

> Episode memory retains these artifacts, and the event trace
> preserves calls, returns, and failures.

来源：[S3.SS2.p3](https://arxiv.org/html/2610.38352v1#S3.SS2.p3)；核验缓存 SHA-256 `51ae93ab4c3f3275aa181a9bb283a533f444e5b3a680622d03f33b898924f53d`；严格连续子串匹配已通过。

> We first train Qwen3.5-9B with LoRA

来源：[S5.SS1.p1](https://arxiv.org/html/2610.38352v1#S5.SS1.p1)；核验缓存 SHA-256 `51ae93ab4c3f3275aa181a9bb283a533f444e5b3a680622d03f33b898924f53d`；严格连续子串匹配已通过。

> For the policy comparison, all models use the same instructions, tool schemas,
> runtime, and rendering budget.

来源：[S6.SS1.p2](https://arxiv.org/html/2610.38352v1#S6.SS1.p2)；核验缓存 SHA-256 `51ae93ab4c3f3275aa181a9bb283a533f444e5b3a680622d03f33b898924f53d`；严格连续子串匹配已通过。

> Our variants differ only in the training stages applied to the
> shared 9B backbone within the same production environment.

来源：[S6.SS1.p2](https://arxiv.org/html/2610.38352v1#S6.SS1.p2)；核验缓存 SHA-256 `51ae93ab4c3f3275aa181a9bb283a533f444e5b3a680622d03f33b898924f53d`；严格连续子串匹配已通过。

## IntReal: A Real-World Dataset and Benchmark for Multimodal Interleaved Generation

[官方论文](https://arxiv.org/abs/2610.38425) · [HF 条目](https://huggingface.co/papers/2610.38425)

HF 榜日：2026-10-30；首次发表：2026-10-28T08:09:05Z；版本更新：2026-10-28T08:09:05Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

交错图文生成的数据集、指标与模型 post-training，不是 Harness 或递归改进评测。

> By benchmarking four families of UMMs, we show that IntReal Evaluation Suite reveals distinct strengths and weaknesses across models.

来源：[官方摘要](https://arxiv.org/abs/2610.38425)；核验缓存 SHA-256 `bbe42ad3556aae8bffdf1f7a2631f566c31533c49602e4777c78bea5f566d56b`；严格连续子串匹配已通过。

> Post-training experiments demonstrate the utility of IntReal-100K for improving interleaved generation

来源：[官方摘要](https://arxiv.org/abs/2610.38425)；核验缓存 SHA-256 `bbe42ad3556aae8bffdf1f7a2631f566c31533c49602e4777c78bea5f566d56b`；严格连续子串匹配已通过。

## AskStream: When and What to Ask Proactively under Uncertainty in Streaming Video Understanding

[官方论文](https://arxiv.org/abs/2610.38678) · [HF 条目](https://huggingface.co/papers/2610.38678)

HF 榜日：2026-10-30；首次发表：2026-10-28T18:54:27Z；版本更新：2026-10-28T18:54:27Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

评测流视频中的 wait/ask/answer 决策，属于普通交互能力基准，不是 Harness 演化。

> we introduce AskStream, the first multi-turn benchmark spanning video and user uncertainty for streaming video understanding, with four task categories and eight subtasks.

来源：[官方摘要](https://arxiv.org/abs/2610.38678)；核验缓存 SHA-256 `f61516870af505b287fadfdf69195915459d7c63f2eb6410dbc37f49df63e295`；严格连续子串匹配已通过。

## Intrinsic Distribution Matching

[官方论文](https://arxiv.org/abs/2610.39633) · [HF 条目](https://huggingface.co/papers/2610.39633)

HF 榜日：2026-10-30；首次发表：2026-10-29T08:57:17Z；版本更新：2026-10-29T08:57:17Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

图像生成分布匹配蒸馏/LoRA，EMA 是训练估计器，不是独立自改进环或 Harness 修改。

> Experiments use full-parameter and low-rank adaptation (LoRA) tuning on Z-Image-Turbo 6B and Qwen-Image 20B.

来源：[官方摘要](https://arxiv.org/abs/2610.39633)；核验缓存 SHA-256 `4bfc27782bca5b5004e8a09ba3f15c5e50a59f6552cd26fc1147192d252ef058`；严格连续子串匹配已通过。

## EditAgent: Rethinking Agentic Image Editing

[官方论文](https://arxiv.org/abs/2610.39664) · [HF 条目](https://huggingface.co/papers/2610.39664)

HF 榜日：2026-10-30；首次发表：2026-10-29T09:15:52Z；版本更新：2026-10-29T09:15:52Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

固定工具池/路由/验证记录修订当前图像；训练数据随后单轮 fine-tune 编辑器，不修改可复用 Harness。

> It routes each step to general editors and specialized methods, and attaches to each candidate a verification record.

来源：[官方摘要](https://arxiv.org/abs/2610.39664)；核验缓存 SHA-256 `40f18a1d23d07c8c0f8e35013f57883a6df555077b6d40d93932c69d494bbb87`；严格连续子串匹配已通过。

> Candidates are generated in parallel and judged in one listwise call

来源：[官方摘要](https://arxiv.org/abs/2610.39664)；核验缓存 SHA-256 `40f18a1d23d07c8c0f8e35013f57883a6df555077b6d40d93932c69d494bbb87`；严格连续子串匹配已通过。

> After every turn, a history check therefore shows the VLM the original image, the results of earlier turns and the current image, and asks whether each earlier request still holds.

来源：[S4.SS3.p1](https://arxiv.org/html/2610.39664v1#S4.SS3.p1)；核验缓存 SHA-256 `aeb16669535b4be7c640c8caebb9d569d05f8bbb5df4519cf0ca5a9804cf179b`；严格连续子串匹配已通过。

> We fully finetune Qwen-Image-Edit-2511 and FLUX.2-klein-base-9B on each dataset for one epoch and evaluate them as standalone editors.

来源：[S5.SS3.p1](https://arxiv.org/html/2610.39664v1#S5.SS3.p1)；核验缓存 SHA-256 `aeb16669535b4be7c640c8caebb9d569d05f8bbb5df4519cf0ca5a9804cf179b`；严格连续子串匹配已通过。

## Your LR Schedule May Not Be Principled: Effective Learning Rate Scheduling in Weight-Normalized Training

[官方论文](https://arxiv.org/abs/2610.40362) · [HF 条目](https://huggingface.co/papers/2610.40362)

HF 榜日：2026-10-30；首次发表：2026-10-29T16:15:08Z；版本更新：2026-10-29T16:15:08Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

学习率调度理论及预训练对照，外部固定 schedule 不构成多轮自主修改训练方法或 Harness。

> Schedule design should therefore target ELR rather than the nominal learning rate (LR) alone.

来源：[官方摘要](https://arxiv.org/abs/2610.40362)；核验缓存 SHA-256 `161474cc143e47d0cff03daa504474bdece38689de2e2521fee3c35a41bfc572`；严格连续子串匹配已通过。

> Experiments on 128 B-token Mixture-of-Experts pretraining demonstrate that AIR outperforms cosine and other candidate schedules

来源：[官方摘要](https://arxiv.org/abs/2610.40362)；核验缓存 SHA-256 `161474cc143e47d0cff03daa504474bdece38689de2e2521fee3c35a41bfc572`；严格连续子串匹配已通过。

## HairDeck: Animation-Ready Stylized Hair Cards from a Single Image

[官方论文](https://arxiv.org/abs/2610.40599) · [HF 条目](https://huggingface.co/papers/2610.40599)

HF 榜日：2026-10-30；首次发表：2026-10-29T17:50:26Z；版本更新：2026-10-29T17:50:26Z。

Harness 建议：`exclude`；广义 RSI 建议：`exclude`；owner decision：`defer`。

图像生成可动画发片资产的 diffusion 方法，未研究 Agent 系统或自改进。embodied 仅为邻近主题，不能当 RSI 分类。

> each card is a single token, and a set diffusion transformer denoises all cards together.

来源：[官方摘要](https://arxiv.org/abs/2610.40599)；核验缓存 SHA-256 `bb8e14e28d43ef3bad99fa5ceda17a81bb4495ce1016cce56f70f30181527efd`；严格连续子串匹配已通过。

