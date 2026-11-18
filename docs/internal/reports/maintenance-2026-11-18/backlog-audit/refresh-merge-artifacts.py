"""Fetch the exact merged inputs omitted by the first free refresh."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[5]
REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/backlog-audit'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit/merged-inputs-v1'
RAW.mkdir(parents=True, exist_ok=True)
MANIFEST = REPORT / 'merged-inputs-v1.json'
assert not MANIFEST.exists(), 'Preserve the existing receipt.'
requests_log = []
for number, filename in [
    (117, 'data/feed/raw/arxiv-version-check/2026-11-16.json'),
    (117, 'review/2026-W46.misses.yaml'),
    (134, 'review/backlog/2026-11-16.yaml'),
]:
    pr = json.loads((ROOT / f'data/feed/raw/maintenance-2026-11-18/backlog-audit/remote-refresh-v1/pr-{number}.json').read_text())
    assert pr['merged'] and pr['merged_by']['login'] == 'adongwanai'
    assert pr['base']['repo']['full_name'] == 'adongwanai/follow-rsi'
    target = RAW / f'pr-{number}--{filename.replace("/", "--")}'
    url = f'https://raw.githubusercontent.com/adongwanai/follow-rsi/{pr["merge_commit_sha"]}/{filename}'
    receipt = {'url': url, 'requested_at': datetime.now(timezone.utc).isoformat()}
    response = requests.get(url, timeout=40)
    target.write_bytes(response.content)
    receipt.update(http_status=response.status_code, finished_at=datetime.now(timezone.utc).isoformat(), body_path=str(target.relative_to(ROOT)), sha256=hashlib.sha256(response.content).hexdigest(), bytes=len(response.content), github_pr=number, merge_commit=pr['merge_commit_sha'], head_sha=pr['head']['sha'], owner_login=pr['merged_by']['login'])
    requests_log.append(receipt)
    MANIFEST.write_text(json.dumps({'requests': requests_log, 'paid_requests': 0, 'github_writes': 0}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)
    response.raise_for_status()
