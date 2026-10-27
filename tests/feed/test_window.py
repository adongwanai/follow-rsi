"""Dates, publication history and human approvals are independent boundaries."""
from copy import deepcopy
import json
import pytest
from scripts.feed.window import publication_dates, daily_metadata
from scripts.feed.review import queue_daily_review, validate_daily_review, approved_daily_items
from scripts.feed.storage import load_items, save_items
from test_daily import DAY, make_daily_repo, write_daily


def test_daily_window():
    statuses = []
    for day in ('2026-10-07', '2026-10-26', '2026-10-27'):
        statuses.append(publication_dates({'id': day, 'published': day, 'first_seen': DAY}, DAY, '2026-10-25')['window_status'])
    assert statuses == ['backlog', 'in_window', 'in_window']
    assert publication_dates({'id': 'old', 'published': '2026-09-01', 'first_seen': DAY}, DAY, '2026-10-25')['window_status'] == 'stale'


def test_hf_recommendation_is_not_original_paper_date_or_first_seen():
    item = {'id': 'x', 'published': '2026-10-05', 'first_seen': DAY, 'hf_daily_dates': ['2026-10-27']}
    timing = publication_dates(item, DAY, '2026-10-25')
    assert timing['announced'] == '2026-10-05'
    assert timing['news_date'] == DAY and timing['window_status'] == 'in_window'
    item['hf_daily_dates'] = ['2026-10-20']
    assert publication_dates(item, DAY, '2026-10-25')['window_status'] == 'backlog'
    item['backfill_only'] = True
    item['hf_daily_dates'] = [DAY]
    assert publication_dates(item, DAY, '2026-10-25')['window_status'] == 'backlog'


def test_backlog_cannot_be_accepted_as_daily(tmp_path):
    root = make_daily_repo(tmp_path)
    item = next(i for i in load_items(root) if i['id'] == 'arxiv:2610.99991')
    item.update(published='2026-10-07', updated='2026-10-07')
    save_items(root, [item])
    queue_daily_review(root, DAY)
    write_daily(root, lambda review: next(r for r in review['items'] if r['id'] == item['id']).update(decision='accept'))
    with pytest.raises(ValueError, match='window_status=in_window'):
        validate_daily_review(root, DAY)
    write_daily(root, lambda review: next(r for r in review['items'] if r['id'] == item['id']).update(decision='backlog'))
    validate_daily_review(root, DAY)
    assert approved_daily_items(root, DAY) == []


def test_recap_ids_do_not_reappear_in_daily(tmp_path):
    folder = tmp_path / 'site/recaps'; folder.mkdir(parents=True)
    (folder / '2026-10-14--2026-10-27.json').write_text(json.dumps({'kind':'retrospective', 'date':DAY, 'end':DAY, 'items':[{'id':'seen'}]}))
    assert daily_metadata(tmp_path, {'id':'seen','published':DAY,'hf_daily_dates':[DAY]}, DAY)['window_status'] == 'already_published'
    assert daily_metadata(tmp_path, {'id':'seen','published':DAY,'hf_daily_dates':['2026-10-28']}, '2026-10-28')['window_status'] == 'already_published'


def test_curated_item_uses_library_without_llm(tmp_path):
    import yaml
    from scripts.common import ROOT, read_yaml
    from scripts.feed.cli import process_items
    collection = read_yaml(ROOT / 'data/papers.yaml')
    paper = next(p for p in collection['papers'] if p['id'] == 'riseharness')
    root = make_daily_repo(tmp_path)
    collection['papers'] = [paper]
    (root / 'data/papers.yaml').write_text(yaml.safe_dump(collection, allow_unicode=True, sort_keys=False))
    item = deepcopy(load_items(root)[0])
    item.update(id='arxiv:'+paper['arxiv'], arxiv_id=paper['arxiv'], repo_id=paper['id'], in_repo=True)
    for key in ('llm','summary_zh','summary_en'):
        item.pop(key, None)
    save_items(root, [item])
    class NoAPI:
        def __getattr__(self, name):
            raise AssertionError('Curated records must not call an LLM')
    process_items(root, 'judge', client=NoAPI())
    actual = next(i for i in load_items(root) if i['id'] == item['id'])
    assert actual['summary_zh'] == paper['summary_zh']
    assert actual['summary_en'] == paper['summary_en']
    assert actual['llm']['origin'] == 'evidence_library'
