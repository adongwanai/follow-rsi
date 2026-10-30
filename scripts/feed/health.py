"""Source health, explicit GitHub issue integration, and transparent metrics."""
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import subprocess
import tempfile
from scripts.common import read_yaml
from .storage import load_items, load_state, save_state, write_json
from .scope import archive_counts, direction_of, in_scope, load_scope


def timestamp(value):
    date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return date if date.tzinfo else date.replace(tzinfo=timezone.utc)


def week_of(value):
    date = timestamp(value)
    year, week, _ = date.isocalendar()
    return f'{year}-W{week:02d}'


class GithubIssues:
    """Only instantiate from an explicitly enabled CI/CLI external-write path."""
    def __init__(self, repository):
        self.repository = repository

    def find(self, title):
        result = subprocess.run(['gh', 'issue', 'list', '--repo', self.repository, '--state', 'open',
                                 '--search', title + ' in:title', '--json', 'number,title', '--limit', '100'],
                                check=True, capture_output=True, text=True)
        return next((row['number'] for row in json.loads(result.stdout) if row['title'] == title), None)

    def create(self, title, body):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'body.md'
            path.write_text(body, encoding='utf-8')
            result = subprocess.run(['gh', 'issue', 'create', '--repo', self.repository,
                                     '--title', title, '--body-file', str(path)],
                                    check=True, capture_output=True, text=True)
        return int(result.stdout.strip().rsplit('/', 1)[-1])

    def close(self, number):
        subprocess.run(['gh', 'issue', 'close', str(number), '--repo', self.repository], check=True)


