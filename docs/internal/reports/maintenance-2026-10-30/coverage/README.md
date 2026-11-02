# 2026-10-30 冻结覆盖账本与续跑清单

本包是审核建议和工作状态，**没有 owner accept，没有发布授权**。全部本轮正式决定为 `defer`。固定积压 1124 条，HF 10 月 30 日榜另有 15 条新增；原有 VibeGame 不重复计数，冻结库存共 1139 条。后续 10 月 31 日新增来源不改变这个分母。

当前模型批次为 `blocked`。HTTP 402 后停止付费重试，模型分类处理 631 条；摘要批次实际成功 57 条、翻译失败 1 条、取消或未完成 376 条。随后本地缓存恢复 7 条，RSIHub 另从已入库条目同步双语文字；后者不是模型摘要成功，也没有新增人工批准。

| 续接任务 | 条数 | 含义 |
| --- | ---: | --- |
| 论文双语摘要 | 369 | 已有分类，但摘要和生成校验未完成 |
| 模型 API 错误 | 11 | 有原摘要，保留错误阶段，可在恢复额度后重试 |
| 补原始摘要 | 9 | 不能以标题猜测范围；其中 1 项官方正文为无摘要的社论 |
| 公告双语摘要 | 1 | Terminal X 已有正文范围复核，尚缺双语文字 |
| 来源版本或文本协调 | 73 | 第三轮来源与 canonical 所存输入不同，不能视为同输入复核通过 |
| 已选中但尚无第三轮来源记录 | 164 | 包括范围外候选和抽样缺口；范围内优先队列 211/211 已有来源记录 |

这些队列有重叠，不能相加作为未完成总数。每个 ID 的来源、状态、阶段建议、错误和待补原因在 `item-status.jsonl`；具体 ID 队列在 `resume-plan.json`。保留 33 条 owner 修正、17 条基线文献库条目。RSIHub 是本轮新增的文献库来源，单列且未改变原 owner 决定。

1124 条均有来源核对记录；684 条有本轮分类与所需摘要阶段记录；407 条有第三阶段记录，其中 334 条的所核输入与当前保存数据匹配。三个阶段均匹配的为 163 条。relevance、classify、gate 合计只算一个模型阶段。历史三阶段 83 条、可复用来源候选 77 条另计，不能追加成这次新审数量。

65 篇公告全部有单独的正文模型流程，其中 19 篇另有另一位 agent 读原始来源的复核。没有给公告伪造论文 `llm.label`。HF 16 篇在独立附录中各有 3 个阶段、2 个报告和 2 位记录审核者；其中第 1、2 阶段出自同一报告，第三轮收到过类别概览，不声称完全盲审。

基线原事实字段变化如实记录：VibeGame 增加链接；3 条 S2 记录补充来源摘要。没有在覆盖脚本内改写这些字段。原日期、版本和摘要差异仍保留待协调。45-case gate 的完整运行与质量结论见 `../harness-gate-eval/`：precision 0.9231，recall 0.8571，召回率未达 0.90；本包不改变这个结论。

## 离线检查与恢复入口

以下命令从仓库根目录执行。`check` 和 `prepare` 不访问网络、不读密钥、不修改 canonical。脚本先校验包哈希，`prepare` 还逐项核对冻结记录是否被后续更新；新增 ID 不会混入续跑队列。

```sh
.venv/bin/python docs/internal/reports/maintenance-2026-10-30/coverage/resume.py check
.venv/bin/python docs/internal/reports/maintenance-2026-10-30/coverage/resume.py prepare --stage summarize --workdir build/resume-2026-10-30-summary
.venv/bin/python docs/internal/reports/maintenance-2026-10-30/coverage/resume.py prepare --stage judge --workdir build/resume-2026-10-30-api
```

额度和本地环境变量恢复后，只有显式 `run` 才调用当前仓库的模型处理代码。它在独立目录续跑并保存断点，默认单并发；若再次出现配置/额度错误，原异常继续上抛。可用 `--env-file` 指向已配置的本地密钥文件，勿将文件提交或在聊天中粘贴密钥。

```sh
.venv/bin/python docs/internal/reports/maintenance-2026-10-30/coverage/resume.py run --stage summarize --workdir build/resume-2026-10-30-summary
.venv/bin/python docs/internal/reports/maintenance-2026-10-30/coverage/resume.py run --stage judge --workdir build/resume-2026-10-30-api
```

本次仅验证离线检查和准备过程，未运行上述付费命令。该入口不自动补原文、不汇入 canonical、不生成审核单、不 accept、不合并、不发布。API 错误重判后若得到正例或边界，还需另行补摘要和比对第三轮建议。73 条来源差异以及范围争议均须按现有来源记录解决，不能通过改旧报告使其“匹配”。

`generator-snapshots/` 保存本次账本生成器的代码原件；它们原在本地 `build/backlog-all-2026-10-30/`，依赖该目录中的证据缓存，不能直接在归档路径运行。`resume.py` 是本包可直接执行的恢复入口。

## 快照和证据路径

`snapshots/items.jsonl` 是 1139 条的冻结 canonical，SHA-256 为 `e9632c353f3285cda18b8f0592e6f7517245778a1dc07e27ebab8ec7a434f820`；`snapshots/baseline-items.jsonl` 是不可变的 1124 条基线。它们仅供重现本报告，不能覆盖后续新数据。

原始账本中的路径和哈希保留生成时含义。`report-map.json` 把主要原报告路径映射到本包或相邻的持久文件；没有改写原证据哈希。论文全文、HTML 和模型缓存仍在本地 `build/`、`data/feed/cache/`，没有为本包复制全文。`verification.json` 记录本次对保存源文件、引句和数量的校验；它不是论文性能复现或 owner 审核。

`package-manifest.json` 给出本包文件哈希。冻结报告和继续运行的输出必须分开保留，不能覆盖历史结果。
