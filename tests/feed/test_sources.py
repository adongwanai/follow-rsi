from datetime import datetime, timezone
import json
from pathlib import Path
from unittest.mock import Mock
import pytest
import requests
from scripts.feed import fetch_arxiv, fetch_hf, fetch_rss, fetch_s2, fetch_github
from scripts.feed.normalize import normalize_record, split_arxiv, arxiv_ids

FIX = Path(__file__).parent / 'fixtures'
NOW = '2026-10-27T12:00:00+00:00'


def hf_response(payload, status=200):
    response = requests.Response()
    response.status_code = status
    response.url = 'https://huggingface.co/api/daily_papers'
    response._content = json.dumps(payload).encode()
    response.encoding = 'utf-8'
    return response


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


def test_rss_financial_archive_link_is_not_an_old_arxiv_identifier():
    sec = 'https://www.sec.gov/Archives/edgar/data/1526520/000110465925041251/example.htm'
    assert split_arxiv(sec) == (None, 0)
    assert arxiv_ids(sec + ' and https://arxiv.org/abs/cs/0309048v3') == ['cs/0309048']


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
    session.get.return_value = hf_response(json.loads((FIX / 'hf.json').read_text()))
    source = {'id': 'hf-daily', 'params': {'url': 'https://huggingface.co/api/daily_papers', 'keywords': []}}
    records, raw = fetch_hf.fetch(source, datetime(2026, 10, 27, tzinfo=timezone.utc), session, days=14)
    assert session.get.call_count == 14
    dates = [call.kwargs['params']['date'] for call in session.get.call_args_list]
    assert dates[0] == '2026-10-27' and dates[-1] == '2026-10-14'
    assert len(raw['days']) == 14 and len(records) == 14
    assert [item['hf_daily_dates'] for item in records] == [[date] for date in dates]
    assert raw['status'] == 'ok' and raw['errors'] == {}


def test_hf_not_ready_day_keeps_other_days_and_actual_request_times(monkeypatch):
    current = datetime(2026, 10, 30, tzinfo=timezone.utc)
    clock = Mock(wraps=datetime)
    times = [datetime(2026, 10, 30, 0, 3, second, tzinfo=timezone.utc) for second in range(4)]
    clock.now.side_effect = times
    monkeypatch.setattr(fetch_hf, 'datetime', clock)
    error = {'error': '✖ "date" must be less than or equal to "2026-10-29T00:00:00.000Z"\n  → at date'}
    session = Mock()
    session.get.side_effect = [hf_response(error, 400), hf_response(json.loads((FIX / 'hf.json').read_text()))]
    source = {'id': 'hf-daily', 'params': {'url': 'https://huggingface.co/api/daily_papers'}}
    records, raw = fetch_hf.fetch(source, current, session, days=2)
    assert [item['hf_daily_dates'] for item in records] == [['2026-10-29']]
    assert list(raw['days']) == ['2026-10-29'] and raw['status'] == 'partial'
    assert list(raw['errors']) == ['2026-10-30']
    today, yesterday = raw['attempts']['2026-10-30'], raw['attempts']['2026-10-29']
    assert today['status'] == 'not_ready' and today['http_status'] == 400
    assert today['available_through'] == '2026-10-29'
    assert json.loads(today['response_body']) == error
    assert today['params'] == {'date': '2026-10-30'}
    assert today['requested_at'] == times[0].isoformat() and today['finished_at'] == times[1].isoformat()
    assert yesterday['status'] == 'ok' and yesterday['http_status'] == 200
    assert yesterday['requested_at'] == times[2].isoformat() and yesterday['finished_at'] == times[3].isoformat()


@pytest.mark.parametrize(('status', 'message'), [
    (400, 'Invalid request'),
    (429, 'Rate limit exceeded'),
    (500, 'Server error'),
    (429, '"date" must be less than or equal to "2026-10-29T00:00:00.000Z"'),
    (400, '"date" must be less than or equal to "2026-10-30T00:00:00.000Z"'),
])
def test_hf_http_failure_is_never_an_empty_success_or_unverified_not_ready(status, message):
    session = Mock()
    session.get.return_value = hf_response({'error': message}, status)
    source = {'id': 'hf-daily', 'params': {'url': 'https://huggingface.co/api/daily_papers'}}
    records, raw = fetch_hf.fetch(source, datetime(2026, 10, 30, tzinfo=timezone.utc), session, days=1)
    assert records == [] and raw['days'] == {} and raw['status'] == 'error'
    assert raw['errors']['2026-10-30'].startswith('error: HTTPError:')
    attempt = raw['attempts']['2026-10-30']
    assert attempt['status'] == 'error' and attempt['http_status'] == status
    assert json.loads(attempt['response_body']) == {'error': message}


