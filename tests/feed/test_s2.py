"""Offline request-boundary tests for keyed and anonymous Semantic Scholar."""
from datetime import datetime, timezone
import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import requests

from scripts.feed import fetch_arxiv, fetch_s2
from scripts.feed.health import update_health
from scripts.feed.storage import load_state, save_state

NOW = datetime(2026, 10, 27, tzinfo=timezone.utc)


def response(status=200, payload=None):
    result = requests.Response()
    result.status_code = status
    result.url = fetch_s2.BASE + '/paper/arXiv:2505.22954'
    result._content = json.dumps({'data': []} if payload is None else payload).encode()
    return result


@pytest.fixture
def fake_clock(monkeypatch):
    clock = SimpleNamespace(now=100.0, sleeps=[])
    def sleep(seconds):
        assert seconds >= 0
        clock.sleeps.append(seconds)
        clock.now += seconds
    monkeypatch.setattr(fetch_s2.time, 'monotonic', lambda: clock.now)
    monkeypatch.setattr(fetch_s2.time, 'sleep', sleep)
    monkeypatch.setattr(fetch_s2, '_last_request', None)
    return clock


@pytest.fixture
def source_repo(tmp_path):
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/papers.yaml').write_text('papers:\n- id: dgm\n  arxiv: "2505.22954"\n  section: evolve_main\n  must_read: true\n')
    (tmp_path / 'feed').mkdir()
    (tmp_path / 'feed/sources.yaml').write_text('sources:\n- id: s2-citations\n  kind: s2_citations\n  enabled: true\n  schedule: weekly\n')
    return tmp_path


@pytest.mark.parametrize('key,mode,minimum', [('test-only-key', 'authenticated', 1.0),
                                            (None, 'anonymous', 3.0), ('', 'anonymous', 3.0)])
def test_header_and_shared_request_spacing(monkeypatch, fake_clock, key, mode, minimum):
    if key is None:
        monkeypatch.delenv('S2_API_KEY', raising=False)
    else:
        monkeypatch.setenv('S2_API_KEY', key)
    starts = []
    session = Mock()
    session.get.side_effect = lambda *args, **kwargs: starts.append(fake_clock.now) or response(payload={'paperId': 'known'})
    for _ in range(3):
        assert fetch_s2.request('paper/arXiv:2505.22954', {'fields': 'paperId'}, session) == {'paperId': 'known'}
    assert len(starts) == 3
    for previous, current in zip(starts, starts[1:]):
        assert current - previous > minimum
    assert len(fake_clock.sleeps) == 2
    for call in session.get.call_args_list:
        headers = call.kwargs['headers']
        assert headers['User-Agent'] == 'FollowRSI/0.1'
        if mode == 'authenticated':
            assert headers['x-api-key'] == key
        else:
            assert 'x-api-key' not in headers
        assert call.kwargs['timeout'] == 30


@pytest.mark.parametrize('key', [None, 'test-only-key'])
def test_429_backoff_recovers_and_grows_exponentially(monkeypatch, fake_clock, key):
    if key:
        monkeypatch.setenv('S2_API_KEY', key)
    else:
        monkeypatch.delenv('S2_API_KEY', raising=False)
    session = Mock()
    session.get.side_effect = [response(429), response(429), response(payload={'paperId': 'known'})]
    assert fetch_s2.request('paper/arXiv:2505.22954', session=session) == {'paperId': 'known'}
    assert session.get.call_count == 3
    assert len(fake_clock.sleeps) == 2
    assert fake_clock.sleeps[1] == pytest.approx(fake_clock.sleeps[0] * 2)
    assert fake_clock.sleeps[0] > (1 if key else 3)


def test_429_stops_after_five_retries_and_preserves_the_http_error(monkeypatch, fake_clock):
    monkeypatch.delenv('S2_API_KEY', raising=False)
    session = Mock()
    session.get.return_value = response(429)
    with pytest.raises(requests.HTTPError) as failure:
        fetch_s2.request('paper/arXiv:2505.22954', session=session)
    assert failure.value.response.status_code == 429
    assert session.get.call_count == 6
    assert len(fake_clock.sleeps) == 5
    assert fake_clock.sleeps == pytest.approx([3.1, 6.2, 12.4, 24.8, 49.6])


@pytest.mark.parametrize('status', [401, 403, 404, 500])
def test_other_http_errors_fail_without_retry(monkeypatch, fake_clock, status):
    monkeypatch.delenv('S2_API_KEY', raising=False)
    session = Mock()
    session.get.return_value = response(status)
    with pytest.raises(requests.HTTPError) as failure:
        fetch_s2.request('paper/arXiv:2505.22954', session=session)
    assert failure.value.response.status_code == status
    assert session.get.call_count == 1 and fake_clock.sleeps == []


