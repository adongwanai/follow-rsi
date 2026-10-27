"""Weekly CI-only arXiv discovery. Candidates are issues, never paper-data edits."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from common import ROOT, read_yaml

PHRASES = ('harness evolution', 'harness self-evolution', 'harness optimization', 'self-evolving harness', 'recursive self-improvement')
QUERY = '(' + ' OR '.join(f'(ti:"{p}" OR abs:"{p}")' for p in PHRASES) + ') AND (ti:agent OR abs:agent)'
ATOM = {'a': 'http://www.w3.org/2005/Atom'}
ID_RE = re.compile(r'(?:\d{4}\.\d{4,5}|cs/\d{7})(?:v\d+)?')


def normalize_id(value):
    value = value.strip()
    if '://' in value:
        path = urlparse(value).path
        value = re.sub(r'^/(?:abs|pdf)/', '', path).removesuffix('.pdf')
    if not ID_RE.fullmatch(value):
        raise ValueError(f'Invalid arXiv identifier: {value}')
    return re.sub(r'v\d+$', '', value)


def parse_feed(xml):
    entries = []
    for entry in ET.fromstring(xml).findall('a:entry', ATOM):
        raw_id = entry.findtext('a:id', namespaces=ATOM)
        title = entry.findtext('a:title', namespaces=ATOM)
        abstract = entry.findtext('a:summary', namespaces=ATOM)
        if raw_id is None or title is None or abstract is None:
            raise ValueError('arXiv entry is missing id, title, or abstract')
        pid = normalize_id(raw_id)
        entries.append({'id': pid, 'title': title.strip(), 'abstract': abstract.strip(), 'url': 'https://arxiv.org/abs/' + pid})
    return entries


def issue_ids(issues):
    found = set()
    for issue in issues:
        for raw in re.findall(r'https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/((?:\d{4}\.\d{4,5}|cs/\d{7})(?:v\d+)?)(?:\.pdf)?', (issue.get('title') or '') + '\n' + (issue.get('body') or '')):
            found.add(normalize_id(raw))
    return found


def select_candidates(entries, known, limit=15):
    result, seen = [], set(known)
    for entry in entries:
        if entry['id'] not in seen:
            result.append(entry)
            seen.add(entry['id'])
            if len(result) == limit:
                break
    return result


def issue_body(entry):
    return entry['title'] + '\n\n' + entry['url'] + '\n\n' + entry['abstract'] + '\n'


def gh(*args):
    return subprocess.run(['gh', *args], check=True, capture_output=True, text=True).stdout


def watch(dry_run=False):
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise RuntimeError('Network monitoring runs only in GitHub Actions. Unit tests use offline Atom fixtures.')
    repo = os.environ['GITHUB_REPOSITORY']
    papers = read_yaml(ROOT / 'data/papers.yaml')['papers']
    known = {normalize_id(p['arxiv']) for p in papers if 'arxiv' in p}
    # Both open and closed candidate issues count; paginate to prevent repeat posts.
    pages = json.loads(gh('api', '--paginate', '--slurp', f'repos/{repo}/issues?state=all&per_page=100'))
    known |= issue_ids(issue for page in pages for issue in page)
    query = urlencode({'search_query': QUERY, 'start': 0, 'max_results': 100, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
    request = Request('https://export.arxiv.org/api/query?' + query, headers={'User-Agent': 'awesome-harness-evolution/1.0 (weekly candidate discovery)'})
    with urlopen(request, timeout=60) as response:
        entries = parse_feed(response.read())
    candidates = select_candidates(entries, known)
    if dry_run:
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
        return
    if candidates:
        labels = json.loads(gh('label', 'list', '--repo', repo, '--limit', '1000', '--json', 'name'))
        if not any(label['name'] == 'candidate' for label in labels):
            gh('label', 'create', 'candidate', '--repo', repo, '--color', '8B909B', '--description', 'Unreviewed arXiv candidate')
    for entry in candidates:
        with tempfile.TemporaryDirectory() as temporary:
            body = Path(temporary) / 'issue.md'
            body.write_text(issue_body(entry), encoding='utf-8')
            gh('issue', 'create', '--repo', repo, '--title', entry['title'], '--label', 'candidate', '--body-file', str(body))
    print(f'Opened {len(candidates)} candidate issues.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    watch(parser.parse_args().dry_run)
