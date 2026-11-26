"""Archive Round-3 independent reviews, reconcile parent Round-2/3 decisions, and preflight all six dated review queues."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import collections
import gzip
import hashlib
import json
import shutil
import sys
import yaml

R = Path.cwd()
if str(R) not in sys.path:
    sys.path.insert(0, str(R))

from scripts.feed.storage import load_items
from scripts.feed.review import _review_row, source_hash, validate_daily_review
from scripts.feed.window import daily_metadata
from scripts.feed.dates import daily_section
from scripts.feed.guard import check_summary, unknown_evidence
from scripts.feed.scope import load_scope, require_scope

SCRATCH = Path("/Users/mac/.gemini/antigravity/brain/9baa8f34-70a0-48b3-bdde-43db27349843/scratch/review-2026-11-26")
B = R / "build/maintenance-2026-11-26"
D = R / "docs/internal/reports/maintenance-2026-11-26"
P = D / "primary-review"
O = B / "reviews"
P.mkdir(parents=True, exist_ok=True)
O.mkdir(parents=True, exist_ok=True)


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


items = {x["id"]: x for x in load_items(R)}
scope = load_scope(R)

# 1. Copy independent Round-3 JSON reports and archive referenced raw fulltexts.
reports = {}
for kind, fname in (("hf", "final.json"), ("other", "final.json"), ("backlog", "review.json")):
    src_dir = SCRATCH / f"independent-{kind}"
    dst_dir = D / f"independent-{kind}"
    raw_dir = R / f"data/feed/raw/maintenance-2026-11-26/independent-{kind}"
    dst_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src_dir / fname, dst_dir / fname)
    payload = json.loads((dst_dir / fname).read_text(encoding="utf-8"))
    reports[kind] = payload

    archived = []
    seen_paths = set()
    if kind in ("hf", "other"):
        inp = SCRATCH / f"{kind}-input.json"
        inp_bytes = inp.read_bytes()
        inp_gz = raw_dir / "input.json.gz"
        inp_gz.write_bytes(gzip.compress(inp_bytes, mtime=0))
        archived.append({
            "original_path": str(inp),
            "archive": str(inp_gz.relative_to(R)),
            "original_sha256": digest(inp_bytes),
            "archive_sha256": digest(inp_gz.read_bytes()),
            "bytes": len(inp_bytes),
        })
        for row in payload["items"]:
            for ev in row.get("evidence", []):
                sp = ev.get("source_path")
                if not sp or sp in seen_paths:
                    continue
                p = Path(sp)
                if not p.is_file():
                    continue
                seen_paths.add(sp)
                content = p.read_bytes()
                target = raw_dir / (p.name + ".gz")
                target.write_bytes(gzip.compress(content, mtime=0))
                archived.append({
                    "original_path": sp,
                    "archive": str(target.relative_to(R)),
                    "original_sha256": digest(content),
                    "archive_sha256": digest(target.read_bytes()),
                    "bytes": len(content),
                })
    else:
        rec = SCRATCH / "legacy-recheck-receipts.json"
        rec_bytes = rec.read_bytes()
        rec_gz = raw_dir / "fetch-receipts.json.gz"
        rec_gz.write_bytes(gzip.compress(rec_bytes, mtime=0))
        archived.append({
            "original_path": str(rec),
            "archive": str(rec_gz.relative_to(R)),
            "original_sha256": digest(rec_bytes),
            "archive_sha256": digest(rec_gz.read_bytes()),
            "bytes": len(rec_bytes),
        })
    write_json(dst_dir / "source-storage-index.json", archived)

# 2. Parent Round-2/Round-3 refinements (preserving original independent files untouched).
direction_changes = {
    "arxiv:2611.31794": {
        "primary": "evaluation_benchmark",
        "harness_sub": None,
        "secondary": ["harness"],
    },
}
summary_changes = {
    "arxiv:2611.31794": (
        "评测通用编码脚手架迭代修改目标智能体技能、提示、工具与控制代码；部分基准存在移除模型调用的规则替代捷径。",
        "Benchmarks off-the-shelf coding harnesses editing target agent skills, prompts, tools, and code under fixed budgets, exposing deterministic-controller shortcuts on several tasks.",
    ),
    "arxiv:2611.33757": (
        "从成对成败轨迹演化上下文触发式诊断干预策略并经跨任务重放筛选迁移；部分头条提升的配对置信区间跨零。",
        "Evolves context-triggered diagnostic intervention policies from paired traces with cross-task replay selection for transfer; paired confidence intervals on several headline gains cross zero.",
    ),
    "arxiv:2611.33700": (
        "基于反馈引擎分别驱动SQL模型训练与规划技能脚手架的有界重放修复；两套演化环尚未做联合交替归因。",
        "Uses a shared feedback engine to drive SQL model training and replay-gated planning-and-skill harness repairs; alternating joint credit assignment remains open.",
    ),
    "arxiv:2611.29036": (
        "提出多方协作简报基准，并在专题实验中基于覆盖率反馈搜索检索与综合指令脚手架以评估跨项目迁移。",
        "Introduces a collaborative briefing benchmark and evaluates coverage-guided search over retrieval and synthesis harness instructions for cross-project transfer.",
    ),
}

rows = []
DAYS = ("2026-11-21", "2026-11-22", "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26")

for kind in ("hf", "other"):
    report = reports[kind]
    review_src = str((D / f"independent-{kind}/final.json").relative_to(R))
    for r in report["items"]:
        item = items[r["id"]]
        assert r["input_source_hash"] == source_hash(item), (r["id"], r["input_source_hash"], source_hash(item))
        decision = r["decision"]
        action = r.get("publication_action", "apply")
        hf_dates = sorted(item.get("hf_daily_dates") or [])
        day = hf_dates[-1] if hf_dates else str(item.get("updated") or item.get("published"))[:10]
        reason = r["reason_zh"]
        sm = None
        direction = None

        if action == "metadata_receipt_only":
            decision = "defer"
            reason += " 本行defer只记录新增观察到的HF推荐日元数据回执并阻止重复出版，保留既有科学审核与原source_hash绑定。"
        elif decision in ("accept", "backlog"):
            direction = deepcopy(direction_changes.get(item["id"], r["direction"]))
            if item["id"] in summary_changes:
                sm = dict(zip(("summary_zh", "summary_en"), summary_changes[item["id"]]))
            else:
                sm = {"summary_zh": r["summary_zh"], "summary_en": r["summary_en"]}
            require_scope({"id": item["id"], "direction": direction}, scope)
            if day < "2026-11-21":
                decision = "backlog"
                day = "2026-11-26"
            else:
                decision = "accept"
        else:
            assert decision == "reject", (item["id"], decision)
            if day < "2026-11-21":
                day = "2026-11-26"

        assert day in DAYS, (item["id"], day)
        if item["id"] == "arxiv:2611.32185":
            reason += " 母代理二轮初筛曾将其列为候选正例；经三轮交叉核对§4.5 Eq.3与Alg.1–2确认部署工件为无大模型调用的~2 FPS纯视觉/几何求解脚本，S_i仅为单任务假设记录，故采纳排除并保留初筛纠正记录。"
        if item["id"] == "arxiv:2611.31794":
            reason += " 母代理将主方向由harness/evolve_main细化为evaluation_benchmark（secondary含harness），因本文核心贡献是对现成编码Harness作迭代优化器的系统基准评测与规则替代捷径诊断。"

        limits = r.get("limitations_zh", [])
        if limits:
            reason += " " + " ".join(limits)

        rows.append({
            "id": item["id"],
            "edition_date": day,
            "reviewed_on": "2026-11-26",
            "source_hash": source_hash(item),
            "decision": decision,
            "application": action,
            "direction": direction,
            "summary_override": sm,
            "reason": reason.strip(),
            "review_source": review_src,
            "evidence": deepcopy(r),
            "evidence_quick": unknown_evidence(),
        })

assert len(rows) == 246 and len({x["id"] for x in rows}) == 246
decision_counts = dict(collections.Counter(r["decision"] for r in rows))
assert decision_counts == {"accept": 25, "backlog": 2, "reject": 215, "defer": 4}, decision_counts

# 3. Build all six dated review queues (preserving unpublished Nov-23 rows on 2026-11-23).
queues = {day: {"date": day, "reviewed_on": "2026-11-26", "items": [], "lab_updates": []} for day in DAYS}
for prior_day in ("2026-11-21", "2026-11-22", "2026-11-23"):
    prior_path = R / f"review/daily/{prior_day}.yaml"
    if prior_path.exists():
        (P / f"prior-review-{prior_day}.yaml").write_bytes(prior_path.read_bytes())

prior_23 = yaml.safe_load((R / "review/daily/2026-11-23.yaml").read_text(encoding="utf-8"))
preserved_23_ids = []
for group in ("items", "lab_updates"):
    for old_row in prior_23[group]:
        it = items[old_row["id"]]
        timing = daily_metadata(R, it, "2026-11-23")
        if timing["window_status"] == "already_published":
            continue
        refreshed = deepcopy(old_row)
        refreshed.update(timing)
        refreshed["daily_section"] = daily_section({**it, **timing}, "2026-11-23")
        queues["2026-11-23"][group].append(refreshed)
        preserved_23_ids.append(old_row["id"])
assert len(preserved_23_ids) == 30, len(preserved_23_ids)

checks = []
for r in rows:
    item = items[r["id"]]
    day = r["edition_date"]
    timing = daily_metadata(R, item, day)
    note_text = r["reason"] + " 三轮证据见 docs/internal/reports/maintenance-2026-11-26/primary-review/final-adjudication.json。"
    if item["kind"] in ("post", "release"):
        row = {
            "id": item["id"],
            "title": item["title"],
            "kind": item["kind"],
            "links": deepcopy(item.get("links", {})),
            "source_hash": r["source_hash"],
            "llm": deepcopy(item.get("llm", {})),
            "direction_override": None,
            "decision": r["decision"],
            "note": note_text,
            "published": item["published"],
            "updated": item.get("updated", item["published"]),
            "hf_daily_dates": item.get("hf_daily_dates", []),
            **timing,
            "daily_section": daily_section({**item, **timing}, day),
        }
        queues[day]["lab_updates"].append(row)
    else:
        row = _review_row(item)
        row.update(timing)
        row["daily_section"] = daily_section({**item, **timing}, day)
        row.update(
            decision=r["decision"],
            promote_to_repo=False,
            evidence_quick=r["evidence_quick"],
            evidence_notice="三轮来源与范围交叉审查；未实验复现。",
            note=note_text,
        )
        if r["summary_override"]:
            row.update(summary_override=r["summary_override"], direction_override=r["direction"])
            g = check_summary(item["title"], item.get("abstract", ""), **r["summary_override"])
            assert g["ok"], (item["id"], g)
            checks.append({"id": item["id"], "guard": g, "summary_contains_numeric_claims": False})
        queues[day]["items"].append(row)

validation = []
for day, q in queues.items():
    data = yaml.safe_dump(q, allow_unicode=True, sort_keys=False, width=110).encode("utf-8")
    (O / f"{day}.yaml").write_bytes(data)
    p = R / f"review/daily/{day}.yaml"
    prior = p.read_bytes() if p.exists() else None
    try:
        p.write_bytes(data)
        validate_daily_review(R, day)
    finally:
        if prior is None:
            p.unlink()
        else:
            p.write_bytes(prior)
    validation.append({
        "date": day,
        "reviewed_on": "2026-11-26",
        "path": str(p.relative_to(R)),
        "items": len(q["items"]),
        "lab_updates": len(q["lab_updates"]),
        "counts": dict(collections.Counter(x["decision"] for x in q["items"] + q["lab_updates"])),
        "sha256": digest(data),
        "apply_ids": [x["id"] for x in rows if x["edition_date"] == day and x["application"] == "apply"],
        "metadata_only_ids": [x["id"] for x in rows if x["edition_date"] == day and x["application"] != "apply"],
        "preserved_prior_unpublished_ids": preserved_23_ids if day == "2026-11-23" else [],
    })

spotchecks = [
    "arxiv:2611.34750", "arxiv:2611.32185", "arxiv:2611.32085", "arxiv:2611.33836",
    "arxiv:2611.32093", "arxiv:2611.31733", "arxiv:2611.32325", "arxiv:2611.29807",
    "arxiv:2611.30965", "arxiv:2611.29513", "arxiv:2611.32606", "arxiv:2611.31201",
    "arxiv:2611.34400", "arxiv:2611.32508", "arxiv:2611.29274",
    "post:https://sakana.ai/marlin-update-2/",
    "post:https://deepmind.google/blog/interpreting-mass-spectra-with-google-antigravity/",
]

write_json(P / "final-adjudication.json", {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "reviewed_on": "2026-11-26",
    "reviewer": "Parent Antigravity agent under standing owner authorization; no claim of manual owner per-paper reading",
    "round1": "Full stable ID/raw/canonical reconciliation across all 12 enabled sources, 6 complete HF boards (Nov 21–26), and official arXiv metadata.",
    "round2": "Parent inspected fulltexts and exact update objects, execution feedback, and cross-task retention across 60+ positive, borderline, and exclusion candidates plus lab posts/releases.",
    "round3": "Three independent blind subagents cross-reviewed all 159 HF items, all 87 Non-HF items, and all 8 open issues / 4 anchors, archiving exact source bytes and preserving differences.",
    "parent_exclusion_spotchecks": spotchecks,
    "parent_corrections": [
        "OVOK (arxiv:2611.32185): parent Round-2 initially treated (S, U, W) as a candidate positive; Round-3 cross-check of Sec. 4.5 Eq. 3 & Alg. 1–2 verified W* is a standalone ~2 FPS CV/geometry solver without runtime LLM calls and S_i holds single-task hypotheses inside a fixed P-E-V loop, so reject is adopted and the Round-2 opinion is preserved.",
        "AGL-SKILL (arxiv:2611.31794): refined primary direction from harness/evolve_main to evaluation_benchmark (secondary: ['harness']) and highlighted deterministic-controller replacement shortcuts on ALFWorld/LiveMath.",
        "Explicit statistical and coupling boundaries added to summaries of TransHarness (paired CIs crossing zero on headline DeepSeek slices), Sports Agent (parallel loops without alternating joint credit assignment), and GroupBrief (benchmark + Sec. 5 harness search).",
    ],
    "counts": decision_counts,
    "new_intake_counts": {
        "total": 242,
        "accept_daily": 25,
        "historical_backlog": 2,
        "reject": 215,
        "defer": 0,
    },
    "metadata_only_existing_hf": 4,
    "per_date": validation,
    "summary_guards": checks,
    "scope_review_not_replication": True,
    "paid_model_calls": 0,
    "paid_tokens": 0,
    "global_quality_warning": {
        "recall": 0.892857,
        "threshold": 0.90,
        "complete": False,
        "rerun": False,
    },
    "items": rows,
})
write_json(B / "review-preflight.json", {"reviews": validation})
print(json.dumps([{k: v for k, v in x.items() if not k.endswith("_ids")} for x in validation], ensure_ascii=False))
