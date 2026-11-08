# HF 14 天逐日回放

回放日期：2026-10-14–2026-10-27。输入为已保存的真实 HF 每日榜单；调用生产代码 `fetch_hf.parse_json` 与 `window.publication_dates`，不请求网络、不写出版物。

**这是时间窗与现有人工决定的回放，不是 277 篇自动分类重新评测。** 仅采用 owner 复审明确保留的 8 篇及明确补回的 8 篇；其他候选没有因此得到接受决定。假设当时每日都完成了这些人工决定，下表列出各篇首次进入普通日报的日期。实际这批数据来自 14 天回填，只能作为待审创刊回顾，未生成 14 份假日报。

HF 宽口径预筛后共 277 篇唯一候选；其中 33 篇有本次 owner 决定（16 保留/补回、1 顺延、10 移出、6 拒绝），其余 244 篇没有新的人工接受决定。45 例自动闸门评测另见 [gate-report](../../../feed/eval/gate-report.md)，不能把这里的人工决定当成自动闸门的 precision/recall。

| HF 榜单日期 | 原榜条数 | 预筛候选 | 可归入的已审篇数 | 论文（原始发表日） |
| --- | ---: | ---: | ---: | --- |
| 2026-10-14 | 50 | 32 | 2 | [ViewCraft](https://arxiv.org/abs/2610.15915)（2026-10-11）；[Harness²](https://arxiv.org/abs/2610.14224)（2026-10-09） |
| 2026-10-15 | 50 | 26 | 0 | — |
| 2026-10-16 | 50 | 30 | 1 | [Self-Evolving Agent Harness (theory)](https://arxiv.org/abs/2610.18813)（2026-10-13） |
| 2026-10-17 | 0 | 0 | 0 | — |
| 2026-10-18 | 0 | 0 | 0 | — |
| 2026-10-19 | 50 | 29 | 2 | [HexaShell](https://arxiv.org/abs/2610.23479)（2026-10-16）；[TokenEconomizer](https://arxiv.org/abs/2610.22732)（2026-10-15） |
| 2026-10-20 | 50 | 28 | 2 | [HarnessPro](https://arxiv.org/abs/2610.26770)（2026-10-19）；[Self-HPO](https://arxiv.org/abs/2610.22791)（2026-10-16） |
| 2026-10-21 | 50 | 29 | 5 | [Evolving Agent Interfaces (Agent S4)](https://arxiv.org/abs/2610.28601)（2026-10-20）；[HarnessAdapt-RL](https://arxiv.org/abs/2610.28069)（2026-10-20）；[RiseHarness](https://arxiv.org/abs/2610.27435)（2026-10-20）；[TEAL](https://arxiv.org/abs/2610.27327)（2026-10-19）；[CoEvo-RSI](https://arxiv.org/abs/2610.25078)（2026-10-18） |
| 2026-10-22 | 50 | 31 | 3 | [SERA](https://arxiv.org/abs/2610.29560)（2026-10-21）；[GRSE](https://arxiv.org/abs/2610.27227)（2026-10-19）；[Socratic Skill Learning](https://arxiv.org/abs/2610.17860)（2026-10-13） |
| 2026-10-23 | 49 | 25 | 0 | — |
| 2026-10-24 | 0 | 0 | 0 | — |
| 2026-10-25 | 0 | 0 | 0 | — |
| 2026-10-26 | 45 | 18 | 0 | — |
| 2026-10-27 | 45 | 29 | 1 | [Skill^∞](https://arxiv.org/abs/2610.35434)（2026-10-26） |

合计 16 篇：15 篇 Harness 方法、1 篇 Harness 专项理论。重复推荐只计一次，`first_seen` 不参与日期判定；原始发表日即使更早也保留显示。每次均用前一非空刊期为下界，无前期时用 D−2。

CarryOn (robot) 保持 defer；EAU、DuoDiscover、SwarmRSI、DiscoveryRSI、Épi、TokenWorth 及 4 篇通用评测/综述移出 Harness 回顾；MemPilot 等 6 篇拒绝。原 10 月 27 日日报继续撤回。回顾一旦合并，后续日报通过已发布 ID 去重，不再重复上述 16 篇。

原始榜单 SHA-256：`93cfa7520a6497b30997549c2954b33b719cb3c49ceb63d6070cb244f97d0e13`。
owner 复审文件 SHA-256：`e5ccb837b14f7241b7a2327ef92784caa65eeb01b09a15e5d41ebd38e6a4b22f`。
