#!/usr/bin/env python3
"""Check or resume the frozen 2026-10-30 work in a separate local directory.

check and prepare are offline. Only the explicit run command calls the existing
model pipeline. No command integrates results, reviews, queues, or publishes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import unicodedata

PACKAGE = Path(__file__).resolve().parent
SOURCE_FIELDS = ('kind', 'title', 'abstract', 'version', 'comments')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def record_hash(item):
    return sha(json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def source_hash(item):
    values = {key: ' '.join(unicodedata.normalize('NFKC', item[key]).split())
              if isinstance(item.get(key), str) else item.get(key) for key in SOURCE_FIELDS}
    return record_hash(values)


def read_rows(path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    result = {row['id']: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f'Duplicate IDs: {path}')
    return result


def verify_package():
    manifest = json.loads((PACKAGE / 'package-manifest.json').read_text())
    for row in manifest['files']:
        if sha((PACKAGE / row['path']).read_bytes()) != row['sha256']:
            raise ValueError(f'Frozen package changed: {row["path"]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'prepare', 'run'))
    parser.add_argument('--root', type=Path, default=PACKAGE.parents[4])
    parser.add_argument('--stage', choices=('judge', 'summarize'))
    parser.add_argument('--workdir', type=Path)
    parser.add_argument('--env-file', type=Path)
    parser.add_argument('--workers', type=int, default=1)
    args = parser.parse_args()
    root = args.root.resolve()
    verify_package()
    plan = json.loads((PACKAGE / 'resume-plan.json').read_text())
    frozen = read_rows(PACKAGE / 'item-status.jsonl')
    current = read_rows(root / 'data/feed/items.jsonl')
    changed = [ident for ident, row in frozen.items()
               if ident not in current or record_hash(current[ident]) != row['canonical_record_sha256']]
    if args.action == 'check':
        print(json.dumps({'status': 'offline_check_complete', 'frozen_ids': len(frozen),
                          'current_ids': len(current), 'changed_or_missing_ids': changed,
                          'queue_counts': plan['queue_counts'], 'network_requests': 0,
                          'publication_authorized': False}, ensure_ascii=False, indent=2))
        return
    if not args.stage or not args.workdir:
        parser.error('prepare/run require --stage and --workdir')
    queue = 'retry_model_api' if args.stage == 'judge' else 'resume_summary'
    ids = plan['queues'][queue]
    work = args.workdir.resolve()
    if not work.is_relative_to(root / 'build') or work == root / 'build':
        parser.error('--workdir must be a new subdirectory of repository build/')
    if args.action == 'prepare':
        altered_targets = sorted(set(ids) & set(changed))
        if altered_targets:
            raise ValueError('Frozen targets changed; reconcile before continuation: ' + ', '.join(altered_targets))
        work.mkdir(parents=True, exist_ok=False)
        (work / 'feed').mkdir()
        shutil.copytree(root / 'feed/prompts', work / 'feed/prompts')
        for name in ('model.yaml', 'sources.yaml', 'taxonomy.yaml'):
            shutil.copy2(root / 'feed' / name, work / 'feed' / name)
        (work / 'data/feed').mkdir(parents=True)
        shutil.copy2(root / 'data/papers.yaml', work / 'data/papers.yaml')
        shutil.copytree(root / 'data/feed/cache', work / 'data/feed/cache')
        selected = [current[ident] for ident in ids]
        assert all(not row.get('in_repo') and row.get('review', {}).get('kind') != 'correction'
                   for row in selected)
        (work / 'data/feed/items.jsonl').write_text(
            ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in selected))
        (work / 'resume-receipt.json').write_text(json.dumps({
            'stage': args.stage, 'ids': ids, 'canonical_sha256_at_prepare': sha((root / 'data/feed/items.jsonl').read_bytes()),
            'frozen_plan_sha256': sha((PACKAGE / 'resume-plan.json').read_bytes()),
            'network_requests': 0, 'publication_authorized': False,
        }, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'status': 'prepared_offline', 'stage': args.stage, 'ids': len(ids),
                          'workdir': str(work.relative_to(root)), 'network_requests': 0}, ensure_ascii=False))
        return
    receipt = json.loads((work / 'resume-receipt.json').read_text())
    if (receipt['stage'] != args.stage or receipt['ids'] != ids
            or receipt['frozen_plan_sha256'] != sha((PACKAGE / 'resume-plan.json').read_bytes())):
        raise ValueError('Prepared continuation does not match this frozen plan')
    saved = read_rows(work / 'data/feed/items.jsonl')
    if set(saved) != set(ids):
        raise ValueError('Prepared IDs changed')
    for ident, item in saved.items():
        if (source_hash(item) != frozen[ident]['source_input_sha256']
                or item.get('review') != frozen[ident]['historical_owner_review']
                or item.get('in_repo') or item.get('review', {}).get('kind') == 'correction'):
            raise ValueError(f'Protected source/owner state changed: {ident}')
    sys.path.insert(0, str(root))
    from scripts.feed.cli import configure, process_items
    configure(work, args.env_file)
    result = process_items(work, args.stage, workers=args.workers)
    print(json.dumps({'result': result, 'output_directory': str(work.relative_to(root)),
                      'canonical_updated': False, 'publication_authorized': False}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
