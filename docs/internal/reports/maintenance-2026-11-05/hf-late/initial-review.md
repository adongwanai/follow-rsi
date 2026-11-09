# 11/05 HF late snapshot — preliminary abstract review

观察时间：2026-11-05T15:36:25.291934+08:00。本次仅免费请求当日HF完整榜单一次（HTTP 200），从11:15的5篇增至20篇；新增15篇、无移除，原5篇题名/摘要/日期字段无变化。原始快照SHA-256保持。

新增15篇摘要初筛均为排除建议；其中 **PyRUA-DataFarm、EmoReward、SleuthVLM** 保留优先正文待查，不能据此宣布最终无符合项。14篇当前不在canonical；PyRUA-DataFarm已于上午S2入库，这次是新的HF推荐归属，原first_seen必须保留。

对HF完整榜单新增15篇逐篇读取完整原始摘要，未按关键词丢弃。本文件只是范围初筛，未读正文或独立复核，不等同正式排除、批准、日报生成或发布。3篇显式保留优先正文待查；HF日期均按原API字段保留，未将HF推荐日或reported发布时间伪装成官方v1日期。20篇是15:36观察快照，仍不是全天最终榜单。

| ID | 题名 | HF报告论文日期 | HF推荐日 | 初步建议 | 正文待查 |
| --- | --- | --- | --- | --- | --- |
| arxiv:2611.06910 | FrontierPhysics: Evaluating Agents for End-to-End Physics Research | 2026-11-04T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.06918 | From Pixels to Actions - Towards Native Vision-Language-Action Policies | 2026-11-04T18:59:58.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.05320 | PyRUA-DataFarm: LLM Agent as a Cost-Efficient Teleoperator for Real-Ready Robot Data | 2026-11-03T18:25:14.000Z | 2026-11-05 | exclude（建议） | 优先 |
| arxiv:2611.06483 | What Does Multi-Turn Reinforcement Learning Really Improve in LLM Agents? | 2026-11-04T13:24:54.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.01120 | StreamDuo: A Live Commentator and a Research Agent for Unseen Games | 2026-10-31T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.06518 | EmoReward: Self-Evolving Reward Calibration for Emotional Video Generation RL | 2026-11-04T00:00:00.000Z | 2026-11-05 | exclude（建议） | 优先 |
| arxiv:2611.06796 | VA-TDM: A Unified View for Improving Few-Step Diffusion Models by Velocity Adversarial Distillation | 2026-11-04T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.03228 | AnchorComplete: Recovering Complete Scene Meshes from Partial Point Clouds | 2026-11-02T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2610.41104 | MUON-RT Reusing the Teacher's Trajectory for Momentum-Free Muon for LLM Self-Distillation | 2026-10-30T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2610.40131 | VideoMemBench: How Well Do MLLMs Remember in Video Conversations? | 2026-11-03T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.06728 | Turns Matter: Advancing Streaming Video RL via Turn-Level Credit | 2026-11-04T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.06083 | SleuthVLM: Do We Really Need Audio-in-Video for Omni Video Understanding? | 2026-11-04T00:00:00.000Z | 2026-11-05 | exclude（建议） | 优先 |
| arxiv:2610.40516 | How I Aligned Your Model: Scaling Up Multilingual Safety Training with Templates | 2026-10-29T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.05304 | LoopVQ: Sub 1-bit KV Cache Quantization for Looped Transformers | 2026-11-03T18:16:29.000Z | 2026-11-05 | exclude（建议） | 未读正文 |
| arxiv:2611.05609 | On the Generalization Limitation of On-Policy Distillation for Post-RL Consolidation | 2026-11-03T00:00:00.000Z | 2026-11-05 | exclude（建议） | 未读正文 |

## arxiv:2611.06910 · FrontierPhysics: Evaluating Agents for End-to-End Physics Research

