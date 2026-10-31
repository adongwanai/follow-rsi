"""Compare frozen independent scope findings with the primary review.

This is a post-freeze artifact; it must not rewrite frozen findings or sources.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
PRIMARY = OUT.parent / "primary/review-results.json"
FROZEN_SHA = "9643bc9680169bb9997b7ffdac0e61ff4815a7ebb188fa64c6c706ddb58b51bd"
PRIMARY_SHA = "c8fa683ff616cc433350c4bc7b6abb9d169982c7f3b5a570b381adcf6463136d"
FIGURE = ROOT / "build/maintenance-2026-10-31/primary/sources/2610.39884.figure5.png"
FIGURE_META = FIGURE.with_suffix(".meta.json")
FIGURE_SHA = "98623fd1ea2f00e5310a983db4dddbd2772f40459297335687df579f3c21cfbf"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


assert digest(OUT / "frozen-findings.json") == FROZEN_SHA
assert digest(PRIMARY) == PRIMARY_SHA
assert digest(FIGURE) == FIGURE_SHA == load(FIGURE_META)["sha256"]
frozen = load(OUT / "frozen-findings.json")
source_input_export = load(OUT / "export-path-redaction.json")
source_inputs = load(OUT / "source-inputs.json")
assert frozen["source_inputs_sha256"] == source_input_export["frozen_original_sha256"]
assert digest(OUT / "source-inputs.json") == source_input_export["exported_sha256"]
assert source_input_export["changed_json_pointers"] == ["/criteria/owner_document"]
assert source_inputs["criteria"]["owner_document"] == source_input_export["path_mapping"][0]["exported_value"]
assert not Path(source_inputs["criteria"]["owner_document"]).is_absolute()
non_path_inputs = load(OUT / "source-inputs.json")
non_path_inputs["criteria"].pop("owner_document")
non_path_sha = sha256(json.dumps(non_path_inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert non_path_sha == source_input_export["non_path_content_sha256_before"] == source_input_export["non_path_content_sha256_after"]
assert source_input_export["path_only_byte_replacement_verified_at_export"]
assert digest(OUT / "frozen-findings.json") == source_input_export["frozen_findings_sha256"]
assert digest(OUT / "source-reviews.jsonl") == source_input_export["source_reviews_sha256"]
assert digest(ROOT / "build/maintenance-2026-10-31/primary/intake-manifest.json") == source_inputs["intake_sha256"]
assert digest(ROOT / "build/maintenance-2026-10-31/primary/official-metadata.json") == source_inputs["official_metadata_sha256"]
independent = {row["id"]: row for row in map(json.loads, (OUT / "source-reviews.jsonl").read_text().splitlines())}
primary_report = load(PRIMARY)
primary = {row["id"]: row for row in primary_report["items"]}
assert set(primary) == set(independent) == set(frozen["items"])
normalize = {"harness": "include", "exclude": "exclude", "other_direction": "exclude", "borderline": "defer"}
snapshot = {
    "source_file": str(PRIMARY.relative_to(ROOT)),
    "source_sha256": PRIMARY_SHA,
    "primary_completed_at": primary_report["completed_at"],
    "independent_frozen_at": frozen["frozen_at"],
    "captured_after_independent_freeze": True,
    "comparison_dimensions": "Harness eligibility only. Other RSI direction labels are not asserted to agree.",
    "items": [],
}
rows = []
for aid in sorted(primary):
    p, i = primary[aid], independent[aid]
    snapshot["items"].append({key: p[key] for key in ["id", "title", "harness_scope_recommendation", "scope_kind", "harness_sub", "reason_zh", "boundary_note_zh", "source_quotes", "owner_decision", "owner_reviewed", "publication_authorized"]})
    rows.append({
        "id": aid,
        "title": i["title"],
        "primary_original": p["harness_scope_recommendation"],
        "primary_normalized": normalize[p["harness_scope_recommendation"]],
        "independent_frozen": i["recommendation"],
        "harness_eligibility_agreement": normalize[p["harness_scope_recommendation"]] == i["recommendation"],
        "independent_type": i["suggested_type"],
        "formal_decision": "defer",
    })
disagreements = [row for row in rows if not row["harness_eligibility_agreement"]]
assert [row["id"] for row in disagreements] == ["arxiv:2610.39884"]
assert all(row["owner_decision"] == "defer" and not row["owner_reviewed"] and not row["publication_authorized"] for row in primary.values())
save("primary-comparison-snapshot.json", snapshot)

comparison = {
    "review_date": "2026-10-31",
    "compared_at": datetime.now(timezone.utc).isoformat(),
    "status": "post_freeze_comparison_not_owner_approval",
    "independent_frozen_sha256": FROZEN_SHA,
    "primary_original_sha256": PRIMARY_SHA,
    "source_inputs_export": {"mapping_file": "export-path-redaction.json", "frozen_original_sha256": source_input_export["frozen_original_sha256"], "exported_sha256": source_input_export["exported_sha256"], "path_only_export_mapping_verified": True, "historical_frozen_reference_preserved": True},
    "primary_comparison_snapshot_sha256": digest(OUT / "primary-comparison-snapshot.json"),
    "normalization": normalize,
    "normalization_limit": snapshot["comparison_dimensions"],
    "counts": {"matched_ids": len(rows), "initial_harness_agreement": len(rows) - len(disagreements), "initial_harness_disagreement": len(disagreements), "independent_recommendations": dict(Counter(row["independent_frozen"] for row in rows)), "reconciled_suggestions": {"include": 5, "exclude": 30, "defer": 2}},
    "items": rows,
    "disagreement": {
        "id": "arxiv:2610.39884",
        "title": "KARMA",
        "primary_initial": "harness/component",
        "independent_frozen": "defer/borderline",
        "positive_evidence": "Six typed modules can be edited; schema/context render the retained knowledge; feedback, atomic mutations, validation and retention are documented.",
        "unresolved_evidence": "The displayed accepted cycle changes experience rules E17-E19. The inspected text does not identify an accepted role/output_protocol/action_descriptions patch. Editable capability alone does not establish those actual changes.",
        "taxonomy_boundary": "Owner taxonomy separates reusable procedural skill/policy artifacts from experience entries and rule-handbook contents. Frozen executable code alone is not an exclusion criterion because system prompts can qualify.",
        "source_paragraph_indices": [47, 48, 49, 50, 124, 128, 134, 145, 147],
        "primary_acknowledgement": "After comparison, the primary reviewer acknowledged its initial reason had overstated editable role/protocol/action capability as demonstrated actual edits. The reviewer inspected official Figure 5 and revised the final suggestion to borderline. The original primary recommendation is preserved, with reconciliation recorded separately.",
        "post_freeze_figure_check": {"file": str(FIGURE.relative_to(ROOT)), "url": load(FIGURE_META)["url"], "sha256": FIGURE_SHA, "observation_method": "Both reviewers visually inspected the shared official image after independent findings had been frozen; these labels are not counted among the 57 text-substring checks.", "accepted_mutation_labels": ["E17 experience", "E18 experience", "E19 experience"], "rejected_mutation_labels": ["E06 experience", "E12 experience", "E07 experience"], "limit": "The displayed cycles do not enumerate every accepted mutation in all runs."},
        "reconciled_suggestion": "defer/borderline",
        "followup": "Inspect actual retained mutation fields and rule semantics; obtain owner scope adjudication. Do not auto-accept or mechanically exclude.",
        "formal_decision": "defer",
    },
    "shared_boundary": {"id": "arxiv:2610.39714", "title": "MoLRSI", "recommendation": "defer", "reason": "The principal loop changes scientific workflows and experience; ancillary retained skill repair is plausible but actual reusable agent-program changes and attribution require evidence."},
    "material_candidate_limits": {
        "arxiv:2610.37905": "Online ordered stream with repeated companies, not independent/company-disjoint held-out testing.",
        "arxiv:2610.38392": "Mostly controlled deletion pressure; natural optimizer/GEPA experiments are limited case studies.",
        "arxiv:2610.39122": "Only the fixed-model procedural skill branch is Harness-related; a separate RL branch is not coevolution. Disk skill format remains unknown.",
        "arxiv:2610.39358": "The paired gate permits some performance decrease under its tolerance; accepted does not imply strict improvement.",
        "arxiv:2610.39508": "The paper acknowledges inspection of held-out failure cases during development; test-time bank freezing does not establish untouched held-out development.",
    },
    "source_verification_count_clarification": {"raw_http_body_files": 50, "body_metadata_files": 13, "derived_paragraph_files": 13, "total_source_files": 76, "exact_body_quote_checks": 57},
    "all_formal_decisions": "defer",
    "publication_authorized": False,
    "paid_api_calls": 0,
}
save("comparison.json", comparison)

text = """# 冻结后的交叉对照

