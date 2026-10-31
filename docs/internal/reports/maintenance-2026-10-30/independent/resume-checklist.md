# 2026-10-30 独立复核续接清单

当前只完成离线归档和分歧对照，所有正式决定继续为 `defer`。本轮收尾没有付费模型调用，没有改 canonical、审核单、论文库，也没有提交、推送或发布。

## 已完成，可复用

- [x] 冻结当前发布范围正例／边界的 199 / 199 项来源复核；含可疑 Harness 边界的优先队列 211 / 211 项均有来源记录。
- [x] 保存 42 项正文逐段裁决、42 项负例摘要检查、1570 条原文连续引句校验；引句存在不等于分类正确或性能获证。
- [x] 保存 HF 2026-10-30 的 16 项官方身份／摘要及 6 项正文选读；15 项新增、1 项既有 VibeGame。保留 HF 上榜日与论文原日期的区分。
- [x] 将 canonical gate 分歧与第三轮模型自身的修正分表，保留原始输出、API 失败和各自输入指纹。
- [x] 保持归档 manifest、冻结建议和 HF JSON 哈希不变；本包哈希通过验证。

## 后续复核，不可当作已通过

- [ ] 对 `gate-comparison.json` 的 13 项明确 gate 分歧逐项作最终 owner 审核。其中 6 项有 Codex 正文裁决，7 项仍是模型建议；不直接回写 canonical。
- [ ] 解决 28 项独立 `defer` 边界：区分策略／工具程序与固定管理器下的经验内容；明确 training_env_reward 与 improver 程序的边界；按 coevolution 例外重新判断权重共同迭代。
- [ ] 复核 canonical 的 32 项 borderline 和 133 项缺失 gate；普通 `include` 不是 Harness 批准，缺失 gate 也不是排除。
- [ ] 单独重开 AgentBug-Smith 的 `SKILL.md`＋pattern-scanner 蒸馏组件审核。该发现保持待审，不把整个 bug 修复任务自动接纳为 Harness。
- [ ] 对照 pipeline 的 source/canonical 输入指纹结果，确认拟应用建议的身份、版本、摘要与正文输入。两处题名排版差异已列在比较表，不自动改原始数据。
- [ ] 当前发布范围以外的 162 项正例／边界尚无独立来源第三轮，ID 已列入 JSON 的 `resume.out_of_scope_positive_missing_review_ids`。这些条目不能宣称三轮完成。
- [ ] 取得 2 项负例样本的官方摘要后再审核：`s2:35489297d4e58b5a925de8741050055e799325aa`、`s2:632b5b25ba18a2a2d45a6f62d49f68f3291e2cb7`。
- [ ] 后续恢复模型调用须由主任务另行安排；本次没有付费重试。HTTP 402 的 13 项原始状态保留：12 项有直接正文裁决，另 1 项有官方摘要排除筛查（`arxiv:2610.17616`）；BetterDeck 没有模型调用。缺官方摘要的 3 项另列为阻塞，其中 1 项在范围外正例缺失列表、2 项是上述负例样本。
- [ ] 独立 HF 建议与主审、身份／日期核验对齐后交 owner 审核；只有 owner 接纳后才能进入发布，不用“已生成日报”替代审核通过。

固定积压分母 1124，当前 canonical 1139；50 项保护项不进入本轮改写。不得汇报为“1139 项均已三轮审查”。没有重新运行实验，也未独立认证论文性能数字。

## 本地验证与恢复入口

`gate-comparison.json` 提供逐项分歧、模型修正、未决和缺失 ID；`manifest.json` 是覆盖事实，`frozen-findings.json` 是先冻结的独立建议。以 docs 归档包为准，不用 build 中的 in-progress manifest 替换它。

可离线运行 `python3 build/backlog-all-2026-10-30/independent-round3/finish_gate_comparison.py` 重新核对当前绑定；canonical 或冻结输入一旦变化会停止，必须显式重新建立比较版本，不能用旧建议静默覆盖新状态。
