"""Validate source metadata and put it in the feed's common representation."""
from datetime import datetime, timezone
import re
import unicodedata
from urllib.parse import urlparse

ARXIV_RE = re.compile(r'(?<![\w.])(?P<id>\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v(?P<version>\d+))?(?![\w.])', re.I)
URL_RE = re.compile(r'https?://[^\s<>"\]]+')


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def split_arxiv(value):
    match = ARXIV_RE.search(str(value or ''))
    if not match:
        return None, 0
    return match.group('id'), int(match.group('version') or 1)


def arxiv_ids(text):
    return list(dict.fromkeys(match.group('id') for match in ARXIV_RE.finditer(text)))


def compact(value):
    return ' '.join(str(value or '').split())


def code_links(text):
    links = []
    for url in URL_RE.findall(text):
        url = url.rstrip('.,;:)')
        if urlparse(url).hostname in {'github.com', 'gitlab.com', 'codeberg.org', 'bitbucket.org'}:
            links.append(url)
    return sorted(set(links))


def title_tokens(title):
    title = unicodedata.normalize('NFKC', title).casefold()
    return set(re.findall(r'\w+', title))


def normalize_record(raw, now=None):
    item = dict(raw)
    item['kind'] = raw.get('kind', 'paper')
    if item['kind'] not in {'paper', 'post', 'release'}:
        raise ValueError(f"Unsupported source item kind: {item['kind']}")
    item['title'] = compact(raw.get('title'))
    if not item['title']:
        raise ValueError('Source metadata has no title')
    item['links'] = dict(raw.get('links', {}))
    arxiv_id, inferred_version = split_arxiv(raw.get('arxiv_id') or item['links'].get('arxiv'))
    item['arxiv_id'] = arxiv_id
    item['version'] = int(raw.get('version') or inferred_version)
    if arxiv_id:
        item['kind'] = 'paper'
        item['id'] = f'arxiv:{arxiv_id}'
        item['links']['arxiv'] = f'https://arxiv.org/abs/{arxiv_id}'
    else:
        link = item['links'].get('url') or item['links'].get('s2')
        item['id'] = raw.get('id') or (f"{item['kind']}:{link}" if link else None)
        if not item['id']:
            raise ValueError('Non-arXiv source metadata needs an id or a source URL')
    item['authors'] = [compact(author) for author in raw.get('authors', [])]
    item['abstract'] = compact(raw.get('abstract'))
    item['comments'] = compact(raw.get('comments'))
    for field in ('categories', 'source_hits', 'seed_hits', 'aliases'):
        item[field] = sorted(set(raw.get(field, [])))
    item['code_links'] = sorted(set(raw.get('code_links', [])) | set(code_links(item['abstract'] + ' ' + item['comments'])))
    if item['code_links']:
        item['links']['code'] = item['code_links'][0]
    item['hf_upvotes'] = int(raw.get('hf_upvotes') or 0)
    item['in_repo'] = bool(raw.get('in_repo', False))
    item['author_tracked'] = bool(raw.get('author_tracked', False))
    item['first_seen'] = raw.get('first_seen') or now or utc_now()
    item['published'] = str(raw.get('published') or '')
    item['updated'] = str(raw.get('updated') or item['published'])
    item['retracted'] = bool(raw.get('retracted') or re.search(r'\b(?:withdrawn|retracted)\b', item['comments'], re.I)
                             or re.search(r'\bthis (?:paper|submission|manuscript) (?:has been|is|was) (?:withdrawn|retracted)\b', item['abstract'], re.I))
    return item


def normalize_records(records, now=None):
    return [normalize_record(record, now=now) for record in records]
