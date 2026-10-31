#!/usr/bin/env python3
"""Prepare a named continuation queue offline; never call a model or publish."""
import argparse
import json
from pathlib import Path
import shutil
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[3]
sys.path.insert(0, str(ROOT))

from scripts.feed.review import source_hash
from scripts.feed.storage import load_items, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue', choices=('resume_summary', 'retry_model_api', 'classify_new_papers'))
    parser.add_argument('--workdir', type=Path)
    args = parser.parse_args()
    plan = json.loads((PACKAGE / 'resume-plan.json').read_text())
    items = {row['id']: row for row in load_items(ROOT)}
    selected = plan['queues'][args.queue] if args.queue else list(plan['source_and_owner_guards'])
    for ident in selected:
        item = items[ident]
        expected = plan['source_and_owner_guards'][ident]
        if (source_hash(item) != expected['source_hash'] or item.get('review') != expected['owner_review']
                or item.get('in_repo', False) != expected['in_repo']):
            raise ValueError(f'Source or owner state changed; reconcile before continuing: {ident}')
    if not args.queue:
        print(json.dumps({'verified_ids': len(selected), 'queue_counts': plan['queue_counts'],
                          'network_requests': 0, 'publication_authorized': False}))
        return
    if args.workdir is None:
        parser.error('--queue requires --workdir')
    work = args.workdir.resolve()
    if not work.is_relative_to(ROOT / 'build') or work == ROOT / 'build':
        parser.error('--workdir must be a new subdirectory of repository build/')
    if any(items[key].get('in_repo') or items[key].get('review', {}).get('kind') == 'correction' for key in selected):
        raise ValueError('Protected catalog or owner correction in a model queue')
    work.mkdir(parents=True, exist_ok=False)
    (work / 'feed').mkdir()
    shutil.copytree(ROOT / 'feed/prompts', work / 'feed/prompts')
    for name in ('model.yaml', 'sources.yaml', 'taxonomy.yaml'):
        shutil.copy2(ROOT / 'feed' / name, work / 'feed' / name)
    (work / 'data/feed').mkdir(parents=True)
    shutil.copy2(ROOT / 'data/papers.yaml', work / 'data/papers.yaml')
    shutil.copytree(ROOT / 'data/feed/cache', work / 'data/feed/cache')
    (work / 'data/feed/items.jsonl').write_text(''.join(
        json.dumps(items[key], ensure_ascii=False, sort_keys=True) + '\n' for key in selected))
    stage = 'summarize' if args.queue == 'resume_summary' else 'judge'
    receipt = {'queue': args.queue, 'stage': stage, 'ids': selected, 'prepared_ids': len(selected),
               'plan': 'docs/internal/reports/maintenance-2026-10-31/resume-plan.json',
               'network_requests': 0, 'canonical_updated': False, 'publication_authorized': False}
    write_json(work / 'resume-receipt.json', receipt)
    print(json.dumps({**receipt, 'workdir': str(work.relative_to(ROOT))}, ensure_ascii=False))


if __name__ == '__main__':
    main()
