# 2026-10-31 独立第三轮来源复核

状态：**已在对照主审前冻结；全部正式决定仍为 defer，未批准发布。** 本轮没有付费 API 调用，没有改 canonical、审核单或论文库。

HF 10 月 31 日接口返回 HTTP 200 空列表。10 月 30 日后补 23 篇，remote-main 新增 20 个稳定 ID，重叠 6 篇，去重审核 37 篇。后补条目仍属于 10 月 30 日，不能包装成今日新论文。原始发表日、最新版本日与 HF 上榜日分开保存；Broken on Arrival 的官方首次发表为 9 月 5 日，HF 的 10 月 25 日不能代替首发日期。

独立读完 37 篇官方摘要，并对 13 篇候选、边界及固定框架负例读正文选段。范围建议为 include 5、exclude Harness 30、defer 2；这些是供 owner 复核的专题判断。既没有宣称 37 篇全文精读，也没有独立认证论文数字。

## 候选与未决边界

| 条目 | 独立建议 | 依据与限制 |
| --- | --- | --- |
| arxiv:2610.37905 · FilingLoop: Evaluating and Evolving LLM Agents for Corporate Disclosure Review and Revision | include / component | FilingLoop 用已锁定的评估反馈替换 Reviewer／Filer 的 Markdown 程序性技能，仅用于后续未尝试案例；这部分是 Harness 技能组件，企业文件修订本身不是。 在线同一有序流中适应，企业可重复出现；不是公司互斥留出泛化。准入检查结构／内容，不按留出表现择优；未认证论文数字。 |
| arxiv:2610.38392 · Masked Erosion: How Acceptance Gates Lose Redundant Safeguards in Self-Improving Agents | include / safety_governance | 专门研究冻结模型周围的文本 Harness 被编辑、通过准入后成为下一代时的安全冗余流失；属于 Harness 演化评测，不要求评测器也自我修改。 多数实验人为提议删除，用于隔离准入机制；自然优化器小样本是案例，不估计真实部署中的风险频率。没有复现实验。 |
| arxiv:2610.39122 · Appreciation Teaches Unauthorized Execution: Self-Evolution Degrades the Robustness of Personal Agents to Indirect Prompt Injection | include / safety_governance | 仅 MetaClaw 技能演化分支属于 Harness 相关评测：完成会话的反馈生成可复用过程指令，后续会话插入系统提示并固定库做测试。RL 分支单独属于权重训练，两者不是共同迭代。 资格仅指技能过程指令分支；RL 分支另列。库的磁盘文件格式未独立查代码，不能自行补为 SKILL.md。模拟反馈和指定任务的结论不代表任意个人 Agent。 |
| arxiv:2610.39358 · Before the Next Rollout: Diagnosing Skill Utility Shifts from Policy Updates | include / coevolution | 策略经 GRPO 更新后，用失败轨迹编辑有 ID／版本的程序性技能正文，再在固定新策略下配对验证并保留候选技能库。外部技能与权重分别迭代，适用 coevolution 例外。 依据是有版本的过程正文修订，不是单纯经验项打分。准入容差允许下降，不能宣称每次接纳都严格提升；Figure 7 的版本 schema 需与实际运行工件进一步对齐。 |
| arxiv:2610.39508 · Compile Away Uncertainty: Self-Evolving Agent Skills via Programmatic Compilation | include / component | SkillCompiler 按操作执行反馈修复程序、条件与依赖，验证后版本化留在 Program Asset Bank／技能结构中供后续任务使用；可复用程序组件与任务临时产物有明确区分。 最终测试冻结技能库，但开发曾查看留出失败案例，因此不能标为完全干净的未见测试。局部程序校验不证明任意输入语义正确；数值与实验未独立复现。 |
| arxiv:2610.39714 · MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery | defer / ai4ai_with_possible_skill_component | MoLRSI 主体用固定选择规则读取工作流与经验记忆，科学工作流是任务产物；附加资源技能有执行失败修复和留存描述，但需确认实际保留的修改是 Agent 可复用调用程序，还是科研代码／依赖安装修复。仅该组件待审，不直接接纳整个搜索政策。 主流程的 effective search policy 随记忆状态改变，不等于选择规则程序被改写。技能验证／修复组件有描述，但实际修改位置和后续继承工件需补证；不能将科研工作流整体当作 Harness。 |
| arxiv:2610.39884 · KARMA: Training-Free Knowledge-Atomic Harness Evolution for Industrial Advertising Agents | defer / experience_world_model_with_possible_prompt_component | KARMA 改六类知识文件，显示的已接纳案例是经验规则；接口也允许 role／output_protocol／action_descriptions 改写，不能只因代码冻结一律排除，也不能把可编辑能力当作这些程序性字段实际演化的证据。需要真实保留补丁区分知识内容与策略工件。 固定执行代码并不排除系统提示演化；但六模块编辑能力也不能证明实验实际改过程序性提示。已展示案例主要是经验决策规则。离线匹配历史操作不证明业务收益。 |

## 正文核对的排除项