@pytest.mark.parametrize('failure', ['timeout', 'invalid_json', 'invalid_shape'])
def test_hf_failed_day_continues_with_next_day(failure):
    bad = hf_response({'error': 'Unexpected JSON shape'})
    if failure == 'timeout':
        bad = requests.Timeout('HF timed out')
    elif failure == 'invalid_json':
        bad._content = b'not json'
    session = Mock()
    session.get.side_effect = [bad, hf_response(json.loads((FIX / 'hf.json').read_text()))]
    source = {'id': 'hf-daily', 'params': {'url': 'https://huggingface.co/api/daily_papers'}}
    records, raw = fetch_hf.fetch(source, datetime(2026, 10, 30, tzinfo=timezone.utc), session, days=2)
    assert len(records) == 1 and records[0]['hf_daily_dates'] == ['2026-10-29']
    assert raw['status'] == 'partial' and raw['attempts']['2026-10-30']['status'] == 'error'
    assert list(raw['errors']) == ['2026-10-30']
    if failure != 'timeout':
        assert raw['attempts']['2026-10-30']['response_body'] == bad.text


def test_hf_daily_date_comes_only_from_the_queried_day():
    raw = json.loads((FIX / 'hf.json').read_text())
    raw[0]['paper']['publishedAt'] = '2026-10-01T00:00:00Z'
    raw[0]['paper']['submittedOnDailyAt'] = '2026-10-06T00:00:00Z'
    raw[0]['publishedAt'] = '2026-10-07T00:00:00Z'
    result = fetch_hf.parse_json(raw, now=NOW, daily_date='2026-10-14')[0]
    assert result['hf_daily_dates'] == ['2026-10-14']
    assert result['hf_reported_published'] == '2026-10-01T00:00:00Z'
    assert result['published'] == result['updated'] == result['announced'] == ''
    assert result['metadata_pending'] and result['announced_source'] == 'unknown'
    assert result['hf_submitted_at'] == '2026-10-06T00:00:00Z'
    assert result['first_seen'] == NOW
    assert fetch_hf.parse_json(raw, now=NOW)[0]['hf_daily_dates'] == []


def test_normalize_preserves_observed_daily_dates_without_inference():
    result = normalize_record({'title': 'Observed paper', 'arxiv_id': '2610.10001',
                              'hf_daily_dates': ['2026-10-15', '2026-10-14', '2026-10-15']}, now=NOW)
    assert result['hf_daily_dates'] == ['2026-10-14', '2026-10-15']
    assert normalize_record({'title': 'No observed date', 'arxiv_id': '2610.10002',
                             'published': '2026-10-01', 'hf_submitted_at': '2026-10-06'}, now=NOW)['hf_daily_dates'] == []


@pytest.mark.parametrize(('dates', 'announced', 'source'), [
    ({'published': '2026-10-14T00:00:00Z', 'hf_submitted_at': '2026-10-20'}, '2026-10-14', 'published'),
    ({'hf_submitted_at': '2026-10-20T00:00:00Z'}, '2026-10-20', 'hf_submitted_at'),
    ({}, '', 'unknown'),
])
def test_announced_preserves_paper_date_and_never_uses_fetch_time(dates, announced, source):
    item = normalize_record({'title': 'Paper', 'arxiv_id': '2610.10001', **dates}, now=NOW)
    assert item['announced'] == announced
    assert item['announced_source'] == source


def test_s2_schema_mock_and_author_heuristic():
    items = fetch_s2.parse_json(json.loads((FIX / 's2_mock.json').read_text()), seed_id='dgm', now=NOW)
    assert items[0]['seed_hits'] == ['dgm'] and items[0]['arxiv_id'] == '2610.10001'
    assert items[0]['code_links'] == ['https://github.com/example/agent']
    authors = fetch_s2.select_authors([
        {'authors': [{'name': 'A', 'authorId': '1'}, {'name': 'B', 'authorId': '2'}]},
        {'authors': [{'name': 'A', 'authorId': '1'}, {'name': 'C', 'authorId': '3'}]},
    ])
    assert {a['authorId'] for a in authors} == {'1', '2', '3'}
    assert authors[0]['seed_appearances'] == 2


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