初始独立判断与主审共对照 37 个稳定 ID，按 Harness 准入归一化后 **36 项一致，1 项有分歧**。归一化只把主审 `harness` 对应 `include`、`other_direction/exclude` 对应排除 Harness、`borderline` 对应待定；不声称其他 RSI 大类的细分标签也完全一致。

独立结果先冻结，再读取主审分类。原始建议仍是 **5 项建议纳入、30 项排除 Harness、2 项边界待定**。`frozen-findings.json` 未重写；全部正式决定仍为 `defer`，未批准发布。

## KARMA：保留分歧及证据边界

主审初始建议 `harness/component`，独立建议待定。六类模块可以修改、修改会写入文件、验证后继续使用，这些正证据成立。可执行代码冻结也不构成排除依据，因为系统提示本身可以是 Harness 工件。

但目前展示的已接纳案例是 Appendix D 中经验规则 E17–E19 的变更。正文列出的角色、输出协议和动作说明的**可编辑接口**，不足以证明实验实际接纳过这些字段的程序性修改。正文段落 134 本身明确区分提案中的预期变化与 mutation journal 记录的实际变化。主审在对照后承认，原理由将这种能力写成了已发生的修改，表述超出已展示证据。

冻结后，两位审查者又目视核对了官方 Figure 5。图中的已接纳 E17、E18、E19 和被拒绝 E06、E12、E07 均明确标为 `experience`。主审据此将最终建议改为 `borderline`，最终一致的建议为 **5 纳入、30 排除 Harness、2 待定**；原始 36 一致／1 分歧的记录不覆盖。

