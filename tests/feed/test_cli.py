"""The complete offline pipeline must stop at the owner gate and resume safely."""
from copy import deepcopy
from concurrent.futures import Future
import hashlib
import json
import sys

import pytest
import yaml

from scripts.common import ROOT, read_yaml
from scripts.feed import cli, fetch_arxiv
from scripts.feed.cli import configure, process_items, run_pipeline, run_stage
from scripts.feed.guard import unknown_evidence
from scripts.feed.review import validate_daily_review
from scripts.feed.storage import load_items, save_items, write_json
from test_daily import accept_daily, make_daily_repo, write_daily
from test_review import make_repo

DAY = '2026-10-27'


class OfflineLLM:
    model = 'offline-fixture'
    def __init__(self):
        self.calls = []

    def run(self, name, item, **kwargs):
        self.calls.append(name)
        output = {
            'relevance': {'label': 'include', 'exclude_reason': None,
                          'reason_zh': '跨任务保留技能', 'confidence': .9, 'scope_kind': 'method',
                          'scope_support': {'object_quote': 'Execution feedback revises skill files, retained across tasks.',
                                            'feedback_quote': 'Execution feedback revises skill files, retained across tasks.',
                                            'persistence_quote': 'Execution feedback revises skill files, retained across tasks.',
                                            'study_quote': None, 'exclusion_quote': None}},
            'classify': {'primary': 'harness', 'harness_sub': 'component',
                         'secondary': [], 'improved_object_zh': '技能', 'confidence': .9},
            'harness_gate': {'improved_object': 'skill_files', 'improved_object_zh': '技能文件',
                             'model_frozen': 'yes', 'harness_specific': 'yes', 'verdict': 'harness',
                             'suggested_primary': 'harness', 'why_zh': '按反馈修订并保留技能',
                             'feedback_driven': {'value': 'yes', 'quote': 'Execution feedback revises skill files, retained across tasks.'},
                             'persists_across_tasks': {'value': 'yes', 'quote': 'Execution feedback revises skill files, retained across tasks.'}},
            'evidence': unknown_evidence(),
            'summarize': {'summary_zh': '技能跨任务保留，在留出任务上达到 20%。'},
            'translate': {'summary_en': 'Skills persist across tasks, reaching 20% on held-out tasks.'},
        }[name]
        return {'data': output, 'model': 'offline-fixture', 'prompt_hash': name,
                'cache_key': name, 'cached': False}


def empty_source_repo(tmp_path):
    root = make_repo(tmp_path)
    item = deepcopy(load_items(root)[0])
    item['abstract'] += ' Execution feedback revises skill files, retained across tasks.'
    for key in ('llm', 'summary_zh', 'summary_en', 'evidence_quick'):
        item.pop(key)
    (root / 'data/feed/items.jsonl').unlink()
    return root, item


def test_all_stages_stop_before_pending_publication_and_rerun_without_new_llm_calls(tmp_path, monkeypatch):
    root, item = empty_source_repo(tmp_path)
    monkeypatch.setattr(fetch_arxiv, 'fetch_sources', lambda *a, **k: {
        'records': [deepcopy(item)], 'outcomes': [], 'raw_paths': []})
    client = OfflineLLM()
    results = run_pipeline(root, date=DAY, workers=1, client=client)
    assert results[-1]['status'] == 'awaiting_owner_review'
    review = read_yaml(root / f'review/daily/{DAY}.yaml')
    assert review['items'][0]['decision'] == 'defer'
    feed = json.loads((root / 'site/feed/latest.json').read_text())
    assert feed['items'] == []
    assert not (root / f'daily/{DAY}.md').exists()
    assert run_stage(root, 'publish', date=DAY)['published'] is False
    before = (root / 'data/feed/items.jsonl').read_bytes()
    calls = list(client.calls)
    run_pipeline(root, date=DAY, workers=1, client=client)
    assert (root / 'data/feed/items.jsonl').read_bytes() == before
    assert client.calls == calls


def test_empty_pipeline_does_not_publish_an_edition(tmp_path, monkeypatch):
    root, _ = empty_source_repo(tmp_path)
    monkeypatch.setattr(fetch_arxiv, 'fetch_sources', lambda *a, **k: {
        'records': [], 'outcomes': [], 'raw_paths': []})
    result = run_pipeline(root, date=DAY)
    assert result[-1]['status'] == 'no_approved_items'
    assert not (root / f'daily/{DAY}.md').exists()


