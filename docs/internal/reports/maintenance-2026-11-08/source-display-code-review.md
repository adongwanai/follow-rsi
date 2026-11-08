# 来源状态显示修复：独立代码审查

- 审查基线：`HEAD 8d47374b0f004c8db42fd2104d8ece88c7864c00`。
- 范围：`scripts/feed/digest.py`、`scripts/feed/templates/daily.html`、`tests/feed/test_daily.py` 相对 HEAD 的改动；只沿调用链查看必要上下文。
- 结论：**未发现阻塞缺陷或需修改的生产代码问题。**

## 核对结果

1. **状态区分符合现有采集语义。** `digest.py:234–243` 优先将 `availability=not_ready` 显示为“榜单未就绪”；其余有错误且条数非零的快照显示“部分采集，尚未完成”，有错误且条数为零时显示“抓取失败”。`health.py:71–79` 的条数与错误均取自同一次 outcome，未沿用上次成功条数；HF 的 not_ready 标记由 `fetch_arxiv.py:154–157` 对请求结果明确判定。因此该处没有把 S2 已返回的部分结果说成完全失败。
2. **历史归属正确。** `digest.py:235–236` 的旧格式回退只查看当前传入刊期的 `status_report`；不从当前全局 `state.json` 或每日状态表推断历史刊期。`initialize_public` 仍从存储 manifest 渲染，`_source_snapshot` 只为新刊期增加 `availability` 字段，既有刊期继续保留自身 `sources`。
3. **没有修改论文或审核事实。** 改动仅涉及来源快照的附加状态与显示标签，没有改标题、摘要、论文日期、HF 推荐日期、科学数字、审核决定或 PR 凭据。历史渲染不会为旧 manifest 回填字段。
4. **没有吞掉异常。** 新函数不增加 try/except 或静默错误回退；来源实际 error 仍保留在 manifest。`source["count"]` 继续遵守现有内部快照契约。
5. **模板接线完整。** `daily.html:42` 使用相同函数生成中英文标签；`_render_day` 与复用该模板的 `_render_recap` 都传入该函数。索引、单期和撤回页的现有分支保持可用。

## 测试与非阻塞覆盖建议

实际运行：

```text
.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/feed/test_daily.py -k 'source_not_ready_partial_and_failed_are_distinct_in_public_brief or status_bulletin_requires_opt_in_and_preserves_observed_snapshot'
4 passed, 37 deselected in 2.16s
```

新用例覆盖新格式与缺少 `availability` 的旧格式，核对中文 Markdown、英文 Markdown、单期 HTML、最新索引中的三种状态与来源顺序；既有用例核对旧简报 manifest 不被后续状态说明覆盖。

**建议补强但不阻塞当前修复：** `tests/feed/test_daily.py:492–496` 的旧格式分支目前仍保留与旧快照一致的全局 `state.json` 和 `daily-status.json`。可在重新渲染前把这两份全局记录改为相反状态，再断言旧 manifest 字节不变、旧来源标签仍取自身 `status_report`。这样能直接捕获未来错误地读取今天全局状态的回归。当前实现通过代码检查已满足该要求，建议并非已确认的生产缺陷。

## 审查边界

- 本次只写本审查报告，没有修改生产代码、论文数据、manifest 或测试文件。
- 仅执行上述 4 个相关离线用例；没有运行全套测试、联网、付费 API、提交、PR 或部署。
- 不将本次显示层审查当作来源重新采集、论文实验复现或线上页面核验。
