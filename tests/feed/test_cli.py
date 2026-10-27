"""The complete offline pipeline must stop at the owner gate and resume safely."""
from copy import deepcopy
import json

import pytest

from scripts.common import read_yaml
from scripts.feed import fetch_arxiv
from scripts.feed.cli import configure, run_pipeline, run_stage
from scripts.feed.guard import unknown_evidence
from scripts.feed.storage import load_items
from test_review import make_repo

DAY = '2026-10-27'


class OfflineLLM:
    def __init__(self):
        self.calls = []

    def run(self, name, item, **kwargs):
        self.calls.append(name)
        output = {
            'relevance': {'label': 'include', 'exclude_reason': None,
                          'reason_zh': '跨任务保留技能', 'confidence': .9},
            'classify': {'primary': 'harness', 'harness_sub': 'component',
                         'secondary': [], 'improved_object_zh': '技能', 'confidence': .9},
            'evidence': unknown_evidence(),
            'summarize': {'summary_zh': '技能跨任务保留，在留出任务上达到 20%。'},
            'translate': {'summary_en': 'Skills persist across tasks, reaching 20% on held-out tasks.'},
        }[name]
        return {'data': output, 'model': 'offline-fixture', 'prompt_hash': name,
                'cache_key': name, 'cached': False}


def empty_source_repo(tmp_path):
    root = make_repo(tmp_path)
    item = deepcopy(load_items(root)[0])
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
    assert review['items'][0]['decision'] == 'pending'
    feed = json.loads((root / 'site/feed/latest.json').read_text())
    assert feed['items'] == []
    assert not (root / f'daily/{DAY}.md').exists()
    with pytest.raises(ValueError, match='pending'):
        run_stage(root, 'publish', date=DAY)
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
