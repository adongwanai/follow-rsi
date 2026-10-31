import json
import shutil
from types import SimpleNamespace

import pytest
import yaml

from scripts.common import ROOT, read_yaml
from scripts.feed.guard import unknown_evidence
from scripts.feed.llm import FeedLLM, LLMConfigurationError, LLMError

VALID = {'label': 'include', 'exclude_reason': None, 'reason_zh': '修改保留到后续任务', 'confidence': 0.9,
         'scope_kind': 'method', 'scope_support': {'object_quote': None, 'feedback_quote': None,
          'persistence_quote': 'Changes persist to later tasks.', 'study_quote': None, 'exclusion_quote': None}}
ITEM = {'id': 'arxiv:2610.12345', 'arxiv_id': '2610.12345', 'version': 1,
        'title': 'An iterative agent', 'abstract': 'Changes persist to later tasks.'}
SUMMARY_LIMIT_CASES = [
    pytest.param('summarize', 'summary_zh', 'AutoSaddler：' + '研' * 60 + '。',
                 'AutoSaddler：' + '研' * 61 + '。', id='chinese'),
    pytest.param('translate', 'summary_en', ' '.join(['Research'] * 30) + '.',
                 ' '.join(['Research'] * 31) + '.', id='english'),
]


class Transport:
    def __init__(self, outputs):
        self.outputs = iter(outputs)
        self.calls = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def create(self, **kwargs):
        self.calls.append(kwargs)
        value = next(self.outputs)
        if isinstance(value, Exception):
            raise value
        content = value if isinstance(value, str) else json.dumps(value)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


@pytest.fixture
def prompt_root(tmp_path):
    shutil.copytree(ROOT / 'feed/prompts', tmp_path / 'feed/prompts')
    return tmp_path


def test_cache_hit_and_version_prompt_model_invalidation(prompt_root):
    transport = Transport([VALID] * 4)
    client = FeedLLM('model-a', transport, root=prompt_root)
    first = client.run('relevance', ITEM)
    assert not first['cached']
    assert client.run('relevance', ITEM)['cached']
    version = client.run('relevance', {**ITEM, 'version': 2})
    assert version['cache_key'] != first['cache_key']
    path = prompt_root / 'feed/prompts/relevance.md'
    path.write_text(path.read_text() + '\nReview persistence carefully.\n')
    changed = client.run('relevance', ITEM)
    assert changed['prompt_hash'] != first['prompt_hash']
    other = FeedLLM('model-b', transport, root=prompt_root).run('relevance', ITEM)
    assert other['cache_key'] != changed['cache_key']
    assert len(transport.calls) == 4
    assert all(call['temperature'] == 0 for call in transport.calls)
    assert transport.calls[0]['response_format']['json_schema']['strict']


def test_stage_model_routes_request_and_separates_cache(prompt_root):
    from test_judge import CLASSIFY, GATE
    config_path = prompt_root / 'feed/model.yaml'
    config = {'stages': {'classify': {'model': 'classifier-model'},
                         'harness_gate': {'model': 'gate-model', 'timeout_seconds': 180}}}
    config_path.write_text(yaml.safe_dump(config))
    transport = Transport([CLASSIFY, GATE, GATE])
    client = FeedLLM('base-model', transport, root=prompt_root)
    variables = {'taxonomy_definitions': '{}'}
    client.run('classify', ITEM, variables=variables)
    first = client.run('harness_gate', ITEM, variables=variables)
    assert client.run('harness_gate', ITEM, variables=variables)['cached']
    config['stages']['harness_gate']['model'] = 'new-gate-model'
    config_path.write_text(yaml.safe_dump(config))
    changed = client.run('harness_gate', ITEM, variables=variables)
    assert [call['model'] for call in transport.calls] == [
        'classifier-model', 'gate-model', 'new-gate-model']
    assert [call['timeout'] for call in transport.calls] == [60, 180, 180]
    assert first['cache_key'] != changed['cache_key']


def test_retry_schema_failure_once_and_never_cache_invalid(prompt_root):
    transport = Transport(['not JSON', {**VALID, 'label': 'bad'}])
    with pytest.raises(LLMError, match='invalid after one retry'):
        FeedLLM('model-a', transport, root=prompt_root).run('relevance', ITEM)
    assert len(transport.calls) == 2
    assert not list((prompt_root / 'data/feed/cache').glob('*.json'))
    transport = Transport([{**VALID, 'exclude_reason': 'off_topic'}, VALID])
    result = FeedLLM('model-a', transport, root=prompt_root).run('relevance', ITEM)
    assert result['data'] == VALID
    assert len(transport.calls) == 2


@pytest.mark.parametrize('stage,field,valid,overflow', SUMMARY_LIMIT_CASES)
def test_summary_length_retry_preserves_complete_result_and_accepts_limit(prompt_root, stage, field, valid, overflow):
    transport = Transport([{field: overflow}, {field: valid}])
    client = FeedLLM('model-a', transport, root=prompt_root)
    variables = {'summary_zh': '跨任务保留技能。'}
    result = client.run(stage, ITEM, variables=variables)
    assert result['data'] == {field: valid}
    assert result['retry_count'] == 1 and result['truncated_fields'] == []
    assert len(transport.calls) == 2
    assert json.loads(transport.calls[-1]['messages'][-2]['content']) == {field: overflow}
    assert 'exceeds' in transport.calls[-1]['messages'][-1]['content']
    assert client.run(stage, ITEM, variables=variables)['data'] == {field: valid}
    assert len(transport.calls) == 2


