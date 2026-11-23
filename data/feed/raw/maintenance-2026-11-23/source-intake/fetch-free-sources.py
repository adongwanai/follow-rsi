"""Free source-only collection in an isolated root; never calls LLM or publication stages."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
import requests
import yaml

REPO = Path.cwd()
sys.path.insert(0, str(REPO))
from scripts.feed import fetch_arxiv, fetch_hf, fetch_rss, fetch_s2, fetch_github
from scripts.feed.health import update_health
from scripts.feed.storage import save_raw, write_json, load_state

ROOT = REPO / 'build/maintenance-2026-11-23/source-intake'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(parents=True, exist_ok=True)
NOW = datetime.now(timezone.utc)
DAY = '2026-11-23'
assert NOW.date().isoformat() == DAY, 'Run date must match the intended daily source window.'
START = json.loads((ROOT/'run-state.json').read_text())['started_at'] if (ROOT/'run-state.json').exists() else NOW.isoformat()
REGISTRY = yaml.safe_load((ROOT / 'feed/sources.yaml').read_text())
SOURCES = [s for s in REGISTRY['sources'] if s['enabled']]
BASELINE = json.loads((ROOT / 'canonical-baseline.json').read_text())
KNOWN = set(BASELINE['ids'])

# Keep credential values inside their existing environment / gh client.
# No local credential file is read and no model credential is loaded.
environment_s2_present = bool(os.environ.get('S2_API_KEY', '').strip())
gh_auth = subprocess.run(['gh','auth','status','--active'],capture_output=True,text=True)
if os.environ.get('S2_API_KEY'):
    os.environ['S2_API_KEY'] = os.environ['S2_API_KEY'].strip()
AUTH = {'semantic_scholar': 'authenticated' if os.environ.get('S2_API_KEY') else 'anonymous',
        'semantic_scholar_interval_seconds': 1.1 if os.environ.get('S2_API_KEY') else 3.1,
        'semantic_scholar_max_429_retries': 5,
        'github': 'authenticated_via_gh_cli' if gh_auth.returncode==0 else 'gh_cli_auth_unavailable',
        'model_credentials_loaded': False}

def relative(path):
    return Path(path).relative_to(REPO).as_posix()

def stamp():
    return datetime.now(timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

class RecordingSession:
    last_s2_dispatch_ns = None

    def __init__(self, source_id):
        self.session = requests.Session()
        self.source_id = source_id
        self.started = time.monotonic()
        self.directory = ROOT / 'network' / source_id
        self.directory.mkdir(parents=True, exist_ok=True)
        self.attempts = []
        self.path = self.directory / 'attempts.jsonl'

    def get(self, url, **kwargs):
        is_s2 = self.source_id.startswith('s2-')
        previous_dispatch = RecordingSession.last_s2_dispatch_ns
        if is_s2:
            self.bounded_sleep(0)
            if previous_dispatch is not None:
                interval_ns = int(AUTH['semantic_scholar_interval_seconds'] * 1_000_000_000)
                while time.monotonic_ns() < previous_dispatch + interval_ns:
                    self.bounded_sleep((previous_dispatch + interval_ns - time.monotonic_ns()) / 1_000_000_000)
            kwargs['timeout'] = min(kwargs.get('timeout', 30), self.remaining())
        begin = time.monotonic()
        row = {'requested_at': stamp(), 'request_url': url, 'params': kwargs.get('params'), 'status': 'started'}
        try:
            dispatch_ns = time.monotonic_ns()
            row['dispatch_monotonic_ns'] = dispatch_ns
            if is_s2:
                row['previous_s2_dispatch_monotonic_ns'] = previous_dispatch
                row['s2_dispatch_gap_seconds'] = (dispatch_ns - previous_dispatch) / 1_000_000_000 if previous_dispatch is not None else None
                row['required_dispatch_gap_seconds'] = AUTH['semantic_scholar_interval_seconds']
                RecordingSession.last_s2_dispatch_ns = dispatch_ns
            if self.source_id == 'github-releases':
                from urllib.parse import urlencode
                endpoint=url.removeprefix('https://api.github.com/')
                if kwargs.get('params'):endpoint+='?'+urlencode(kwargs['params'])
                result=subprocess.run(['gh','api',endpoint,'--include'],capture_output=True,timeout=35)
                if result.returncode and not result.stdout.startswith(b'HTTP/'):
                    raise requests.ConnectionError('gh API request failed: '+result.stderr.decode(errors='replace').strip())
                header,sep,content=result.stdout.replace(b'\r\n',b'\n').partition(b'\n\n')
                if not sep:raise ValueError('GitHub response has no HTTP header boundary')
                lines=header.decode().splitlines();response=requests.Response()
                response.status_code=int(lines[0].split()[1]);response.url=url
                response.headers.update(dict(line.split(': ',1) for line in lines[1:] if ': ' in line))
                response._content=content
            else:
                response = self.session.get(url, **kwargs)
            body = self.directory / f'{len(self.attempts)+1:04d}.body'
            body.write_bytes(response.content)
            row.update(http_status=response.status_code, final_url=response.url,
                       status='http_response', body_path=relative(body), body_sha256=sha(body),
                       bytes=len(response.content), content_type=response.headers.get('Content-Type'),
                       http_date=response.headers.get('Date'),
                       api_key_header_present=bool(kwargs.get('headers', {}).get('x-api-key')))
            return response
        except requests.RequestException as error:
            row.update(status='network_error', error=f'{type(error).__name__}: {error}')
            raise
        finally:
            row.update(finished_at=stamp(), elapsed_seconds=round(time.monotonic()-begin, 3))
            self.attempts.append(row)
            with self.path.open('a') as handle:
                handle.write(json.dumps(row, ensure_ascii=False)+'\n')

    def remaining(self):
        value = 180 - (time.monotonic() - self.started)
        if value <= 0:
            raise ValueError('BoundedSourceTraversal: source reached the 180-second attempt window; successful responses retained; unvisited coverage is unknown.')
        return value

    def bounded_sleep(self, seconds):
        remaining = self.remaining()
        if seconds >= remaining:
            time.sleep(remaining)
            self.remaining()
        if seconds > 0:
            time.sleep(seconds)


def bounded_s2_request(path, params=None, session=None):
    """Bound retries and pacing at the actual recorded transport boundary."""
    assert isinstance(session, RecordingSession)
    headers = {'User-Agent': 'FollowRSI/0.1'}
    if os.environ.get('S2_API_KEY'):
        headers['x-api-key'] = os.environ['S2_API_KEY']
    for attempt in range(6):
        response = session.get(fetch_s2.BASE + '/' + path, params=params, headers=headers, timeout=30)
        if response.status_code != 429 or attempt == 5:
            response.raise_for_status()
            return response.json()
        session.bounded_sleep(AUTH['semantic_scholar_interval_seconds'] * 2 ** attempt)


fetch_s2.request = bounded_s2_request

write_json(ROOT/'auth-presence.json', {'checked_at': stamp(), 'environment_s2_key_present': environment_s2_present, 'env_local_s2_key_present': 'not_read', 'run_mode': AUTH['semantic_scholar'], 'collector_explicitly_clears_s2_key': False, 'configured_key_was_skipped': 'unknown_local_secret_file_not_read', 'credentials_printed': False, 'model_credentials_loaded': False})
write_json(ROOT/'run-state.json', {'status':'running','started_at':START,'target_day':DAY,'auth':AUTH,'enabled_sources':[s['id'] for s in SOURCES], 'paid_calls':0, 'production_writes':0})

ERRORS = (requests.RequestException, ET.ParseError, ValueError, KeyError, TypeError)

def collect(source):
    source_id = source['id']
    checkpoint = ROOT/'source-results'/f'{source_id}.json'
    if checkpoint.exists():
        saved=json.loads(checkpoint.read_text())
        return saved
    begin=time.monotonic();started=stamp();session=RecordingSession(source_id)
    print(json.dumps({'event':'source_started','source':source_id,'at':started}),flush=True)
    found=[];raw=None;degraded=False;failure=None;api_failure=None
    try:
        kind=source['kind']
        if kind=='hf_daily':
            full_board_source = {**source, 'params': {**source['params'], 'keywords': []}}
            found,raw=fetch_hf.fetch(full_board_source,now=NOW,session=session,days=6)
            # A Monday request can be three days beyond the most recent open list.
            limits = sorted({a['available_through'] for a in raw['attempts'].values() if a.get('available_through')})
            latest = limits[-1] if limits else None
            if latest and latest not in raw['attempts']:
                latest_now = datetime.fromisoformat(latest + 'T00:00:00+00:00')
                more, extra = fetch_hf.fetch(full_board_source,now=latest_now,session=session,days=1)
                found.extend(more)
                for key in ['days','attempts','errors']:
                    raw[key].update(extra[key])
            raw['most_recent_explicit_available_day'] = latest
            raw['coverage_note'] = 'All members from each successful requested board are retained in raw responses; reconciliation disables the keyword prefilter.'
        elif kind=='arxiv_query':
            try:
                found,raw=fetch_arxiv.fetch(source,days=6,now=NOW,session=session)
            except ERRORS as error:
                failures=load_state(ROOT)['sources'].get(source_id,{}).get('consecutive_errors',0)
                if failures<2:
                    raise
                api_failure=f'{type(error).__name__}: {error}'
                found,raw=fetch_arxiv.fallback_rss(source,now=NOW.isoformat(),session=session)
                raw['api_error']=api_failure;degraded=True
        elif kind in {'s2_citations','s2_authors'}:
            found,raw=fetch_s2.fetch(source,ROOT,now=NOW,session=session)
        elif kind=='rss':
            found,raw=fetch_rss.fetch(source,now=NOW,session=session)
        elif kind=='github_releases':
            found,raw=fetch_github.fetch(source,ROOT,now=NOW,session=session)
        else:
            raise ValueError('Unsupported enabled source kind: '+kind)
    except ERRORS as error:
        failure=f'{type(error).__name__}: {error}'
    recovered_pages=[]
    if source['kind'] in {'s2_citations','s2_authors'} and failure:
        # A later 429 must not discard pages which have already returned HTTP 200.
        seed_ids={p['arxiv']:p['id'] for p in fetch_s2.seed_papers(yaml.safe_load((ROOT/'data/papers.yaml').read_text())['papers'])}
        seen_pages=set();retained_metadata=[]
        for receipt in session.attempts:
            if receipt.get('http_status')!=200:
                continue
            payload=json.loads((REPO/receipt['body_path']).read_text())
            url=receipt['request_url'];params=receipt.get('params') or {}
            retained_metadata.append({'request_url':url,'params':params,'body_path':receipt['body_path'],'body_sha256':receipt['body_sha256']})
            if not (url.endswith('/citations') or url.endswith('/papers')):
                continue
            key=(url,params.get('offset'))
            if key in seen_pages:
                continue
            seen_pages.add(key)
            seed=seed_ids.get(url.split('paper/arXiv:',1)[1].removesuffix('/citations')) if '/citations' in url else None
            parsed=fetch_s2.parse_json(payload,source_id,seed_id=seed,author_tracked=source['kind']=='s2_authors',now=NOW.isoformat())
            cutoff=(NOW-timedelta(days=30)).date().isoformat()
            found.extend(x for x in parsed if x['published'] and x['published']>=cutoff)
            recovered_pages.append({**retained_metadata[-1],'unfiltered_records':len(parsed)})
        raw={'format':'s2-partial-recovery-from-network-receipts','auth_mode':AUTH['semantic_scholar'],'source_failed':True,
             'failure':failure,'pages':recovered_pages,'successful_http_responses':retained_metadata,
             'records':found,'coverage_note':'Only successful responses recovered; source traversal ended early.'}
    observed_at=stamp()
    for record in found:
        record['source_observed_at']=observed_at
        record['first_seen']=observed_at
        record['first_seen_policy']='actual_source_collection_timestamp'
    raw_path=None
    if raw is not None:
        raw_path=save_raw(ROOT,source_id,DAY,raw)
    if raw and raw.get('errors'):
        failure=str(raw['errors'])
    outcome={'source_id':source_id,'kind':source['kind'],'started_at':started,'finished_at':stamp(),
             'elapsed_seconds':round(time.monotonic()-begin,3),'ok':failure is None,'count':len(found),
             'unique_ids':len({x['id'] for x in found}),'ids':[x['id'] for x in found],
             'degraded':degraded,'error':failure or api_failure,'api_error_before_fallback':api_failure,
             'request_count':len(session.attempts),'http_status_counts':dict(Counter(str(x.get('http_status',x['status'])) for x in session.attempts)),
             'network_attempts':relative(session.path),'raw_path':relative(raw_path) if raw_path else None,
             'records':found,'raw_available':raw is not None}
    if source_id.startswith('s2-'):
        outcome['auth_mode']=AUTH['semantic_scholar'];outcome['min_interval_seconds']=AUTH['semantic_scholar_interval_seconds']
        outcome.update(recovered_partial=bool(recovered_pages),recovered_successful_pages=len(recovered_pages),source_traversal_complete=failure is None)
    if source_id=='hf-daily' and raw:
        payload=raw.get('days',{}).get(DAY)
        attempt=raw.get('attempts',{}).get(DAY,{})
        outcome['hf_today']={'date':DAY,'request_status':attempt.get('status'),'available_through':attempt.get('available_through'),
                            'raw_members':len(payload) if payload is not None else None,
                            'all_requested_board_records':len(found), 'keyword_prefilter_enabled':False,
                            'paper_ids':[x['paper']['id'] for x in payload] if payload is not None else [],
                            'all_requested_board_ids':[x['id'] for x in found],
                            'date_meaning':'Membership in the explicitly requested HF daily recommendation list; not paper publication or first_seen.',
                            'original_dates_verified':False,'qualified_harness_count':None}
    write_json(checkpoint,outcome)
    print(json.dumps({'event':'source_completed','source':source_id,'at':outcome['finished_at'],'ok':outcome['ok'],'count':len(found),'requests':len(session.attempts),'degraded':degraded},ensure_ascii=False),flush=True)
    return outcome

# HF first. Each API family remains serial so rate-limit guarantees are preserved.
outcomes=[]
for source in SOURCES:
    if source['kind']=='hf_daily':
        outcomes.append(collect(source))
groups=[ [s for s in SOURCES if s['kind']=='arxiv_query'],
         [s for s in SOURCES if s['kind'] in {'s2_citations','s2_authors'}],
         [s for s in SOURCES if s['kind']=='rss'],
         [s for s in SOURCES if s['kind']=='github_releases'] ]
def collect_group(group):
    return [collect(s) for s in group]
with ThreadPoolExecutor(max_workers=4) as pool:
    pending=[pool.submit(collect_group,g) for g in groups if g]
    for completed in as_completed(pending):
        outcomes.extend(completed.result())


write_json(ROOT/'run-state.json',{'status':'source_collection_complete','target_day':DAY,'started_at':START,'finished_at':stamp(),'paid_calls':0,'production_writes':0,'auth':AUTH,'completed_sources':[x['source_id'] for x in outcomes]})
print(json.dumps({'event':'all_sources_complete','sources':len(outcomes),'records':sum(x['count'] for x in outcomes)},ensure_ascii=False),flush=True)
