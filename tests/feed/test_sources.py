from datetime import datetime, timezone
import json
from pathlib import Path
from unittest.mock import Mock
import pytest
from scripts.feed import fetch_arxiv, fetch_hf, fetch_rss, fetch_s2, fetch_github
from scripts.feed.normalize import normalize_record, split_arxiv

FIX = Path(__file__).parent / 'fixtures'
NOW = '2026-10-27T12:00:00+00:00'


def test_recorded_arxiv_metadata_only():
    items = fetch_arxiv.parse_atom((FIX / 'arxiv.xml').read_text(), now=NOW)
    assert items[0]['arxiv_id'] == '2505.22954'
    assert items[0]['title'] and items[0]['authors'] and items[0]['abstract']
    assert items[0]['version'] >= 1
    assert not any('pdf' in url for url in items[0]['links'].values())


def test_arxiv_ids_old_versions_and_retraction():
    assert split_arxiv('https://arxiv.org/abs/cs/0309048v3') == ('cs/0309048', 3)
    item = normalize_record({'arxiv_id': '2610.10001v2', 'title': 'Test', 'comments': 'This manuscript was withdrawn.'}, now=NOW)
    assert item['version'] == 2 and item['retracted']
    assert item['id'] == 'arxiv:2610.10001'


def test_arxiv_invalid_boundary_and_rate_limit(monkeypatch):
    with pytest.raises(ValueError):
        fetch_arxiv.parse_atom('<html/>')
    session = Mock()
    session.get.return_value.text = (FIX / 'arxiv.xml').read_text()
    sleep = Mock()
    monkeypatch.setattr(fetch_arxiv.time, 'monotonic', lambda: 10.0)
    monkeypatch.setattr(fetch_arxiv.time, 'sleep', sleep)
    monkeypatch.setattr(fetch_arxiv, '_last_request', 9.0)
    fetch_arxiv.request({'id_list': '2505.22954'}, session)
    sleep.assert_called_once_with(2.0)
    assert 'User-Agent' in session.get.call_args.kwargs['headers']


def test_hf_uses_original_abstract_and_real_code():
    raw = json.loads((FIX / 'hf.json').read_text())
    result = fetch_hf.parse_json(raw, now=NOW)[0]
    assert result['abstract'] == ' '.join(raw[0]['paper']['summary'].split())
    assert result['abstract'] != raw[0]['paper']['ai_summary']
    assert result['hf_upvotes'] == raw[0]['paper']['upvotes']
    assert result['links']['hf'].endswith(raw[0]['paper']['id'])
    assert raw[0]['paper']['githubRepo'] in result['code_links']
    assert fetch_hf.parse_json(raw, keywords=['zzzz-unmatched-keyword'], now=NOW) == []


def test_hf_covers_each_requested_day_without_network():
    session = Mock()
    session.get.return_value.json.return_value = json.loads((FIX / 'hf.json').read_text())
    source = {'id': 'hf-daily', 'params': {'url': 'https://huggingface.co/api/daily_papers', 'keywords': []}}
    records, raw = fetch_hf.fetch(source, datetime(2026, 10, 27, tzinfo=timezone.utc), session, days=14)
    assert session.get.call_count == 14
    dates = [call.kwargs['params']['date'] for call in session.get.call_args_list]
    assert dates[0] == '2026-10-27' and dates[-1] == '2026-10-14'
    assert len(raw['days']) == 14 and len(records) == 14


def test_s2_schema_mock_and_author_heuristic(monkeypatch):
    items = fetch_s2.parse_json(json.loads((FIX / 's2_mock.json').read_text()), seed_id='dgm', now=NOW)
    assert items[0]['seed_hits'] == ['dgm'] and items[0]['arxiv_id'] == '2610.10001'
    assert items[0]['code_links'] == ['https://github.com/example/agent']
    authors = fetch_s2.select_authors([
        {'authors': [{'name': 'A', 'authorId': '1'}, {'name': 'B', 'authorId': '2'}]},
        {'authors': [{'name': 'A', 'authorId': '1'}, {'name': 'C', 'authorId': '3'}]},
    ])
    assert {a['authorId'] for a in authors} == {'1', '2', '3'}
    assert authors[0]['seed_appearances'] == 2
    monkeypatch.delenv('S2_API_KEY', raising=False)
    with pytest.raises(ValueError, match='S2_API_KEY'):
        fetch_s2.request('paper/test')


