import json
import shutil
from types import SimpleNamespace

import pytest

from scripts.common import ROOT
from scripts.feed.guard import unknown_evidence
from scripts.feed.llm import FeedLLM, LLMConfigurationError, LLMError

VALID = {'label': 'include', 'exclude_reason': None, 'reason_zh': '修改保留到后续任务', 'confidence': 0.9}
ITEM = {'id': 'arxiv:2610.12345', 'arxiv_id': '2610.12345', 'version': 1,
        'title': 'An iterative agent', 'abstract': 'Changes persist to later tasks.'}


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


def test_network_error_is_visible_without_secret_details(prompt_root):
    transport = Transport([RuntimeError('sensitive provider response')])
    with pytest.raises(LLMError) as caught:
        FeedLLM('model-a', transport, root=prompt_root).run('relevance', ITEM)
    assert 'RuntimeError' in str(caught.value)
    assert 'sensitive' not in str(caught.value)
    assert caught.value.__cause__ is not None
    assert len(transport.calls) == 1


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


def test_length_retry_clarifies_literal_character_budget(prompt_root):
    transport = Transport([{**VALID, 'reason_zh': 'Meta-Agent ' * 5}, VALID])
    result = FeedLLM('model-a', transport, root=prompt_root).run('relevance', ITEM)
    assert result['retry_count'] == 1
    assert 'Unicode' in transport.calls[1]['messages'][-1]['content']
    assert result['response_prompt_hash']


def test_missing_key_is_explicit(monkeypatch):
    for name in ('LLM_API_KEY', 'LLM_MODEL', 'LLM_PROVIDER'):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(LLMConfigurationError, match='LLM_API_KEY'):
        FeedLLM.from_env()
