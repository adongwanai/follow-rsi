"""Semantic Scholar discovery with keyed or conservatively paced anonymous access."""
from collections import Counter
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import time
import requests
from scripts.common import read_yaml
from .normalize import normalize_record
from .storage import load_state, save_state

BASE = 'https://api.semanticscholar.org/graph/v1'
FIELDS = 'paperId,title,abstract,authors,externalIds,publicationDate,url,fieldsOfStudy'
REQUEST_INTERVALS = {'authenticated': 1.1, 'anonymous': 3.1}
MAX_RATE_LIMIT_RETRIES = 5
_last_request = None


def seed_papers(papers):
    extra = {'hyperagents', 'meta-harness', 'hgm', 'ace'}
    return [paper for paper in papers if paper.get('arxiv') and
            (paper.get('must_read') or paper['section'] == 'foundations' or paper['id'] in extra)]


def select_authors(seed_metadata, limit=150):
    """Last-listed author is a tracking heuristic, not verified correspondence."""
    authors, counts, last = {}, Counter(), set()
    for paper in seed_metadata:
        for author in paper.get('authors', []):
            if author.get('authorId'):
                authors[author['authorId']] = author
                counts[author['authorId']] += 1
        if paper.get('authors') and paper['authors'][-1].get('authorId'):
            last.add(paper['authors'][-1]['authorId'])
    eligible = [ident for ident, count in counts.items() if count >= 2 or ident in last]
    eligible.sort(key=lambda ident: (-counts[ident], authors[ident]['name'], ident))
    return [{**authors[ident], 'seed_appearances': counts[ident], 'last_author_heuristic': ident in last}
            for ident in eligible[:limit]]


def request(path, params=None, session=None):
    global _last_request
    key = os.environ.get('S2_API_KEY')
    interval = REQUEST_INTERVALS['authenticated' if key else 'anonymous']
    headers = {'User-Agent': 'FollowRSI/0.1'}
    if key:
        headers['x-api-key'] = key
    for attempt in range(MAX_RATE_LIMIT_RETRIES + 1):
        if _last_request is not None:
            delay = _last_request + interval - time.monotonic()
            if delay > 0:
                time.sleep(delay)
        _last_request = time.monotonic()
        response = (session or requests).get(BASE + '/' + path, params=params,
                                            headers=headers, timeout=30)
        if response.status_code != 429 or attempt == MAX_RATE_LIMIT_RETRIES:
            response.raise_for_status()
            return response.json()
        time.sleep(interval * 2 ** attempt)


def parse_json(payload, source_id='s2-citations', seed_id=None, author_tracked=False, now=None):
    rows = payload.get('data', []) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError('S2 data must be a JSON list')
    records = []
    for row in rows:
        paper = row.get('citingPaper', row)
        if not paper.get('title'):
            raise ValueError('S2 metadata missing title')
        external = paper.get('externalIds') or {}
        aid = external.get('ArXiv')
        record = {'id': f"s2:{paper['paperId']}", 'arxiv_id': aid,
                  'title': paper['title'], 'abstract': paper.get('abstract') or '',
                  'authors': [a['name'] for a in paper.get('authors', [])],
                  'categories': paper.get('fieldsOfStudy') or [], 'published': paper.get('publicationDate') or '',
                  'links': {'s2': paper.get('url') or f"https://www.semanticscholar.org/paper/{paper['paperId']}"},
                  'source_hits': [source_id], 'seed_hits': [seed_id] if seed_id else [],
                  'author_tracked': author_tracked, 'metadata_pending': bool(aid and not paper.get('abstract'))}
        records.append(normalize_record(record, now=now))
    return records


def pages(path, params, session=None):
    result, offset = [], 0
    while True:
        payload = request(path, {**params, 'offset': offset, 'limit': 100}, session)
        result.append(payload)
        if 'next' not in payload:
            return result
        offset = payload['next']


def fetch(source, root, now=None, session=None):
    current = now or datetime.now(timezone.utc)
    mode = 'authenticated' if os.environ.get('S2_API_KEY') else 'anonymous'
    state = load_state(root)
    source_state = state['sources'].setdefault(source['id'], {
        'consecutive_failures': 0, 'consecutive_errors': 0, 'seen_ids': [], 'weekly': {}})
    source_state.update(auth_mode=mode, min_interval_seconds=REQUEST_INTERVALS[mode])
    # Persist before the network request so failures and exhausted 429s retain the mode.
    save_state(root, state)
    cutoff = (current - timedelta(days=30)).date().isoformat()
    seeds = seed_papers(read_yaml(Path(root) / 'data' / 'papers.yaml')['papers'])
    records, raw = [], {'format': 's2-json', 'auth_mode': mode, 'pages': {}, 'seed_metadata': []}
    if source['kind'] == 's2_citations':
        for seed in seeds:
            payloads = pages(f"paper/arXiv:{seed['arxiv']}/citations", {'fields': FIELDS}, session)
            raw['pages'][seed['id']] = payloads
            for payload in payloads:
                records.extend(parse_json(payload, source['id'], seed['id'], now=current.isoformat()))
    else:
        for seed in seeds:
            raw['seed_metadata'].append(request(f"paper/arXiv:{seed['arxiv']}", {'fields': 'authors'}, session))
        authors = select_authors(raw['seed_metadata'])
        raw['tracked_authors'] = authors
        for author in authors:
            payloads = pages(f"author/{author['authorId']}/papers", {'fields': FIELDS}, session)
            raw['pages'][author['authorId']] = payloads
            for payload in payloads:
                records.extend(parse_json(payload, source['id'], author_tracked=True, now=current.isoformat()))
    # S2 exposes publicationDate, not the date a citation was added. The raw
    # response retains undated records for diagnosis; no date is invented.
    return [item for item in records if item['published'] and item['published'] >= cutoff], raw