@pytest.mark.parametrize('label', ['include', 'borderline'])
@pytest.mark.parametrize('gate', [None, {'verdict': 'harness'}])
def test_old_automatic_harness_without_complete_gate_is_migrated_once(tmp_path, label, gate):
    root, item = empty_source_repo(tmp_path)
    item['llm'] = {'label': label, 'primary': 'harness', 'harness_sub': 'component',
                   'secondary': [], 'confidence': .8}
    item['summary_zh'], item['summary_en'] = '旧自动摘要', 'Old automatic summary'
    if gate is None:
        item.pop('gate')
    else:
        item['gate'] = deepcopy(gate)
    item['review'] = {'kind': 'daily', 'decision': 'defer', 'note': 'Keep this owner note'}
    save_items(root, [item])
    client = OfflineLLM()
    assert process_items(root, 'judge', workers=1, client=client)['processed'] == 1
    updated = load_items(root)[0]
    assert updated['gate']['verdict'] == 'harness'
    assert updated['llm']['harness_gate']['sample_count'] == 1
    assert updated['review'] == item['review']
    assert 'summary_zh' not in updated and 'summary_en' not in updated
    before = (root / 'data/feed/items.jsonl').read_bytes()
    calls = list(client.calls)
    assert process_items(root, 'judge', workers=1, client=client)['processed'] == 0
    assert client.calls == calls and (root / 'data/feed/items.jsonl').read_bytes() == before


@pytest.mark.parametrize('corrected', [False, True])
def test_complete_gate_and_owner_corrections_are_not_rejudged(tmp_path, monkeypatch, corrected):
    from scripts.feed.llm import FeedLLM
    root, item = empty_source_repo(tmp_path)
    item['llm'] = {'label': 'include', 'primary': 'harness', 'harness_sub': 'component', 'secondary': []}
    item['summary_zh'], item['summary_en'] = '保留摘要', 'Retain this summary'
    if corrected:
        item.pop('gate')
        item['review'] = {'kind': 'correction', 'decision': 'move',
                          'direction_override': 'ai4ai', 'correction_sha256': 'owner-receipt'}
    save_items(root, [item])
    def no_api(*args, **kwargs):
        raise AssertionError('Completed or corrected records must not create an API client')
    monkeypatch.setattr(FeedLLM, 'from_env', no_api)
    before = (root / 'data/feed/items.jsonl').read_bytes()
    for stage in ('judge', 'summarize'):
        assert process_items(root, stage)['processed'] == 0
    assert (root / 'data/feed/items.jsonl').read_bytes() == before


def test_failed_automatic_judgement_is_retried_without_overwriting_owner_correction(tmp_path):
    root, item = empty_source_repo(tmp_path)
    item['label'] = 'error'
    item['llm'] = {'label': 'error', 'error': {'stage': 'relevance', 'message': 'Schema error'}}
    item['summary_zh'], item['summary_en'] = '', ''
    corrected = deepcopy(item)
    corrected.update(id='arxiv:2610.99994', arxiv_id='2610.99994')
    corrected['review'] = {'kind': 'correction', 'decision': 'reject', 'note': 'Owner decision'}
    save_items(root, [item, corrected])
    client = OfflineLLM()
    assert process_items(root, 'judge', workers=1, client=client)['processed'] == 1
    updated = {row['id']: row for row in load_items(root)}
    assert updated[item['id']]['llm']['label'] == 'include'
    assert 'error' not in updated[item['id']]['llm']
    assert 'summary_zh' not in updated[item['id']]
    assert updated[corrected['id']] == corrected
    calls = list(client.calls)
    assert process_items(root, 'judge', workers=1, client=client)['processed'] == 0
    assert client.calls == calls


