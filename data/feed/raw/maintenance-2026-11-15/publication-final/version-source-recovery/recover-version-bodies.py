"""Recover frozen version-specific source bodies, without review or canonical mutation."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import time

from bs4 import BeautifulSoup
import fitz
import requests

ROOT = Path.cwd()
WORK = ROOT / 'build/maintenance-2026-11-15/version-source-recovery'
EXPECTED_INPUT_SHA = 'c910787a438e56adfd709c5ca56af72f078334b459ae087178d578ef25661b76'
INTERVAL_SECONDS = 3.2


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    path = WORK / name
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


assert digest(WORK / 'input-worklist.json') == EXPECTED_INPUT_SHA
input_data = json.loads((WORK / 'input-worklist.json').read_text())
excluded = json.loads((WORK / 'excluded-ten-pairs.json').read_text())
assert not ({item['id'] for item in input_data['items']} & {item['id'] for item in excluded['items']})
for directory in ['bodies', 'texts', 'receipts']:
    (WORK / directory).mkdir(exist_ok=True)
state_path = WORK / 'recovery-state.json'
if state_path.exists():
    state = json.loads(state_path.read_text())
    assert state['input_sha256'] == EXPECTED_INPUT_SHA
else:
    state = {'started_at': now(), 'input_sha256': EXPECTED_INPUT_SHA,
             'source_worklist': 'build/maintenance-2026-11-15/backlog-audit/version-source-recovery-worklist.json',
             'items': deepcopy(input_data['items']), 'stopped_reason': None,
             'paid_calls': 0, 'canonical_writes': 0, 'content_reviews_completed': 0,
             'formal_version_adoptions': 0}
    for item in state['items']:
        item['queue_processing_complete'] = False
        item['body_review_completed'] = False
        item['version_adopted'] = False
        item['recovery_status'] = 'not_yet_attempted'
        for side in item['sides']:
            side['initial_status'] = side['status']
            side['status'] = 'not_yet_attempted'
            side['attempts'] = []
            side['source_recovery'] = None
            if side['version'] == 'unknown':
                side['blocker'] = 'missing_original_version_identity'
                side['attempt_permitted'] = False
            else:
                assert isinstance(side['version'], int) and side['version'] > 0
                side['attempt_permitted'] = True
    save('recovery-state.json', state)
request_log = WORK / 'requests.jsonl'
attempts = [json.loads(line) for line in request_log.read_text().splitlines()] if request_log.exists() else []
last_dispatch = None
stop_requested = False


def summarize():
    rows = state['items']
    sides = [side for row in rows for side in row['sides']]
    known = [side for side in sides if side['attempt_permitted']]
    candidates = [side for row in rows for side in row['sides'] if side['side'] == 'candidate']
    pairs = [row for row in rows if row['current_version'] != 'unknown']
    summary = {
        'updated_at': now(), 'input_items': len(rows),
        'known_version_pairs': len(pairs),
        'missing_original_version_identity': sum(row['current_version'] == 'unknown' for row in rows),
        'queue_items_processed': sum(row['queue_processing_complete'] for row in rows),
        'queue_items_not_yet_processed': sum(not row['queue_processing_complete'] for row in rows),
        'known_version_sides': len(known),
        'known_version_side_status': dict(Counter(side['status'] for side in known)),
        'candidate_side_status': dict(Counter(side['status'] for side in candidates)),
        'fully_recovered_known_pairs': sum(all(side['status'] == 'recovered' for side in row['sides']) for row in pairs),
        'pairs_with_failed_requests': sum(any(side['status'] == 'request_failed' for side in row['sides']) for row in pairs),
        'reused_cached_versions': sum(side.get('source_recovery', {}).get('method') == 'cached_versioned_body'
                                     for side in known if side.get('source_recovery')),
        'newly_fetched_versions': sum(side.get('source_recovery', {}).get('method') == 'official_versioned_request'
                                     for side in known if side.get('source_recovery')),
        'actual_requests': len(attempts),
        'http_status_counts': dict(Counter(str(attempt.get('http_status', 'network_error')) for attempt in attempts)),
        'valid_fulltext_responses': sum(bool(attempt.get('body_validation', {}).get('usable_versioned_fulltext')) for attempt in attempts),
        'stopped_reason': state['stopped_reason'],
        'paid_calls': 0, 'canonical_writes': 0, 'content_reviews_completed': 0,
        'formal_version_adoptions': 0,
        'boundary': 'Source recovery only. Target-body recovery does not resolve unknown original identity or complete a version/content/scope review.',
    }
    save('progress.json', summary)
    return summary


def inspect_body(path, arxiv_id, version, request_url):
    content = path.read_bytes()
    expected = f'{arxiv_id}v{version}'
    result = {'expected_arxiv_version': expected, 'body_sha256': hashlib.sha256(content).hexdigest(),
              'body_path': str(path.relative_to(ROOT)), 'bytes': len(content),
              'usable_versioned_fulltext': False}
    if content.startswith(b'%PDF'):
        result['content_kind'] = 'pdf'
        try:
            with fitz.open(stream=content, filetype='pdf') as document:
                result['page_count'] = len(document)
                text = '\n'.join(page.get_text() for page in document)
                first_page = document[0].get_text() if len(document) else ''
        except (fitz.FileDataError, fitz.EmptyFileError) as error:
            result['validation_error'] = f'{type(error).__name__}: {error}'
            return result, None
        embedded = sorted(set(re.findall(re.escape(arxiv_id) + r'v\d+', first_page)))
        result['embedded_versions_on_first_page'] = embedded
        expected_url = f'https://arxiv.org/pdf/{expected}'
        if embedded and expected not in embedded:
            result['validation_error'] = 'PDF watermark identifies a different version.'
        elif request_url == expected_url and result['page_count'] > 0:
            result['usable_versioned_fulltext'] = True
            result['version_binding'] = 'matching_first_page_watermark_and_explicit_version_url' if expected in embedded else 'explicit_official_version_url_only; no first-page version token found'
        else:
            result['validation_error'] = 'PDF lacks a valid explicit version binding.'
    else:
        soup = BeautifulSoup(content, 'html.parser')
        article = soup.find('article')
        embedded = sorted(set(re.findall(re.escape(arxiv_id) + r'v\d+', content.decode('utf-8', errors='replace'))))
        watermark_element = soup.find(id='watermark-tr')
        watermark = watermark_element.get_text(' ', strip=True) if watermark_element else ''
        watermark_versions = sorted(set(re.findall(re.escape(arxiv_id) + r'v\d+', watermark)))
        result.update(content_kind='html', article_present=article is not None,
                      html_closed=b'</html>' in content.lower(), embedded_versions=embedded,
                      watermark=watermark, watermark_versions=watermark_versions,
                      html_title=soup.title.get_text(' ', strip=True) if soup.title else None)
        text = article.get_text('\n', strip=True) if article else ''
        result['article_characters'] = len(text)
        result['usable_versioned_fulltext'] = bool(article and result['html_closed'] and watermark_versions == [expected])
        result['version_binding'] = 'matching_arxiv_page_watermark' if result['usable_versioned_fulltext'] else None
        if not result['usable_versioned_fulltext']:
            result['validation_error'] = 'No complete article with the requested embedded arXiv version; HTTP success alone is insufficient.'
    if result['usable_versioned_fulltext']:
        result['text_characters'] = len(text)
        result['text_sha256'] = hashlib.sha256(text.encode()).hexdigest()
        result['text_extraction_status'] = 'nonempty' if text else 'empty_pdf_text_layer'
        return result, text
    return result, None


def bind_body(item, side, validation, text, method, receipt_path=None, original_cache=None):
    arxiv_id = item['id'].removeprefix('arxiv:')
    path = WORK / 'texts' / f'{arxiv_id}v{side["version"]}.{validation["content_kind"]}.txt'
    path.write_text(text)
    recovery = {**validation, 'method': method, 'recovered_at': now(),
                'text_path': str(path.relative_to(ROOT)), 'text_sha256': digest(path),
                'content_review_completed': False, 'version_adopted': False}
    if receipt_path:
        recovery['receipt_path'] = str(receipt_path.relative_to(ROOT))
        recovery['receipt_sha256'] = digest(receipt_path)
    if original_cache:
        recovery['original_cache'] = original_cache
    side.update(status='recovered', source_recovery=recovery)


def acquire(item, side, url, kind):
    global last_dispatch, stop_requested
    if last_dispatch is not None:
        delay = INTERVAL_SECONDS - (time.monotonic() - last_dispatch)
        if delay > 0:
            time.sleep(delay)
    arxiv_id = item['id'].removeprefix('arxiv:')
    attempt_number = len(attempts) + 1
    body_path = WORK / 'bodies' / f'{arxiv_id}v{side["version"]}.{attempt_number:04d}.{kind}'
    receipt_path = WORK / 'receipts' / f'{attempt_number:04d}.json'
    last_dispatch = time.monotonic()
    attempt = {'attempt_number': attempt_number, 'id': item['id'], 'side': side['side'],
               'version': side['version'], 'request_url': url, 'requested_at': now(),
               'dispatch_monotonic_ns': time.monotonic_ns(), 'request_kind': kind}
    save('active-request.json', attempt)
    text = None
    try:
        response = requests.get(url, timeout=(10, 35),
                                headers={'User-Agent': 'FollowRSI/0.1 (versioned source archival)'})
        body_path.write_bytes(response.content)
        attempt.update(http_status=response.status_code, final_url=response.url,
                       content_type=response.headers.get('Content-Type'), bytes=len(response.content),
                       body_path=str(body_path.relative_to(ROOT)), body_sha256=digest(body_path))
        if response.status_code == 200:
            validation, text = inspect_body(body_path, arxiv_id, side['version'], url)
            if ((validation.get('version_binding') or '').startswith('explicit_official_version_url_only')
                    and response.url.rstrip('/') != url.rstrip('/')):
                validation['usable_versioned_fulltext'] = False
                validation['validation_error'] = 'No embedded version token and final PDF URL differs from the explicit requested version.'
                text = None
            attempt['body_validation'] = validation
        else:
            attempt['error'] = f'HTTP {response.status_code}'
        if response.status_code == 429:
            state['stopped_reason'] = 'arxiv_rate_limit_429; remaining requests not attempted'
            stop_requested = True
    except requests.RequestException as error:
        attempt['error'] = f'{type(error).__name__}: {error}'
    attempt['finished_at'] = now()
    receipt_path.write_text(json.dumps(attempt, ensure_ascii=False, indent=2) + '\n')
    with request_log.open('a') as output:
        output.write(json.dumps(attempt, ensure_ascii=False) + '\n')
    attempts.append(attempt)
    side['attempts'].append({'receipt_path': str(receipt_path.relative_to(ROOT)), 'receipt_sha256': digest(receipt_path),
                             'http_status': attempt.get('http_status'), 'request_url': url})
    (WORK / 'active-request.json').unlink()
    if attempt.get('body_validation', {}).get('usable_versioned_fulltext'):
        bind_body(item, side, attempt['body_validation'], text, 'official_versioned_request', receipt_path)
    save('recovery-state.json', state)
    summarize()
    return side['status'] == 'recovered'


summarize()
for index, item in enumerate(state['items']):
    if item['queue_processing_complete']:
        continue
    if stop_requested:
        break
    for side in item['sides']:
        if not side['attempt_permitted'] or side['status'] in {'recovered', 'request_failed'}:
            continue
        arxiv_id = item['id'].removeprefix('arxiv:')
        for cached in side['cached_fulltext']:
            source = ROOT / cached['path']
            assert digest(source) == cached['sha256'], source
            kind = 'pdf' if source.read_bytes().startswith(b'%PDF') else 'html'
            destination = WORK / 'bodies' / f'{arxiv_id}v{side["version"]}.cached.{kind}'
            shutil.copyfile(source, destination)
            validation, text = inspect_body(destination, arxiv_id, side['version'], side[f'{kind}_url'])
            if validation['usable_versioned_fulltext']:
                bind_body(item, side, validation, text, 'cached_versioned_body', original_cache=cached)
                break
        if side['status'] != 'recovered':
            if not acquire(item, side, side['html_url'], 'html') and not stop_requested:
                acquire(item, side, side['pdf_url'], 'pdf')
            if side['status'] != 'recovered':
                side['status'] = 'request_failed'
                side['blocker'] = state['stopped_reason'] or 'No usable version-specific fulltext obtained from official HTML/PDF attempts.'
        save('recovery-state.json', state)
        summarize()
        if stop_requested:
            break
    known_sides = [side for side in item['sides'] if side['attempt_permitted']]
    item['queue_processing_complete'] = all(side['status'] in {'recovered', 'request_failed'} for side in known_sides)
    if item['current_version'] == 'unknown':
        item['recovery_status'] = 'missing_original_version_identity'
        item['external_blocked'] = True
    elif all(side['status'] == 'recovered' for side in item['sides']):
        item['recovery_status'] = 'recovered'
        item['external_blocked'] = False
    elif any(side['status'] == 'request_failed' for side in item['sides']):
        item['recovery_status'] = 'request_failed'
        item['external_blocked'] = True
    save('recovery-state.json', state)
    progress = summarize()
    print(json.dumps({'queue_index': index + 1, 'id': item['id'], 'recovery_status': item['recovery_status'],
                      'side_status': {side['side']: side['status'] for side in item['sides']},
                      'requests_total': len(attempts), 'queue_processed': progress['queue_items_processed']}, ensure_ascii=False), flush=True)
state['finished_at'] = now()
save('recovery-state.json', state)
print(json.dumps({'event': 'finished', **summarize()}, ensure_ascii=False), flush=True)
