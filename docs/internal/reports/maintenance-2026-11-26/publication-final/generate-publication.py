"""Compile reviewed Nov 21–26 editions, W47 supplement, and Nov 26 historical recap from verified merged review PRs."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib
import json
import os
import subprocess
import sys
import yaml

R = Path.cwd()
if str(R) not in sys.path:
    sys.path.insert(0, str(R))

from scripts.feed.ci import merged_review_requests, human_owner_review
from scripts.feed.review import apply_daily_review, source_hash, approved_weekly_backlog, validate_weekly_picks, daily_editions_for_week
from scripts.feed.digest import publish_day, render_recap, initialize_public, _public_item, _directions, _summary_intro, _metrics
from scripts.feed.health import update_health
from scripts.feed.storage import load_items, save_items, write_json

B = R / "build/maintenance-2026-11-26"
D = R / "docs/internal/reports/maintenance-2026-11-26"
OUT = D / "publication-final"
OUT.mkdir(parents=True, exist_ok=True)
STAMP = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
REPO = "adongwanai/follow-rsi"
ENV = {**os.environ, "GODEBUG": "http2client=0"}


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], cwd=R, env=ENV, text=True))


def verify(entry):
    n = entry["number"]
    pr = gh("api", f"repos/{REPO}/pulls/{n}")
    assert pr["merged"] and pr["base"]["ref"] == "main" and pr["head"]["sha"] == entry["head"], (n, pr.get("merged"))
    pages = gh("api", "--paginate", "--slurp", f"repos/{REPO}/pulls/{n}/files?per_page=100")
    files = [r for p in pages for r in p]
    assert len(files) == pr["changed_files"] == 1
    req = merged_review_requests({"pull_request": pr}, [r["filename"] for r in files], REPO)
    assert len(req) == 1 and req[0]["path"] == entry["path"]
    owner = human_owner_review(pr, [], REPO)
    cp = B / f"pr-audit/pr-{n}-checks.json"
    checks = json.loads(cp.read_text(encoding="utf-8"))
    assert checks["head"] == entry["head"]
    for name in ("build", "validate"):
        found = [r for r in checks["checks"]["check_runs"] if r["name"] == name]
        assert found and max(found, key=lambda r: r["id"])["conclusion"] == "success"
    found = [r for r in checks["statuses"]["statuses"] if r["context"] == "Follow RSI owner decisions"]
    assert found and max(found, key=lambda r: r["id"])["state"] == "success"
    content = subprocess.check_output(["git", "show", pr["merge_commit_sha"] + ":" + entry["path"]], cwd=R)
    assert digest(content) == entry["sha256"] and content == (R / entry["path"]).read_bytes()
    receipt = {
        "request": req[0],
        "github_pr": n,
        "head": entry["head"],
        "owner_login": owner,
        "merge_commit": pr["merge_commit_sha"],
        "review_sha256": digest(content),
        "verified_at": STAMP,
        "check_receipt_sha256": digest(cp.read_bytes()),
        "authorization": "Standing owner authorization; not a claim of manual owner per-paper reading.",
    }
    write_json(OUT / f"verified-review-{n}.json", receipt)
    write_json(OUT / f"pr-{n}-files.json", files)
    return receipt, content


def prov(r):
    return {k: r[k] for k in ("github_pr", "owner_login", "merge_commit")}


assert not (OUT / "generation-receipt.json").exists(), "Do not repeat application; render stored manifests instead."
plan = json.loads((B / "created-review-prs.json").read_text(encoding="utf-8"))["reviews"]
verified = {}
for e in plan:
    verified[e["number"]] = (*verify(e), e)

before = {x["id"]: deepcopy(x) for x in load_items(R)}
prior = {str(p.relative_to(R)): digest(p.read_bytes()) for f in ("daily", "weekly", "recaps") for p in (R / "site" / f).glob("*.json")}
for d_short, d_full in (("21", "2026-11-21"), ("22", "2026-11-22"), ("23", "2026-11-23")):
    write_json(OUT / f"prior-nov{d_short}-observed-status.json", json.loads((R / f"site/daily/{d_full}.json").read_text(encoding="utf-8")))
    write_json(OUT / f"prior-provenance-{d_full}.json", json.loads((R / f"data/feed/review-provenance/{d_full}.json").read_text(encoding="utf-8")))
old_w47 = json.loads((R / "site/weekly/2026-W47.json").read_text(encoding="utf-8"))
write_json(OUT / "prior-w47-manifest.json", old_w47)
write_json(OUT / "prior-canonical-boundaries.json", {k: {"source_hash": source_hash(v), "first_seen": v["first_seen"]} for k, v in before.items()})

adjud = json.loads((D / "primary-review/final-adjudication.json").read_text(encoding="utf-8"))
byid = {r["id"]: r for r in adjud["items"]}

# 1. Apply 242 new canonical decisions cleanly with subset isolation and idempotency verification.
for e in sorted(plan, key=lambda x: x["date"]):
    receipt, content, _ = verified[e["number"]]
    selected = set(e["apply_ids"])
    path = R / e["path"]
    full = yaml.safe_load(content)
    subset = deepcopy(full)
    for group in ("items", "lab_updates"):
        subset[group] = [r for r in full[group] if r["id"] in selected]
    assert {r["id"] for r in subset["items"] + subset["lab_updates"]} == selected
    histories = []
    for key in selected:
        old = deepcopy(before[key])
        if old.get("review"):
            if old["review"] not in old.setdefault("review_history", []):
                old["review_history"].append(deepcopy(old["review"]))
            histories.append(old)
    if histories:
        save_items(R, histories)
    try:
        path.write_text(yaml.safe_dump(subset, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
        changed = apply_daily_review(R, e["date"], now=STAMP, provenance=prov(receipt))
        second = apply_daily_review(R, e["date"], now=STAMP, provenance=prov(receipt))
    finally:
        path.write_bytes(content)
    write_json(OUT / f"applied-{e['date']}.json", {"applied": changed, "second_apply_changed": second, "ids": sorted(selected), "receipt": receipt})
    assert changed == len(selected) and second == 0, (e["date"], changed, len(selected), second)

# 2. Write review-provenance and metadata_review_receipts for the 4 existing HF date updates.
for e in plan:
    receipt = verified[e["number"]][0]
    write_json(R / f"data/feed/review-provenance/{e['date']}.json", {**receipt["request"], **prov(receipt)})
    for key in e["metadata_only_ids"]:
        item = deepcopy(before[key])
        r = byid[key]
        meta = {
            **prov(receipt),
            "kind": r["application"],
            "date": e["date"],
            "reviewed_on": "2026-11-26",
            "source_hash": source_hash(item),
            "previous_approval_source_hash": item.get("review", {}).get("source_hash"),
            "scientific_review_preserved": True,
            "scientific_content_reapproved": False,
            "republished": False,
            "note": r["reason"],
        }
        item.setdefault("metadata_review_receipts", []).append(meta)
        save_items(R, [item])
        write_json(OUT / ("metadata-" + key.replace(":", "-") + ".json"), meta)

# 3. Update state.json and daily-status.json truthfully.
snapshot = json.loads((R / "data/feed/raw/maintenance-2026-11-26/source-intake/all-source-snapshot.json").read_text(encoding="utf-8"))
state = json.loads((R / "data/feed/state.json").read_text(encoding="utf-8"))
write_json(OUT / "source-state-before.json", state)
public_sources = {}
fetch = []
boards = {"2026-11-21": 0, "2026-11-22": 0, "2026-11-23": 26, "2026-11-24": 50, "2026-11-25": 50, "2026-11-26": 46}
for s in snapshot["sources"]:
    key = s["source_id"]
    ok = s["status"] == "ok"
    avail = "available" if ok else "partial" if s["status"] == "partial" else "failed"
    r = state["sources"][key]
    r.update(last_count=s["configured_window_records"], last_run=s["finished_at"], last_ok=ok, last_error=s["error"], availability=avail, degraded=not ok)
    if ok:
        r.update(last_success=s["finished_at"], consecutive_errors=0, consecutive_failures=0)
    else:
        r["consecutive_errors"] = r.get("consecutive_errors", 0) + 1
        r["consecutive_failures"] = r.get("consecutive_failures", 0) + 1
    if key == "hf-daily":
        r.update(today_board_status="available", today_board_count=46, available_through=None, boards=boards)
    public_sources[key] = {"count": s["configured_window_records"], "run_at": s["finished_at"], "error": s["error"], "availability": avail}
    fetch.append({k: s[k] for k in ("source_id", "started_at", "finished_at", "request_count", "http_status_counts", "source_traversal_complete", "error")} | {"ok": ok, "count": s["configured_window_records"], "availability": avail, "degraded": not ok})

state["last_fetch"] = {
    "run_at": snapshot["generated_at"],
    "sources": fetch,
    "snapshot": "data/feed/raw/maintenance-2026-11-26/source-intake/all-source-snapshot.json",
    "report": "docs/internal/reports/maintenance-2026-11-26/source-intake/README.md",
}
state["last_hf_supplement"] = {
    "observed_at": snapshot["generated_at"],
    "boards": boards,
    "available_through": None,
    "reconciliation_report": "docs/internal/reports/maintenance-2026-11-26/source-intake/hf-board-reconciliation.json",
}
write_json(R / "data/feed/state.json", state)

statuses = json.loads((R / "data/feed/daily-status.json").read_text(encoding="utf-8"))
write_json(OUT / "daily-status-before.json", statuses)
for row in statuses["days"]:
    if row["date"] in ("2026-11-21", "2026-11-22", "2026-11-23"):
        n_acc = {"2026-11-21": 2, "2026-11-22": 1, "2026-11-23": 5}[row["date"]]
        row["status"] = "published"
        row["supplement_checked_at"] = snapshot["generated_at"]
        row["supplement_reviewed_on"] = "2026-11-26"
        row["reason_zh"] += f" 11/26复抓全量信源后按真实来源窗口补刊{n_acc}篇通过三轮复核的论文，保留首次状态简报发布时间与当时观测快照。"
        row["reason_en"] += f" On Nov 26, full-source collection added {n_acc} three-round-verified paper(s) under this edition's true source window, preserving the initial status bulletin timestamp and snapshot."

for day, count_acc, hf_cnt, desc_zh, desc_en in [
    (
        "2026-11-24", 10, 50,
        "11/26北京时间18:58–19:03采集全部12路启用来源并复抓11/24完整HF榜50篇（含2篇HF纳入、2条既有HF推荐日元数据回执）及其他信源8篇纳入，本期合计10篇按11/24真实推荐日与来源窗口补刊，实际审核日11/26。71条范围排除保留；付费模型请求0，全局质量评测告警（recall 0.892857 vs 0.90）如实保留。",
        "Collected across all 12 enabled sources on Nov 26 (18:58–19:03 Asia/Shanghai), reconciling the complete 50-paper Nov 24 HF board (two HF inclusions and two existing-item HF date receipts) plus eight inclusions from other sources. Ten papers are published under their true Nov 24 window (reviewed Nov 26), with 71 exclusions retained, zero paid generation calls, and the recall 0.892857 vs 0.90 warning preserved.",
    ),
    (
        "2026-11-25", 5, 50,
        "11/26复抓11/25完整HF榜50篇均经三轮范围审查排除；其他启用信源在11/25真实来源窗口内有5篇通过三轮复核（HoMe、TransHarness、Sports Agent、EGSE、Skeptic），按11/25刊期补刊，实际审核日11/26，另61条范围排除保留。不将非HF论文冒称HF推荐；付费模型请求0。",
        "All 50 papers on the complete Nov 25 HF board were excluded in three-round scope review; five papers from other enabled sources within the Nov 25 source window (HoMe, TransHarness, Sports Agent, EGSE, Skeptic) passed three-round verification and are published in this delayed Nov 25 edition (reviewed Nov 26), with 61 exclusions retained and zero paid generation calls.",
    ),
    (
        "2026-11-26", 2, 46,
        "11/26北京时间18:58–19:03实际尝试全部12路启用来源：当日HF榜开放46篇（RoboEvo²与SEEK 2篇通过三轮复核纳入，ELITE补记推荐日元数据回执，其余排除），同时复抓11/21–25全榜（0/0/26/50/50篇）。三路arXiv窗口11/17/5条，五路RSS窗口15/9/43/4/0条，13个GitHub仓库窗口release 5条；S2 citations保存310条窗口记录（43次请求含15次429至180秒截止），authors遇429未完成遍历，未覆盖部分保持unknown。较早窗口的HookEvo与ZhuLong-SE单列于11/26历史补录，不冒充今日新增。付费生成请求0，范围审查不声称实验复现。",
        "All 12 enabled sources were attempted on Nov 26 at 18:58–19:03 Asia/Shanghai: the same-day 46-paper HF board yielded two three-round-verified inclusions (RoboEvo² and SEEK) and one metadata receipt for ELITE, alongside complete Nov 21–25 boards (0/0/26/50/50). Three arXiv queries returned 11/17/5 window records, five RSS feeds 15/9/43/4/0, and 13 GitHub repos 5 releases; S2 citations retained 310 window records (43 requests, 15 HTTP 429s before the 180s bound) and S2 authors hit HTTP 429, leaving unvisited coverage unknown. Earlier-window HookEvo and ZhuLong-SE appear separately in the Nov 26 historical recap. Zero paid generation calls; scope review is not experimental replication.",
    ),
]:
    assert not any(r["date"] == day for r in statuses["days"]), day
    statuses["days"].append({
        "date": day,
        "reviewed_on": "2026-11-26",
        "checked_at": snapshot["generated_at"],
        "status": "published",
        "hf_snapshot": {"observed_on": "2026-11-26", "count": hf_cnt},
        "reason_zh": desc_zh,
        "reason_en": desc_en,
        "source_snapshot": "data/feed/raw/maintenance-2026-11-26/source-intake/all-source-snapshot.json",
        "collection_report": "docs/internal/reports/maintenance-2026-11-26/primary-review/final-adjudication.json",
        "paid_generation_requests": 0,
        "paid_generation_tokens": 0,
    })
statuses["updated_at"] = STAMP
write_json(R / "data/feed/daily-status.json", statuses)

# 4. Render all six daily editions (2026-11-21..2026-11-26).
expected_counts = {"2026-11-21": 2, "2026-11-22": 1, "2026-11-23": 5, "2026-11-24": 10, "2026-11-25": 5, "2026-11-26": 2}
generation = []
for day, exp_n in expected_counts.items():
    result = publish_day(R, day, client=None, now=STAMP, allow_status=True)
    p = R / f"site/daily/{day}.json"
    edition = json.loads(p.read_text(encoding="utf-8"))
    assert len(edition["items"]) == exp_n and edition.get("kind") != "daily_status", (day, len(edition["items"]))
    edition["sources"] = deepcopy(public_sources)
    edition["collection_observed_at"] = snapshot["generated_at"]
    edition["review_provenance"] = json.loads((R / f"data/feed/review-provenance/{day}.json").read_text(encoding="utf-8"))
    if day in ("2026-11-21", "2026-11-22", "2026-11-23"):
        old_prov = json.loads((OUT / f"prior-provenance-{day}.json").read_text(encoding="utf-8"))
        edition["review_provenance_history"] = [old_prov]
        edition["intro"]["zh"] += f" 本期于11/26审核并按真实来源窗口补刊；11/23首版状态简报快照已归档保留，不冒称{day[5:].replace('-', '/')}当日已采集。"
        edition["intro"]["en"] += f" Reviewed and supplemented on Nov 26 under this edition's true source window; the initial Nov 23 status bulletin snapshot is archived and preserved."
    elif day in ("2026-11-24", "2026-11-25"):
        edition["intro"]["zh"] += " 本期于11/26采集完成三轮审查并补刊；HF论文按实际推荐日，其他信源论文按真实来源窗口归期，不顺延冒充11/26当日新增。"
        edition["intro"]["en"] += " Collected, three-round reviewed, and published late on Nov 26; HF papers keep their observed recommendation dates and other papers keep their true source windows."
    else:
        edition["intro"]["zh"] += " 11/26采集全部12路启用来源（当日HF榜46篇，S2受429与时间窗限制未完全遍历）；较早来源窗口正例单列于历史补录，不混入本期计数。"
        edition["intro"]["en"] += " Collected across all 12 enabled sources on Nov 26 (46-paper same-day HF board; S2 partially traversed under HTTP 429 and time bounds); earlier-window inclusions appear separately in the historical recap."
    write_json(p, edition)
    result["manifest"] = str(Path(result["manifest"]).relative_to(R))
    generation.append(result)

# 5. Refresh 2026-W47 (now 34 + 2 + 1 = 37 daily papers, preserving 33 frozen backlog entries and null latency).
validate_weekly_picks(R, "2026-W47")
daily_w47 = daily_editions_for_week(R, "2026-W47")
public_w47 = list({x["id"]: deepcopy(x) for e in daily_w47 for x in e["items"]}.values())
assert len(public_w47) == 37, len(public_w47)
after_items = {x["id"]: x for x in load_items(R)}
directions = _directions(yaml.safe_load((R / "feed/taxonomy.yaml").read_text(encoding="utf-8")))
weekly = deepcopy(old_w47)
weekly["items"] = public_w47
weekly["counts"] = {k: sum(x["direction"]["primary"] == k for x in public_w47) for k in directions}
weekly["intro"] = _summary_intro("2026-W47", weekly["counts"], directions, public_w47)
weekly["updated_at"] = STAMP
weekly["daily_review_provenance"] = [e.get("review_provenance") for e in daily_w47 if e.get("review_provenance")]
weekly["metrics"] = _metrics(R, "2026-W47", list(after_items.values()), [after_items[x["id"]] for x in public_w47], STAMP)
weekly["metrics"]["latency_days"] = None
weekly["editor_note_zh"] = old_w47["editor_note_zh"].replace("含34篇", "含37篇") + " 11/26补抓信源另按真实来源日补入11/21两篇（HyperHarness、GroupBrief）与11/22一篇（DoppelVet）。"
weekly["editor_note_en"] = old_w47["editor_note_en"].replace("contain 34 papers", "contain 37 papers") + " On Nov 26, source reconciliation added two Nov 21 papers (HyperHarness, GroupBrief) and one Nov 22 paper (DoppelVet) under their true source dates."
assert weekly["backlog"] == old_w47["backlog"] and len(weekly["backlog"]) == 33 and weekly["published_at"] == old_w47["published_at"]
write_json(R / "site/weekly/2026-W47.json", weekly)
generation.append({"week": "2026-W47", "accepted": 37, "historical_previously_published": 33, "manifest": "site/weekly/2026-W47.json"})

metrics_path = R / "data/feed/metrics.json"
m = json.loads(metrics_path.read_text(encoding="utf-8"))
m["weeks"]["2026-W47"]["latency_days"] = None
if "2026-W48" in m["weeks"]:
    m["weeks"]["2026-W48"]["latency_days"] = None
write_json(metrics_path, m)

# 6. Render 2026-11-26--2026-11-26 historical recap for the 2 pre-window backlog approvals (HookEvo, ZhuLong-SE).
repo_papers = yaml.safe_load((R / "data/papers.yaml").read_text(encoding="utf-8"))["papers"]
backlog_new = approved_weekly_backlog(R, "2026-W48")
assert len(backlog_new) == 2 and {x["id"] for x in backlog_new} == {"arxiv:2611.27294", "arxiv:2611.26912"}, [x["id"] for x in backlog_new]
public_new = [{**_public_item(x, {"decision": "backlog"}, "2026-W48", repo_papers), "review_date": x["review"]["reviewed_on"], "window_status": "backlog"} for x in backlog_new]
recap_prov = verified[next(x["number"] for x in plan if x["date"] == "2026-11-26")][0]
recap = {
    "start": "2026-11-26",
    "end": "2026-11-26",
    "published_at": STAMP,
    "title_zh": "历史补录 · 11 月 26 日审核",
    "title_en": "Historical additions reviewed November 26",
    "reviewed_only": True,
    "items": public_new,
    "lab_updates": [],
    "picks": [],
    "sources": public_sources,
    "reviewed_on": "2026-11-26",
    "review_provenance": recap_prov,
    "intro": {
        "zh": "本次单列2篇较早来源窗口论文（HookEvo发表于11/20、ZhuLong-SE发表于11/19）；11/26是实际发现、三轮审核与补录日，不计入11/26当日新增论文。部分基准缺独立验证划分及单平台样本量等限制均明确保留。",
        "en": "Two earlier-window papers (HookEvo published Nov 20 and ZhuLong-SE published Nov 19) are listed separately. Nov 26 is the actual discovery, three-round review, and retrospective-publication date, not a same-day new-paper claim. Split and single-platform evaluation limits remain explicit.",
        "source": "source-bound-editorial-review",
    },
}
update_health(R, [], now=snapshot["generated_at"])
recap_res = render_recap(R, recap)
generation.append({k: (str(Path(v).relative_to(R)) if k in ("manifest", "html") else v) for k, v in recap_res.items()})
initialize_public(R)

# 7. Verify canonical & historical manifest preservation invariants.
after = {x["id"]: x for x in load_items(R)}
assert len(after) == len(before) == 2701
assert all(after[k]["first_seen"] == v["first_seen"] and source_hash(after[k]) == source_hash(v) for k, v in before.items())
for key in ("arxiv:2611.25534", "arxiv:2611.27689", "arxiv:2611.25476", "arxiv:2611.21056"):
    assert before[key].get("review") == after[key].get("review"), key
allowed_modified_manifests = {
    "site/daily/2026-11-21.json",
    "site/daily/2026-11-22.json",
    "site/daily/2026-11-23.json",
    "site/weekly/2026-W47.json",
}
for p_rel, sha in prior.items():
    if p_rel not in allowed_modified_manifests:
        assert digest((R / p_rel).read_bytes()) == sha, p_rel
for d_short, d_full in (("21", "2026-11-21"), ("22", "2026-11-22"), ("23", "2026-11-23")):
    assert json.loads((R / f"site/daily/{d_full}.json").read_text(encoding="utf-8"))["published_at"] == json.loads((OUT / f"prior-nov{d_short}-observed-status.json").read_text(encoding="utf-8"))["published_at"]
assert not (R / "site/daily/2026-10-27.json").exists()

write_json(OUT / "generation-receipt.json", {
    "generated_at": STAMP,
    "generation": generation,
    "canonical_count": len(after),
    "first_seen_and_scientific_source_hashes_unchanged_during_apply": True,
    "old_hf_scientific_reviews_preserved": True,
    "prior_nov21_22_23_statuses_archived": True,
    "paid_generation_requests": 0,
    "paid_generation_tokens": 0,
    "quality_warning": {"recall": 0.892857, "threshold": 0.90, "complete": False},
    "online_verified": False,
    "boundary": "Local generation from verified merged reviews. Publication PR, Pages deployment, and public byte verification still required.",
})
print(json.dumps(generation, ensure_ascii=False), flush=True)