def update_health(root, outcomes, now=None, issue_client=None):
    current = now or datetime.now(timezone.utc)
    if isinstance(current, str):
        current = timestamp(current)
    moment = current.isoformat()
    week = week_of(moment)
    state, events = load_state(root), []
    registry = read_yaml(Path(root) / 'feed' / 'sources.yaml')['sources']
    enabled = {entry['id']: entry for entry in registry if entry['enabled']}
    for ident, entry in enabled.items():
        source = state['sources'].setdefault(ident, {'consecutive_failures': 0, 'consecutive_errors': 0,
                                                    'seen_ids': [], 'weekly': {}})
        source.setdefault('enabled_since', moment)
        source.update(enabled=True, schedule=entry['schedule'], kind=entry['kind'])
    for ident, source in state['sources'].items():
        source['enabled'] = ident in enabled
    for outcome in outcomes:
        ident = outcome['source_id']
        source = state['sources'].setdefault(ident, {'consecutive_failures': 0, 'consecutive_errors': 0,
                                                    'seen_ids': [], 'weekly': {}})
        healthy = outcome['ok'] and outcome['count'] > 0 and not outcome.get('degraded')
        api_error = not outcome['ok'] or outcome.get('degraded', False)
        source['last_run'] = moment
        source['last_count'] = outcome['count']
        source['last_ok'] = outcome['ok']
        source['last_error'] = outcome.get('error')
        source['degraded'] = outcome.get('degraded', False)
        source['consecutive_failures'] = 0 if healthy else source['consecutive_failures'] + 1
        source['consecutive_errors'] = source['consecutive_errors'] + 1 if api_error else 0
        if outcome['ok']:
            source['last_success'] = moment
        seen = set(source['seen_ids'])
        fresh = set(outcome.get('ids', [])) - seen
        source['seen_ids'] = sorted(seen | set(outcome.get('ids', [])))
        source['weekly'][week] = source['weekly'].get(week, 0) + len(fresh)
        source['total_found'] = len(source['seen_ids'])
    for ident in enabled:
        source = state['sources'][ident]
        healthy = source.get('last_ok') and source.get('last_count', 0) > 0 and not source.get('degraded')
        title = f'Source down: {ident}'
        if source['consecutive_failures'] >= 3 and not source.get('issue_number'):
            event = {'action': 'open', 'source_id': ident, 'title': title,
                     'body': f"Three consecutive empty or failed runs.\n\nLast error: {source['last_error'] or '0 entries'}\n\nDegraded RSS mode: {source['degraded']}"}
            events.append(event)
            if issue_client:
                source['issue_number'] = issue_client.find(title) or issue_client.create(title, event['body'])
        if healthy and source.get('issue_number'):
            events.append({'action': 'close', 'source_id': ident, 'number': source['issue_number']})
            if issue_client:
                issue_client.close(source.pop('issue_number'))
        last_record = source.get('last_run') or source['enabled_since']
        source['missing_days'] = max(0, (current.date() - timestamp(last_record).date()).days)
        if source['missing_days'] < 2 and source.get('missing_issue_number'):
            events.append({'action': 'close', 'source_id': ident, 'number': source['missing_issue_number']})
            if issue_client:
                issue_client.close(source.pop('missing_issue_number'))
        if source['missing_days'] >= 2 and not source.get('missing_issue_number'):
            title = f'Source not run: {ident}'
            event = {'action': 'open', 'source_id': ident, 'title': title,
                     'body': f"Enabled source has no run record for {source['missing_days']} calendar days.\n\nLast run: {source.get('last_run') or 'never'}\n\nEnabled since: {source['enabled_since']}"}
            events.append(event)
            if issue_client:
                source['missing_issue_number'] = issue_client.find(title) or issue_client.create(title, event['body'])
    if outcomes:
        state['last_fetch'] = {'run_at': moment, 'sources': [
            {key: value for key, value in outcome.items() if key != 'ids'} for outcome in outcomes]}
    save_state(root, state)
    successes = [row['last_success'] for row in state['sources'].values() if row.get('last_success')]
    last_success = max(successes) if successes else None
    age = max(0, int((current - timestamp(last_success)).total_seconds() // 3600)) if last_success else None
    status = {'checked_at': moment, 'last_success': last_success, 'age_hours': age,
              'last_fetch': state.get('last_fetch'),
              'sources': {key: {k: v for k, v in value.items() if k != 'seen_ids'} for key, value in state['sources'].items()},
              'pending_issue_actions': events if issue_client is None else []}
    write_json(Path(root) / 'site' / 'feed' / 'status.json', status)
    badge = {'schemaVersion': 1, 'label': 'feed',
             'message': f'updated {age}h ago' if age is not None else 'not run',
             'color': 'red' if age is None or age > 48 else 'blue'}
    write_json(Path(root) / 'badges' / 'feed-updated.json', badge)
    write_json(Path(root) / 'site' / 'badges' / 'feed-updated.json', badge)
    return status


def version_alerts(root, items=None, issue_client=None):
    state = load_state(root)
    sent = state.setdefault('version_alerts', {})
    events = []
    for item in items if items is not None else load_items(root):
        if item.get('retracted'):
            key = f"retracted:{item['id']}"
            title = f"Retraction: {item.get('arxiv_id') or item['id']}"
        elif item.get('in_repo') and item.get('version_changed'):
            key = f"version:{item['id']}:{item['version']}"
            title = f"{item.get('repo_id', item['id'])} 出了 v{item['version']}，请复核证据卡片中的数字"
        else:
            continue
        if key in sent:
            continue
        body = f"Metadata change detected: {item['title']}\n\n{item['links'].get('arxiv', '')}\n\nThe source evidence card has not been changed automatically."
        events.append({'title': title, 'body': body})
        if issue_client:
            sent[key] = issue_client.find(title) or issue_client.create(title, body)
    if issue_client:
        save_state(root, state)
    return events


def publication_times(root):
    """First public daily-edition timestamp per paper; demo artifacts never count."""
    times = {}
    for path in sorted((Path(root) / 'site/daily').glob('????-??-??.json')):
        edition = json.loads(path.read_text(encoding='utf-8'))
        if not edition.get('reviewed_only') or edition.get('demo'):
            continue
        published = timestamp(edition['published_at'])
        for item in edition['items']:
            ident = item['id']
            times[ident] = min(times[ident], published) if ident in times else published
    return times


def compute_metrics(root, items=None, week=None):
    items = load_items(root) if items is None else items
    scope = load_scope(root)
    week = week or week_of(datetime.now(timezone.utc).isoformat())
    found = [p for p in items if p['kind'] == 'paper' and week_of(p['first_seen']) == week]
    reviewed = [p for p in items if p['kind'] == 'paper' and p.get('review', {}).get('week') == week]
    accepted = [p for p in reviewed if p['review']['decision'] in {'accept', 'move'} and not p.get('retracted')
                and in_scope(direction_of(p), scope)]
    included = [p for p in reviewed if p.get('llm', {}).get('label') == 'include'
                and p['review']['decision'] in {'accept', 'move', 'reject'}
                and in_scope(direction_of(p), scope)]
    accepted_include = [p for p in included if p['review']['decision'] in {'accept', 'move'}]
    yields = {}
    for item in accepted:
        for source in item['source_hits']:
            value = yields.setdefault(source, {'accepted': 0, 'exclusive': 0})
            value['accepted'] += 1
            value['exclusive'] += len(item['source_hits']) == 1
    published = publication_times(root)
    latencies = [(published[p['id']] - timestamp(p['published'])).total_seconds() / 86400
                 for p in accepted if p['published'] and p['id'] in published]
    attempted = [p for p in found if 'summary_zh' in p or p.get('guard_failed')]
    guard_failures = sum(bool(p.get('initial_guard_failed') or p.get('guard_failed')) for p in attempted)
    path = Path(root) / 'data' / 'feed' / 'metrics.json'
    metrics = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'weeks': {}}
    previous = metrics.setdefault('weeks', {}).get(week, {})
    metrics['weeks'][week] = {**previous, 'found': len(found), 'accepted': len(accepted),
                             'archive_by_direction': archive_counts(root, week),
                             'precision': len(accepted_include) / len(included) if included else None,
                             'latency_days': statistics.median(latencies) if latencies else None,
                             'source_yield': yields, 'guard_fail_rate': guard_failures / len(attempted) if attempted else None}
    write_json(path, metrics)
    state = load_state(root)
    for source, entry in state['sources'].items():
        entry['total_accepted'] = sum(p.get('review', {}).get('decision') in {'accept', 'move'}
                                      and in_scope(direction_of(p), scope) and not p.get('retracted')
                                      and source in p['source_hits'] for p in items)
    save_state(root, state)
    return metrics['weeks'][week]
