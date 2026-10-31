# 2026-10-30 审核覆盖清单

固定基线 1124 条；当前库存 1139 条。HF 今日榜 16 篇，其中 1 篇原已在库、15 篇为基线之外的新附录。新附录不会回填到 1124 的分母。

本清单是审核工作记账。所有本轮正式决定均为 defer；来源核验、模型处理和多阶段复核均不等于 owner accept，也不构成发布授权。

Canonical SHA-256：`e9632c353f3285cda18b8f0592e6f7517245778a1dc07e27ebab8ec7a434f820`。模型批次状态：`blocked`。

| 基线覆盖状态 | 条数 |
| --- | ---: |
| current_three_round_advice | 163 |
| model_advice_only | 787 |
| protected_owner_correction | 33 |
| new_curated_catalog_source | 1 |
| protected_curated_catalog | 17 |
| official_body_model_advice | 47 |
| source_blocked | 9 |
| prior_three_round_reuse_candidate | 56 |
| model_error_pending | 11 |

| 本轮阶段 | 有记录 | 所核字段与当前输入匹配 |
| --- | ---: | ---: |
| 1. 来源身份、原日期、版本与摘要差异核对 | 1124 | 1124 |
| 2. 分类与必需双语摘要；文章使用独立正文流程 | 684 | 684 |
| 3. 另一个 agent 的来源范围复核及记录的裁定 | 407 | 334 |

三阶段且所核输入匹配：163 条；其中具有至少 3 个不同报告文件的为 163 条。文件数量不代表独立审核者数量；逐项保留 phase、reviewer、原始输入和正文哈希。第一轮仅核对来源和元数据，不认证论文全部事实。

保留 33 条 owner 修正与 17 条文献库条目。历史三轮记录 83 条；当前输入相同的历史复用候选 77 条，均与本轮覆盖分开。

另有 1 条本轮新增的文献库同步来源；逐字核对文献库双语文本，单列 provenance，不计为新的 LLM 摘要成功，也不改动历史 owner 决定。

65 篇官方文章：65 篇有单独的正文模型审查，19 篇另有来源复核。没有给这些文章伪造 paper 类型的 llm.label。

需要双语摘要 537 条，当前仍不完整 370 条，guard_failed 0 条。生成质量与范围建议分别计数。

其中模型摘要续跑单为 369 篇论文，另有 Terminal X 这 1 篇公告缺少双语摘要；后者已有正文范围复核，不能笼统记作未审。

| 尚存问题 | 条数 |
| --- | ---: |
| missing_original_abstract | 9 |
| publisher_abstract_access_blocked | 8 |
| new_advice_input_or_body_hash_mismatch | 73 |
| model_advice_uses_superseded_prompt | 25 |
| missing_summary_zh | 370 |
| missing_summary_en | 370 |
| missing_summarize_provenance | 370 |
| missing_translate_provenance | 370 |
| summary_number_guard_not_confirmed | 370 |
| model_processing_error_not_a_scope_decision | 20 |
| prior_advice_needs_current_rule_reconciliation | 60 |
| prior_three_round_source_equivalence_not_established | 6 |

元数据差异只报告、不由覆盖脚本改动：

| 差异或限制 | 条数 |
| --- | ---: |
| saved_abstract_differs_from_official_latest_string | 125 |
| saved_version_differs_from_official_latest | 137 |
| saved_publication_day_differs_from_official | 14 |
| editorial_has_official_body_but_no_abstract | 1 |

HF 今日榜附录（按论文原日期正序；上榜日期单列）：

| 论文 | HF 上榜日 | 原始发表日 | 来源范围建议 | 本轮匹配阶段 |
| --- | --- | --- | --- | --- |
| CoSTA: Compressed Speech Token Adaptation for Efficient Spoken Dialogue Models | 2026-10-30 | 2026-10-15 | exclude | 1,2,3 |
| Your Benchmark Is an Empirical Measure Over Difficulty | 2026-10-30 | 2026-10-21 | exclude | 1,2,3 |
| VibeGame: Prompt-to-Game Development with AI-Native Engine and Self-Evolving Adversarial Agent Team | 2026-10-30 | 2026-10-22 | harness | 1,2,3 |
| A Broader Look into MLLM's Retrieval Heads | 2026-10-30 | 2026-10-23 | exclude | 1,2,3 |
| After One-Click Video: The Inflow of Service-Type Content, the Failure of the Recommendation Pool Mechanism, and the BoLe System | 2026-10-30 | 2026-10-24 | exclude | 1,2,3 |
| Co-Design Bench: Multimodal Collaborative Coding Evaluation for Agentic Models | 2026-10-30 | 2026-10-26 | exclude | 1,2,3 |
| SO-101 Bench: Accessible Spatial Manipulation | 2026-10-30 | 2026-10-27 | exclude | 1,2,3 |
| WorkFactory: Turning Professional Intents into Executable Work for Scalable Agent Training | 2026-10-30 | 2026-10-27 | other_direction | 1,2,3 |
| WebAnything: From the Wild Web to Scalable Agent Environments | 2026-10-30 | 2026-10-27 | other_direction | 1,2,3 |
| WeVisCut: The Whole Editing Room in One Agent From Narration to Long-Form Video | 2026-10-30 | 2026-10-28 | exclude | 1,2,3 |
| IntReal: A Real-World Dataset and Benchmark for Multimodal Interleaved Generation | 2026-10-30 | 2026-10-28 | exclude | 1,2,3 |
| AskStream: When and What to Ask Proactively under Uncertainty in Streaming Video Understanding | 2026-10-30 | 2026-10-28 | exclude | 1,2,3 |
| Intrinsic Distribution Matching | 2026-10-30 | 2026-10-29 | exclude | 1,2,3 |
| EditAgent: Rethinking Agentic Image Editing | 2026-10-30 | 2026-10-29 | exclude | 1,2,3 |
| Your LR Schedule May Not Be Principled: Effective Learning Rate Scheduling in Weight-Normalized Training | 2026-10-30 | 2026-10-29 | exclude | 1,2,3 |
| HairDeck: Animation-Ready Stylized Hair Cards from a Single Image | 2026-10-30 | 2026-10-29 | exclude | 1,2,3 |

今日 HF 每篇的 primary 第 1、2 阶段共用一份报告，第三阶段来自另一位 agent：真实计为 3 阶段、2 个报告、2 位记录的审核者。第三阶段曾收到主动披露的分类概览，不声称完全盲审。

固定 45-case gate 的独立结果见旁边的 harness-gate-eval 报告：运行完整但召回门槛未通过。多轮记录、源码测试或摘要生成完成均不会覆盖这个质量失败。

完整逐项证据、原 owner 状态、模型错误和摘要缺口保存在 coverage-ledger.json；数据仅供 owner 审核。