def test_network_failure_is_not_swallowed(monkeypatch, fake_clock):
    monkeypatch.delenv('S2_API_KEY', raising=False)
    session = Mock()
    session.get.side_effect = requests.Timeout('S2 request timed out')
    with pytest.raises(requests.Timeout, match='timed out'):
        fetch_s2.request('paper/arXiv:2505.22954', session=session)
    session.get.assert_called_once()


@pytest.mark.parametrize('key,mode', [(None, 'anonymous'), ('test-only-key', 'authenticated')])
@pytest.mark.parametrize('status', [200, 429, 503])
def test_fetch_records_access_mode_even_on_failure(source_repo, monkeypatch, fake_clock, key, mode, status):
    if key:
        monkeypatch.setenv('S2_API_KEY', key)
    else:
        monkeypatch.delenv('S2_API_KEY', raising=False)
    source = {'id': 's2-citations', 'kind': 's2_citations'}
    session = Mock()
    session.get.return_value = response(status)
    if status == 200:
        items, raw = fetch_s2.fetch(source, source_repo, NOW, session)
        assert items == [] and raw['auth_mode'] == mode
    else:
        with pytest.raises(requests.HTTPError):
            fetch_s2.fetch(source, source_repo, NOW, session)
    state = load_state(source_repo)['sources']['s2-citations']
    assert state['auth_mode'] == mode
    assert state['min_interval_seconds'] > (1 if key else 3)
    assert 'test-only-key' not in (source_repo / 'data/feed/state.json').read_text()
    health = update_health(source_repo, [{'source_id': source['id'], 'ok': status == 200, 'count': 0,
                                         'error': None if status == 200 else f'HTTP {status}'}], NOW)
    assert health['sources'][source['id']]['auth_mode'] == mode
    assert load_state(source_repo)['sources'][source['id']]['consecutive_errors'] == (status != 200)


def test_mode_change_preserves_health_counters_and_source_history(source_repo, monkeypatch, fake_clock):
    save_state(source_repo, {'sources': {'s2-citations': {
        'auth_mode': 'authenticated', 'consecutive_failures': 2, 'consecutive_errors': 2,
        'seen_ids': ['arxiv:old'], 'weekly': {'2026-W44': 1}}}})
    monkeypatch.delenv('S2_API_KEY', raising=False)
    session = Mock()
    session.get.return_value = response()
    fetch_s2.fetch({'id': 's2-citations', 'kind': 's2_citations'}, source_repo, NOW, session)
    state = load_state(source_repo)['sources']['s2-citations']
    assert state['auth_mode'] == 'anonymous'
    assert state['consecutive_errors'] == 2 and state['seen_ids'] == ['arxiv:old']
    assert state['weekly'] == {'2026-W44': 1}


def test_anonymous_author_discovery_keeps_shared_spacing(source_repo, monkeypatch, fake_clock):
    monkeypatch.delenv('S2_API_KEY', raising=False)
    session = Mock()
    session.get.side_effect = [response(payload={'authors': [{'authorId': 'author-1', 'name': 'Author'}]}),
                               response(payload={'data': []})]
    items, raw = fetch_s2.fetch({'id': 's2-authors', 'kind': 's2_authors'}, source_repo, NOW, session)
    assert items == [] and raw['auth_mode'] == 'anonymous'
    assert session.get.call_count == 2
    assert session.get.call_args_list[1].args[0].endswith('/author/author-1/papers')
    assert all('x-api-key' not in call.kwargs['headers'] for call in session.get.call_args_list)
    assert sum(fake_clock.sleeps) > 3
    assert load_state(source_repo)['sources']['s2-authors']['auth_mode'] == 'anonymous'


def test_dispatcher_reports_anonymous_429_and_health_keeps_mode(source_repo, monkeypatch, fake_clock):
    monkeypatch.delenv('S2_API_KEY', raising=False)
    network = Mock(return_value=response(429))
    monkeypatch.setattr(fetch_s2.requests, 'get', network)
    result = fetch_arxiv.fetch_sources(source_repo, schedule='weekly', now=NOW)
    assert network.call_count == 6
    assert result['records'] == []
    outcome = result['outcomes'][0]
    assert outcome['ok'] is False and '429' in outcome['error']
    health = load_state(source_repo)
    assert health['sources']['s2-citations']['auth_mode'] == 'anonymous'
    assert health['sources']['s2-citations']['consecutive_errors'] == 1