@pytest.mark.parametrize('entry_link,expected', [
    ('<link href="/us-midterms-analysis/" rel="alternate" type="text/html"/>',
     'https://sakana.ai/us-midterms-analysis/'),
    ('', 'https://sakana.ai/us-midterms-analysis'),
])
def test_rss_sakana_relative_link_or_id_resolves_against_response_url(entry_link, expected):
    session = Mock()
    session.get.return_value.url = 'https://sakana.ai/feed.xml'
    session.get.return_value.text = f'''<feed xmlns="http://www.w3.org/2005/Atom">
      <title>Blog</title><id>/feed.xml</id><entry>
        <title>Intelligence Report: SNSのAI分析からみる米中間選挙</title>
        {entry_link}<id>/us-midterms-analysis</id>
        <published>2026-10-30T00:00:00+09:00</published>
      </entry></feed>'''
    source = {'id': 'rss-sakana', 'params': {'url': 'http://sakana.ai/feed.xml'}}
    records, _ = fetch_rss.fetch(source, datetime(2026, 10, 29, tzinfo=timezone.utc), session)
    assert records[0]['links']['url'] == expected
    assert records[0]['id'] == f'post:{expected}'


def test_rss_rejects_entry_without_http_url():
    body = '''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
      <title>Invalid URL fixture</title><link href="javascript:alert(1)"/>
      <id>urn:example:invalid</id></entry></feed>'''
    with pytest.raises(ValueError, match='absolute HTTP'):
        fetch_rss.parse_feed(body, 'rss-fixture', NOW, feed_url='https://example.com/feed.xml')


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
    monkeypatch.setattr(fetch_arxiv, 'fetch_ids', Mock(return_value=[normalize_record({
        'arxiv_id': '2610.35001', 'title': 'Hydrated fixture',
        'published': '2026-10-26T00:00:00Z', 'updated': '2026-10-26T00:00:00Z',
        'published_source': 'arxiv'}, now=NOW)]))
    result = fetch_arxiv.fetch_sources(tmp_path, days=14, now=NOW, source_ids=['hf-daily'])
    assert result['outcomes'][0]['count'] == 1
    assert hf.call_args.kwargs['days'] == 14
    arxiv.assert_not_called()
    assert (tmp_path / 'data/feed/raw/hf-daily/2026-10-27.json').exists()
    assert result['raw_paths'] == ['data/feed/raw/hf-daily/2026-10-27.json']


def test_registry_dispatch_preserves_hf_partial_records_and_reports_failure(tmp_path, monkeypatch):
    import yaml
    (tmp_path / 'feed').mkdir()
    source = {'id': 'hf-daily', 'kind': 'hf_daily', 'schedule': 'daily', 'enabled': True,
              'params': {'url': 'https://huggingface.co/api/daily_papers'}}
    (tmp_path / 'feed/sources.yaml').write_text(yaml.safe_dump({'sources': [source]}))
    error = {'error': '✖ "date" must be less than or equal to "2026-10-29T00:00:00.000Z"\n  → at date'}
    get = Mock(side_effect=[hf_response(error, 400), hf_response(json.loads((FIX / 'hf.json').read_text()))])
    monkeypatch.setattr(fetch_hf.requests, 'get', get)
    monkeypatch.setattr(fetch_arxiv, 'fetch_ids', Mock(return_value=[normalize_record({
        'arxiv_id': '2610.35001', 'title': 'Hydrated fixture',
        'published': '2026-10-26T00:00:00Z', 'updated': '2026-10-26T00:00:00Z',
        'published_source': 'arxiv'}, now=NOW)]))
    result = fetch_arxiv.fetch_sources(tmp_path, days=2, now='2026-10-30T00:00:00+00:00')
    outcome = next(row for row in result['outcomes'] if row['source_id'] == 'hf-daily')
    assert outcome['ok'] is False and outcome['count'] == 1
    assert '2026-10-30' in outcome['error'] and 'not_ready' in outcome['error']
    assert result['records'][0]['hf_daily_dates'] == ['2026-10-29']
    raw = json.loads((tmp_path / 'data/feed/raw/hf-daily/2026-10-30.json').read_text())
    assert raw['status'] == 'partial' and list(raw['days']) == ['2026-10-29']
    assert raw['attempts']['2026-10-30']['http_status'] == 400