来源：[HF](https://huggingface.co/papers/2611.06910) · [arXiv入口](https://arxiv.org/abs/2611.06910)；原始定位 `$[1].paper.summary`；摘要SHA-256 `6a8331420906331aa028a64d58f90d56a0d37e78ee52206041e5456a3ac4d548`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-04T00:00:00.000Z`；HF record.publishedAt `2026-11-03T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

AI agents are playing an increasingly important role in physics research. However, existing physics benchmarks only evaluate fixed questions, isolated sub-tasks, or paper reproduction with given solutions, and rarely check research quality alongside correctness. We introduce FrontierPhysics, an end-to-end benchmark with 56 tasks made by 42 physicists based on their own research, covering nine domains across theoretical, computational, and experimental physics. Each task requires agents to review the literature, develop a research plan, conduct research and experiments, and produce structured outputs and scientific manuscripts. Combining deterministic verifiers with expert-authored rubrics, FrontierPhysics evaluates whether agents' research is correct and publishable. Across 22 models in 26 configurations, no configuration passes more than 46 of its 168 rollouts. Manual review of agent trajectories shows that frontier agents' main weaknesses are insufficiently rigorous reasoning and limited expert intuition, rather than gaps in physics knowledge or execution errors.

初步范围建议：**exclude / formal defer**。一般物理科研Agent端到端评测，评估科研正确性与可发表性；摘要没有把可复用Harness工件的反馈演化作为评测对象，不能仅因比较Agent配置纳入Harness专题。

## arxiv:2611.06918 · From Pixels to Actions - Towards Native Vision-Language-Action Policies

来源：[HF](https://huggingface.co/papers/2611.06918) · [arXiv入口](https://arxiv.org/abs/2611.06918)；原始定位 `$[2].paper.summary`；摘要SHA-256 `b16b8944fbe07bd13c86e875aac63cde2614c9303878567f1f0d277f23bf31f1`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-04T18:59:58.000Z`；HF record.publishedAt `2026-11-04T13:59:58.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Vision-language-action models are typically built on a simple premise: perception is first compressed by visual encoders, and action reasoning begins only afterwards. Yet manipulation often hinges on precisely the visual signals most vulnerable to this abstraction, e.g., local geometry, boundaries, depth, and subtle state changes. This raises a fundamental question: should action policies inherit a fixed visual endpoint, or directly access evolving visual computation? We introduce NEO-VLA, a structurally encoder-free vision-language-action framework. Images are tokenized by lightweight patch convolutional layers and evolve jointly with language throughout the backbone, allowing a flow-matching action expert to draw from instruction-conditioned visual representations at different depths. This simple change reveals a consistent pattern. Native architectures outperform encoder-based counterparts under controlled comparisons; full fine-tuning reduces but does not erase the gap, and additional scale alone cannot recover it. More strikingly, layer-wise probing shows that the action-critical signals often peak well before the final visual representation. Across diverse manipulation settings and distribution shifts, NEO-VLA consequently achieves stronger and more robust control. Together, these results suggest that embodied control benefits from access to visual representations across the computational hierarchy, rather than a fixed encoder output.

初步范围建议：**exclude / formal defer**。改进对象是VLA神经结构及分层视觉表征与动作学习；摘要未描述外部Agent程序依据反馈修改和持留。

## arxiv:2611.05320 · PyRUA-DataFarm: LLM Agent as a Cost-Efficient Teleoperator for Real-Ready Robot Data

来源：[HF](https://huggingface.co/papers/2611.05320) · [arXiv入口](https://arxiv.org/abs/2611.05320)；原始定位 `$[3].paper.summary`；摘要SHA-256 `492ec97b9283ef8b8299bfa05c7f26c1f4656f5a496d06753fa01258b9376c87`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-03T18:25:14.000Z`；HF record.publishedAt `2026-11-03T13:25:14.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Teleoperation remains the default way to collect robot demonstrations, but every episode costs robot and operator time, and every new task starts from scratch. We ask whether a coding agent can take over the teleoperator's job. In our DataFarm, the agent receives a data request and one calibration episode of the robot in the target scene and rebuilds the task in simulation: it writes the scene, an expert controller, and a success judge. The simulator supplies exact actions, and a video model conditioned on real images renders each rollout as photographic video, generating all camera views together consistently. The output is real-ready data: synchronized camera views labelled with the robot's actions, on which a policy can be trained directly and deployed on the real robot. Independent judges certify the expert and every rendered episode before admission. On five real-robot tasks, policies trained only on farm data match policies trained on as many teleoperated episodes (93 vs. 84 successes in 100 trials), and under an unseen tablecloth and coloured light they keep 87 successes where the teleoperation-trained policies fall to 46. Adapting a task is fully automatic and costs \21 of API usage on average, paid once per task, plus 5 for a render contract; every further episode costs \0.80 on average for simulation, rendering, and review, with no robot or operator. One hour of three-view data for a task costs 107 on average, these costs included, slightly below a quote of \117 for teleoperation in China and below 290 in labour alone in North America.

初步范围建议：**exclude / formal defer**。Agent为目标机器人任务生成仿真场景、专家控制器和成功判据，经独立judge验收生成数据；所描述工件是该任务的数据生产产物，尚无Agent自身跨任务执行Harness被反馈修订的证据。保留当前排除建议，优先核对controller/judge是否有独立Harness演化链。

正文待查：
- 核对专家controller和judge是单个目标任务产物，还是供Agent跨任务复用且经反馈更新的执行程序。
- 核对验收对象是生成数据/控制器可用性，还是Harness候选版本。

## arxiv:2611.06483 · What Does Multi-Turn Reinforcement Learning Really Improve in LLM Agents?

来源：[HF](https://huggingface.co/papers/2611.06483) · [arXiv入口](https://arxiv.org/abs/2611.06483)；原始定位 `$[4].paper.summary`；摘要SHA-256 `2e0e2509fcb1197d29354f24e04442f3e9a769c5c55f2575a37bfbbc4aad00f4`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-04T13:24:54.000Z`；HF record.publishedAt `2026-11-04T08:24:54.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

While multi-turn agentic reinforcement learning (RL) excels on long-horizon tasks, its performance gains remain highly sensitive to interaction constraints. Evaluating across sampling breadth K and interaction depth T via Pass@(K,T), we show that trajectory-level RL advantages depend on sufficient turn budgets, diminishing significantly when budgets tighten. Besides, agentic RL does not uniformly elevate single-step decision quality; rather, its strength concentrates in error recovery and long-horizon resilience. To mitigate the deployment risks caused by this budget dependence, we provide a preliminary discussion on the benefits and limitations of process supervision signals and introduce BudgetMix RL as an alternative that varies interaction budgets during training. Experiments demonstrate that BudgetMix RL achieves robust performance across diverse execution settings. Project Page: https://rethinking-agentic-rl.github.io/

初步范围建议：**exclude / formal defer**。讨论多轮RL训练所得模型能力对交互预算的依赖，并在训练中混合预算；模型error recovery或执行步数变化本身不证明外部可复用程序演化。

## arxiv:2611.01120 · StreamDuo: A Live Commentator and a Research Agent for Unseen Games

来源：[HF](https://huggingface.co/papers/2611.01120) · [arXiv入口](https://arxiv.org/abs/2611.01120)；原始定位 `$[5].paper.summary`；摘要SHA-256 `c12de4a5bce7c4cfc0a52f65b45bde3dc90a003c8c1903879d5f2294c84a46da`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-10-31T00:00:00.000Z`；HF record.publishedAt `2026-10-30T20:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Streaming video LLMs can now commentate live gameplay, but they are trained and tested on the same games. We study cross-game streaming commentary, in which a model trained on one game commentates games it has never seen, and find that current commentators transfer their timing but not their knowledge of the game world. We propose StreamDuo, which pairs a trainable commentator with a frozen research agent that reads the wiki of the game being played. When the commentator sees something it cannot name, it sends the current frames, and the research agent returns a few wiki entries two seconds later while the stream continues. We train only the commentator, on a single game, in two stages. Information-gain labels teach it to ask only where an answer would help it say what the human caster said, and on-policy self-distillation from a copy of itself that sees the ideal answer teaches it to use noisy answers. Trained on Baldur's Gate 3 and tested on ten unseen games, StreamDuo raises entity recall from 0.082 to 0.116 over Proact-VL trained on the same data, cuts source-game leakage from 9.9% to 1.0%, and achieves the best timing and the highest judged liveliness and overall quality among streaming models.

初步范围建议：**exclude / formal defer**。固定研究Agent从wiki检索并向commentator返回条目，训练的是commentator提问及使用答案的模型能力；摘要没有持久外部程序修订。

## arxiv:2611.06518 · EmoReward: Self-Evolving Reward Calibration for Emotional Video Generation RL

来源：[HF](https://huggingface.co/papers/2611.06518) · [arXiv入口](https://arxiv.org/abs/2611.06518)；原始定位 `$[8].paper.summary`；摘要SHA-256 `1738be7bb71f82ea5354991b36950a5e41ad47aeaaafc16228015623f2623945`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-04T00:00:00.000Z`；HF record.publishedAt `2026-11-03T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Group Relative Policy Optimization (GRPO) has advanced generative model post-training in verifiable domains such as code and mathematics, but evaluating video quality, especially emotional expression, often depends on subjective aesthetics and has no uniquely correct target. Existing approaches typically rely on fixed rewards for visual quality, motion quality, and text alignment that poorly capture emotional intent and can invite reward hacking, while RLHF is difficult to scale and subject to individual aesthetic differences that complicate the calibration of facial, body motion, and chromatic cues across narrative contexts. We introduce EmoReward, a new self-evolving training mechanism that distills evidence reliability from reward traces collected during an actual training run to adaptively guide multi-reward weight allocation in subsequent training by determining which emotional evidence to trust and how much to weight it. EmoReward first plans specific grounding cues from the emotional prompt to guide evaluation, then uses heterogeneous signal primitives to score the generated video during the act stage. Reflective Reward Gating calibrates their contributions through instance-level gates for phase, face confidence, conflict, and subtlety, then renormalizes weights over the active set to produce the sample's fused reward. RewardMemory then estimates each primitive's reliability from rollout scores and outcomes within each emotional regime in the finished training run, then fixes bounded multipliers that calibrate fusion weights in the next training run without updating reward models. Experiments on HunyuanVideo 1.5 show improvements across multiple RL algorithms and compare EmoReward with other agentic reward methods under SAGE-GRPO. Ablations and transfer experiments on SD 3.5 and FLUX further support adaptive reward calibration for visual generation.

初步范围建议：**exclude / formal defer**。明确有跨训练轮反馈与持留：RewardMemory从完成的训练轨迹估计可靠性，并把有界乘子固定给下一轮奖励融合。摘要所改对象是训练奖励权重，按现有taxonomy属于data_task；不能将“奖励模型未训练”直接等同于Harness演化。优先核对是否另有奖励评分/控制程序的反馈修订。

正文待查：
- 核对持久更新是否仅为训练reward融合数值权重，还是同时生成并更新可复用评分/控制代码或程序性策略。
- 将本例已明确存在的反馈和跨轮持留与外部Harness工件条件分别核对；不因同时训练视频模型单独排除。

## arxiv:2611.06796 · VA-TDM: A Unified View for Improving Few-Step Diffusion Models by Velocity Adversarial Distillation

来源：[HF](https://huggingface.co/papers/2611.06796) · [arXiv入口](https://arxiv.org/abs/2611.06796)；原始定位 `$[9].paper.summary`；摘要SHA-256 `740911eb1a7c8f8a8965df0874cb60aeaa32e69ab546fffe422b6624a29a7f90`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-04T00:00:00.000Z`；HF record.publishedAt `2026-11-03T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Few-step distillation offers efficient generation with diffusion and flow models, but preserving quality with only a few sampling steps remains challenging. Distribution-matching methods via score distillation provide a strong foundation, yet they rely on accurately tracking the student's changing distribution. At intermediate generation steps in few-step sampling, student-score estimation can be difficult, and commonly used estimators may describe a different distribution from the one used to update the student. Flow matching allows a more flexible approach to supervision through velocity fields constructed from the student's sampling process. Building on this perspective, we introduce Velocity Adversarial Distillation (VAD), which uses a learned critic to compare student and teacher fields and turn their disagreement into feedback for learning. VAD unifies score distillation, Fisher-based matching, and moment matching, also explaining existing heuristic MMD updates and delivering new training objectives. We further develop VA-TDM, which follows trajectory distribution matching: providing supervision for partial denoising along the student trajectory. Beyond this, VA-TDM combines transition-aware online velocity learning and dual-form VAD supervision across intermediate student transitions. Extensive results show that VA-TDM is powerful for learning few-step generators, achieving state-of-the-art four-step performance in both text-to-image and text-to-video generation across various backbones and scaling effectively to 33B MiniMax-H3. In particular, our VA-TDM-H3 notably outperforms the few-step Fast-H3 and is closer to the original many-step H3 according to human preference.

初步范围建议：**exclude / formal defer**。学习critic与学生速度场并蒸馏少步生成模型，属于神经生成模型训练目标和权重优化；无外部Agent程序更新。

## arxiv:2611.03228 · AnchorComplete: Recovering Complete Scene Meshes from Partial Point Clouds

来源：[HF](https://huggingface.co/papers/2611.03228) · [arXiv入口](https://arxiv.org/abs/2611.03228)；原始定位 `$[10].paper.summary`；摘要SHA-256 `32fb2a1af18835287b1e632fcd28651d75e1ba7120d60f3cbb7ec24cf89e689a`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-02T00:00:00.000Z`；HF record.publishedAt `2026-11-01T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Most image-based 3D reconstructors primarily recover visible surfaces, producing partial point clouds with large holes and leaving unobserved geometry unresolved. To address this limitation, we introduce AnchorComplete, a framework that reconstructs complete scene meshes from partial point clouds while preserving observed geometry and supporting scenes of varying scales. Building on TRELLIS.2, our method combines partial-point conditioning, which integrates global scene tokens with local spatial evidence to anchor generation to the input, and metric-scale coarse-to-fine generation, which progressively refines scene geometry within fixed-size windows while maintaining global structural consistency. Experiments on Replica and SCRREAM demonstrate that AnchorComplete consistently outperforms strong baselines in complete-scene reconstruction, particularly under sparse-view settings.

初步范围建议：**exclude / formal defer**。点云到完整场景mesh的几何重建框架，改进条件输入和多尺度生成；未涉及Agent外部程序演化。

## arxiv:2610.41104 · MUON-RT Reusing the Teacher's Trajectory for Momentum-Free Muon for LLM Self-Distillation

来源：[HF](https://huggingface.co/papers/2610.41104) · [arXiv入口](https://arxiv.org/abs/2610.41104)；原始定位 `$[12].paper.summary`；摘要SHA-256 `aa277612427a5d7c19c83c5a75cb15d35cfebeb85650cfac24fe050d596eac6e`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-10-30T00:00:00.000Z`；HF record.publishedAt `2026-10-29T20:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Self-distillation methods for large language models with an exponential moving average (EMA) teacher already retain a history of student updates. Muon nevertheless stores a separate momentum buffer, increasing persistent training memory. We propose Muon with Reused Teacher (Muon-RT), which reuses the teacher-student displacement to eliminate momentum buffers for hidden weight matrices. We show that this displacement encodes an exponentially weighted history of applied updates and smooths temporally uncorrelated noise under a local model. Muon-RT removes its radial component, normalizes it spectrally, and mixes it with the current gradient after Newton-Schulz (NS) orthogonalization. Under explicit regularity and alignment assumptions, we establish linear contraction of an expected objective-gap bound toward a residual error level. With Self-Distillation Fine-Tuning (SDFT) on Qwen2.5-7B-Instruct, Muon-RT improves average accuracy over AdamW by 2.6 points with 42% less persistent memory, and over momentum Muon by 5.4 points with 27% less persistent memory. With Self-Distillation Policy Optimization (SDPO) on Olmo-3-7B-Instruct, it improves average accuracy over AdamW by 2.0 points.

初步范围建议：**exclude / formal defer**。重用EMA教师与学生参数位移以取代Muon动量缓存，优化训练内存和权重更新；此处teacher trajectory不是Agent可复用程序工件。

## arxiv:2610.40131 · VideoMemBench: How Well Do MLLMs Remember in Video Conversations?

来源：[HF](https://huggingface.co/papers/2610.40131) · [arXiv入口](https://arxiv.org/abs/2610.40131)；原始定位 `$[13].paper.summary`；摘要SHA-256 `31ed88577767d29036e0c449bda0dfe9384159ef2e30a9a241e55a3c5517edbc`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-03T00:00:00.000Z`；HF record.publishedAt `2026-11-02T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Multimodal large language models (MLLMs) can now process hour-long videos, making extended multi-turn dialogue over a single video a natural mode of use. Sustaining such a dialogue requires more than answering each question in isolation: the model must retrieve and reuse information established earlier in the conversation, both what it has seen and what it has said, an ability we term in-context video memory. Existing video QA benchmarks leave this ability unmeasured: their questions are mutually independent, never reference one another, and each is answerable from the video alone, so nothing ever requires carrying information across turns. We introduce VideoMemBench, in which each sample pairs a single video with a long multi-turn dialogue, whose turns are connected by typed cross-turn dependencies: an Episodic Dependency refers back to a visual episode described in an earlier turn, probing memory of what the model has seen, while an Answer Dependency builds on the model's own earlier answer, probing memory of what the model has said. Every dependency is verified considering two properties: 1) necessity, meaning the question cannot be answered without its earlier turns, and 2) non-leakage, meaning the question does not restate the information from its earlier turns. To enforce these properties, we design a construction pipeline with three LLM roles: a planner, a generator, and a judger, with each dialogue reviewed by human experts. VideoMemBench comprises 326 videos with 2,476 turns, of which 1,387 depend on earlier turns, including multi-parent dependencies and long-range call-back. Among over 20 evaluated open- and closed-source MLLMs, Claude Opus 5 performs the best with an overall score of only 45.7%, highlighting the challenge of in-context video memory. Our dataset and evaluation are released.

初步范围建议：**exclude / formal defer**。评测视频对话中的跨轮信息记忆，planner/generator/judger构造基准数据；既未评测记忆管理机制的反馈修改，也未描述程序工件持久演化。

## arxiv:2611.06728 · Turns Matter: Advancing Streaming Video RL via Turn-Level Credit

来源：[HF](https://huggingface.co/papers/2611.06728) · [arXiv入口](https://arxiv.org/abs/2611.06728)；原始定位 `$[14].paper.summary`；摘要SHA-256 `dd31140edaf4883e9f710210b4652696bab99c542c93981861c14726823b4ec1`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-04T00:00:00.000Z`；HF record.publishedAt `2026-11-03T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Streaming video understanding requires models to repeatedly decide whether to respond or continue observing. Recently, Group Relative Policy Optimization (GRPO) has been applied to this setting, with existing approaches emphasizing reward design while retaining a single trajectory-level advantage across turns. Such shared credit can reinforce redundant replies after earlier successes and discourage useful follow-ups after earlier failures. We propose TurnWise, a turn-level GRPO framework that aligns learning with individual streaming decisions. TurnWise addresses the mismatch between trajectory-level feedback and turn-level interaction, promoting informative responses and reducing redundancy. Specifically, turn-level credit assignment uses silence-completed prefix scoring to construct group-relative advantages from each decision's remaining return, separating its learning signal from earlier rewards. Turn-mean policy optimization averages token losses within each turn and then across turns, giving response and waiting decisions equal weight regardless of output length. These complementary designs improve streaming policy learning without a learned critic or additional rollouts. Extensive experiments show our method outperforms prior RL approaches for streaming video understanding.

初步范围建议：**exclude / formal defer**。TurnWise重分配GRPO的轮级优势和训练loss，改进流式视频响应策略学习；没有描述外部Harness工件的反馈更新。

## arxiv:2611.06083 · SleuthVLM: Do We Really Need Audio-in-Video for Omni Video Understanding?

来源：[HF](https://huggingface.co/papers/2611.06083) · [arXiv入口](https://arxiv.org/abs/2611.06083)；原始定位 `$[15].paper.summary`；摘要SHA-256 `6cafb013441e91e870f336c2f8d150b1e0dedd34e8fe590a52c7a8d728cdedbb`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-04T00:00:00.000Z`；HF record.publishedAt `2026-11-03T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Omni models answer questions about videos by jointly processing sampled frames and audio in one turn, with progress driven largely by scaling model size and omni training data. We ask whether a model needs to hear the audio directly at all, and present SleuthVLM, an agent harness built on a VLM that never hears the audio directly: speech will be transcribed into text, and the VLM will sleuth the video on its own without any predefined workflow. On four omni benchmarks with videos up to 90 minutes, SleuthVLM achieves the best average accuracy: 75.0%, 2.6 points above Gemini 3.8 Flash, and it also tops the Video-MME-v2 leaderboard with 77.8%; with an open-source 27B VLM, it beats all open-source omni models. We draw three findings: SleuthVLM beats a model that glances; hearing is not the bottleneck, agentic ability is; omni understanding needs better agentic ability, not just more omni data for modality alignment. So we provide a simple but effective starting point for doing omni video understanding. Omni understanding needs better agents, not just bigger models that hear.

初步范围建议：**exclude / formal defer**。摘要明确提出VLM agent harness并允许动态调查视频，但“without any predefined workflow”说明运行时行动自由度，不等同于生成、接受并在后续任务继承Harness修订。当前按固定框架排除建议，优先正文核实是否有未在摘要交代的持久程序演化。

正文待查：
- 核对动态sleuthing仅为工具调用/当次规划，还是修改跨视频保留的工具、技能、提示或上下文管理程序。
- 若有可复用程序候选修订、反馈准入和后续继承，应改为纳入候选；不能因为框架名称或没有预设workflow直接定性。

## arxiv:2610.40516 · How I Aligned Your Model: Scaling Up Multilingual Safety Training with Templates

来源：[HF](https://huggingface.co/papers/2610.40516) · [arXiv入口](https://arxiv.org/abs/2610.40516)；原始定位 `$[17].paper.summary`；摘要SHA-256 `bb7c425ced93bbd4dc6d2d214b7d2651e68d21f1e21dae04bb51e2f2fb5a5774`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-10-29T00:00:00.000Z`；HF record.publishedAt `2026-10-28T20:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Safety alignment for Large Language Models is heavily focused on English with limited multilingual representation, particularly damaging low-resource language performance. Related open training datasets are often limited in size or do not follow region-localized harmful topics to broaden the scope of alignment beyond cultures. We propose a scalable template-based augmentation pipeline to produce massive multilingual refusal and benign corpora, extracting safe templates from harmful prompts, translating them and then filling in the slots with culturally authentic entities, both harmful and benign. As a result, we release MSafeTemp, a validated corpus spanning 60 languages useful for multilingual safety alignment and evaluation. Using the dataset, we show that English-only evaluation misjudges multilingual safety: for several models, attacks that fail in English succeed once translated, while culturally localized variants expose further failures that translation alone misses. We also confirm that augmenting safety training data through templates allows for higher diversity and quality of alignment, resulting in improved safety performance beyond English. MSafeTemp and the respective pipeline are aimed at facilitating research and development of safer and more responsible models for less-represented cultures.

初步范围建议：**exclude / formal defer**。按固定模板生成、翻译和填槽，构造多语安全训练语料并评价模型；摘要没有依据Agent反馈持续改写自身执行程序。

## arxiv:2611.05304 · LoopVQ: Sub 1-bit KV Cache Quantization for Looped Transformers

来源：[HF](https://huggingface.co/papers/2611.05304) · [arXiv入口](https://arxiv.org/abs/2611.05304)；原始定位 `$[18].paper.summary`；摘要SHA-256 `bd25720313793bab42b2de348785470910faa393ad8df7210cc7c929ec4031d8`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-03T18:16:29.000Z`；HF record.publishedAt `2026-11-03T13:16:29.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Looped transformers are a parameter-efficient alternative to standard transformers for language modeling. By reapplying the same layers across multiple loop steps, recent looped language models match the performance of non-looped models several times their size. While this architecture effectively reduces parameter memory, each loop step still stores its own keys and values, so the key-value (KV) cache grows linearly with the number of loop steps and becomes the main memory bottleneck. We observe that the KV cache of looped models is highly redundant along the loop axis and that the loop steps differ substantially in their sensitivity to quantization. Based on these observations, we propose LoopVQ, a KV cache vector quantization method for looped transformers that codes channels of multiple loop steps jointly, and fine-tunes the codebooks to match the output of the full-precision model. At 0.5 bits per element, LoopVQ outperforms existing KV cache vector quantization methods for standard LLMs on general, long chain-of-thought reasoning, and long-context retrieval tasks with Ouro and Huginn models. Its design is orthogonal to these methods, and combined with TaSQ, it retains much of the BF16 accuracy even at 0.25 bits per element. We also implement LoopVQ in SGLang, where it nearly halves the decode latency at a 32K-token context and raises the peak serving throughput by up to 4.3times and 6.1times on the 1.4B and 2.6B Ouro models compared to the BF16 baseline.

初步范围建议：**exclude / formal defer**。对looped transformer KV cache做向量量化和码本微调，SGLang是部署实现；循环网络结构与缓存压缩不构成Agent Harness演化。

## arxiv:2611.05609 · On the Generalization Limitation of On-Policy Distillation for Post-RL Consolidation

来源：[HF](https://huggingface.co/papers/2611.05609) · [arXiv入口](https://arxiv.org/abs/2611.05609)；原始定位 `$[19].paper.summary`；摘要SHA-256 `2f34101e6e1bbe4ac5a32334460064a1a90e02eb9b0fcc53d795ae89dca3b3a2`。
HF推荐日 `2026-11-05`；HF paper.publishedAt `2026-11-03T00:00:00.000Z`；HF record.publishedAt `2026-11-02T19:00:00.000Z`；submittedOnDailyAt `2026-11-05T00:00:00.000Z`。这些来源字段未冒充本次官方日期核验。

Multi-teacher on-policy distillation (MOPD) extends on-policy distillation (OPD) to consolidate capabilities from multiple teachers. Although prior work reports near-perfect in-distribution (IND) distillation performance, we find that this can mask incomplete capability consolidation beyond the supervised distribution. A preliminary study on synthetic reasoning shows that OPD does not fully transfer teachers' generalization capabilities. We then extend this investigation to real-world tasks, evaluating extrapolative and compositional generalization across mathematical reasoning, coding, agent, and long-context capabilities using Qwen3 models. Across extrapolative settings, OPD and MOPD reach 96.04-102.73% of their teachers' IND scores. Yet their out-of-distribution (OOD) scores remain 2.45-16.25% below the base model's. Across three compositional settings, MOPD improves IND performance over the base model, but its performance on composed tasks as OOD remains 18.19-24.34% below that of the best teachers. To understand these gaps, we examine teacher capability and data coverage as two potential bottlenecks. Jointly alleviating these bottlenecks eliminates OOD forgetting in our experiments and suggests the potential for generalization beyond the teacher. (M)OPD also reduces OOD forgetting on average relative to its reinforcement learning (RL) baselines. Analysis of the associated update geometry reveals smaller and more spectrally concentrated updates on average than those of the RL baselines, along with greater shared update structure under MOPD. Motivated by these findings, we propose geometry-based patching and base-preserving replay to improve OOD performance while largely preserving IND performance. Our findings identify a blind spot in capability consolidation via (M)OPD, highlighting the need for algorithms that explicitly support OOD retention and generalization.

初步范围建议：**exclude / formal defer**。分析on-policy蒸馏的泛化及权重更新几何，提出参数patching与replay；patching指模型更新而非外部可复用Agent程序。
