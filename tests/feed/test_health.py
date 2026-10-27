from unittest.mock import Mock
from pathlib import Path
import shutil
import pytest
from scripts.common import ROOT
import json
from scripts.feed.health import update_health, compute_metrics, version_alerts, publication_times
from scripts.feed.storage import load_state, save_items
from scripts.feed.normalize import normalize_record

NOW = '2026-10-27T12:00:00+00:00'


@pytest.fixture(autouse=True)
def scope_config(tmp_path):
    (tmp_path / 'feed').mkdir()
    for name in ('sources.yaml', 'taxonomy.yaml'):
        shutil.copyfile(ROOT / 'feed' / name, tmp_path / 'feed' / name)


def test_three_empty_runs_open_once_and_recovery_closes(tmp_path):
    client = Mock()
    client.find.return_value = None
    client.create.return_value = 7
    bad = [{'source_id': 'hf-daily', 'ok': True, 'count': 0, 'ids': []}]
    for _ in range(4):
        update_health(tmp_path, bad, NOW, client)
    client.create.assert_called_once()
    assert load_state(tmp_path)['sources']['hf-daily']['issue_number'] == 7
    good = [{'source_id': 'hf-daily', 'ok': True, 'count': 1, 'ids': ['arxiv:2610.10001']}]
    update_health(tmp_path, good, NOW, client)
    client.close.assert_called_once_with(7)
    assert 'issue_number' not in load_state(tmp_path)['sources']['hf-daily']


def test_local_health_never_writes_issues_and_counts_unique_items(tmp_path):
    bad = [{'source_id': 'arxiv-rsi', 'ok': False, 'count': 0, 'error': '503 unavailable'}]
    for _ in range(3):
        status = update_health(tmp_path, bad, NOW)
    assert status['pending_issue_actions'][0]['title'] == 'Source down: arxiv-rsi'
    assert load_state(tmp_path)['sources']['arxiv-rsi']['consecutive_errors'] == 3
    good = [{'source_id': 'hf-daily', 'ok': True, 'count': 1, 'ids': ['same']}]
    for _ in range(2):
        update_health(tmp_path, good, NOW)
    assert load_state(tmp_path)['sources']['hf-daily']['weekly']['2026-W44'] == 1
    status = update_health(tmp_path, [], '2026-10-30T12:00:00+00:00')
    assert status['age_hours'] == 72
    assert json.loads((tmp_path / 'badges/feed-updated.json').read_text())['color'] == 'red'
    assert (tmp_path / 'site/badges/feed-updated.json').read_bytes() == (tmp_path / 'badges/feed-updated.json').read_bytes()


def test_version_alerts_and_retraction_are_explicit(tmp_path):
    paper = normalize_record({'title': 'Test', 'arxiv_id': '2610.10001v2', 'in_repo': True}, now=NOW)
    paper.update(version_changed=True, repo_id='test')
    client = Mock()
    client.find.return_value = None
    client.create.return_value = 9
    assert '出了 v2' in version_alerts(tmp_path, [paper], client)[0]['title']
    assert version_alerts(tmp_path, [paper], client) == []
    client.create.assert_called_once()
    paper['retracted'] = True
    assert version_alerts(tmp_path, [paper])[0]['title'].startswith('Retraction:')


def test_metrics_preserve_recall_and_report_first_guard_failure(tmp_path):
    paper = normalize_record({'title': 'Test', 'arxiv_id': '2610.10001', 'published': '2026-10-20', 'source_hits': ['hf-daily']}, now=NOW)
    paper.update(llm={'label': 'include', 'primary': 'harness', 'harness_sub': 'component', 'secondary': []}, summary_zh='摘要', initial_guard_failed=True,
                 review={'week': '2026-W44', 'decision': 'accept', 'reviewed_at': NOW})
    save_items(tmp_path, [paper])
    daily = tmp_path / 'site/daily/2026-10-28.json'
    daily.parent.mkdir(parents=True)
    daily.write_text(json.dumps({'reviewed_only': True, 'published_at': '2026-10-28T12:00:00Z',
                                 'items': [{'id': paper['id']}]}))
    result = compute_metrics(tmp_path, week='2026-W44')
    assert result['found'] == result['accepted'] == 1
    assert result['precision'] == result['guard_fail_rate'] == 1
    assert result['latency_days'] == 8.5
    assert result['source_yield'] == {'hf-daily': {'accepted': 1, 'exclusive': 1}}


def test_pending_and_deferred_items_do_not_lower_reviewed_precision(tmp_path):
    items = []
    for index, decision in enumerate(['accept', 'reject', 'defer', 'pending']):
        item = normalize_record({'title': decision, 'arxiv_id': f'2610.{index:05}',
                                 'published': '2026-10-20'}, now=NOW)
        item.update(llm={'label': 'include', 'primary': 'harness', 'harness_sub': 'component', 'secondary': []}, review={'week': '2026-W44', 'decision': decision})
        items.append(item)
    result = compute_metrics(tmp_path, items=items, week='2026-W44')
    assert result['found'] == 4 and result['accepted'] == 1
    assert result['precision'] == .5
    assert result['latency_days'] is None


def test_publication_latency_uses_first_actual_daily_edition_not_demo(tmp_path):
    directory = tmp_path / 'site/daily'
    directory.mkdir(parents=True)
    for day, extra in [('25', {'demo': True}), ('27', {}), ('28', {})]:
        (directory / f'2026-10-{day}.json').write_text(json.dumps({
            'reviewed_only': True, 'published_at': f'2026-10-{day}T12:00:00Z',
            'items': [{'id': 'paper'}], **extra}))
    assert publication_times(tmp_path)['paper'].isoformat() == '2026-10-27T12:00:00+00:00'
