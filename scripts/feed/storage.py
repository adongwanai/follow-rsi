"""Feed records keyed by id, with legacy duplicates resolved to the latest row."""
import json
from pathlib import Path


def feed_dir(root):
    return Path(root) / 'data' / 'feed'


def load_items(root):
    path = feed_dir(root) / 'items.jsonl'
    latest = {}
    if path.exists():
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            item = json.loads(line)
            if not isinstance(item, dict) or not isinstance(item.get('id'), str):
                raise ValueError(f'{path}:{number}: each record needs a string id')
            latest[item['id']] = item
    return list(latest.values())


def save_items(root, items):
    """Upsert complete snapshots by id; identical reruns leave the bytes intact.

    Rewriting also compacts a legacy append-only file to its latest row per id.
    """
    directory = feed_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    latest = {item['id']: item for item in load_items(root)}
    changed = 0
    for item in items:
        if latest.get(item['id']) != item:
            changed += 1
            latest[item['id']] = item
    content = ''.join(json.dumps(item, ensure_ascii=False, sort_keys=True) + '\n' for item in latest.values())
    path = directory / 'items.jsonl'
    if not path.exists() or path.read_text(encoding='utf-8') != content:
        pending = directory / 'items.jsonl.tmp'
        pending.write_text(content, encoding='utf-8')
        pending.replace(path)
    return changed


def load_state(root):
    path = feed_dir(root) / 'state.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'sources': {}}


def save_state(root, state):
    write_json(feed_dir(root) / 'state.json', state)


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def save_raw(root, source_id, date, payload):
    path = feed_dir(root) / 'raw' / source_id / f'{date}.json'
    write_json(path, payload)
    return path