@pytest.fixture
def hf_dates_source(tmp_path, monkeypatch):
    (tmp_path / 'feed').mkdir()
    (tmp_path / 'feed/sources.yaml').write_text(
        'sources:\n- id: hf-daily\n  kind: hf_daily\n  schedule: daily\n  enabled: true\n  params: {}\n')
    raw = [{'paper': {'id': '2601.15351', 'title': 'Publication date verification fixture',
                     'summary': 'Original HF abstract retained for review.',
                     'publishedAt': '2026-10-23T12:00:00Z',
                     'submittedOnDailyAt': '2026-10-27T01:00:00Z'}}]
    records = fetch_hf.parse_json(raw, now=NOW, daily_date='2026-10-27')
    monkeypatch.setattr(fetch_hf, 'fetch', Mock(return_value=(records, {'format': 'fixture', 'rows': raw})))
    paper = normalize_record({'arxiv_id': '2601.15351v2', 'title': raw[0]['paper']['title'],
                              'published': '2026-01-21T12:00:00Z', 'updated': '2026-10-23T12:00:00Z',
                              'published_source': 'arxiv', 'source_hits': ['arxiv-version-check']}, now=NOW)
    return tmp_path, records[0], paper


def test_hf_hydration_uses_arxiv_dates_without_changing_recommendation_or_abstract(hf_dates_source, monkeypatch):
    from scripts.feed.dedupe import dedupe_items
    from scripts.feed.window import publication_dates
    root, raw, paper = hf_dates_source
    hydrate = Mock(return_value=[paper])
    monkeypatch.setattr(fetch_arxiv, 'fetch_ids', hydrate)
    result = fetch_arxiv.fetch_sources(root, now=NOW, source_ids=['hf-daily'])
    item = normalize_record(result['records'][0], now=NOW)
    hydrate.assert_called_once_with(['2601.15351'], now=NOW)
    assert item['version'] == 2 and not item['metadata_pending']
    assert item['published'] == paper['published'] and item['updated'] == paper['updated']
    assert item['announced'] == '2026-01-21' and item['announced_source'] == 'arxiv'
    assert item['hf_reported_published'] == '2026-10-23T12:00:00Z'
    assert item['hf_daily_dates'] == ['2026-10-27'] and item['abstract'] == raw['abstract']
    timing = publication_dates(item, '2026-10-27', '2026-10-25')
    assert timing['news_date'] == '2026-10-27' and timing['announced'] == '2026-01-21'
    # Existing same-version records can contain the formerly trusted HF date.
    old = normalize_record({**raw, 'version': 2, 'published': '2026-10-23T12:00:00Z',
                            'metadata_pending': False}, now=NOW)
    old['review'] = {'decision': 'defer', 'note': 'Keep owner note'}
    merged = dedupe_items([item], [old])[0]
    assert merged['published'] == paper['published'] and merged['announced'] == '2026-01-21'
    assert merged['announced_source'] == merged['published_source'] == 'arxiv'
    assert merged['review'] == old['review']


