"""Metadata-only arXiv requests and the source registry dispatcher."""
from datetime import datetime, timedelta, timezone
import time
import xml.etree.ElementTree as ET
from pathlib import Path
import requests
from scripts.common import read_yaml
from .normalize import normalize_record, normalize_records, split_arxiv
from .storage import load_state, save_raw

API = 'https://export.arxiv.org/api/query'
USER_AGENT = 'FollowRSI/0.1 (open-source RSI metadata tracker; no PDF retrieval)'
CATEGORIES = ('cs.AI', 'cs.CL', 'cs.LG', 'cs.MA', 'cs.SE', 'cs.RO', 'cs.NE')
_last_request = 0.0
NS = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom',
      'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'}


def request(params, session=None):
    global _last_request
    remaining = 3.0 - (time.monotonic() - _last_request)
    if remaining > 0:
        time.sleep(remaining)
    _last_request = time.monotonic()
    response = (session or requests).get(API, params=params, headers={'User-Agent': USER_AGENT}, timeout=45)
    response.raise_for_status()
    return response.text


def parse_atom(text, source_id='arxiv', now=None):
    root = ET.fromstring(text)
    if root.tag != '{http://www.w3.org/2005/Atom}feed':
        raise ValueError('arXiv endpoint did not return an Atom feed')
    records = []
    for entry in root.findall('a:entry', NS):
        ident = entry.findtext('a:id', '', NS)
        arxiv_id, version = split_arxiv(ident)
        if not arxiv_id:
            raise ValueError(f'arXiv API returned an invalid/error entry: {entry.findtext("a:summary", "", NS)}')
        record = {
            'arxiv_id': arxiv_id, 'version': version,
            'title': entry.findtext('a:title', '', NS),
            'abstract': entry.findtext('a:summary', '', NS),
            'authors': [a.findtext('a:name', '', NS) for a in entry.findall('a:author', NS)],
            'comments': entry.findtext('arxiv:comment', '', NS),
            'published': entry.findtext('a:published', '', NS),
            'updated': entry.findtext('a:updated', '', NS),
            'published_source': 'arxiv',
            'categories': [c.get('term') for c in entry.findall('a:category', NS)],
            'links': {'arxiv': f'https://arxiv.org/abs/{arxiv_id}'}, 'source_hits': [source_id],
        }
        records.append(normalize_record(record, now=now))
    return records


def fetch_ids(ids, session=None, now=None):
    """Fetch up to 100 ids per metadata request, keeping the global 3-second limit."""
    records = []
    ids = list(dict.fromkeys(ids))
    for start in range(0, len(ids), 100):
        body = request({'id_list': ','.join(ids[start:start + 100]), 'max_results': 100}, session)
        records.extend(parse_atom(body, source_id='arxiv-version-check', now=now))
    return records


def fetch(source, days=3, now=None, session=None):
    current = now or datetime.now(timezone.utc)
    if isinstance(current, str):
        current = datetime.fromisoformat(current.replace('Z', '+00:00'))
    cutoff = current - timedelta(days=days - 1)
    date_range = f'submittedDate:[{cutoff:%Y%m%d0000} TO {current:%Y%m%d2359}]'
    query = f'({source["params"]["query"]}) AND {date_range}'
    records, pages = [], []
    start = 0
    while True:
        body = request({'search_query': query, 'sortBy': 'submittedDate', 'sortOrder': 'descending',
                        'start': start, 'max_results': 100}, session)
        page = parse_atom(body, source_id=source['id'], now=current.isoformat())
        pages.append(body)
        records.extend(page)
        total = int(ET.fromstring(body).findtext('opensearch:totalResults', str(len(page)), NS))
        start += len(page)
        if not page or start >= total:
            break
    return records, {'format': 'atom-pages', 'query': query, 'pages': pages}


def fallback_rss(source, now=None, session=None):
    from .fetch_rss import parse_feed
    records, bodies = [], []
    keywords = source['params']['fallback_keywords']
    for category in CATEGORIES:
        # RSS requests use the same conservative arXiv pacing.
        global _last_request
        delay = 3.0 - (time.monotonic() - _last_request)
        if delay > 0:
            time.sleep(delay)
        _last_request = time.monotonic()
        response = (session or requests).get(f'https://rss.arxiv.org/rss/{category}',
                                            headers={'User-Agent': USER_AGENT}, timeout=45)
        response.raise_for_status()
        bodies.append(response.text)
        for item in parse_feed(response.text, source['id'], now=now):
            if any(keyword.casefold() in (item['title'] + ' ' + item['abstract']).casefold() for keyword in keywords):
                item['degraded_source'] = True
                records.append(item)
    return records, {'format': 'arxiv-category-rss', 'pages': bodies}


