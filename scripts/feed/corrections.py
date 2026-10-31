"""Apply an explicit owner correction without rewriting the original review receipt."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from scripts.common import read_yaml
from scripts.feed.review import day_week, source_hash
from scripts.feed.scope import archive_out_of_scope
from scripts.feed.storage import load_items, save_items

GROUPS = ('keep_harness', 'defer', 'move_out_of_harness', 'general_rsi_eval_theory', 'reject')


def apply_correction(root, date, start=None, end=None):
    root = Path(root)
    path = root / 'review/corrections' / f'{date}.yaml'
    correction = read_yaml(path)
    if correction['date'] != date or correction['edition_action'] != 'retract_and_republish':
        raise ValueError('Correction must explicitly replace the withdrawn edition')
    withdrawn = json.loads((root / 'data/feed/withdrawn-editions.json').read_text())
    if date not in withdrawn:
        raise ValueError('Withdraw the original edition before applying its correction')
    groups = [(name, row) for name in GROUPS for row in correction[name]]
    ids = [f"arxiv:{row['arxiv']}" for _, row in groups]
    original = read_yaml(root / 'review/daily' / f'{date}.yaml')
    approved = {row['id'] for row in original['items'] if row['decision'] in ('accept', 'move')}
    if len(ids) != len(set(ids)) or set(ids) != approved:
        raise ValueError('Owner correction must cover every originally published paper exactly once')
    receipt = hashlib.sha256(path.read_bytes()).hexdigest()
    sources = {item['id']: item for item in load_items(root)}
    translations = read_yaml(root / 'review/corrections' / f'{date}.en.yaml')
    changed, kept = [], []
    for group, row in groups:
        item = deepcopy(sources['arxiv:' + row['arxiv']])
        direction = None
        decision = {'keep_harness': 'accept', 'defer': 'defer', 'reject': 'reject',
                    'move_out_of_harness': 'move', 'general_rsi_eval_theory': 'move'}[group]
        if group == 'keep_harness':
            direction = {'primary': 'harness', 'harness_sub': row['sub'], 'secondary': row.get('secondary', [])}
            item['gate'] = {
                'verdict': 'harness', 'harness_specific': 'yes', 'origin': 'owner_correction',
                'improved_object_zh': row['improved_object_zh'], 'why_zh': row['why_zh'],
                'feedback_driven': {'value': 'unclear', 'quote': None},
                'persists_across_tasks': {'value': 'unclear', 'quote': None},
            }
            item['evidence_quick']['code_released'] = {
                'value': row['code_released'],
                'quote': item['code_links'][0] if row['code_released'] == 'yes' else None,
            }
        elif group in ('move_out_of_harness', 'general_rsi_eval_theory'):
            direction = {'primary': row['primary'], 'harness_sub': None, 'secondary': row.get('secondary', [])}
        review = {'kind': 'correction', 'date': date, 'week': day_week(date), 'decision': decision,
                  'direction_override': direction, 'source_hash': source_hash(item),
                  'correction_file': str(path.relative_to(root)), 'correction_sha256': receipt,
                  'group': group, 'promote_to_repo': False,
                  'note': row.get('why_zh') or row.get('note_zh') or '不计入 Harness 专题方法数。'}
        if group == 'reject':
            review['exclude_reason'] = row['exclude_reason']
        if group == 'keep_harness':
            review['summary_override'] = {'summary_zh': row['why_zh'], 'summary_en': translations[row['arxiv']]}
        item['review'] = review
        changed.append(item)
        if group == 'keep_harness':
            public_source = deepcopy(item)
            public_source['llm'] = {**item['llm'], **direction}
            public_source.update(review['summary_override'])
            public_source['review_short_title'] = row['title']
            kept.append(public_source)
    from scripts.feed.library import curated_item
    for row in correction['missed_should_appear']['skipped_because_in_repo']:
        item = curated_item(sources['arxiv:' + row['arxiv']], root)
        item['review'] = {
            'kind': 'correction', 'date': date, 'week': day_week(date), 'decision': 'accept',
            'direction_override': None, 'source_hash': source_hash(item),
            'correction_file': str(path.relative_to(root)), 'correction_sha256': receipt,
            'group': 'skipped_because_in_repo', 'promote_to_repo': False,
            'note': '依据 owner 复审清单补回；摘要和证据直接取人工证据库。',
        }
        changed.append(item)
        kept.append({**item, 'review_short_title': row['title']})
    for item in kept:
        if item.get('retracted'):
            raise ValueError(f"{item['id']}: retracted items cannot be restored by a correction")
    if start and end:
        if start > end:
            raise ValueError('Retrospective dates are reversed')
        for item in kept:
            if not any(start <= day <= end for day in item.get('hf_daily_dates', [])):
                raise ValueError(f"{item['id']}: no observed HF recommendation in the retrospective window")
    save_items(root, changed)
    archive_out_of_scope(root)
    return kept, receipt


def publish_corrected_recap(root, date, start, end):
    """This explicit operation uses the owner's keep list, never automatic include labels."""
    from scripts.feed.digest import _directions, _public_item, render_recap
    root = Path(root)
    kept, receipt = apply_correction(root, date, start, end)
    repository = read_yaml(root / 'data/papers.yaml')['papers']
    week = day_week(end)
    items = []
    from scripts.feed.window import publication_dates
    for item in sorted(kept, key=lambda item: (item['published'], item['id']), reverse=True):
        item.update(publication_dates(item, end, start))
        item['window_status'] = 'backlog'
        public = _public_item(item, {'decision': 'accept'}, week, repository)
        public.update(short_title=item['review_short_title'], review_date=date, daily_section='historical')
        items.append(public)
    path = root / 'site/recaps' / f'{start}--{end}.json'
    previous = json.loads(path.read_text()) if path.exists() else None
    stamp = previous['published_at'] if previous else datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    directions = _directions(read_yaml(root / 'feed/taxonomy.yaml'))
    edition = {'kind': 'retrospective', 'date': date, 'week': week, 'start': start, 'end': end,
               'title_zh': '创刊回顾 · 10 月 14–27 日', 'title_en': 'Inaugural retrospective · October 14–27',
               'published_at': stamp, 'reviewed_only': True, 'review_source': f'review/corrections/{date}.yaml',
               'review_sha256': receipt, 'items': items, 'lab_updates': [], 'picks': [],
               'counts': {key: sum(item['direction']['primary'] == key for item in items) for key in directions},
               'source_runs': json.loads((root / 'site/feed/status.json').read_text()).get('last_fetch', {}),
               'intro': {'zh': f'依据人工复审与证据库补回清单整理 {len(items)} 篇专题论文，汇集 10 月 14–27 日的 HF 推荐。每篇分别标注推荐日和原始发表日；这是创刊回顾。从 10 月 28 日起，今日动态按 HF 当日推荐榜与其他信源的新动态整理，经审核后发布。',
                         'en': f'This retrospective includes {len(items)} papers from the owner correction and evidence-library restoration list, recommended by HF during October 14–27. Recommendation and original publication dates are shown separately. Starting October 28, daily editions follow HF daily recommendations and new updates from other sources, subject to owner review.'}}
    render_recap(root, edition)
    return edition