@pytest.mark.parametrize('response', ['network_error', 'wrong_identity', 'missing_identity', 'missing_date'])
def test_hf_failed_hydration_keeps_dates_unknown_and_reports_failure(hf_dates_source, monkeypatch, response):
    import requests
    from scripts.feed.dedupe import dedupe_items
    from scripts.feed.window import publication_dates
    root, raw, paper = hf_dates_source
    if response == 'network_error':
        hydrate = Mock(side_effect=requests.HTTPError('503 metadata unavailable'))
    else:
        returned = [] if response == 'missing_identity' else [{**paper,
            **({'arxiv_id': '2601.99999', 'id': 'arxiv:2601.99999'} if response == 'wrong_identity'
               else {'published': ''})}]
        hydrate = Mock(return_value=returned)
    monkeypatch.setattr(fetch_arxiv, 'fetch_ids', hydrate)
    result = fetch_arxiv.fetch_sources(root, now=NOW, source_ids=['hf-daily'])
    item = normalize_record(result['records'][0], now=NOW)
    outcome = next(row for row in result['outcomes'] if row['source_id'] == 'arxiv-hydration')
    assert outcome['ok'] is False and outcome['error']
    assert item['metadata_pending'] and item['metadata_error'] == outcome['error']
    assert item['published'] == item['updated'] == item['announced'] == ''
    assert item['announced_source'] == 'unknown'
    assert item['hf_reported_published'] == '2026-10-23T12:00:00Z'
    assert item['hf_daily_dates'] == ['2026-10-27'] and item['abstract'] == raw['abstract']
    timing = publication_dates(item, '2026-10-27', '2026-10-25')
    assert timing['announced'] == '' and timing['announced_source'] == 'unknown'
    old = normalize_record({**raw, 'published': '2026-10-23T12:00:00Z',
                            'metadata_pending': False}, now=NOW)
    merged = dedupe_items([item], [old])[0]
    assert merged['published'] == merged['updated'] == merged['announced'] == ''
    assert merged['metadata_error'] == outcome['error']


def test_rss_post_dates_filter_before_hydration():
    session = Mock()
    session.get.return_value.url = 'https://example.com/feed'
    session.get.return_value.text = '''<rss version="2.0"><channel><title>Lab</title><item><title>Old paper link</title><link>https://example.com/old</link><pubDate>Wed, 01 Jan 2025 00:00:00 GMT</pubDate><description>https://arxiv.org/abs/2501.10001</description></item></channel></rss>'''
    source = {'id': 'rss-lab', 'params': {'url': 'https://example.com/feed', 'lookback_days': 14}}
    items, raw = fetch_rss.fetch(source, datetime(2026, 10, 27, tzinfo=timezone.utc), session)
    assert items == []


def test_arxiv_fourteen_calendar_days_include_today(monkeypatch):
    request = Mock(return_value='<feed xmlns="http://www.w3.org/2005/Atom"/>')
    monkeypatch.setattr(fetch_arxiv, 'request', request)
    source = {'id': 'arxiv-harness', 'params': {'query': 'ti:harness'}}
    _, raw = fetch_arxiv.fetch(source, days=14, now=datetime(2026, 10, 27, tzinfo=timezone.utc))
    assert 'submittedDate:[202610140000 TO 202610272359]' in raw['query']
    assert '20261013' not in request.call_args.args[0]['search_query']


def test_rss_fourteen_day_window_excludes_thirteenth_and_includes_fourteenth():
    session = Mock()
    session.get.return_value.url = 'https://example.com/feed'
    entries = ''.join(f'<item><title>Day {day}</title><link>https://example.com/{day}</link>'
                      f'<pubDate>{weekday}, {day} Oct 2026 00:00:00 GMT</pubDate></item>'
                      for day, weekday in [(13, 'Tue'), (14, 'Wed'), (27, 'Tue')])
    session.get.return_value.text = f'<rss version="2.0"><channel><title>Lab</title>{entries}</channel></rss>'
    source = {'id': 'rss-lab', 'params': {'url': 'https://example.com/feed', 'lookback_days': 14}}
    items, _ = fetch_rss.fetch(source, datetime(2026, 10, 27, tzinfo=timezone.utc), session)
    assert [item['published'][:10] for item in items] == ['2026-10-14', '2026-10-27']


def test_github_fourteen_day_window_excludes_thirteenth_and_includes_fourteenth(tmp_path):
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/papers.yaml').write_text('papers:\n- code: https://github.com/example/agent\n')
    session = Mock()
    session.get.return_value.json.return_value = [
        {'draft': False, 'tag_name': f'v{day}', 'published_at': f'2026-10-{day}T00:00:00Z',
         'html_url': f'https://github.com/example/agent/releases/tag/v{day}'}
        for day in (13, 14, 27)]
    source = {'id': 'github-releases', 'params': {'lookback_days': 14}}
    items, _ = fetch_github.fetch(source, tmp_path, datetime(2026, 10, 27, tzinfo=timezone.utc), session)
    assert [item['published'][:10] for item in items] == ['2026-10-14', '2026-10-27']