@pytest.mark.parametrize('changed_stage', ['relevance', 'classify', 'harness_gate'])
def test_changed_prompt_rejudges_old_exclude_once_and_preserves_owner_correction(
        tmp_path, monkeypatch, changed_stage):
    root, item = empty_source_repo(tmp_path)
    prompts = root / 'feed/prompts'
    prompts.mkdir()
    for stage in ('relevance', 'classify', 'harness_gate', 'evidence'):
        (prompts / f'{stage}.md').write_bytes((ROOT / 'feed/prompts' / f'{stage}.md').read_bytes())
    provenance = {'template_hash': hashlib.sha256((prompts / f'{changed_stage}.md').read_bytes()).hexdigest()}
    item['llm'] = {'label': 'exclude', changed_stage: (
        {'samples': [provenance]} if changed_stage == 'harness_gate' else provenance)}
    item['label'] = 'exclude'
    item['summary_zh'], item['summary_en'] = '过时摘要', 'Outdated summary'
    item['review'] = {'kind': 'daily', 'decision': 'defer', 'note': 'Keep the owner note'}
    corrected = deepcopy(item)
    corrected.update(id='arxiv:2610.99994', arxiv_id='2610.99994')
    corrected['review'] = {'kind': 'correction', 'decision': 'reject', 'note': 'Owner decision'}
    save_items(root, [item, corrected])
    client = OfflineLLM()
    original_run = client.run

    def run_with_provenance(name, *args, **kwargs):
        return {**original_run(name, *args, **kwargs),
                'template_hash': hashlib.sha256((prompts / f'{name}.md').read_bytes()).hexdigest()}

    monkeypatch.setattr(client, 'run', run_with_provenance)
    before = (root / 'data/feed/items.jsonl').read_bytes()
    assert process_items(root, 'judge', workers=1, client=client)['processed'] == 0
    assert not client.calls
    assert (root / 'data/feed/items.jsonl').read_bytes() == before
    with (prompts / f'{changed_stage}.md').open('a') as stream:
        stream.write('\nUpdated scope rule for the regression fixture.\n')

    assert process_items(root, 'judge', workers=1, client=client)['processed'] == 1
    updated = {row['id']: row for row in load_items(root)}
    assert updated[item['id']]['llm']['label'] == 'include'
    assert updated[item['id']]['review'] == item['review']
    assert 'summary_zh' not in updated[item['id']] and 'summary_en' not in updated[item['id']]
    assert updated[corrected['id']] == corrected
    before = (root / 'data/feed/items.jsonl').read_bytes()
    calls = list(client.calls)
    assert process_items(root, 'judge', workers=1, client=client)['processed'] == 0
    assert client.calls == calls
    assert (root / 'data/feed/items.jsonl').read_bytes() == before


@pytest.mark.parametrize('stage', ['judge', 'summarize'])
@pytest.mark.parametrize('in_flight', [False, True])
def test_payment_failure_cancels_unstarted_work_and_keeps_completed_results(
        tmp_path, monkeypatch, capsys, stage, in_flight):
    from scripts.feed.llm import LLMConfigurationError

    root, template = empty_source_repo(tmp_path)
    items = []
    for index in range(5):
        item = deepcopy(template)
        item.update(id=f'arxiv:2610.{99990 + index}', arxiv_id=f'2610.{99990 + index}')
        if stage == 'summarize':
            item.update(label='include', llm={'label': 'include'})
        items.append(item)
    save_items(root, items)
    failure = LLMConfigurationError('LLM provider returned HTTP 402 (insufficient balance)')
    futures = []
    completed = {}

    class ScheduledExecutor:
        """Fix completion order so queue cancellation has no timing-dependent assertion."""
        def __init__(self, max_workers):
            assert max_workers == 2

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def submit(self, operation, item, client, root):
            future = Future()
            index = len(futures)
            if index == 1:
                future.set_exception(failure)
            elif index in (0, 2):
                result = deepcopy(item)
                result.update(label='include', llm={'label': 'include'})
                if stage == 'summarize':
                    result.update(summary_zh='完成的摘要', summary_en='Completed summary')
                completed[item['id']] = result
                if index == 2 and in_flight:
                    future.set_running_or_notify_cancel()
                else:
                    future.set_result(result)
            futures.append(future)
            return future

    def completed_in_order(pending):
        order = list(pending.items())
        # Cancelled work may be yielded before the last successful in-flight result.
        for future, ident in [*order[:2], *order[3:], order[2]]:
            if future.running():
                future.set_result(completed[ident])
            yield future

    monkeypatch.setattr(cli, 'ThreadPoolExecutor', ScheduledExecutor)
    monkeypatch.setattr(cli, 'as_completed', completed_in_order)
    with pytest.raises(LLMConfigurationError, match='HTTP 402') as error:
        process_items(root, stage, workers=2, client=OfflineLLM())
    assert error.value is failure
    assert all(future.cancelled() for future in futures[3:])
    saved = {row['id']: row for row in load_items(root)}
    for item in items:
        assert saved[item['id']] == completed.get(item['id'], item)
    progress = capsys.readouterr().out
    assert f'{stage}: 5/5 processed' not in progress
    assert f'{stage}: interrupted; 2/5 results saved' in progress


