from copy import deepcopy
from pathlib import Path
from scripts.feed.storage import load_items, save_items
from scripts.feed.normalize import normalize_record
from scripts.feed.dedupe import dedupe_items

NOW = '2026-10-27T12:00:00+00:00'


def item(**changes):
    return normalize_record({'arxiv_id': '2610.10001', 'title': 'Recursive agent improvement across tasks',
                             'abstract': 'An agent retains improvements.', 'source_hits': ['hf-daily'], **changes}, now=NOW)


def test_latest_record_upsert_and_idempotent_pipeline(tmp_path):
    paper = item()
    save_items(tmp_path, dedupe_items([paper], repo_papers=[]))
    path = tmp_path / 'data/feed/items.jsonl'
    original = path.read_bytes()
    save_items(tmp_path, dedupe_items([paper], load_items(tmp_path), []))
    assert path.read_bytes() == original
    changed = {**paper, 'summary_zh': '人工审核摘要'}
    assert save_items(tmp_path, [changed]) == 1
    assert len(path.read_text().splitlines()) == 1
    assert load_items(tmp_path) == [changed]
    third = {**changed, 'summary_zh': '再次核对的摘要'}
    assert save_items(tmp_path, [third]) == 1
    assert len(path.read_text().splitlines()) == 1
    assert load_items(tmp_path) == [third]


def test_versions_aliases_and_source_merge_preserve_review():
    first = item()
    first['llm'] = {'label': 'include', 'model': 'example'}
    first['review'] = {'decision': 'accept'}
    second = item(arxiv_id='2610.10001v2', title='A renamed recursive agent', source_hits=['arxiv-rsi'], hf_upvotes=8)
    combined = dedupe_items([second], [first], [{'id': 'repo-paper', 'arxiv': '2610.10001'}])[0]
    assert combined['version'] == 2 and combined['version_changed']
    assert combined['previous_version'] == 1 and combined['repo_id'] == 'repo-paper'
    assert combined['source_hits'] == ['arxiv-rsi', 'hf-daily']
    assert combined['llm'] == first['llm'] and combined['review'] == first['review']
    assert first['title'] in combined['aliases']


def test_conference_preprint_fuzzy_title_match_and_distinct_papers():
    paper = item()
    conference = item(arxiv_id=None, id='s2:conference', title=paper['title'].upper() + '.', links={'s2': 'https://example.com/paper'})
    records = dedupe_items([conference], [paper])
    assert len(records) == 1 and 's2:conference' in records[0]['aliases']
    unrelated = item(arxiv_id='2610.10002', title='Visual grounding for medical image analysis')
    assert len(dedupe_items([unrelated], records)) == 2


def test_new_source_same_version_does_not_erase_judgement():
    first = item()
    first.update(summary_zh='已审摘要', llm={'label': 'include'}, review={'decision': 'accept'})
    result = dedupe_items([item(source_hits=['rss-weco'])], [first])[0]
    assert result['summary_zh'] == first['summary_zh']
    assert result['llm'] == first['llm'] and result['review'] == first['review']


def test_daily_date_union_keeps_dates_and_decisions_across_sources(tmp_path):
    first = item(hf_daily_dates=['2026-10-14'])
    first.update(summary_zh='已审摘要', label='include', primary='harness',
                 llm={'label': 'include'}, review={'decision': 'accept'})
    save_items(tmp_path, [first])
    repeated = item(hf_daily_dates=['2026-10-16', '2026-10-14'],
                    first_seen='2026-10-28T12:00:00Z')
    arxiv = item(arxiv_id='2610.10001v2', source_hits=['arxiv-harness'])
    result = dedupe_items([repeated, arxiv], load_items(tmp_path))[0]
    assert result['hf_daily_dates'] == ['2026-10-14', '2026-10-16']
    assert result['source_hits'] == ['arxiv-harness', 'hf-daily']
    for field in ('first_seen', 'summary_zh', 'label', 'primary', 'llm', 'review'):
        assert result[field] == first[field]
    assert save_items(tmp_path, [result]) == 1
    assert len((tmp_path / 'data/feed/items.jsonl').read_text().splitlines()) == 1
    assert save_items(tmp_path, dedupe_items([repeated, arxiv], load_items(tmp_path))) == 0


def test_legacy_duplicate_migration_preserves_latest_review_and_other_ids(tmp_path):
    import json
    first = item()
    latest = {**first, 'summary_zh': '人工摘要', 'review': {'decision': 'accept'},
              'llm': {'label': 'include'}, 'hf_daily_dates': ['2026-10-14']}
    other = item(arxiv_id='2610.10002')
    path = tmp_path / 'data/feed/items.jsonl'
    path.parent.mkdir(parents=True)
    path.write_text(''.join(json.dumps(row) + '\n' for row in [first, other, latest]))
    assert save_items(tmp_path, []) == 0
    assert len(path.read_text().splitlines()) == 2
    assert {row['id']: row for row in load_items(tmp_path)} == {latest['id']: latest, other['id']: other}
