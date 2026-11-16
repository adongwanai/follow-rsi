# 2026-11-16 免费来源交接

这是来源身份、日期和对账结果；未修改 canonical、审核决定、Git 或出版物，未调用付费模型。

- 12 路全部实际尝试，路由请求 90 次，补充公告正文/DOI 官方请求 7 次。
- 全量原始出现 3669 条 / 3499 个 ID；配置窗口内 350 条 / 318 个 ID。
- 相对 2090 条基线，提议新增 3 条：2 个 OpenAI 公告，1 个 S2/DOI 论文身份；0 旧来源/推荐日补记，0 模糊身份归并。
- HF 11/16 为 HTTP 400 not_ready，API 明确 available_through=11/13；11/15、11/14 分别为 HTTP 200 空数组；11/13 完整 34 条与前次成员及科学字段一致，无晚到成员或漏记推荐日。三种状态不混同。
- 3 路 arXiv 查询均为 HTTP 429；S2 引用保留 20 个成功页，S2 作者保留 10 份种子作者元数据、未走到作者论文页；两路均在 180 秒边界结束，未访问覆盖为 unknown。
- 两篇新公告官方正文、H1 与页头日期已核：页头 11/15，RSS 11/15 22:00 UTC，实际 first_seen 11/16。updated 为空、version=0 仅表示 unknown 占位；2610.09093 只作为公告引用论文，不转为今天新增。
- 新 DOI 10.1016/j.eswa.2026.135083 的官方 XML 明示 Available online 13 November 2026；并列保留 S2 11/01、Crossref 仅 11 月及第二作者 Yan-Qing Cai / Yanchang Cai 冲突。没有摘要或正文；ScienceDirect 403、text/plain 400，XML 200 只有 coredata。
- 原始字节和 SHA 全部保留；含匿名路由字段的 DOI 跳转页及拦截页仅本地。公开清单不含完整 canonical/重复派生快照，原始相同响应按哈希复用既有归档。
- source-evidence-index.json 是逐项主审入口；effective-integration-proposal.json 是最小规范记录提议；source-metadata-corrections.json 保留规范化前后差异。
- 来源 QA 13 / 13 通过。这不代表三轮范围审查或发布完成。

最小归档以 minimal-publication-files.json 为准；response-storage-index.json 明确原路径、可复用公共路径和本地限定正文，不能把本地文件称为公开附件。
