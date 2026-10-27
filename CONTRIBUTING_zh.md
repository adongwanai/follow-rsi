# 贡献指南

论文信息只改 `data/papers.yaml`，它是唯一数据源。不要手改 README、论文页中的生成区块或生成的 JSON、徽章、分享卡片。阅读路线在 `data/routes.yaml`，发布地址在 `data/site.yaml`。

任何数字和证据值的变化都要在 PR 中提供正文页码或表号。`unknown` 改为 `yes` 或 `no` 时必须写明依据，不能根据摘要、代码链接、标题或常识推断。缺失字段输出 `unknown`；`partial`、`na` 也必须有出处。`topology` 描述结构，不是证据得分，没有出处就保留 `unknown`。

`needs_reading: true` 必须在所有展示中标明「待细读 / Needs verification」。候选使用 `section: candidates` 和 `status: candidate`；arXiv 监控 issue 不会自动把论文写进正式列表。

英文摘要和结果只能翻译对应中文，不增加或删除事实。数字、单位、正负号、区间、百分号保持原样，并设置 `en_machine_translated: true`。测试比较数字 token 及出现次数，但不能替代语义审校；中文数词不要转成新增的阿拉伯数字。

可以编辑 AUTO 标记之外的手写内容，包括笔记、视频、方向解读和 idea。未填的位置保留 `<!-- TODO -->`，不要删改 AUTO 标记。论文页顶端标题属于手写区，改标题时需手动同步；证据卡标题随数据更新。

```sh
pip install -r requirements.txt
python scripts/validate.py
python scripts/build.py
pytest
```

提交数据和重新生成的文件。PR 检查发现生成物过期会提示运行 `python scripts/build.py`。构建器全程离线，不修改 `papers.yaml`。

## 作者徽章

每篇论文的 endpoint 位于 `<pages-url>/badges/<id>.json`。替换两个占位后复制：

```markdown
![evidence](https://img.shields.io/endpoint?url=<pages-url>/badges/<id>.json)
```

四项为留出集、同预算对照、跨模型迁移和成本。四项全为 `yes` 用绿色；存在 `unknown` 用灰色；其余用群青。待细读标记也会进入徽章。徽章记录证据，不代表背书或质量排名。

## 发布

填写 `data/site.yaml` 中的仓库、Pages 和可选订阅地址；将 `CITATION.cff` 与许可证中的 `<AUTHOR_NAME>` 替换为作者。重新构建并渲染卡片后，Star 链接、回流二维码和绝对地址的 OG 标签才会启用。未配置时明确显示占位。到 Settings → Pages 选择 GitHub Actions，到 Settings → Social preview 上传 `assets/social-preview.png`。

核心依赖只有 PyYAML、jsonschema、Jinja2、pytest。Playwright 仅用于独立的图片与浏览器验证步骤；二维码使用带许可证的本地 JavaScript，不增加安装依赖或网络请求。见 [开发说明](docs/development.md)。

监控每周一 UTC 01:17 执行，在标题和摘要中检索关键词并要求出现 `agent`，排除数据中已有的 arXiv ID 和已打开或已关闭的 issue，最多创建 15 个候选 issue，仅使用原始标题、链接和摘要。本地构建和测试不联网检索论文。
