import pytest

from scripts.feed.review import queue_daily_review, validate_daily_review
from scripts.feed.storage import load_items, save_items
from test_daily import DAY, NEXT, accept_daily, make_daily_repo


def test_library_members_still_enter_news_review_with_real_source_dates(tmp_path):
    root = make_daily_repo(tmp_path)
    item = next(row for row in load_items(root) if row['arxiv_id'] == '2610.99991')
    item.update(in_repo=True, published='2026-10-05T00:00:00Z', updated='2026-10-05T00:00:00Z',
                first_seen=DAY + 'T08:00:00Z', hf_daily_dates=['2026-10-20'])
    save_items(root, [item])
    review = queue_daily_review(root, DAY)
    row = next(row for row in review['items'] if row['id'] == item['id'])
    assert row['decision'] == 'defer'
    assert row['published'] == '2026-10-05T00:00:00Z'
    assert row['hf_daily_dates'] == ['2026-10-20']
    assert row['daily_section'] == 'historical'
    item['hf_daily_dates'].append(DAY)
    save_items(root, [item])
    row = next(row for row in queue_daily_review(root, DAY)['items'] if row['id'] == item['id'])
    assert row['daily_section'] == 'hf_today'


def test_recommendation_date_change_invalidates_old_approval(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    item = next(row for row in load_items(root) if row['arxiv_id'] == '2610.99991')
    item['hf_daily_dates'] = ['2026-10-20']
    save_items(root, [item])
    with pytest.raises(ValueError, match='source changed'):
        validate_daily_review(root, DAY)
    row = next(row for row in queue_daily_review(root, DAY)['items'] if row['id'] == item['id'])
    assert row['decision'] == 'defer'


def test_owner_correction_prevents_original_acceptance_from_recurring(tmp_path):
    from scripts.feed.review import source_hash
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    item = next(row for row in load_items(root) if row['arxiv_id'] == '2610.99991')
    item['review'] = {'kind': 'correction', 'date': DAY, 'decision': 'reject',
                      'source_hash': source_hash(item)}
    save_items(root, [item])
    for day in (DAY, NEXT):
        assert item['id'] not in {row['id'] for row in queue_daily_review(root, day)['items']}


def test_owner_correction_deferral_overrides_original_acceptance(tmp_path):
    from scripts.feed.review import source_hash
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    item = next(row for row in load_items(root) if row['arxiv_id'] == '2610.99991')
    item['review'] = {'kind': 'correction', 'date': DAY, 'decision': 'defer',
                      'note': 'Owner requires a full-text check.', 'source_hash': source_hash(item)}
    save_items(root, [item])
    for day in (DAY, NEXT):
        row = next(row for row in queue_daily_review(root, day)['items'] if row['id'] == item['id'])
        assert row['decision'] == 'defer'
        assert row['note'] == item['review']['note']
