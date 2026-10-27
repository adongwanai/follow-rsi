"""GitHub release versions and links; no inferred release summaries."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse
import os
import requests
from scripts.common import read_yaml
from .normalize import normalize_record


def repositories(papers):
    repos = set()
    for paper in papers:
        url = urlparse(paper.get('code', ''))
        parts = url.path.strip('/').split('/')
        if url.hostname == 'github.com' and len(parts) >= 2:
            repos.add('/'.join(parts[:2]).removesuffix('.git'))
    return sorted(repos)


def parse_json(payload, repository, source_id='github-releases', now=None):
    if not isinstance(payload, list):
        raise ValueError('GitHub releases endpoint must return a JSON list')
    records = []
    for row in payload:
        if row['draft']:
            continue
        records.append(normalize_record({'kind': 'release', 'title': f"{repository} {row['tag_name']}",
                                         'release_version': row['tag_name'], 'abstract': '',
                                         'published': row['published_at'], 'links': {'url': row['html_url']},
                                         'source_hits': [source_id], 'code_links': [f'https://github.com/{repository}']}, now=now))
    return records


def fetch(source, root, now=None, session=None):
    from .fetch_arxiv import USER_AGENT
    current = now or datetime.now(timezone.utc)
    cutoff = (current - timedelta(days=source['params'].get('lookback_days', 14))).date().isoformat()
    headers = {'User-Agent': USER_AGENT, 'Accept': 'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    records, payloads, errors = [], {}, {}
    papers = read_yaml(Path(root) / 'data' / 'papers.yaml')['papers']
    for repository in repositories(papers):
        try:
            response = (session or requests).get(f'https://api.github.com/repos/{repository}/releases',
                                                params={'per_page': 100}, headers=headers, timeout=30)
            response.raise_for_status()
            payload = response.json()
            payloads[repository] = payload
            records.extend(item for item in parse_json(payload, repository, source['id'], current.isoformat())
                           if item['published'][:10] >= cutoff)
        except (requests.RequestException, ValueError, KeyError) as error:
            errors[repository] = str(error)
    return records, {'format': 'github-json', 'repositories': payloads, 'errors': errors}
