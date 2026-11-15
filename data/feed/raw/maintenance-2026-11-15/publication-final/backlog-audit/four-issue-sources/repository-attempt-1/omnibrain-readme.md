<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/omnibrain-wordmark.svg" width="380" alt="OmniBrain-0">
</p>

<h1 align="center">OmniBrain-0: A Unified Agentic Model for Embodied Intelligence</h1>

<p align="center">
  Xiaomi Embodied Intelligence Team &nbsp;×&nbsp; Tsinghua University &nbsp;×&nbsp; University of Macau
</p>

<p align="center">
  <a href="https://arxiv.org/pdf/2610.36013"><img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/badge-paper.svg" height="28" alt="Paper: Technical Report"></a>
  &nbsp;
  <a href="https://public-bots.github.io/OmniBrain-0/"><img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/badge-project.svg" height="28" alt="Project Page"></a>
  &nbsp;
  <a href="#release-status"><img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/badge-code.svg" height="28" alt="Code: Release Soon"></a>
</p>

## 🌟 Core Highlights

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/repository-overview.webp?v=overleaf-20261020" width="100%" alt="Overview of OmniBrain-0: three-stage training, unified agentic execution, performance, and rubric-guided recursive self-improvement">
</p>


**OmniBrain-0 is a compact agentic brain that unifies manipulation and navigation in one learned high-level decision model.** It understands instructions, plans over multiple steps, coordinates specialist tools, tracks execution progress, and recovers from failures using environmental feedback.

The unified model learns task-level decisions while perception modules, VLA/VLN policies, and motion controllers retain their specialized execution capabilities.

- **One shared agent:** manipulation and navigation use the same high-level decision model.
- **4B / 9B models:** compact planners learn skill orchestration and feedback-driven recovery.
- **Five task benchmarks:** LIBERO-Pro, LIBERO-Plus, RoboCasa365, RoboTwin 2.0, and R2R-CE.
- **Recursive self-improvement:** rubric-guided reminders and verified trajectories connect interaction evidence to continued learning.

## Agent Architecture

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/architecture.webp?v=overleaf-20261020" width="100%" alt="Unified agentic execution framework connecting perception, manipulation, navigation and motion tools through observations and feedback">
</p>

The shared high-level model selects semantic tool invocations. Each execution returns observations and feedback for the next decision; expert interactions from the same framework supply trajectories for learning.

## Results

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/performance.webp?v=overleaf-20261020" width="100%" alt="Cross-domain performance comparison on LIBERO-Pro, RoboCasa365, RoboTwin 2.0, and R2R-CE from Figure 1 of the technical report">
</p>

Task success rates (%) reported in the manuscript. The RSI column denotes the model iterated through the RSI Data Flywheel.

| Benchmark | 4B | 9B | RSI iteration |
|:--|--:|--:|--:|
| LIBERO-Pro | 62.4 | 65.5 | **69.3** |
| LIBERO-Plus | 82.3 | 83.8 | **84.5** |
| RoboCasa365 | 33.6 | 39.6 | **43.2** |
| RoboTwin 2.0 | 87.2 | 88.2 | **89.4** |
| R2R-CE | 55.0 | 65.0 | **66.0** |

The first four rows report Overall / Total success. R2R-CE reports SR on the 100-episode `rand100` subset of Val-Unseen. These task evaluations are complemented by EmbSpatial-Bench, RefSpatial-Bench, and real-world manipulation tasks.

## Task Execution

### Manipulation with recovery

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/trace-libero.webp?v=overleaf-20261020" width="100%" alt="LIBERO-Pro execution traces showing a failed moka-pot grasp, revised decisions, recovery and verified placement">
</p>

The initial moka-pot grasp fails. OmniBrain-0 inspects the execution outcome, changes the action order, activates the stove, refines the grasp target, and retries before placing the pot on the burner.

### Bimanual task progress

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/trace-robotwin.webp?v=overleaf-20261020" width="100%" alt="RoboTwin 2.0 execution traces for arranging colored blocks and opening a microwave">
</p>