| 条目 | 独立建议 | 依据与限制 |
| --- | --- | --- |
| arxiv:2610.23656 · ABF-Bench: A Verifiable Benchmark for Agentic Blockchain Forensics | static_framework | ABF 有 Harness，但更新的是本次调查的 findings、leads、notes；正文给出固定工具和提示规则，没有反馈改写并跨任务保留程序的闭环。 |
| arxiv:2610.34298 · Matched Capabilities, Different Behaviors: A Controlled Study of MCP and CLI Interfaces for Language Agents | task_local_repair | DART 在当前动作失败后修正接口表达并保持语义动作不变；修复对象是单次调用，不会把新的控制程序保留到后续任务。 |
| arxiv:2610.38174 · Scaling Lean Theorem Proving for Real-World Code Verification | task_local_proof_search | EasyProver 的递归是当前证明任务中的子 Agent 搜索；可变产物是证明与基准任务，没有保留新的 Agent 程序版本。 |
| arxiv:2610.38568 · A-RSI: Adaptive Task Refresh for Zero-Data Multimodal Self-Improvement | model_weights | A-RSI 的生成模板、采样规则与控制器在训练前固定，持续更新的是 Solver 权重，训练反馈只决定何时切换预备任务池；没有外部程序共演化。 |
| arxiv:2610.38796 · Routed Continual Learning | experience_world_model | Routed CL 的路由提示和记忆系统库固定；仅选择状态簇、积累经验、做有界 schema 配置。配置验证后对该簇冻结，不能把路由选择当成管理程序演化。 |
| arxiv:2610.39417 · Well-Specified and Well-Tested? Assessing SWE-bench-Style Datasets with a Self-Evolving Agent | experience_world_model | ExLabel 用固定 RAG／维护程序增删改 Understanding、Successes、Mistakes 经验项；变的是经验内容而非管理策略或技能程序，不能因自称 self-evolving 就纳入。 |

另有 24 项按官方摘要排除 Harness，其中物理 RSI 综述和 From Grind to Grasp 可作广义 RSI 背景；其他包含模型训练、生成模型、静态评测等。摘要排除只表示本轮未取得 Harness 资格证据，若后续正文出现独立程序组件可重新审核。

## 这轮特别保留的限制

- FilingLoop 更新的是 Markdown 程序性技能；它测在线流式适应，企业可重复出现，没有独立公司留出测试。
- Masked Erosion 多为受控删除实验；自然优化器结果是小样本案例，不外推为普遍发生频率。
- Appreciation 的技能分支与 RL 分支分开判断；没有把它们写成 coevolution，技能磁盘格式保持未知。
- Before the Next Rollout 实际分别迭代权重与有版本的技能正文；准入容差允许下降，不能宣称所有已接纳修改都严格改善。
- SkillCompiler 的程序组件资格清楚，但论文承认开发中查看留出失败案例，不能写成完全未见的测试。
- MoLRSI 与 KARMA 保留两项边界：实际修改对象／已接纳补丁不足以在本轮彻底区分程序性工件和经验内容。

## 审查独立性与续接

来源采集复用 primary 保存的官方 HTTP 响应；冻结前只读取输入 ID、官方摘要／正文和日期信息，没有读这 37 项主审分类或理由。已知项目 taxonomy 与前一日的裁决，因此不声称不知道历史背景，也不把共享采集说成独立网络重验。

`source-reviews.jsonl` 保存逐项理由、引句、原日期、来源版本、选读章节、局限和后续动作；`frozen-findings.json` 先固定建议，随后才能与主审比较。来源全文仍位于本地 build 缓存，本包仅保存短引句和哈希。

后续：逐项对照主审；MoLRSI 需要保留的技能／工具修复 diff 与后续引用，KARMA 需要被接纳 mutation journal 的具体字段；所有候选仍交 owner 接纳。

## 冻结后完成的交叉对照

见 `comparison.md`、`comparison.json` 和 `comparison-validation.json`。初始 37 项 Harness 准入判断为 36 一致、1 分歧；补查 KARMA 官方 Figure 5 后，主审认可原理由把接口可编辑能力写成了实际修改，最终改为 borderline。最终共同建议为 5 纳入、30 排除 Harness、2 待定，正式决定仍全部 defer。独立冻结结论与来源引句未改写；新增图像检查单独标为冻结后证据。

## 导出时的路径净化

`source-inputs.json` 只将 `/criteria/owner_document` 的本机绝对路径改为来源文件名 `CODEX_PROMPT_FIX_AUDIT.md`；该外部文件不随报告打包，原内容 SHA 保留。脚本根目录继续由自身位置解析，所有论文缓存路径均为仓库相对路径，不依赖本机目录。

- 冻结原件 SHA：`ab33149808054f7a69cc76ef4b0aa1c28d770c77d37f55de427a8d4f76ba0bd7`。
- 净化导出版 SHA：`d2ff29d58084446df69d3cf239337a6b8a818f4442048a0a71bcbabaf34d2e52`。
- 移除这个路径字段后，两版内容的规范化 SHA 均为 `db45e0262f598f55ba2d178d0d45e42a317bacfdbea2362d756e587f8cfe8530`。

`export-path-redaction.json` 记录净化映射和导出时逐字替换检查。`frozen-findings.json` 继续引用冻结原件的 SHA，未伪装成导出版哈希；逐篇 `source-reviews.jsonl` 和冻结意见均保留原字节。`comparison-validation.json` 校验这条映射、未变的论文输入和原始来源哈希。不要重跑 `assemble_review.py` 来覆盖既有冻结记录；本次只运行对照校验器并更新包清单。
