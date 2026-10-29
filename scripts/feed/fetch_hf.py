"""Hugging Face Daily Papers metadata, with explicit keyword prefiltering."""
from datetime import datetime, timedelta, timezone
import requests
from .normalize import normalize_record


def parse_json(payload, source_id='hf-daily', keywords=(), now=None, daily_date=None):
    if not isinstance(payload, list):
        raise ValueError('HF daily endpoint must return a JSON list')
    items = []
    for row in payload:
        paper = row['paper']
        title, abstract = row.get('title') or paper['title'], paper.get('summary', '')
        if keywords and not any(k.casefold() in (title + ' ' + abstract).casefold() for k in keywords):
            continue
        ident = paper['id']
        items.append(normalize_record({
            'arxiv_id': ident, 'title': title, 'abstract': abstract,
            'authors': [a['name'] for a in paper.get('authors', [])],
            # HF may report the current arXiv version date here, not v1.
            'hf_reported_published': paper.get('publishedAt') or row.get('publishedAt', ''),
            'metadata_pending': True,
            'links': {'arxiv': f'https://arxiv.org/abs/{ident}', 'hf': f'https://huggingface.co/papers/{ident}'},
            'source_hits': [source_id], 'hf_upvotes': paper.get('upvotes', row.get('upvotes', 0)),
            'code_links': [paper['githubRepo']] if paper.get('githubRepo') else [],
            'hf_submitted_at': paper.get('submittedOnDailyAt') or row.get('publishedAt', ''),
            # Membership in a queried daily list is distinct from submission,
            # paper publication, and the time this tracker first fetched it.
            'hf_daily_dates': [daily_date] if daily_date else [],
        }, now=now))
    return items


def fetch(source, now=None, session=None, days=3):
    from .fetch_arxiv import USER_AGENT
    current = now or datetime.now(timezone.utc)
    records, payloads = [], {}
    for offset in range(days):
        date = (current - timedelta(days=offset)).date().isoformat()
        response = (session or requests).get(source['params']['url'], params={'date': date},
                                            headers={'User-Agent': USER_AGENT}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        payloads[date] = payload
        records.extend(parse_json(payload, source['id'], source['params'].get('keywords', []),
                                  current.isoformat(), daily_date=date))
    return records, {'format': 'hf-json-days', 'days': payloads}
