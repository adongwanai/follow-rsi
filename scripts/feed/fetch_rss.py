"""RSS/Atom discovery. Posts with arXiv links contribute source hits to papers."""
from datetime import datetime, timedelta, timezone
from html import unescape
import re
import calendar
import feedparser
import requests
from .normalize import arxiv_ids, normalize_record


def plain_text(html):
    return unescape(re.sub(r'<[^>]+>', ' ', html))


def parse_feed(text, source_id, now=None):
    feed = feedparser.parse(text)
    if not feed.version:
        raise ValueError('RSS endpoint returned neither valid RSS nor Atom')
    records = []
    for entry in feed.entries:
        link = entry.get('link', '')
        if not link or not entry.get('title'):
            raise ValueError('RSS entry requires a title and URL')
        content = ' '.join([entry.get('summary', ''), *[c.get('value', '') for c in entry.get('content', [])]])
        parsed = entry.get('published_parsed') or entry.get('updated_parsed')
        published = datetime.fromtimestamp(calendar.timegm(parsed), timezone.utc).isoformat() if parsed else ''
        ids = arxiv_ids(link + ' ' + content)
        if ids:
            # A blog's prose is not a paper abstract. Hydration by the metadata
            # stage is required before automatic judgement.
            for aid in ids:
                record = {'arxiv_id': aid, 'title': entry['title'], 'abstract': '',
                          'links': {'arxiv': f'https://arxiv.org/abs/{aid}', 'post': link},
                          'source_hits': [source_id], 'metadata_pending': True, 'source_published': published}
                if 'arxiv.org' in link:
                    record.update(abstract=plain_text(content), published=published, metadata_pending=False)
                records.append(normalize_record(record, now=now))
        else:
            records.append(normalize_record({'kind': 'post', 'title': entry['title'],
                                            'abstract': plain_text(content), 'published': published,
                                            'links': {'url': link}, 'source_hits': [source_id]}, now=now))
    return records


def fetch(source, now=None, session=None):
    from .fetch_arxiv import USER_AGENT
    current = now or datetime.now(timezone.utc)
    response = (session or requests).get(source['params']['url'], headers={'User-Agent': USER_AGENT}, timeout=30)
    response.raise_for_status()
    items = parse_feed(response.text, source['id'], current.isoformat())
    cutoff = (current - timedelta(days=source['params'].get('lookback_days', 14) - 1)).date().isoformat()
    # Undated linked papers are retained for metadata hydration rather than discarded.
    items = [item for item in items if not (item.get('source_published') or item['published'])
             or (item.get('source_published') or item['published'])[:10] >= cutoff]
    return items, {'format': 'rss', 'body': response.text}
