"""Discovery stays broad while every public output obeys Harness scope."""
from copy import deepcopy
import json

import pytest

from scripts.common import read_yaml
from scripts.feed.cli import process_items
from scripts.feed.digest import _write_feed, publish_day, publish_week
from scripts.feed.health import compute_metrics
from scripts.feed.promote import promote_candidates
from scripts.feed.review import queue_daily_review, queue_weekly_picks, validate_daily_review
from scripts.feed.scope import archive_counts, archive_out_of_scope, in_scope, load_scope
from scripts.feed.storage import load_items, save_items
from test_daily import DAY, accept_daily, make_daily_repo, write_daily
from test_review import WEEK


@pytest.mark.parametrize('primary,secondary,expected', [
    ('harness', [], True),
    ('evaluation_benchmark', ['harness'], True),
    ('theory_survey', ['model_weights', 'harness'], True),
    ('safety_governance', ['harness'], True),
    ('evaluation_benchmark', ['model_weights'], False),
    ('model_weights', ['harness'], False),
    ('ai4ai', ['harness'], False),
    (None, ['harness'], False),
    ('invented', ['harness'], False),
])
def test_cross_secondary_is_scoped_but_other_primary_directions_are_not(tmp_path, primary, secondary, expected):
    root = make_daily_repo(tmp_path)
    assert in_scope({'primary': primary, 'secondary': secondary}, load_scope(root)) is expected


def add_paper(root, ident, primary, secondary=None, label='include'):
    item = deepcopy(next(item for item in load_items(root) if item['id'] == 'arxiv:2610.99991'))
    item.update(id='arxiv:' + ident, arxiv_id=ident)
    item['llm'].update(label=label, primary=primary, secondary=secondary or [],
                       harness_sub='component' if primary == 'harness' else None)
    save_items(root, [item])
    return item


def test_outside_include_and_borderline_are_archived_once_and_never_queued(tmp_path):
    root = make_daily_repo(tmp_path)
    add_paper(root, '2610.99981', 'model_weights', ['harness'])
    add_paper(root, '2610.99982', 'ai4ai', label='borderline')
    add_paper(root, '2610.99983', 'theory_survey', ['harness'])
    add_paper(root, '2610.99984', None, label='error')
    before = (root / 'data/feed/items.jsonl').read_bytes()
    queue = queue_daily_review(root, DAY)
    queued = {row['arxiv_id'] for row in queue['items']}
    assert '2610.99983' in queued and '2610.99984' in queued
    assert '2610.99981' not in queued and '2610.99982' not in queued
    archive = root / 'data/feed/archive/2026-10.jsonl'
    data = [json.loads(line) for line in archive.read_text().splitlines()]
    assert len(data) == 2 and all(row['summary_zh'] and row['summary_en'] for row in data)
    archived = archive.read_bytes()
    queue_daily_review(root, DAY)
    assert archive.read_bytes() == archived
    assert (root / 'data/feed/items.jsonl').read_bytes() == before
    metrics = compute_metrics(root, week=WEEK)
    assert metrics['archive_by_direction'] == {'ai4ai': 1, 'model_weights': 1}
    assert archive_counts(root, WEEK) == metrics['archive_by_direction']


def test_outside_papers_still_receive_summary_before_archiving(tmp_path, monkeypatch):
    root = make_daily_repo(tmp_path)
    item = add_paper(root, '2610.99981', 'model_weights')
    del item['summary_zh'], item['summary_en']
    save_items(root, [item])
    assert archive_out_of_scope(root) == 0
    called = []
    def summarize(item, client, root):
        called.append(item['id'])
        return {**item, 'summary_zh': '保留更新以供后续训练使用。', 'summary_en': 'Retain updates for later training.'}
    monkeypatch.setattr('scripts.feed.judge.summarize_item', summarize)
    result = process_items(root, 'summarize', client=object())
    assert called == ['arxiv:2610.99981'] and result['archived'] == 1
    assert process_items(root, 'summarize', client=object())['archived'] == 0


def test_override_cannot_accept_outside_primary_even_with_harness_secondary(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    write_daily(root, lambda review: review['items'][1].update(direction_override={
        'primary': 'model_weights', 'secondary': ['harness']}))
    for action in (validate_daily_review, publish_day):
        with pytest.raises(ValueError, match='publish_scope'):
            action(root, DAY)
    with pytest.raises(ValueError, match='publish_scope'):
        promote_candidates(root, date=DAY)
    assert not (root / 'site/feed/latest.json').exists()


def test_unknown_classification_can_only_publish_after_in_scope_owner_override(tmp_path):
    root = make_daily_repo(tmp_path)
    item = next(item for item in load_items(root) if item['id'] == 'arxiv:2610.99991')
    item['llm'] = {'label': 'error', 'confidence': 0}
    save_items(root, [item])
    queue_daily_review(root, DAY)
    accept_daily(root)
    with pytest.raises(ValueError, match='invalid primary'):
        validate_daily_review(root, DAY)
    write_daily(root, lambda review: next(row for row in review['items'] if row['arxiv_id'] == '2610.99991').update(
        decision='move', direction_override='harness/improver'))
    assert publish_day(root, DAY)['accepted'] == 1


def test_cross_harness_publication_does_not_promote_cross_papers(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    write_daily(root, lambda review: review['items'][1].update(direction_override={
        'primary': 'evaluation_benchmark', 'secondary': ['harness']}))
    assert publish_day(root, DAY)['accepted'] == 1
    assert promote_candidates(root, date=DAY)['count'] == 0
    queue_weekly_picks(root, WEEK)
    assert publish_week(root, WEEK)['accepted'] == 1


def test_labs_need_explicit_in_scope_direction_and_cannot_bypass_scope(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    write_daily(root, lambda review: review['lab_updates'][0].update(decision='accept'))
    with pytest.raises(ValueError, match='invalid primary'):
        validate_daily_review(root, DAY)
    write_daily(root, lambda review: review['lab_updates'][0].update(direction_override='ai4ai'))
    with pytest.raises(ValueError, match='publish_scope'):
        validate_daily_review(root, DAY)
    write_daily(root, lambda review: review['lab_updates'][0].update(direction_override='harness/component'))
    publish_day(root, DAY)
    manifest = json.loads((root / 'site/daily' / f'{DAY}.json').read_text())
    assert manifest['lab_updates'][0]['direction']['primary'] == 'harness'


def test_old_outside_snapshot_cannot_leak_through_weekly_or_feed(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    publish_day(root, DAY)
    path = root / 'site/daily' / f'{DAY}.json'
    edition = json.loads(path.read_text())
    edition['items'][0]['direction'] = {'primary': 'model_weights', 'harness_sub': None, 'secondary': ['harness']}
    path.write_text(json.dumps(edition))
    queue_weekly_picks(root, WEEK)
    with pytest.raises(ValueError, match='publish_scope'):
        publish_week(root, WEEK)
    with pytest.raises(ValueError, match='publish_scope'):
        _write_feed(root, [], read_yaml(root / 'site.config.yaml'), set())
