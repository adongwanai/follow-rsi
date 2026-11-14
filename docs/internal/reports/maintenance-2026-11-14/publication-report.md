# 2026-11-14 正式应用与出版前回执

本文件记录实际合并的前置审核与本地产物验证，随出版物 PR 提交。此刻尚未完成该出版 PR 的合并、Pages 与 HTTP 验收，不能将本地生成视为已上线。最终部署回执放在 [issue #60](https://github.com/adongwanai/follow-rsi/issues/60) 的 11/14 维护留言中。

## 实际合并与审核应用

| PR | 内容 | 精确审核 head | 真实 merge commit |
| --- | --- | --- | --- |
| [#105](https://github.com/adongwanai/follow-rsi/pull/105) | 来源与三轮证据 | `97c7bead773adc54ad933dbf031a6b6837e84695` | `e512b8f083feadc30514c9f0188eb4a4bcce0541` |
| [#106](https://github.com/adongwanai/follow-rsi/pull/106) | 2026-11-13 日期审核 | `51fc370d8ce43b42ceeef01d4f4f650484ee8942` | `b35666f104d1ba18d6148fd58c0a2bd52afa371b` |
| [#107](https://github.com/adongwanai/follow-rsi/pull/107) | 2026-11-14 日期审核 | `240f4f7c416b6d09d7e33b695472991e5b81d01a` | `37313099fb94078f123ab6ad60c261a00158858c` |

两份日期审核已核真实同仓合并、owner 账户、精确 head 的 build/validate/owner status 及完整合并 YAML 字节，11/14 metadata-only 附件另行核验。原 PR52 的合并内容也已读取核对。持续授权下的 owner 账户合并不是本人逐篇阅读的声明。

仅应用 46 条获批变更：11/13 的 33 条、11/14 的 13 条，总计 **40 reject、1 accept、3 backlog、2 defer**。完整审核文件包含 79 行，但没有重放未变的旧行覆盖后续意见。另有已刊 2611.08318 的 metadata-only 更新，不进入每日 apply 集合；保留原 PR52 的 accept、旧审核日和 review_history，仅增加真实 HF 推荐日绑定。独立应用核验确认全部 47 行变更可解释，2074 条 ID 顺序、first_seen 与原科学版本未被改写。见 [正式应用](publication-generation.json)、[合并前置凭据](publication-prerequisites.json)、[独立应用核验](backlog-audit/post-review-application-verification.json)。

`feed/eval/labeled.yaml` 的变化是正式审核自动回写的标签，不是重跑模型。旧告警仍为 11/05 incomplete、recall 0.892857 < 0.90，没有降低阈值或声称新评测通过。

## 本期、补刊与原刊保护

11/14 是采集与审核简报，**当日新增论文 0**。北京时间10:46开始尝试全部12路来源，HF当日HTTP200空列表；11/13完整34篇、11/12复抓21篇，新增41个稳定ID的三轮范围意见为1纳入、39排除、1待补。Semipy正文403，身份与日期已核，版本与范围仍未知。限流和未触达覆盖保留，不将空榜等同所有来源无更新。

11/13 旧简报原件已归档，补刊仅含 **JustRUA**，实际 reviewed_on 为11/14，保留原 published_at 和 sources 快照；论文发表/版本为11/11、HF推荐日11/13、first_seen为11/14。纳入依据是其执行反馈修改共享操作与指南并跨任务组复用的专项评测。摘要明确自改进没有明显超过默认且成本更高；29.7→50.3属于最终静态方案，不能写成自改进收益。五组轮转、接触被评任务、每配置只评一次等限制保留。

TeleTune、EmbodiedEvo、ECG-RSI 只列正式历史 backlog，不放入今日新增论文；前两者为Harness组件，后者为权重与Harness共演化。Harness Repair仍defer，已恢复官方v1源和无数字摘要，未借用后来版本数据出版。RSIHub、HarnessDev、Aspire、S³Gym的分类与既有阅读路线保持。

metadata-only 应用当时六个保护文件字节未变；随后正常出版使旧HTML的共享导航增加11/14入口，并把11/13入口改为1篇补刊。因此**最终整份HTML不再与旧文件相同**。18个旧HTML均可由原文件执行恰好两段固定导航替换得到，publication-main至末尾逐字相同；其他五个11/05保护文件字节完全不变。原 [11/05 HTML](prior-editions/site/daily/2026-11-05.html) 已按批准SHA归档。见 [精确导航变化回执](navigation-update-receipt.json)。首次过宽的整文件检查失败另存 [first-attempt](backlog-audit/post-review-application-first-attempt.json)，后续核验没有把这一差异掩盖为“六文件均未变化”。共享导航更新由本次出版PR明确记录，不是metadata-only改写论文内容。

旧11/05审核YAML仍是不可变历史快照；新增HF日使它不能直接在当前canonical重放，W45通用promotion同样受限。这一旧回放限制未宣称修复。除11/13归档后补刊外，原日刊manifest、周刊、卡片及README手写区保持。

## 全量对账与可续跑状态

稳定ID并集 **8898**，canonical **2074 = 986正式/目录 + 1023可复用范围意见 + 55待补证 + 10外部阻塞**。原始合格成员漏入、HF漏推荐日、无状态canonical及输入漂移均为0。待证比post-intake多1是Harness Repair当前v1源纠正后的完整出版审核缺口，不是新增外部故障；Semipy是第10个正文外阻。9个旧外阻实际重试18次均未恢复，#19、#20、#23、#30仍保留逐项原因。

本轮39对版本建立比较：24对复用未变范围意见，5对完成实质独立回读，10对仍待实质回读；再加337项未取得已核成对正文，跨表仍有 **347项版本正文比较待办**。29项完成不等于39对全部重审，更不等于采用新版；本轮正式升版为0。缺成对正文的337项尚未抓取，不伪装成外部服务故障。

简报保留早期冻结时点的27完成/349待办快照。此后GraphMemory与RoboHarness完成独立增量，最新有效状态为29/347；旧稿没有覆盖，见 [增量回执](backlog-audit/supplemental-version-review/receipt.json) 和 [最终台账](backlog-audit/post-review/summary.md)。各计数属于不同维度，不能将55待证、10外阻和347版本任务直接相加。完整逐项队列和冻结输入随原始归档保存。

## 验证与费用

最终原始归档共 **792个文件、223364651字节**，SHA逐项复核通过；[归档后保护校验](preservation-post-archive.json) 再次确认构建幂等及私密值扫描通过。该新增回执没有覆盖独立终审引用的冻结post-review回执。

两份日期审核post-apply校验、114篇/9条路线校验通过；完整pytest **430 passed**。构建幂等、canonical变化白名单、来源SHA、旧刊正文与周刊/卡片保护、私密值扫描均已执行。见 [测试回执](validation-post-review.json) 与 [保护校验](preservation-post-review.json)。[独立渲染终审](independent/rendered-publication-review.json) 通过，绑定83个输入文件、0阻断；范围是本地产物及保存的真实凭据，不替代远端CI、线上验收或实验复现。原始终审SHA为 `bc777c1f0b62908840229fda50e47260033a01f96e117d81a3ea0344c02aa2f1`；文档阅读副本仅重映射归档路径，原字节在raw归档保留。

DeepSeek生成请求 **0**、生成token **0**，usage日志仍0行。02:45:22至03:37:29 UTC观察到账户余额下降 **0.04元**；该差额不是本任务发票，不能归因于本任务生成调用，Codex用量也不在该API日志内。余额原值与密钥仅留本地。见 [脱敏结束费用回执](usage-boundary-end.json)。三个feed工作流保持手动禁用；所有变更通过PR，不直接推main。
