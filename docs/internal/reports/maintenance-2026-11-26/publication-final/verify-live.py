"""Live byte-exact HTTP verification across all published Nov 21–26 daily editions, W47, recap, feeds, homepage, and READMEs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

R = Path.cwd()
D = R / "docs/internal/reports/maintenance-2026-11-26/publication-final"
B = R / "build/maintenance-2026-11-26"
BASE = "https://adongwanai.github.io/follow-rsi/"

paths = [f"daily/2026-11-{day}.{suffix}" for day in ("21", "22", "23", "24", "25", "26") for suffix in ("json", "html")]
paths += [
    "daily/index.html",
    "weekly/2026-W47.json",
    "weekly/2026-W47.html",
    "weekly/index.html",
    "recaps/2026-11-26--2026-11-26.json",
    "recaps/2026-11-26--2026-11-26.html",
    "feed/latest.json",
    "feed/atom.xml",
    "feed/status.json",
    "index.html",
    "data.js",
    "papers.json",
    "daily/2026-10-27.html",
    "daily/2026-11-18.json",
    "daily/2026-11-19.json",
    "daily/2026-11-20.json",
    "weekly/2026-W46.json",
    "recaps/2026-11-23--2026-11-23.json",
    "recaps/2026-11-16--2026-11-18.json",
]
paths = list(dict.fromkeys(paths))
targets = [(BASE + p, R / "site" / p) for p in paths]
targets += [(BASE + p, R / "site" / local) for p, local in [("", "index.html"), ("daily/", "daily/index.html"), ("weekly/", "weekly/index.html")]]
targets += [("https://raw.githubusercontent.com/adongwanai/follow-rsi/main/" + p, R / p) for p in ("README.md", "README_en.md")]
assert all(p.is_file() for _, p in targets)
sha = lambda b: hashlib.sha256(b).hexdigest()


def fetch_one(target):
    url, p = target
    r = {
        "url": url,
        "local_path": str(p.relative_to(R)),
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "expected_sha256": sha(p.read_bytes()),
    }
    sep = "&" if "?" in url else "?"
    bust_url = f"{url}{sep}_cb={int(time.time() * 1000)}"
    try:
        req = urllib.request.Request(bust_url, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
        with urllib.request.urlopen(req, timeout=35) as response:
            b = response.read()
            r.update(http_status=response.status, final_url=response.url, bytes=len(b), sha256=sha(b))
    except (urllib.error.URLError, TimeoutError) as e:
        r.update(error_type=type(e).__name__, error=str(e), bytes_match=False)
        return r, None
    r["bytes_match"] = r["sha256"] == r["expected_sha256"]
    return r, b


receipts, bodies = [], {}
for attempt in range(18):
    with ThreadPoolExecutor(max_workers=6) as pool:
        fetched = list(pool.map(fetch_one, targets))
    receipts = [r for r, _ in fetched]
    bodies = {r["local_path"]: b for r, b in fetched if b is not None}
    mismatched = [r["url"] for r in receipts if not r["bytes_match"]]
    if not mismatched:
        break
    print(f"[verify-live attempt {attempt + 1}] waiting on {len(mismatched)} CDN URLs...", flush=True)
    time.sleep(10)

checks = {"all_public_bytes_match": all(r["bytes_match"] for r in receipts)}
if checks["all_public_bytes_match"]:
    feed = json.loads(bodies["site/feed/latest.json"])
    days = {r["date"]: r for r in feed["daily_editions"]}
    wanted = {f"2026-11-{d}": n for d, n in [("21", 2), ("22", 1), ("23", 5), ("24", 10), ("25", 5), ("26", 2)]}
    checks["all_six_daily_counts_and_review_dates"] = all(days[d]["paper_count"] == n and days[d]["reviewed_on"] == "2026-11-26" for d, n in wanted.items())
    checks["all_six_paper_editions"] = all(len(json.loads(bodies[f"site/daily/{d}.json"])["items"]) == n and json.loads(bodies[f"site/daily/{d}.json"]).get("kind") != "daily_status" for d, n in wanted.items())
    checks["prior_nov21_22_23_timestamps_preserved"] = all(
        json.loads(bodies[f"site/daily/2026-11-{d}.json"])["published_at"] == json.loads((D / f"prior-nov{d}-observed-status.json").read_text(encoding="utf-8"))["published_at"]
        for d in ("21", "22", "23")
    )
    recap = json.loads(bodies["site/recaps/2026-11-26--2026-11-26.json"])
    checks["two_historical_additions"] = recap["kind"] == "retrospective" and len(recap["items"]) == 2 and all(r["news_date"] <= "2026-11-20" and r["review_date"] == "2026-11-26" for r in recap["items"])
    w = json.loads(bodies["site/weekly/2026-W47.json"])
    checks["w47_37_daily_33_prior_historical"] = len(w["items"]) == 37 and len(w["backlog"]) == 33 and not ({r["id"] for r in w["items"]} & {r["id"] for r in w["backlog"]})
    status = json.loads(bodies["site/feed/status.json"])
    checks["status_is_current_12_source_snapshot"] = status["checked_at"].startswith("2026-11-26") and sum(r["enabled"] for r in status["sources"].values()) == 12 and status["sources"]["hf-daily"]["today_board_count"] == 46
    checks["s2_partial_and_failure_retained"] = status["sources"]["s2-citations"]["availability"] == "partial" and not status["sources"]["s2-authors"]["last_ok"]
    ns = {"a": "http://www.w3.org/2005/Atom"}
    atom = ET.fromstring(bodies["site/feed/atom.xml"])
    entries = {e.findtext("a:id", namespaces=ns): e for e in atom.findall("a:entry", ns)}
    checks["atom_has_all_six_dates_and_recap"] = all("urn:follow-rsi:daily:" + d in entries for d in wanted) and "urn:follow-rsi:recap:2026-11-26--2026-11-26" in entries
    checks["readmes_link_latest"] = all("daily/2026-11-26.html" in bodies[p].decode("utf-8") and "2026-W47" in bodies[p].decode("utf-8") for p in ("README.md", "README_en.md"))
    checks["withdrawal_preserved"] = "已撤下" in bodies["site/daily/2026-10-27.html"].decode("utf-8") and "2026-10-27" not in feed["dates"] and not (R / "site/daily/2026-10-27.json").exists()
    home = json.loads(bodies["site/data.js"].decode("utf-8").removeprefix("window.HARNESS_DATA = ").rstrip().removesuffix(";"))
    checks["homepage_latest_nov26"] = home["latest_edition"]["date"] == "2026-11-26" and len(home["latest_edition"]["items"]) == 2
    by = {r["id"]: r for r in json.loads((R / "docs/internal/reports/maintenance-2026-11-26/primary-review/final-adjudication.json").read_text(encoding="utf-8"))["items"]}
    pub = [x for d in wanted for x in json.loads(bodies[f"site/daily/{d}.json"])["items"]] + recap["items"]
    checks["all_27_summaries_match_adjudication"] = len(pub) == 27 and all(
        x["summary_zh"] == by[x["id"]]["summary_override"]["summary_zh"] and x["summary_en"] == by[x["id"]]["summary_override"]["summary_en"]
        for x in pub
    )

result = {
    "observed_at": datetime.now(timezone.utc).isoformat(),
    "local_git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip(),
    "requests": receipts,
    "checks": checks,
    "online_verified": all(checks.values()),
    "paid_generation_requests": 0,
    "scope": "Live byte and publication-content verification; not experimental replication.",
}
name = "live-verification-" + datetime.now(timezone.utc).strftime("%H%M%S") + ".json"
(B / name).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "online_verified": result["online_verified"],
    "checked_urls": len(receipts),
    "failed_checks": [k for k, v in checks.items() if not v],
    "mismatched_urls": [r["url"] for r in receipts if not r["bytes_match"]],
    "receipt": str(B / name),
}, ensure_ascii=False), flush=True)
assert result["online_verified"], "Inspect actual receipts before claiming online publication."
(B / "live-verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
