"""Persist this reviewer's source-bound suggestions; no formal owner decisions."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
from bs4 import BeautifulSoup

ROOT = Path.cwd()
OUT = ROOT / "docs/internal/reports/maintenance-2026-11-18/independent-hf17"
INITIAL = OUT / "initial-scope.json"
INDEX = OUT / "source-index.json"
HF = ROOT / "build/maintenance-2026-11-18/source-intake/source-results/hf-daily.json"
META = ROOT / "build/maintenance-2026-11-18/source-intake/official-metadata/records.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def rel(path):
    return path.relative_to(ROOT).as_posix()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


initial = json.loads(INITIAL.read_text())
assert sha(HF) == initial["hf_input_sha256"]
assert sha(META) == initial["metadata_input_sha256"]
sources = {x["id"]: x for x in json.loads(INDEX.read_text())["records"]}
hf_records = {x["id"]: x for x in json.loads(HF.read_text())["records"]
              if "2026-11-17" in x.get("hf_daily_dates", [])}
assert len(hf_records) == 41

# Each exact substring was selected after reading the complete available abstract.
abstract_quotes = {
    "2611.21072": "We introduce Sage S1.5 Flash, a 320-billion-parameter general-purpose mixture-of-experts model designed to reason over scientific evidence and act in interactive environments.",
    "2611.21003": "We also introduce Uno, lossless diffusion adapters that speed up decoding by up to 2.2x without a separate draft model.",
    "2611.19937": "strategy-supervised imitation shapes a structured distribution of candidate portfolios, followed by group-relative reinforcement learning (RL) that refines joint decisions using portfolio-level financial rewards and a frozen policy reference.",
    "2611.21218": "We evaluated frontier large language models on the Atlas and aggregated their results into the InclusionMed Index",
    "2611.07222": "A deterministic sanitizer removes instruction-like regions its fixed rules match before the model reads them and retains the removed spans as evidence",
    "2611.20218": "Starting from a brief handoff, agents must recover requirements distributed across colleagues and workplace records, reconcile conflicting evidence, and implement changes evaluated by private executable tests.",
    "2611.21607": "We introduce ScaleVLA, which connects a 552B DeepSeek-V4.1-Flash backbone to a trainable action DiT",
    "2611.17834": "we train an AI reviewer model, PaperCritic, through reinforcement learning with the F1 score of precision and recall as the reward.",
    "2611.20254": "We also distill the guided flow head into two- and four-step students, requiring 2 or 4 head evaluations per coarse frame.",
    "2611.20882": "Each task provides a working program and specifies the workload, correctness requirements, timing boundaries, and permitted edits, leaving agents to choose where and how to optimize.",
    "2611.17110": "The resulting shared latent action space provides a unified supervision signal for training an embodied foundation model on both human and robot videos.",
    "2611.20986": "Qwen3.5-9B reads a sequence enriched with ESM2 residue features.",
    "2611.21339": "cumulative long tuning with distribution matching distillation (CuLT-DMD) holds parameters fixed throughout each long self-rollout and averages local gradients before updating.",
    "2611.20404": "Latent feedback, which feeds each token's top-layer state into the next token's input, is another way to spend that compute",
    "2611.08977": "Energy-Based Reasoners (EBRs), which learn an energy function over latent reasoning states and formulate looped updates as gradient descent on this energy.",
    "2611.18919": "situations an RL policy keeps failing are mined automatically, sent to a virtual-reality application where a person picks the object up with their own hands, and returned to training as two grasp points.",
    "2611.19537": "coding agents can optimize a reusable goal compiler",
    "2611.20385": "We built DominoBench, a benchmark of still images of 2D rigid-body scenes whose outcome a physics simulator computes.",
    "2611.13685": "we propose Shared Prediction on Action and Representation (SPAR), an MoT architecture in which future visual state prediction can provide independent and complementary learning signals alongside action prediction.",
    "2611.18330": "non-lexical questions use a question-conditioned head and a separate layer-18 turn-end readout.",
    "2611.17933": "We introduce OutfitterBench, where agents manage an outdoor-equipment rental business for 200 days",
    "2611.19649": "We introduce LoopFill, a training-free speculative decoding algorithm for looped LLM that combines multi-token suffix drafts with shallow-loop predictions in a single draft tree.",
    "2611.17610": "We synthesize nine primary empirical evaluations comprising 516 unique multi-agent configurations organized along a resource vector R with six dimensions and a baseline ladder with four categories.",
    "2611.09825": "We present BitDecoding-FP4, an algorithm--system co-design for accurate and efficient native FP4 KV decoding.",
    "2611.19771": "a JEPA world model that observes single-depth-camera point clouds, predicts and plans in their latent space, and acts through a policy head on its frozen latents",
    "2611.16642": "we propose a new distillation method that learns a set of samples such that they directly approximate the per-class data distribution.",
    "2611.04395": "We fine-tune 7-9B open-weight models from three families on multiple-choice questions",
    "2611.21479": "we learn a causal flow map for few-step generation and introduce region-aware score distillation that combines complementary video and image priors",
    "2611.20148": "Centered Ablation (CA) projects the common mode out of the direction, in closed form.",
    "2611.18668": "UMM-JEPA, which reformulates generation as progressive prediction of continuous visual-understanding representations.",
    "2611.20192": "We optimize GlyphAtlas with a mask-weighted flow matching objective and a timestep-weighted text perceptual loss",
    "2611.21605": "We train two Visual Reasoning Agents, ViRA-9B and ViRA-27B, with CrossRPO",
    "2605.09614": "a GRPO-based policy optimization method that selects high-entropy reflection anchors and optimizes a chain-masked finite-window KL surrogate for downstream visual dependence.",
    "2611.11657": "We built a hybrid multi-agent trading system that combines large language model (LLM) analysts with momentum-based portfolio construction and rule-based execution.",
    "2611.21412": "Available axial, coronal and sagittal stacks are independently encoded into multi-scale Gaussian posteriors and fused using a field-of-view-aware Product-of-Gaussians formulation",
    "2611.18981": "GPBam scores retrieval and long-form generation jointly, which makes it a benchmark for legal retrieval as well as for legal writing",
    "2611.06238": "three decision models (4B, 9B and 27B) that train a low-rank adapter and a pointer head on frozen open-weight bases",
    "2611.21439": "Our RL agent employs a lightweight actor-critic architecture with approximately 40K trainable parameters in total.",
}

# Full paragraphs preserve context. MathML and whitespace remain visible; substring
# checks normalize whitespace only, never substitute numbers or source wording.
paragraphs = {
    "2611.07222": ["S3.SS1.p2.1", "S6.p2.1"],
    "2611.20218": ["S3.SS4", "S5.SS2"],
    "2611.20882": ["S2.SS1", "S7"],
    "2611.14960": ["S3.SS1", "S3.SS5", "S6"],
    "2611.19537": ["S1.p1.1", "S2.SS5", "S3.SS3.SSS0.Px2", "S3.SS3.SSS0.Px4", "S3.SS3.SSS0.Px5", "S3.SS4.SSS0.Px1", "S4", "A5.SS0.SSS0.Px8"],
    "2611.17610": ["S3.SS5", "S6.SS4", "S7"],
    "2611.20595": ["S3.SS0.SSS0.Px2.p1.2", "S3.SS0.SSS0.Px4.p1.1", "A2.SS0.SSS0.Px3.p1.1", "A6.p2.1"],
    "2605.09614": ["S4.SS2", "A3.SS1"],
    "2611.11657": ["S3.SS2", "S3.SS3", "S3.SS4", "S4.SS3", "S6.SS2"],
    "2611.16694": ["S4.SS3", "S7.SS2", "S9"],
    "2611.21072": ["S3.SS1.p1.1", "S3.SS2.p1.1", "S6.p1.1"],
}

reasons = {
    "2611.07222": "官方 v2 方法使用每基准固定 lexicon、固定委托/清洗规则；反馈更新目标准入状态并裁定本次调用，不修订防御工件。外部 RL 攻击者不构成防御器与 Harness 共演化。保留 HF .007 与官方 v2 .005 的数字差异。",
    "2611.20218": "评测组织内需求获取、代码交付与验证；变化对象是所交付的外部应用 patch。实验比较固定 Codex/Claude Code scaffold 与 oracle requirements，未专项评估可复用 Harness 的反馈演化。",
    "2611.20882": "任务明确允许编辑外部应用源码、编译选项与依赖；公开测试驱动应用候选迭代，研究的版本谱系仍是应用产物。模型+harness 分数混杂本身不是 Harness 演化专项研究。",
    "2611.14960": "使用 OpenHands 与 mini-SWE-agent，按步保存任务仓库 patch，完成后离线测何时首次正确；原文明确该回溯结果不反馈给 agent。研究任务内停止行为，没有更新并跨任务继承停止器或其它 Harness 工件。",
    "2611.19537": "确有反馈驱动源码搜索、候选选择和跨任务复用，不能将这些条件写成 no。但第一阶段改外部 Craftax 策略，第二阶段改生成该策略的 Python emitter；方法将目标编译器定位为 programmatic goal-conditioned policy。搜索提示明确冻结 coding harness、机器、基策略、监视器与 guard。当前原文未把 emitter 接入模型周围的任务执行/改进 Harness，按 external_artifact / ai4ai 排除本专题。此结论不以具身环境、冻结改进器或无推理期 LLM 本身为理由。",
    "2611.17610": "研究多 Agent 协调相对采样与推理预算的归因，PACE 记录资源并检查预算可比性。未见针对反馈修改并保留 Harness 工件的实验对象；不能将一般通信图、架构对比或自动 MAS 作为 Harness 演化专项证据。",
    "2611.20595": "SilentGuard 的运行过程按固定检查、重试和 alpha 阈值释放/屏蔽/告警。正文确实从其它任务 clean traces 挖掘可复用 contracts，故不能说全是手写或没有跨任务使用；但未报告基于失败/评估反馈修订、选择并保留 contract/enforcement 新版本的系统循环。App.F 的三版本为作者方法开发史，不等于系统自己演化 Harness；按固定防护方法排除，若未来出现 contract 修改谱系可重开。",
    "2605.09614": "反思 anchor 是 GRPO 参数梯度的选择位置，finite-window KL 为权重优化目标。原文明确训练 native decoder，anchor mask 与反事实参照不是跨任务修改的外部指令/技能/代码工件。",
    "2611.11657": "多 Agent 交易器使用显式固定 allocator/执行规则。历史上确有实现版本变化和离线 contracts/调用门控比较，应保留；但作者重建的工程变更不等于系统据执行反馈自动修改自身，组合仓位变化是任务状态。正文说明 post-change production outcomes 未测试，不作为演化收益证据。",
    "2611.16694": "主协议针对同一个 question-evidence pair 做两次推理，变化对象为当前答案；固定 prompt gate 与声望/分歧条件是审计控制，未形成跨任务继承的 Harness 修改。",
    "2611.21072": "官方 v1 正文训练科学模态 projector 与 Agent 模型，ToolSpace 是训练环境/数据合成，未给出独立反馈演化的推理 Harness。HTML 全文与摘要称 S2.1，HF 及 Atom 摘要却称 S1.5；按范围排除，同时保留身份/元数据待核记录，不静默覆盖任何一方。",
}

reviewed_sections = {
    "2611.07222": ["abstract", "S3.SS1", "S6", "reproducibility and limitations excerpts"],
    "2611.20218": ["S3.SS4", "S4.SS2", "S5.SS2", "S7"],
    "2611.20882": ["S2.SS1", "S5.SS1", "S5.SS2", "S7", "S8"],
    "2611.14960": ["S2.SS4", "S3.SS1", "S3.SS5", "S3.SS6", "S6", "A1.SS3"],
    "2611.19537": ["S1", "S2.SS2", "S2.SS3", "S2.SS4", "S2.SS5", "S3.SS3", "S3.SS4", "S4", "A2.SS1", "A2.SS2.SSS0.Px4", "A3.SS1", "A5.SS0.SSS0.Px8"],
    "2611.17610": ["S3.SS5", "S4", "S5.SS1", "S6.SS4", "S7"],
    "2611.20595": ["S1", "S3", "S5.SS3.SSS0.Px2", "A2", "A6", "A8.SS0.SSS0.Px2", "A11.SS0.SSS0.Px9", "all paragraphs matching contract/miner/update/feedback"],
    "2605.09614": ["S3", "S4.SS2", "A3.SS1"],
    "2611.11657": ["S3.SS2", "S3.SS3", "S3.SS4", "S4.SS3", "S6.SS2", "S7"],
    "2611.16694": ["S4.SS3", "S5", "S7.SS2", "S9"],
    "2611.21072": ["abstract", "S2.SS1", "S3.SS1.p1.1", "S3.SS1.SSS1 (ToolSpace)", "S3.SS2.p1.1", "S6.p1.1", "title and model-name occurrences"],
}

records = []
checks = []
for original in initial["records"]:
    item = dict(original)
    sid = item["id"]
    aid = sid.split(":", 1)[1]
    meta = item["official_metadata"]
    hf = hf_records[sid]
    abstract = meta["abstract"]
    quote = abstract_quotes.get(aid)
    if quote is None:
        # The three remaining fulltext-reviewed papers use their full abstract,
        # avoiding any guessed sentence delimiters or source rewording.
        quote = abstract
    assert quote in abstract, (sid, quote)
    checks.append({"id": sid, "kind": "abstract_quote", "passed": True})
    item.update({
        "suggestion": "reject", "scope_opinion": "exclude_harness_publication_scope",
        "formal_owner_decision": None, "publication_approval": False,
        "reviewed_on": "2026-11-18", "recommended_on": "2026-11-17",
        "published_original": meta["published"], "version_updated": meta["updated"],
        "first_seen_observed": hf["first_seen"], "first_seen_mutated": False,
        "reason_zh": reasons.get(aid, item["reason_zh"]),
        "fulltext_review_pending": False,
        "review_basis": "official_abstract_complete_read",
        "source_quote": {"text": quote, "source_kind": "official_arxiv_metadata_abstract",
                         "metadata_file": rel(META), "metadata_file_sha256": sha(META),
                         "abstract_sha256": hashlib.sha256(abstract.encode()).hexdigest()},
        "source_body_quotes": [], "source_conflicts": [],
        "evidence_quick": {k: {"value": "unknown", "quote": None}
                           for k in ["held_out", "matched_budget", "cross_model", "code_released"]},
        "evidence_quick_boundary": "本次为范围复核；未声称实验复现或四项证据完整审计。unknown 不等于 no。",
        "publication_summary_zh": None, "publication_summary_en": None,
        "resume_condition": "若新版本或原文补充显示可复用 Harness 工件的反馈修改与保留，再按新哈希复核。",
    })
    if aid == "2611.19537":
        item["suggested_primary"] = "ai4ai"
        item["harness_sub"] = None
        item["object_analysis"] = {
            "improved_object": "external_artifact",
            "specific_objects": ["Craftax C program policy", "Python emitter mapping structured goals to rule policies"],
            "feedback_driven": "yes", "persists_across_tasks": "yes",
            "harness_specific": "no",
            "positive_counterevidence_retained": "源码候选、训练反馈、验证选择、保留源代码和未见长任务迁移均真实报告；本范围排除只针对修改对象。",
            "boundary_not_used_as_exclusion": ["embodied setting", "fixed external optimizer", "no runtime LLM call alone"],
        }
        item["evidence_quick"]["held_out"] = {"value": "yes", "quote": "transfer zero-shot to longer tasks"}
        item["evidence_quick"]["code_released"] = {"value": "yes", "quote": "https://github.com/vicgalle/craftax-program-policies"}
    if aid == "2611.20595":
        item["object_analysis"] = {
            "improved_object": "fixed_in_loop_checks_and_contract_mining",
            "cross_task_contract_application": "yes",
            "feedback_revised_retained_contract_versions": "unclear",
            "harness_evolution_study": "not_established",
            "positive_counterevidence_retained": "5-fold clean-response contract mining跨任务应用，作者三版方法开发史均保留；不是以缺乏在线反馈或发表前冻结作为排除理由。",
        }
    if sid in sources:
        src = sources[sid]
        body_path, text_path = ROOT / src["body_path"], ROOT / src["text_path"]
        assert sha(body_path) == src["body_sha256"]
        assert sha(text_path) == src["text_sha256"]
        soup = BeautifulSoup(body_path.read_bytes(), "html.parser")
        watermark = soup.find(id="watermark-tr").get_text(" ", strip=True)
        assert f"{aid}v{meta['version']}" in watermark, (sid, watermark)
        title = soup.title.get_text(" ", strip=True)
        title_match = "".join(title.split()) == "".join(meta["title"].split())
        assert title_match, (sid, title, meta["title"])
        body_text = norm(text_path.read_text())
        item["review_basis"] = "official_explicit_version_fulltext_targeted_sections_plus_abstract"
        item["body_source"] = {k: src[k] for k in ["body_path", "body_sha256", "text_path", "text_sha256", "requests"]}
        item["body_source"].update({"watermark": watermark, "html_title": title, "title_matches_metadata_ignoring_whitespace": title_match})
        item["read_scope"] = reviewed_sections[aid]
        for locator in paragraphs[aid]:
            node = soup.find(id=locator)
            assert node is not None, (sid, locator)
            excerpt = node.get_text(" ", strip=True)
            assert norm(excerpt) in body_text, (sid, locator)
            item["source_body_quotes"].append({"locator": locator, "quote": excerpt,
                "source_url": src["requests"][0]["url"] + "#" + locator,
                "body_sha256": src["body_sha256"], "text_sha256": src["text_sha256"],
                "verified_after_whitespace_normalization": True})
            checks.append({"id": sid, "kind": "body_quote", "locator": locator, "passed": True})
        checks.append({"id": sid, "kind": "body_hash_text_hash_version_watermark_title", "passed": True})
        if aid == "2611.21072":
            html_abstract = soup.select_one(".ltx_abstract").get_text(" ", strip=True)
            assert "S1.5" in hf["abstract"] and "S1.5" in abstract
            assert "S2.1" in html_abstract and "S1.5" not in body_text
            item["source_conflicts"].append({"kind": "model_identity_metadata_body_mismatch",
                "hf_abstract_model": "Sage S1.5 Flash", "official_atom_abstract_model": "Sage S1.5 Flash",
                "official_atom_title": meta["title"], "official_html_model": "Sage S2.1 Flash",
                "html_abstract": html_abstract, "source_values_changed": False,
                "resolution": "unresolved_provider_metadata_body_conflict",
                "next_step": "取得同版本元数据修正或作者说明后解除身份告警；范围排除意见保留。"})
        if aid == "2611.07222":
            assert ".007" in hf["abstract"] and ".005" in abstract
            html_abstract = soup.select_one(".ltx_abstract").get_text(" ", strip=True)
            assert ".005" in html_abstract
            item["source_conflicts"].append({"kind": "hf_official_current_version_numeric_mismatch",
                "field": "mean in-scope attack success under released RL attacker",
                "hf_abstract_value": ".007", "official_atom_v2_value": ".005", "official_html_v2_value": ".005",
                "hf_original_abstract": hf["abstract"], "official_html_abstract": html_abstract,
                "resolution": "preserve_each_snapshot_no_unverified_reconciliation", "source_values_changed": False,
                "next_step": "按各版本来源保留数值；不可把 HF .007 改写成原榜 .005 或称已复算。"})
    for entry in item["evidence_quick"].values():
        if entry["value"] == "yes":
            assert entry["quote"] in abstract or entry["quote"] in meta.get("comments", "")
            checks.append({"id": sid, "kind": "evidence_quick_quote", "passed": True})
    records.append(item)

assert set(hf_records) == {x["id"] for x in records}
assert len(records) == len({x["id"] for x in records}) == 41
now = datetime.now(timezone.utc).isoformat()
result = {
    "reviewer": "/root/nov18_hf17_crossreview", "frozen_at": now,
    "initial_frozen_at": initial["frozen_at"],
    "independence": "Independent own judgments and fulltext reading; parent per-paper opinions not read before this final freeze. Parent-provided official metadata only was used as shared source input.",
    "scope": "Complete HF recommendation board 2026-11-17, observed/reviewed 2026-11-18",
    "input_files": [{"path": rel(p), "sha256": sha(p)} for p in [INITIAL, INDEX, HF, META]],
    "definitions_read": ["feed/prompts/harness_gate.md", "feed/taxonomy.yaml", "feed/prompts/evidence.md"],
    "counts": dict(Counter(x["suggestion"] for x in records)),
    "abstracts_read": 41, "targeted_official_fulltexts": 11,
    "accepted": 0, "publishable_positive_summaries": 0,
    "unresolved_source_conflict_ids": [x["id"] for x in records if x["source_conflicts"]],
    "paid_requests": 0, "free_fulltext_requests": 11,
    "review_is": "source-bound scope suggestions, not formal owner acceptance, release authorization or reproduced experimental results",
    "numeric_boundary": "Original numeric fields untouched; source conflicts explicitly retained. No numerical summary proposed for publication. All reported source numbers remain author claims, not independently recomputed measurements.",
    "records": records,
}
final_path = OUT / "final-scope-review.json"
dump(final_path, result)
validation = {"validated_at": now, "final_review_sha256": sha(final_path),
              "checks": checks, "failed": 0, "passed": len(checks),
              "scope": "complete board IDs, 41 abstract excerpts, 11 body/text hashes and explicit-version watermarks/titles, selected body excerpts, conservative evidence quotes"}
dump(OUT / "validation.json", validation)

lines = ["# 2026-11-17 HF 全榜独立范围复核", "",
    "实际复核日：2026-11-18。41 条完整榜单摘要均已阅读；11 篇读取了明确版本的官方正文相关章节。最终建议为 41 项范围排除、0 项纳入；这些是可复用建议，不是 owner 人工逐篇批准，也不代表论文实验重现。", "",
    "初判文件保持原样。Craftax 从初判边界项改为外部程序产物范围排除；其反馈搜索和跨任务复用证据保留为 yes。SilentGuard 的 clean-trace contract mining 及作者方法迭代同样保留，不将其简化为纯手写检查。", "",
    "Sage 的 HF/Atom 摘要 S1.5 与官方 v1 HTML S2.1 身份冲突、SPILLWAY 的 HF .007 与官方 v2 .005 数字差异均待来源澄清；当前范围意见不抹去这些待核记录。", "",
    "本子任务 0 次付费请求，11 次免费官方全文请求；未改 canonical、正式 review、生产代码或 Git。全部具体引句、源文件 SHA256、版本水印、日期与可恢复条件见 JSON。", "",
    f"引句与哈希等 {len(checks)} 项机器校验通过，0 失败。该校验只证明所存来源和引句绑定，不证明论文科学结论。", "",
    "| ID | 官方当前版本 | 范围建议 | 具体原因 |", "|---|---|---|---|"]
for x in records:
    lines.append(f"| {x['id']} | v{x['official_metadata']['version']} | 排除 | {x['reason_zh'].replace('|', '/')} |")
lines += ["", "文件：`initial-scope.json`、`source-index.json`、`final-scope-review.json`、`validation.json`。", ""]
(OUT / "README.md").write_text("\n".join(lines))
print(json.dumps({"records": len(records), "counts": result["counts"], "checks": len(checks),
                  "final_sha256": sha(final_path), "paid_requests": 0}, ensure_ascii=False))
