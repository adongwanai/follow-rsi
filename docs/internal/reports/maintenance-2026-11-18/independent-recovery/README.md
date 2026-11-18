# 11/16 审核单的 11/18 独立恢复复核

原审核日为 11/17；本次复核日为 11/18，不回填成 11/16 当天完成。范围决定仍为 **8 项历史补录、6 项排除、1 项待补**。12 篇 arXiv 当前版本的正文、抽取文本和版本水印均已核验，正文与原审核单绑定的哈希逐项相同。3 份正文复用已提交归档，9 份由显式版本的官方 URL 免费重取。本子任务付费模型请求为 0，未修改 canonical 或正式审核单。

初始回执提出两处审核层修正（现已落实，见下方最终复核）：SkillForge 的试用到活跃转换只使用次数门槛，摘要不能暗示回报阈值；Hippo 多模型分别运行不等于演化产物跨模型迁移，`cross_model` 应为 `unknown`。范围决定与原始科学字段不变。具体替代文本和证据见 [amendments-proposed.json](amendments-proposed.json)。

Reward Engine 主文的 104/68 与表 12 的 104/67 冲突继续保留；定性摘要不引用这些数字。MFM 与 SkillScriptBench 的 `cross_model=unknown` 纠正成立。CoEvolve 仍为任务策略和经验条目的更新；两项权重型方法、Hippo 记忆内容更新、两篇公告的排除理由均经当前版本上下文复核。DOI 的正文与作者身份缺口保持 unknown。

这次不是盲审：复核者可见旧审核单。缺失的旧逐篇独立回执没有被伪造恢复；本目录记录当前复核的真实证据。范围核查不等于全部数字重算、代码或实验复现，也不代表已批准、已合并或已上线。

## 最终修正复核

修正版审核单已绑定到 `31e46a809ca2f542502d5e7174b5fade803e52a0`，SHA256 为 `c2d0199d7f9e43817eb05c83e85a0b6e8a8f7895628c0546b76324830fe7a473`。原审核单及初始独立回执保留；正式 `reviewed_on` 为 11/18。两处提案已精确落实，除真实审核日、修正摘要、Hippo 审核证据及追加纠正说明外，其余 15 条字段不变。8 份中英摘要数字检查通过，12 份正文与抽取文本的哈希再次匹配。

只读代码审查及独立临时副本回放确认：全部 15 条非 `review` 字段原样保留，`source_hash` 不变；MFM、SkillScriptBench 与 Hippo 顶层原自动 `yes` 保留，审核层 `unknown` 正确持久化；前两项的周刊 backlog 输出也保持 `unknown`，Hippo 保持排除。第一次副本 apply 记录 15 条，第二次 0 条；正式 canonical 未写入。主任务提供的 51 项离线测试日志已核对，其全套测试未由本复核者重复运行。

最终回执见 [review-findings-final.json](review-findings-final.json)，代码与证据一致性见 [evidence-persistence-crosscheck.json](evidence-persistence-crosscheck.json)。Reward Engine 的 104/68 与 104/67 反证、DOI 正文与作者身份缺口仍保留。该回执确认来源、范围、摘要与副本持久化，不代表 owner 合并、CI 或线上出版完成。