def fetch_sources(root, schedule='daily', days=3, now=None, source_ids=None, issue_client=None):
    """Fetch enabled registry sources; report failures explicitly without losing other sources."""
    from . import fetch_s2, fetch_hf, fetch_rss, fetch_github
    current = now or datetime.now(timezone.utc)
    if isinstance(current, str):
        current = datetime.fromisoformat(current.replace('Z', '+00:00'))
    registry = read_yaml(Path(root) / 'feed' / 'sources.yaml')
    state = load_state(root)
    records, outcomes, paths = [], [], []
    for source in registry['sources']:
        if not source['enabled'] or (schedule != 'all' and source['schedule'] != schedule) or (source_ids is not None and source['id'] not in source_ids):
            continue
        degraded = False
        try:
            kind = source['kind']
            if kind == 'arxiv_query':
                try:
                    found, raw = fetch(source, days=days, now=current)
                except (requests.RequestException, ET.ParseError, ValueError) as error:
                    failures = state['sources'].get(source['id'], {}).get('consecutive_errors', 0)
                    if failures < 2:
                        raise
                    found, raw = fallback_rss(source, now=current.isoformat())
                    raw['api_error'] = str(error)
                    degraded = True
            elif kind in {'s2_citations', 's2_authors'}:
                found, raw = fetch_s2.fetch(source, root, now=current)
            elif kind == 'hf_daily':
                found, raw = fetch_hf.fetch(source, now=current, days=days)
            elif kind == 'rss':
                found, raw = fetch_rss.fetch(source, now=current)
            elif kind == 'github_releases':
                found, raw = fetch_github.fetch(source, root, now=current)
            else:
                raise ValueError(f'Unknown source kind: {kind}')
            path = save_raw(root, source['id'], current.date().isoformat(), raw)
            records.extend(normalize_records(found, now=current.isoformat()))
            paths.append(path.relative_to(Path(root)).as_posix())
            outcomes.append({'source_id': source['id'], 'ok': not raw.get('errors'), 'count': len(found),
                             'ids': [item['id'] for item in found], 'degraded': degraded,
                             'error': raw.get('api_error') if degraded else (str(raw['errors']) if raw.get('errors') else None)})
        except (requests.RequestException, ET.ParseError, ValueError, KeyError) as error:
            outcomes.append({'source_id': source['id'], 'ok': False, 'count': 0,
                             'error': f'{type(error).__name__}: {error}', 'degraded': False})
    pending = sorted({item['arxiv_id'] for item in records if item.get('metadata_pending') and item.get('arxiv_id')})
    if pending:
        try:
            hydrated = {item['arxiv_id']: item for item in fetch_ids(pending, now=current.isoformat())}
            save_raw(root, 'arxiv-hydration', current.date().isoformat(), {'format': 'metadata', 'records': list(hydrated.values())})
            if set(hydrated) != set(pending):
                raise ValueError(f'arXiv hydration identity mismatch: requested {pending}, returned {sorted(hydrated)}')
            hf_pending = {item['arxiv_id'] for item in records
                          if item.get('metadata_pending') and 'hf_reported_published' in item}
            missing_dates = sorted(ident for ident in hf_pending
                                   if not hydrated[ident]['published'] or not hydrated[ident]['updated'])
            if missing_dates:
                raise ValueError(f'arXiv publication dates missing for {missing_dates}')
            for index, item in enumerate(records):
                if item.get('metadata_pending') and item['arxiv_id'] in hydrated:
                    paper = hydrated[item['arxiv_id']]
                    metadata = ({key: paper[key] for key in ('published', 'updated', 'version',
                                'announced', 'announced_source', 'published_source', 'comments')}
                                if 'hf_reported_published' in item else paper)
                    records[index] = {**item, **metadata, 'metadata_pending': False,
                                      'retracted': item['retracted'] or paper['retracted'],
                                      'source_hits': item['source_hits'], 'seed_hits': item['seed_hits'],
                                      'links': {**item['links'], **paper['links']}}
                    records[index].pop('metadata_error', None)
            outcomes.append({'source_id': 'arxiv-hydration', 'ok': True, 'count': len(hydrated),
                             'ids': [paper['id'] for paper in hydrated.values()], 'degraded': False, 'error': None})
        except (requests.RequestException, ET.ParseError, ValueError) as error:
            message = f'{type(error).__name__}: {error}'
            for item in records:
                if item.get('metadata_pending'):
                    item['metadata_error'] = message
            outcomes.append({'source_id': 'arxiv-hydration', 'ok': False, 'count': 0,
                             'error': message, 'degraded': False})
    from .health import update_health
    update_health(root, outcomes, now=current, issue_client=issue_client)
    return {'records': records, 'outcomes': outcomes, 'raw_paths': paths}