@pytest.mark.parametrize('stage', ['judge', 'summarize'])
def test_previously_judged_promotion_refreshes_from_library_without_api(tmp_path, monkeypatch, stage):
    from scripts.feed.llm import FeedLLM
    root, item = empty_source_repo(tmp_path)
    collection = read_yaml(ROOT / 'data/papers.yaml')
    paper = deepcopy(next(p for p in collection['papers'] if p['id'] == 'riseharness'))
    collection['papers'] = [paper]
    (root / 'data/papers.yaml').write_text(yaml.safe_dump(collection, allow_unicode=True, sort_keys=False))
    item.update(id='arxiv:' + paper['arxiv'], arxiv_id=paper['arxiv'],
                llm={'label': 'include', 'primary': 'ai4ai', 'harness_sub': None, 'secondary': []},
                summary_zh='旧自动摘要', summary_en='Old automatic summary')
    save_items(root, [item])
    write_json(root / 'data/feed/normalized.json', [])
    run_stage(root, 'dedupe', date=DAY)
    assert load_items(root)[0]['in_repo']
    def no_api(*args, **kwargs):
        raise AssertionError('Library refresh must not create an API client')
    monkeypatch.setattr(FeedLLM, 'from_env', no_api)
    assert process_items(root, stage)['processed'] == 1
    updated = load_items(root)[0]
    assert updated['summary_zh'] == paper['summary_zh']
    assert updated['summary_en'] == paper['summary_en']
    assert updated['llm']['origin'] == updated['gate']['origin'] == 'evidence_library'
    assert updated['llm']['primary'] == 'harness'
    before = (root / 'data/feed/items.jsonl').read_bytes()
    assert process_items(root, stage)['processed'] == 0
    assert (root / 'data/feed/items.jsonl').read_bytes() == before
    paper['summary_zh'] = '人工证据库后来修订的摘要'
    (root / 'data/papers.yaml').write_text(yaml.safe_dump(collection, allow_unicode=True, sort_keys=False))
    assert process_items(root, stage)['processed'] == 1
    assert load_items(root)[0]['summary_zh'] == paper['summary_zh']


def test_backfill_marks_existing_and_new_unpublished_ids_but_preserves_publications(tmp_path):
    root = make_repo(tmp_path)
    existing = load_items(root)
    paper, published_paper, published_backlog = existing[:3]
    release = next(item for item in existing if item['kind'] == 'release')
    path = root / 'site/daily' / f'{DAY}.json'
    write_json(path, {'date': DAY, 'items': [{'id': published_paper['id']}],
                      'lab_updates': [{'id': release['id']}]})
    published_bytes = path.read_bytes()
    weekly = root / 'site/weekly/2026-W44.json'
    write_json(weekly, {'week': '2026-W44', 'items': [],
                       'backlog': [{'id': published_backlog['id']}]})
    weekly_bytes = weekly.read_bytes()
    new = {**deepcopy(paper), 'id': 'arxiv:2610.99994', 'arxiv_id': '2610.99994',
           'title': 'Distinct backfill fixture for workflow regression'}
    write_json(root / 'data/feed/normalized.json', [new])
    run_stage(root, 'dedupe', days=14, date=DAY)
    items = {item['id']: item for item in load_items(root)}
    assert items[paper['id']]['backfill_only'] and items[new['id']]['backfill_only']
    assert items[published_paper['id']] == published_paper and items[release['id']] == release
    assert items[published_backlog['id']] == published_backlog
    assert path.read_bytes() == published_bytes
    assert weekly.read_bytes() == weekly_bytes


