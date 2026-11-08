# 2026-11-02 独立复审：补读与勘误

这是在冻结独立复审后阅读分歧清单、补读正文并核对 owner 判据形成的旁记录。原始 findings.json 和 today-findings.json 逐字保留；本文件不是另一轮盲审，也不是人工批准。

- 覆盖全部 13 个历史分歧，另复查同样受共演化规则影响的 SkillForge 和今日 R²Orch，共 15 项。
- 其中 12 项建议变更；全部正式 decision 仍为 defer，publishable / human_approved 均为 false。
- 加上旁记录后的有效建议：历史 164 项为 **22 include / 130 exclude / 12 unknown**；今日 18 项为 **3 include / 14 exclude / 1 unknown**。
- 这里的 include 只表示建议属于 Harness 范围，绝不表示已接受或可发布。

## 规则问题

Owner 明确规定「权重和 Harness 都被迭代修改，算 harness/coevolution」。当前生产 harness_gate 提示词额外要求外部 Harness 为明确主要改进对象，两者存在张力。StateSkill、SkillForge、R²Orch 均有模型更新与独立外部技能版本更新证据，故按 owner 边界纠正建议。

未修改生产提示词，未调用付费模型，未重算或改写自动闸门。正文引文只支持本次待人工审核建议，不冒充摘要子串 gate 证据。R²Orch 的技能库用于训练/改进过程，最终为 zero-skill 部署；不能宣传为最终执行仍携带外部技能库。

## 逐项记录

| 记录 | 原独立建议 → 补读后建议 | 核心依据 / 仍缺证据 |
| --- | --- | --- |
| `arxiv:2609.36603` | unknown → include (component) | 安全政策明确包含后续防御必须检查的条件和必须执行的动作，由失败轨迹蒸馏，并作为行为指令注入以后任务的系统提示；不能仅因存于记忆树就归为经验内容。 |
| `arxiv:2609.37673` | exclude → unknown (unknown) | 正文有输入、顺序步骤、工具依赖和版本明确的可调用技能，也允许不训练基座而更新资产；尚不能把来源纠错和人工交叉审核等同于代理执行反馈自主修订技能。原排除建议的确定性过高。 |
| `arxiv:2610.11344` | unknown → unknown (unknown) | Scientific Evolution 明确保存、连续修订并在以后研究运行中使用 procedure。具体展示却是离散科学模型更新与其检查条件，仍需区分科研产出知识和做研究的 Harness 程序；保持待定而不强行与初审排除意见一致。 |
| `arxiv:2610.11966` | exclude → unknown (unknown) | 方法确实根据相对评估优势更新控制器参数，并从控制器分布采样思维图；已读实现未足以确认参数属于训练出的神经模型权重还是持久外部控制配置。原先直接标为 model_weights 的证据不足。 |
| `arxiv:2610.14601` | exclude → include (coevolution) | 外部 StateSkill 状态图与指导语依据轨迹反馈修订，候选在固定 MLLM 与执行配置下单独验收，改进后保留；另一路 StateGRPO 更新模型。按 owner 的权重与 Harness 分别迭代规则，建议 Harness/coevolution。 |
| `arxiv:2610.22686` | exclude → include (component) | 补读正文确认 procedures/ 不只存经验：保存文本或可执行动作程序，按后续尝试修订并让以后交互继续使用；案例也给出程序调用与新任务复用。仅该程序性组件建议计入 Harness。原抽象级排除遗漏了这些机制。 |
| `arxiv:2610.23288` | exclude → unknown (unknown) | 正文证明反馈校验后的 executable exemplars 可以保留和迁移，不能再简单称只有文本经验；但静态技能库不演化，执行策略又受单动作和当前子任务约束，尚缺可复用 Harness 程序与动作示例的清晰界线。 |
| `s2:35489297d4e58b5a925de8741050055e799325aa` | exclude → unknown (unknown) | Crossref 确认题名与 DOI，但官方摘要/正文仍不可得。原排除仅依赖 canonical/S2 摘要，不能作为已核来源的排除结论，因此改为带外部阻塞的待定。 |
| `arxiv:2610.07650` | unknown → unknown (unknown) | 设计包含程序知识包、版本采用和审查，实证只展示操作员辅助跨机器人迁移。正文同时说明群体聚合与长程演化未验证；仍缺实际工件、接收方采用记录和闭环证据。保留待定，不把设计说成验证成功。 |
| `arxiv:2610.11552` | exclude → include (component) | WorldAbduct 除隐藏规则账本外，还按轨迹分析直接改任务代理协议、状态跟踪、策略上下文或代码；提示 proposal 向指定组件加入指令，验证任务选择更新后再留出测试。原仅按摘要把它归为世界知识条目不完整。 |
| `arxiv:2610.19386` | exclude → unknown (unknown) | 结构图包含技能、代码、角色与工作流节点，typed reflector 会按结果扩展它们。但已展示案例只累加变体/避坑 bullet，明确说 procedure 没有改写。单个例子不足以证明全方法没有可复用行为工件更新，也不足以证明实际代码/技能版本演化，故改待定。 |
| `arxiv:2610.22915` | unknown → unknown (unknown) | RewardPack 并非始终只有任务输出变化：QC 使用标记对照修补可执行检查器，轮次边界可保留、重建或修订版本并携带 repair ledger。但跨任务族改进构建策略的 meta loop 明确未评测，现有证据仍不足以确定持久跨任务 Harness。 |
| `s2:632b5b25ba18a2a2d45a6f62d49f68f3291e2cb7` | exclude → unknown (unknown) | DySkillMem 的精确题名/DOI 已由 Crossref 核验，但 canonical/S2 摘要未能与原站核对。把其描述的固定技能选择当作已证实排除依据不妥，改为带外部阻塞的待定。 |
| `arxiv:2610.09832` | exclude → include (coevolution) | SkillForge 根据父技能内容、适应度及失败例生成技能变体，进入下一代 trial，并按累积适应度更新库；模型 policy 同步更新。两类对象各有反馈和持久版本，因此按 owner 规则建议 Harness/coevolution。 |
| `arxiv:2610.22740` | exclude → include (coevolution) | R²Orch 训练 Director 的同时，LLM editor 根据失败组修订/生成外部技能，并以 identifier、version、content hash 建立新的 trial 版本；未变技能的记录跨 Director 更新保留。按 owner 规则建议 Harness/coevolution。 |

## 尚未解决的边界

EvoSim、Silicon Language、Reward Engine 仍与初始主审的 exclude 不同，本记录保持 unknown。分别需要区分科研模型知识与研究执行程序、核验机器人程序反馈采用链、证明跨任务保留验证器或构建策略。不能为了统一结论而隐藏争议。

IEEE 的 Safe and Scalable Collaboration 与 DySkillMem 已核题名/DOI，但页面 202 空响应、PDF 418；原排除依赖未核实的 S2 摘要，已改为有外部阻塞的 unknown。其日期/作者差异保持不动。

## 校验与可恢复性

精确引句子串与来源 SHA-256 校验 42 条通过；15 个稳定 ID 唯一、13 个原分歧覆盖完整；两个原冻结文件 SHA-256 未变。所有建议仍待人工处理。没有编辑 canonical、审核单、README、网站或生产提示词，没有提交、推送、合并或发布。

机器可读文件：comparison-errata.json。校验结果：comparison-validation.json。comparison-checksums.json 记录交付文件摘要。每项保留前一建议、来源路径、URL、精确引句和待补证原因。
