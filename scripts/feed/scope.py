"""Publication scope is narrower than discovery; keep other RSI work in an archive."""
from collections import Counter
from datetime import date
import json
from pathlib import Path

from scripts.common import ROOT, read_yaml
from scripts.feed.storage import load_items


def load_scope(root=ROOT):
    registry = read_yaml(Path(root) / 'feed/sources.yaml')
    taxonomy = read_yaml(Path(root) / 'feed/taxonomy.yaml')
    return {**registry['publish_scope'], 'cross': list(taxonomy['cross']),
            'known': [*taxonomy['directions'], *taxonomy['cross']]}


def direction_of(item):
    if 'direction' in item:
        return item['direction']
    direction = dict(item.get('llm', {}))
    review = item.get('review', {})
    if review.get('decision') in ('accept', 'move'):
        override = review.get('direction_override')
        if isinstance(override, str):
            primary, _, sub = override.partition('/')
            direction.update(primary=primary, harness_sub=sub or None)
        elif isinstance(override, dict):
            direction.update(override)
    return direction


def in_scope(direction, scope):
    primary = direction.get('primary')
    return (primary in scope['primary'] or
            (primary in scope['cross'] and bool(set(direction.get('secondary') or [])
                                                & set(scope['cross_with_secondary']))))


def scope_status(direction, scope):
    if direction.get('primary') not in scope['known']:
        return 'unclassified'
    return 'in_scope' if in_scope(direction, scope) else 'out_of_scope'


def require_scope(item, scope):
    if not in_scope(direction_of(item), scope):
        raise ValueError(f"{item['id']}: outside publish_scope; correct the direction or defer/reject the item")


def archive_out_of_scope(root=ROOT, items=None):
    """Append complete summarized snapshots by discovery month, without approving them."""
    root = Path(root)
    scope = load_scope(root)
    records = load_items(root) if items is None else items
    grouped = {}
    for item in records:
        if (item['kind'] != 'paper' or item.get('retracted')
                or item.get('review', {}).get('decision') == 'reject'
                or item.get('llm', {}).get('label') not in ('include', 'borderline')
                or scope_status(direction_of(item), scope) != 'out_of_scope'
                or 'summary_zh' not in item or 'summary_en' not in item):
            continue
        month = str(item.get('first_seen') or item['published'])[:7]
        grouped.setdefault(month, []).append({**item, 'archive_reason': 'outside_publish_scope'})
    appended = 0
    for month, rows in grouped.items():
        path = root / 'data/feed/archive' / f'{month}.jsonl'
        previous = {}
        if path.exists():
            for line in path.read_text(encoding='utf-8').splitlines():
                record = json.loads(line)
                previous[record['id']] = record
        changed = [row for row in rows if previous.get(row['id']) != row]
        if changed:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('a', encoding='utf-8') as stream:
                stream.write('\n'.join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in changed) + '\n')
            appended += len(changed)
    return appended


def archive_counts(root, week):
    records = {}
    for path in sorted((Path(root) / 'data/feed/archive').glob('????-??.jsonl')):
        for line in path.read_text(encoding='utf-8').splitlines():
            item = json.loads(line)
            records[item['id']] = item
    counts = Counter()
    for item in records.values():
        value = date.fromisoformat(str(item.get('first_seen') or item['published'])[:10])
        year, number, _ = value.isocalendar()
        if f'{year}-W{number:02d}' == week:
            counts[direction_of(item)['primary']] += 1
    return dict(sorted(counts.items()))