def test_backfill_queue_demotes_existing_unpublished_approval_and_blocks_daily_accept(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    run_stage(root, 'queue', days=14, date=DAY)
    row = next(row for row in read_yaml(root / f'review/daily/{DAY}.yaml')['items']
               if row['id'] == 'arxiv:2610.99991')
    assert row['window_status'] == 'backlog' and row['decision'] == 'defer'
    write_daily(root, lambda review: next(row for row in review['items']
                if row['id'] == 'arxiv:2610.99991').update(decision='accept'))
    with pytest.raises(ValueError, match='window_status=in_window'):
        validate_daily_review(root, DAY)


@pytest.mark.parametrize('resume', ['queue', 'normalize_dedupe_queue'])
def test_backfill_batch_survives_separate_commands_with_default_days(tmp_path, monkeypatch, resume):
    root = make_daily_repo(tmp_path)
    fetched = deepcopy(load_items(root)[0])
    monkeypatch.setattr(fetch_arxiv, 'fetch_sources', lambda *args, **kwargs: {
        'records': [fetched], 'outcomes': [], 'raw_paths': []})
    run_stage(root, 'fetch', days=14, date=DAY)
    assert json.loads((root / 'data/feed/last-fetch.json').read_text())['batch']['lookback_days'] == 14
    if resume == 'normalize_dedupe_queue':
        run_stage(root, 'normalize', date=DAY)
        run_stage(root, 'dedupe', date=DAY)
        batch = json.loads((root / 'data/feed/normalized.json').read_text())['batch']
        assert batch == {'lookback_days': 14, 'backfill_only': True}
    run_stage(root, 'queue', date=DAY)
    assert all(item['backfill_only'] for item in load_items(root))
    rows = read_yaml(root / f'review/daily/{DAY}.yaml')['items']
    assert rows and all(row['window_status'] == 'backlog' for row in rows)


@pytest.mark.parametrize('batch', [None, {'lookback_days': 2, 'backfill_only': False}])
def test_explicit_backfill_normalization_survives_default_dedupe_and_queue(tmp_path, batch):
    root = make_daily_repo(tmp_path)
    fetched = {'records': [deepcopy(load_items(root)[0])], 'outcomes': [], 'raw_paths': []}
    if batch is not None:
        fetched['batch'] = batch
    write_json(root / 'data/feed/last-fetch.json', fetched)
    run_stage(root, 'normalize', days=14, date=DAY)
    normalized = json.loads((root / 'data/feed/normalized.json').read_text())
    assert normalized['batch'] == {
        'lookback_days': 14 if batch is None else 2, 'backfill_only': True}
    run_stage(root, 'dedupe', date=DAY)
    run_stage(root, 'queue', date=DAY)
    assert all(item['backfill_only'] for item in load_items(root))
    rows = read_yaml(root / f'review/daily/{DAY}.yaml')['items']
    assert rows and all(row['window_status'] == 'backlog' for row in rows)


@pytest.mark.parametrize('entrypoint', ['stage', 'command'])
def test_withdrawn_cli_publication_cannot_apply_review_or_change_provenance(tmp_path, monkeypatch, entrypoint):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    receipt = root / 'data/feed/review-provenance' / f'{DAY}.json'
    receipt.parent.mkdir()
    receipt.write_text(json.dumps({'date': DAY, 'github_pr': 1, 'merge_commit': 'original-owner-merge'}))
    (root / 'data/feed/withdrawn-editions.json').write_text(json.dumps({
        DAY: {'reason': 'Historical backfill was published as daily news', 'withdrawn_at': DAY + 'T13:00:00Z'}}))
    monkeypatch.setattr(cli, 'configure', lambda *args: None)
    monkeypatch.setattr(sys, 'argv', ['feed', '--root', str(root), 'publish', '--date', DAY])
    before = {str(path.relative_to(root)): path.read_bytes() for path in root.rglob('*') if path.is_file()}
    with pytest.raises(ValueError, match=f'{DAY} was withdrawn: Historical backfill'):
        if entrypoint == 'stage':
            run_stage(root, 'publish', date=DAY)
        else:
            cli.main()
    assert before == {str(path.relative_to(root)): path.read_bytes() for path in root.rglob('*') if path.is_file()}


def test_explicit_environment_file_is_never_executed(tmp_path, monkeypatch):
    (tmp_path / 'feed').mkdir()
    (tmp_path / 'feed/model.yaml').write_text('provider: deepseek\nmodel: offline\n')
    env = tmp_path / 'local.env'
    env.write_text('LLM_API_KEY=$(touch should-not-exist)\n')
    monkeypatch.delenv('LLM_API_KEY', raising=False)
    configure(tmp_path, env)
    import os
    assert os.environ['LLM_API_KEY'] == '$(touch should-not-exist)'
    assert not (tmp_path / 'should-not-exist').exists()
    env.write_text('HOME=/tmp/wrong\n')
    with pytest.raises(ValueError, match='Unsupported environment assignment'):
        configure(tmp_path, env)