def test_rss_recording_and_paper_link_hydration():
    records = fetch_rss.parse_feed((FIX / 'rss.xml').read_text(), 'rss-weco', NOW)
    assert records and all(item['kind'] in {'paper', 'post'} for item in records)
    body = '<rss version="2.0"><channel><title>Lab</title><item><title>Lab commentary</title><link>https://lab.example/post</link><description>Read https://arxiv.org/abs/2610.10001v2</description></item></channel></rss>'
    item = fetch_rss.parse_feed(body, 'rss-lab', NOW)[0]
    assert item['arxiv_id'] == '2610.10001'
    assert item['metadata_pending'] and item['abstract'] == ''
    assert item['links']['post'] == 'https://lab.example/post'
    with pytest.raises(ValueError):
        fetch_rss.parse_feed('<html>Not a feed</html>', 'bad')


def test_github_recorded_versions_and_repository_urls():
    rows = json.loads((FIX / 'github.json').read_text())
    result = fetch_github.parse_json(rows, 'simular-ai/Agent-S', now=NOW)
    assert result[0]['release_version'] == rows[0]['tag_name']
    assert result[0]['abstract'] == ''
    assert result[0]['links']['url'] == rows[0]['html_url']
    repos = fetch_github.repositories([{'code': 'https://github.com/a/b/tree/main'}, {'code': 'https://github.com/organization'}, {'code': 'https://example.com/a/b'}])
    assert repos == ['a/b']


def test_seed_selection_and_limit():
    papers = [{'id': 'x', 'arxiv': '2610.10001', 'section': 'foundations'},
              {'id': 'hgm', 'arxiv': '2610.10002', 'section': 'improver'},
              {'id': 'y', 'arxiv': '2610.10003', 'section': 'component'},
              {'id': 'z', 'arxiv': '2610.10004', 'section': 'component', 'must_read': True}]
    assert [p['id'] for p in fetch_s2.seed_papers(papers)] == ['x', 'hgm', 'z']
    metadata = [{'authors': [{'authorId': str(i), 'name': str(i)}]} for i in range(200)]
    assert len(fetch_s2.select_authors(metadata)) == 150


def test_registry_dispatch_selects_hf_and_persists_raw(tmp_path, monkeypatch):
    import yaml
    (tmp_path / 'feed').mkdir()
    registry = {'sources': [
        {'id': 'hf-daily', 'kind': 'hf_daily', 'schedule': 'daily', 'enabled': True, 'params': {}},
        {'id': 'arxiv-rsi', 'kind': 'arxiv_query', 'schedule': 'daily', 'enabled': True, 'params': {}},
        {'id': 's2-citations', 'kind': 's2_citations', 'schedule': 'weekly', 'enabled': False, 'params': {}},
    ]}
    (tmp_path / 'feed/sources.yaml').write_text(yaml.safe_dump(registry))
    hf = Mock(return_value=(fetch_hf.parse_json(json.loads((FIX / 'hf.json').read_text()), now=NOW), {'format': 'test-recording'}))
    arxiv = Mock()
    monkeypatch.setattr(fetch_hf, 'fetch', hf)
    monkeypatch.setattr(fetch_arxiv, 'fetch', arxiv)
    result = fetch_arxiv.fetch_sources(tmp_path, days=14, now=NOW, source_ids=['hf-daily'])
    assert result['outcomes'][0]['count'] == 1
    assert hf.call_args.kwargs['days'] == 14
    arxiv.assert_not_called()
    assert (tmp_path / 'data/feed/raw/hf-daily/2026-10-27.json').exists()


def test_rss_post_dates_filter_before_hydration():
    session = Mock()
    session.get.return_value.text = '''<rss version="2.0"><channel><title>Lab</title><item><title>Old paper link</title><link>https://example.com/old</link><pubDate>Wed, 01 Jan 2025 00:00:00 GMT</pubDate><description>https://arxiv.org/abs/2501.10001</description></item></channel></rss>'''
    source = {'id': 'rss-lab', 'params': {'url': 'https://example.com/feed', 'lookback_days': 14}}
    items, raw = fetch_rss.fetch(source, datetime(2026, 10, 27, tzinfo=timezone.utc), session)
    assert items == []