本轮仍保留 owner 裁决边界：这些例图不枚举所有运行的全部修改，继续核对真实已接纳补丁、规则语义及后续引用，再按 owner 的“程序性技能／策略文件”与“经验／规则手册内容”边界裁决。不能只凭 Harness 标题纳入，也不能只凭代码冻结排除。原始主审与独立结论都保留，正式决定全部 `defer`。

## 共同待定与候选限制

- MoLRSI 两轮均认为需要进一步裁决：主循环的科学工作流／经验改进，与附加的可保留资源技能修复，需要分开归因。
- FilingLoop 的程序性 Markdown 技能更新成立，但不是独立公司留出评估。
- Masked Erosion 主要是受控删除实验；不能将小规模自然优化器案例推广为真实部署频率。
- Appreciation 的技能与 RL 分支分开评测，不能混写成共同演化；磁盘技能格式保持未知。
- Before the Next Rollout 确实分别更新权重与技能正文；准入容差允许分数下降，不能宣称每个接纳编辑都严格改善。
- SkillCompiler 正文段落 131 承认开发阶段查看过留出失败案例；冻结测试时的程序库不意味着开发完全未接触留出样本。

## 日期与验证口径

HF 10 月 31 日此次响应为空；23 项是 10 月 30 日上榜后补，20 项来自 remote-main 新稳定 ID，重叠 6 项，去重审查 37 项。审核日期不能代替上榜日期或论文首发日期。

独立包的 76 个来源文件哈希包含 **50 份原始 HTTP 正文、13 份正文来源元数据、13 份派生段落文件**；不是 76 次独立抓取。57 条正文短引句都逐字核对了规范化空白后的连续子串。来源采集与主审共享，判断在对照前独立冻结；未复现实验，也未认证论文数字。

Figure 5 在冻结后补查，其原图哈希为 `98623fd1ea2f00e5310a983db4dddbd2772f40459297335687df579f3c21cfbf`。对图中模块标签的确认属于目视检查，不计入 57 条机器逐字核对的正文引句，也不计入冻结前的 76 个来源文件。
"""
(OUT / "comparison.md").write_text(text)
assert digest(OUT / "frozen-findings.json") == FROZEN_SHA
assert digest(OUT / "source-reviews.jsonl") == frozen["source_reviews_sha256"]
validation = load(OUT / "validation.json")
for path, expected in validation["source_files"].items():
    assert digest(ROOT / path) == expected, path
save("comparison-validation.json", {"result": "pass", "matched_ids": len(rows), "initial_agreements": 36, "initial_disagreements": 1, "reconciled_suggestions": {"include": 5, "exclude": 30, "defer": 2}, "frozen_findings_sha256": FROZEN_SHA, "frozen_findings_unchanged": True, "source_reviews_unchanged": True, "source_hashes_rechecked": len(validation["source_files"]), "paper_intake_and_official_metadata_hashes_verified": True, "source_inputs_export": comparison["source_inputs_export"], "source_inputs_non_path_content_sha256": non_path_sha, "post_freeze_figure_sha256": FIGURE_SHA, "post_freeze_figure_hash_verified": True, "all_formal_decisions": "defer", "publication_authorized": False, "paid_api_calls": 0})
hashes = {str(path.relative_to(OUT)): digest(path) for path in sorted(OUT.rglob("*")) if path.is_file() and path != OUT / "package-hashes.json"}
save("package-hashes.json", {"files": hashes, "contains_full_paper_cache": False, "contains_owner_acceptance": False})
print(json.dumps({"result": "pass", "frozen_sha256": FROZEN_SHA, "initial_agreements": 36, "initial_disagreements": 1, "packaged_files": len(hashes)}))