@pytest.mark.parametrize('stage,field,valid,overflow', SUMMARY_LIMIT_CASES)
def test_repeated_summary_overflow_enters_review_without_partial_text(prompt_root, stage, field, valid, overflow):
    from scripts.feed.judge import summarize_item
    outputs = ([{'summary_zh': '跨任务保留技能。'}] if stage == 'translate' else [])
    transport = Transport([*outputs, {field: overflow}, {field: overflow}])
    result = summarize_item({**ITEM, 'label': 'include'}, FeedLLM('model-a', transport, root=prompt_root))
    assert result['label'] == 'error' and result['review_required']
    assert result['llm']['error']['stage'] == stage
    assert 'invalid after one retry' in result['llm']['error']['message']
    assert result['summary_zh'] == result['summary_en'] == ''
    assert len(transport.calls) == len(outputs) + 2
    cached = [json.loads(path.read_text()) for path in (prompt_root / 'data/feed/cache').glob('*.json')]
    assert len(cached) == len(outputs)
    assert all(entry['data'] != {field: overflow} for entry in cached)


def test_generation_limits_preserve_long_curated_and_owner_summaries(prompt_root):
    from scripts.feed.judge import summarize_item
    from scripts.feed.review import effective_item
    summaries = {'summary_zh': '跨任务保留经过执行反馈修订的技能。' * 5,
                 'summary_en': 'Skills revised using execution feedback remain available for later tasks. ' * 4}
    paper = {'id': 'fixture', 'arxiv': ITEM['arxiv_id'], 'section': 'component', **summaries}
    (prompt_root / 'data').mkdir()
    (prompt_root / 'data/papers.yaml').write_text(yaml.safe_dump({'papers': [paper]}, allow_unicode=True))
    transport = Transport([])
    curated = summarize_item({**ITEM, 'in_repo': True}, FeedLLM('model-a', transport, root=prompt_root),
                             root=prompt_root)
    assert {key: curated[key] for key in summaries} == summaries
    owner_summaries = {key: value + value for key, value in summaries.items()}
    reviewed = effective_item(curated, {'llm': curated['llm'], 'summary_override': owner_summaries},
                              read_yaml(ROOT / 'feed/taxonomy.yaml'))
    assert {key: reviewed[key] for key in summaries} == owner_summaries
    assert transport.calls == []


def test_network_error_is_visible_without_secret_details(prompt_root):
    transport = Transport([RuntimeError('sensitive provider response')])
    with pytest.raises(LLMError) as caught:
        FeedLLM('model-a', transport, root=prompt_root).run('relevance', ITEM)
    assert 'RuntimeError' in str(caught.value)
    assert 'sensitive' not in str(caught.value)
    assert caught.value.__cause__ is not None
    assert len(transport.calls) == 1


def test_insufficient_balance_stops_batch_instead_of_relabeling_papers(prompt_root):
    from scripts.feed.judge import judge_item
    error = RuntimeError('sensitive provider response')
    error.status_code = 402
    transport = Transport([error])
    client = FeedLLM('model-a', transport, root=prompt_root)
    with pytest.raises(LLMConfigurationError, match='HTTP 402') as caught:
        judge_item(ITEM, client, prompt_root)
    assert 'sensitive' not in str(caught.value)
    assert len(transport.calls) == 1
    assert not list((prompt_root / 'data/feed/cache').glob('*.json'))


def test_deepseek_json_mode_still_validates_schema(prompt_root):
    transport = Transport([{'label': 'include'}, VALID])
    result = FeedLLM('deepseek-flash', transport, root=prompt_root, provider='deepseek').run('relevance', ITEM)
    assert result['data'] == VALID
    assert len(transport.calls) == 2
    assert transport.calls[0]['response_format'] == {'type': 'json_object'}


def test_quick_evidence_cannot_return_no(prompt_root):
    invalid = unknown_evidence()
    invalid['held_out']['value'] = 'no'
    valid = unknown_evidence()
    transport = Transport([invalid, valid])
    result = FeedLLM('model-a', transport, root=prompt_root).run(
        'evidence', {**ITEM, 'comments': ''})
    assert result['data'] == valid
    assert len(transport.calls) == 2


def test_long_reason_is_truncated_without_failing_or_retrying(prompt_root):
    transport = Transport([{**VALID, 'reason_zh': 'Meta-Agent ' * 12}])
    result = FeedLLM('model-a', transport, root=prompt_root).run('relevance', ITEM)
    assert result['retry_count'] == 0
    assert len(result['data']['reason_zh']) == 80
    assert result['truncated_fields'] == ['reason_zh']
    assert result['response_prompt_hash']


def test_missing_key_is_explicit(monkeypatch):
    for name in ('LLM_API_KEY', 'LLM_MODEL', 'LLM_PROVIDER'):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(LLMConfigurationError, match='LLM_API_KEY'):
        FeedLLM.from_env()
