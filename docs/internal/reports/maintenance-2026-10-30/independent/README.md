# 2026-10-30 独立第三轮复核

状态：**已冻结；所有正式 decision 均为 defer，未批准公开发布。**

原始积压分母固定为 1124 项，其中 50 项 owner/catalog 保护项完全排除在本轮改写范围外。HF 当日另有 16 项，15 项新增、1 项原有 VibeGame，不能将 16 直接加到积压分母。

- 当前发布范围内正例/边界：199 项，已取得独立原始来源复核 199 项。
- 含可疑 Harness 边界的优先队列：211 项，已复核 211 项。
- 排除项官方摘要人工代理抽查：42 项；当前分层样本 65 项，模型或人工代理已复核 63 项。
- 正文机制逐段裁决 42 项；原文连续引句验证 1570 条。
- 范围外未做第三轮正文的条目仍标明未完成，不冒充全积压三轮通过。

“人工代理”指 Codex 阅读原文，不是 owner 人工批准。模型第三轮使用 deepseek-flash，引用检查能证明引句存在，不能证明分类推论必然正确。优先队列阅读层级：{'official_body_excerpt_and_abstract': 182, 'official_body_selected_passages': 29}。

末批 API 返回 HTTP 402 后已停止付费重试；其中 12 个候选由 Codex 直接阅读官方正文相关章节完成范围复核，另有 1 个最终新增范围候选未发起模型 API 即直接读原文。原模型错误状态保留，不能写成 API 全成功；每条直接阅读记录包含章节、引句、来源哈希和局限。原始模型输入 hash 与人工代理所读来源包 hash 分开保存，包哈希不表示通读每个字符。

## 主要裁决

1. CoHARL、VACE、AdaRSI、CoTrace 等不能仅因同时训练权重排除；真实权重和外部程序共同迭代适用 owner 的 coevolution 例外。
2. RSIHub 建议计作 Harness 演化评测框架；报告结果使用固定 recipe，不应宣称外层 agent 自适应 recipe 改写已实测。
3. VibeGame 建议仅认可保留的 collaboration contracts 组件。主结果没有累计经验，单独迁移消融合并多种工件，无法隔离合同组件贡献；跨类型累计可能降分。
4. Hippo、GraphMemory、EvolveMAS、AMIE 等不能仅因记忆条目被增删改或重排算作程序演化。OOPMAS、InFlowOp 的当前任务流程与经验记录也需保持这一区分。
5. Doc2Harness 明确是单次构建评测；BRACE 文中 DISCORD 则单独评测 Harness 编辑保留，评测本身无需自行产生提案。
6. UniSkill、EASE、EvoSteer、OmniBrain-0、CODA 等保留程序工件与经验内容边界为 defer；ECG-RSI/RRI 的训练环境/奖励生成器与 improver 边界也需 owner 裁决。
7. 负例抽查发现 AgentBug-Smith 的 Appendix I 确实逐次改写 SKILL.md 与 pattern scanners 后在留出任务复用。仅该组件建议重新纳入候选；原始 bug-reproduction/外部修复任务仍不自动属于 Harness RSI。

逐条原文、建议、局限和后续动作见 `adjudications.jsonl`。这些是范围建议，未认证性能数字，也没有原始实验复现。

## HF 当日

16 篇身份、原日期、版本、摘要均对齐官方 Atom；独立阅读 16 个摘要及 6 篇正文相关章节，验证 33 条引句。仅 VibeGame 建议作为 Harness 组件候选；WorkFactory 与 WebAnything 为相关环境/数据线索，广义 RSI 闭环仍待证，其余排除 Harness。HF 上榜日是 10 月 30 日，论文原日是 10 月 15–29 日，分开记录。

完整冻结报告见 `hf-today-report.md` / `.json`，JSON SHA256 为 `35d6c95e8ed3d27bf48c5f42994b6c2d4a793d8e3b0cb35d22574a64c3366944`。

## 审查独立性与判据修正

积压分类标签、方向和 gate 类别只用于选覆盖目标；第三轮不读取主审理由。HF 子集在结论冻结前收到兄弟 agent 主动发送的类别摘要与 VibeGame 局限提示，之后重新对照原文；不声称 HF 完全盲审。

初版第三轮模型提示漏写 owner 的 coevolution 例外。保留原模型输出和 `independent-prompt-v1.txt`；后续模型使用修正版 `independent-prompt.txt`。每条原始记录保留实际 prompt_hash，旧输出不会伪装成新提示运行。相关混合权重/评测案例用原文逐段裁决覆盖；不对未逐段裁决的模型建议宣称 owner 认可。

## 文件与复核

- `source-reviews.jsonl`：全部本次已保存的原始模型记录，含错误/阻塞状态及旧建议；有效修正以 `adjudications.jsonl` 为准。
- `negative-adjudications.jsonl`：42 条官方摘要范围抽查，不声称全文精读。
- `manifest.json`：逐项覆盖、有效建议、缺失项、保护项集合与真实完成状态。
- `source-provenance.json`：官方 URL/版本、输入与原始来源哈希、正文完整/截断范围；没有复制完整论文或 HTML。
- `validation.json`：本地原始文件哈希和连续引句校验结果，表示保存证据一致，不表示自动分类正确。

模型叙述中的额外实验数字未经本轮独立性能审计。正式 gate 校准的质量阈值由主流程另行报告，不能用本包的引用通过率替代召回率验收。

## 冻结后的 gate 对照与续接

最终对照见 [gate-comparison.md](gate-comparison.md) / [gate-comparison.json](gate-comparison.json)。388 个有来源复核的积压条目中，13 项存在明确 gate 与独立建议分歧（6 项正文裁决、7 项模型建议），另有 32 项 canonical borderline、15 项已有 gate 但独立未决、133 项没有 gate。这些分歧与第三轮模型自身被原文修正的 20 项建议分开列示，不把普通 include 当成 Harness 接纳。

[resume-checklist.md](resume-checklist.md) 列出剩余 162 项范围外来源复核、2 项缺摘要样本、28 项独立未决边界和 AgentBug-Smith 组件的待审动作。所有正式决定保持 defer；收尾没有新增付费调用、数据改写或发布。冻结 manifest、findings 与 HF 报告保持原哈希。
