"""RSS/Atom discovery with separate post identities and cited-paper provenance."""
from datetime import datetime, timedelta, timezone
from html import unescape
import re
import calendar
from urllib.parse import urljoin, urlsplit
import feedparser
import requests
from .normalize import arxiv_ids, normalize_record


def plain_text(html):
    return unescape(re.sub(r'<[^>]+>', ' ', html))


def parse_feed(text, source_id, now=None, feed_url=None):
    feed = feedparser.parse(text)
    if not feed.version:
        raise ValueError('RSS endpoint returned neither valid RSS nor Atom')
    records = []
    for entry in feed.entries:
        link = entry.get('link') or entry.get('id', '')
        if not link or not entry.get('title'):
            raise ValueError('RSS entry requires a title and URL')
        link = urljoin(feed_url or '', link)
        parsed_link = urlsplit(link)
        if parsed_link.scheme not in ('http', 'https') or not parsed_link.hostname:
            raise ValueError('RSS entry requires an absolute HTTP(S) URL')
        content = ' '.join(c.get('value', '') for c in entry.get('content', [])) or entry.get('summary', '')
        parsed = entry.get('published_parsed') or entry.get('updated_parsed')
        published = datetime.fromtimestamp(calendar.timegm(parsed), timezone.utc).isoformat() if parsed else ''
        direct_ids = (arxiv_ids(parsed_link.path)
                      if parsed_link.hostname in {'arxiv.org', 'www.arxiv.org', 'export.arxiv.org'} else [])
        if direct_ids:
            # The entry itself is a paper; citations in its body are not its identity.
            aid = direct_ids[0]
            records.append(normalize_record({'arxiv_id': aid, 'title': entry['title'],
                'abstract': plain_text(content), 'published': published, 'metadata_pending': False,
                'links': {'arxiv': f'https://arxiv.org/abs/{aid}'}, 'source_hits': [source_id]}, now=now))
            continue
        ids = arxiv_ids(content)
        post = normalize_record({'kind': 'post', 'title': entry['title'],
            'abstract': plain_text(content), 'published': published,
            'links': {'url': link}, 'source_hits': [source_id], 'referenced_arxiv_ids': ids}, now=now)
        records.append(post)
        for aid in ids:
            # References are discovery evidence, not a claim that this post
            # describes the linked paper. Official metadata supplies its title.
            records.append(normalize_record({'arxiv_id': aid, 'title': f'arXiv {aid}', 'abstract': '',
                'links': {'arxiv': f'https://arxiv.org/abs/{aid}'}, 'source_hits': [source_id],
                'metadata_pending': True, 'source_published': published,
                'discovery_referrers': {link: {'relation': 'cited_by_post', 'source_id': source_id,
                    'title': entry['title'], 'published': published, 'observed_at': post['first_seen']}}}, now=now))
    return records


def fetch(source, now=None, session=None):
    from .fetch_arxiv import USER_AGENT
    current = now or datetime.now(timezone.utc)
    response = (session or requests).get(source['params']['url'], headers={'User-Agent': USER_AGENT}, timeout=30)
    response.raise_for_status()
    # Let the XML declaration determine encoding; Requests may default to Latin-1.
    body = response.content
    items = parse_feed(body, source['id'], current.isoformat(), feed_url=response.url)
    cutoff = (current - timedelta(days=source['params'].get('lookback_days', 14) - 1)).date().isoformat()
    # Undated linked papers are retained for metadata hydration rather than discarded.
    items = [item for item in items if not (item.get('source_published') or item['published'])
             or (item.get('source_published') or item['published'])[:10] >= cutoff]
    encoding = feedparser.parse(body).encoding
    return items, {'format': 'rss', 'body': body.decode(encoding), 'encoding': encoding}