The agent maintains object and grasp state while arranging the blocks, and follows the articulated door motion while opening the microwave.

### Multi-stage household tasks

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/trace-robocasa.webp?v=overleaf-20261020" width="100%" alt="RoboCasa365 execution traces for stirring vegetables and preparing a bread basket">
</p>

The agent revises an off-target vegetable grasp and tracks intermediate outcomes while handling dependent household sub-goals.

### Navigation through ordered landmarks

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/trace-navigation.webp?v=overleaf-20261020" width="100%" alt="R2R-CE navigation traces following a bedroom, bed, closet and bathroom mirror, and a second route through a patio to a kitchen">
</p>

The navigation examples show instruction decomposition, grounded sub-goals, progress tracking, and endpoint verification through successive observations and tool calls.

## Method

OmniBrain-0 learns embodied capabilities through three stages:

1. **Embodied pretraining** establishes a shared initialization from embodied question answering and interaction data.
2. **Domain-specialized distillation** transfers expert planning and recovery behavior into manipulation and navigation agents.
3. **Multi-teacher on-policy distillation (MOPD)** consolidates the domain experts into a unified student using supervision on student-generated decision prefixes.

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/training.webp?v=overleaf-20261020" width="100%" alt="OmniBrain-0 training framework: embodied pretraining, domain-specialized distillation and multi-expert consolidation">
</p>

### Interaction Data Construction

Expert interactions are normalized, checked for trajectory quality, rewritten into state-grounded reasoning, and validated for consistency. Training retains canonical successes and successful recoveries.

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/data-pipeline.webp?v=overleaf-20261020" width="100%" alt="Data pipeline aligning expert observations, decisions, tool invocations and execution feedback">
</p>

## Recursive Self-Improvement

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/reminder-policy.webp?v=overleaf-20261020" width="100%" alt="Rubric-based policy update and reminder-policy validation from Figure 6 of the technical report">
</p>

The verifier assesses collected trajectories. The Meta-Agent refines robotics rubrics, and candidate reminders are validated through further interaction before they are retained.

**Analyze → Guide → Curate → Improve.** A Meta-Agent analyzes interaction evidence and refines rubrics and step-level reminders. Verified trajectories augment domain-expert training; MOPD then consolidates the updated experts into the next unified model.

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/flywheel.webp?v=overleaf-20261020" width="100%" alt="RSI data flywheel connecting challenging interactions, rubric-guided reminders, verified data, expert training and model consolidation">
</p>

### Reminder-Guided Execution

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/reminder.webp?v=overleaf-20261020" width="100%" alt="Reminder triggers at steps 2 and 3 during wine-bottle placement">
</p>

In this wine-bottle placement example, reminders are triggered before the grasp at step 2 and the following arm motion at step 3. The other displayed decisions proceed without reminders.

## Real-World Execution

Real-world evaluation includes block stacking, apple placement, and drawer opening. The examples below show the robot coordinating perception and manipulation tools while updating its decisions from execution feedback.

<p align="center">
  <img src="https://raw.githubusercontent.com/luo-yc17/OmniBrain-0/page/assets/real-world.webp?v=overleaf-20261020" width="100%" alt="Physical robot execution examples for cube stacking and apple placement">
</p>

## Project Website

Visit the project page at **https://public-bots.github.io/OmniBrain-0/**.

Explore interactive execution examples, benchmark results, the training framework, and RSI visualizations on the project website.

Website source and static assets are maintained on the [`page` branch](https://github.com/luo-yc17/OmniBrain-0/tree/page).

## Release Status

**Code: coming soon.**

## Citation

```bibtex
@article{team2026omnibrain,
  title={OmniBrain-0: A Unified Agentic Model for Embodied Intelligence},
  author={Team, Xiaomi Embodied Intelligence and Luo, Yuechen and He, Chong and Li, Fang and Xu, Shaoqing and Wang, Jingkai and Su, Menglun and Liu, Jiaxin and Jiang, Shengyin and Lai, Zhiyi and others},
  journal={arXiv preprint arXiv:2610.36013},
  year={2026}
}
```
