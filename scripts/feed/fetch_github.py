"""GitHub release versions and links; no inferred release summaries."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse
import os
import requests
from scripts.common import read_yaml
from .normalize import normalize_record


def verify_code_links(links, session=None):
    """Verify repository contents, not licensing or reproducibility."""
    if not links:
        return {'evidence': {'value': 'unknown', 'quote': None}, 'checks': []}
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'follow-rsi/code-link-check'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    checks = []
    for link in links:
        parsed = urlparse(link)
        parts = parsed.path.strip('/').split('/')
        if (parsed.scheme not in ('https', 'http') or parsed.hostname != 'github.com'
                or len(parts) != 2 or not all(parts) or parsed.query or parsed.fragment):
            checks.append({'url': link, 'status': 'not_repository_url'})
            continue
        repository = '/'.join(parts).removesuffix('.git')
        try:
            response = (session or requests).get(
                f'https://api.github.com/repos/{repository}/git/trees/HEAD',
                params={'recursive': '1'}, headers=headers, timeout=30)
            response.raise_for_status()
            payload = response.json()
            files = [entry['path'] for entry in payload['tree'] if entry['type'] == 'blob'
                     and not Path(entry['path']).name.lower().startswith('readme')]
            checks.append({'url': link, 'status': 'verified' if files else 'no_non_readme_file',
                           'non_readme_file': files[0] if files else None,
                           'truncated_tree': payload.get('truncated', False)})
            if files:
                return {'evidence': {'value': 'yes', 'quote': link}, 'checks': checks}
        except (requests.RequestException, ValueError, KeyError) as error:
            check = {'url': link, 'status': 'unverified', 'error': type(error).__name__}
            if isinstance(error, requests.HTTPError) and error.response is not None:
                check['http_status'] = error.response.status_code
            checks.append(check)
    return {'evidence': {'value': 'partial', 'quote': links[0]}, 'checks': checks}


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
    cutoff = (current - timedelta(days=source['params'].get('lookback_days', 14) - 1)).date().isoformat()
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
