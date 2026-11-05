# RSI-Dojo 正文补审

正文的 improved harness 是在 AutoTrainess 基础上为轨迹采集增加针对失败模式的指导；没有展示系统自主提案、反馈选优并跨轮继承该指导工件的更新过程。采集指导在最终评测中不使用；反馈用于筛训练轨迹和迭代目标模型。该工作属于自动后训练任务/数据与模型能力研究，不是 Harness 自演化方法或专项评测。

建议仍为 **exclude**，正式决定仍为 **defer**。明确的优先正文缺口已补齐；没有科研数值复算或正式接受。

- [3.2 Trajectory Collection with Improved Harness](https://arxiv.org/html/2611.03698v1#S3.SS2.p1): “The base harness follows AutoTrainess”
- [3.2 Trajectory Collection with Improved Harness](https://arxiv.org/html/2611.03698v1#S3.SS2.p1): “We further augment this harness with additional guidance targeting the identified failure patterns.”
- [3.3 Trajectory Filtering and Model Training](https://arxiv.org/html/2611.03698v1#S3.SS3.p1): “The remaining trajectories are then used to train the agent model.”
- [4.2 Evaluation Models and Environments](https://arxiv.org/html/2611.03698v1#S4.SS2.p2): “During evaluation, we do not include the additional guidance introduced for trajectory collection.”
- [Effect of additional guidance.](https://arxiv.org/html/2611.03698v1#S5.SS2.SSS0.Px1.p1): “We randomly sample 100 trajectories collected with the base harness and 100 trajectories collected after adding our targeted guidance, then analyze their quality.”
- [7 Limitations and Future Work](https://arxiv.org/html/2611.03698v1#S7.p2): “we do not close the loop by using our trained models to train an improved successor of themselves.”

- 读的是方法、评测设置、指导消融与局限的相关段落；不声称代码/补丁审计或全篇数值复算。
- We augment 不足以单独证明人工或自动；排除依据是没有给出系统自修改及工件保留机制，不以同时训练权重作为排除理由。
- S7模型自身递归闭环尚未完成是独立的局限，不能单独用来否认所有可能的Harness机制。
- 旧摘要筛查报告保持冻结，本补审仅补正文依据，不修改first_seen、原发表日、数字或正式决定。
