from copy import deepcopy
import pytest

from scripts.feed.guard import unknown_evidence
from scripts.feed.judge import guard_scope, judge_item, summarize_item
from scripts.feed.llm import LLMError

ITEM = {'id': 'arxiv:2610.12345', 'arxiv_id': '2610.12345', 'version': 1,
        'kind': 'paper', 'title': 'Iterative agents', 'abstract':
        'We revise workflow code using execution feedback. Accepted changes persist across tasks. '
        'We test held-out benchmarks, improving 12.5%.',
        'comments': 'Code: https://github.com/example/agent', 'in_repo': False}
RELEVANCE = {'label': 'include', 'exclude_reason': None, 'reason_zh': '修改保留到后续任务', 'confidence': 0.9,
             'scope_kind': 'method', 'scope_support': {
                 'object_quote': 'We revise workflow code using execution feedback.',
                 'feedback_quote': 'We revise workflow code using execution feedback.',
                 'persistence_quote': 'Accepted changes persist across tasks.',
                 'study_quote': None, 'exclusion_quote': None}}
CLASSIFY = {'primary': 'harness', 'harness_sub': 'evolve_main', 'secondary': [],
            'improved_object_zh': '工作流', 'confidence': 0.8}
GATE = {'improved_object': 'control_flow', 'improved_object_zh': '工作流代码', 'model_frozen': 'yes',
        'feedback_driven': {'value': 'yes', 'quote': 'We revise workflow code using execution feedback.'},
        'persists_across_tasks': {'value': 'yes', 'quote': 'Accepted changes persist across tasks.'},
        'verdict': 'harness', 'suggested_primary': 'harness', 'why_zh': '按反馈修改工作流并复用',
        'harness_specific': 'yes'}


class Client:
    model = 'fake'

    def __init__(self, outputs):
        self.outputs = iter(outputs)
        self.calls = []

    def run(self, name, item, **kwargs):
        self.calls.append((name, deepcopy(kwargs)))
        value = next(self.outputs)
        if isinstance(value, Exception):
            raise value
        return {'data': value, 'model': self.model, 'prompt_hash': name, 'cache_key': name, 'cached': False}


def test_include_pipeline_preserves_provenance_and_sanitizes_evidence():
    evidence = unknown_evidence()
    evidence['held_out'] = {'value': 'yes', 'quote': 'held-out benchmarks'}
    evidence['code_released'] = {'value': 'yes', 'quote': 'https://github.com/example/agent'}
    client = Client([RELEVANCE, CLASSIFY, GATE, evidence])
    result = judge_item(ITEM, client)
    assert [name for name, _ in client.calls] == ['relevance', 'classify', 'harness_gate', 'evidence']
    assert result['primary'] == result['llm']['primary'] == 'harness'
    assert result['confidence'] == 0.8
    assert result['llm']['relevance']['model'] == 'fake'
    assert result['evidence_quick']['held_out']['value'] == 'yes'
    assert result['evidence_quick']['code_released']['value'] == 'unknown'
    assert result['evidence_notice']['zh'] == '自动判断，未核实'
    assert 'llm' not in ITEM


def test_borderline_classified_but_not_quick_evidence_and_exclude_stops():
    client = Client([{**RELEVANCE, 'label': 'borderline'}, CLASSIFY, GATE])
    result = judge_item(ITEM, client)
    assert [name for name, _ in client.calls] == ['relevance', 'classify', 'harness_gate']
    assert result['review_required']
    assert result['evidence_quick'] == unknown_evidence()
    client = Client([{**RELEVANCE, 'label': 'exclude', 'exclude_reason': 'off_topic',
                      'scope_support': {**RELEVANCE['scope_support'], 'exclusion_quote': 'We study galaxy formation.'}}])
    assert judge_item({**ITEM, 'abstract': 'We study galaxy formation.'}, client)['label'] == 'exclude'
    assert len(client.calls) == 1


def test_existing_repo_uses_curated_projection_for_judgement_and_summary(monkeypatch):
    calls = []
    def curated(item, root):
        calls.append(item['id'])
        return {**item, 'summary_zh': '人工整理摘要', 'label': 'include'}
    monkeypatch.setattr('scripts.feed.library.curated_item', curated)
    client = Client([])
    assert judge_item({**ITEM, 'in_repo': True}, client)['summary_zh'] == '人工整理摘要'
    assert summarize_item({**ITEM, 'in_repo': True}, client)['summary_zh'] == '人工整理摘要'
    assert calls == [ITEM['id'], ITEM['id']]
    assert not client.calls


def test_lab_updates_never_judged():
    client = Client([])
    assert judge_item({**ITEM, 'kind': 'post'}, client)['kind'] == 'post'
    assert not client.calls


@pytest.mark.parametrize('field', ['object_quote', 'feedback_quote', 'persistence_quote'])
@pytest.mark.parametrize('quote', [None, 'A claimed sentence absent from the abstract.', ' ' * 12])
def test_missing_or_unmatched_support_never_includes(field, quote):
    relevance = deepcopy(RELEVANCE)
    relevance['scope_support'][field] = quote
    result = judge_item(ITEM, Client([relevance, CLASSIFY, GATE]))
    assert result['label'] == result['gate']['verdict'] == 'borderline'
    assert result['scope_support'][field] is None
    assert result['scope_guard']['issues'] == ['scope_support.' + field]
    assert result['llm']['relevance']['data']['scope_support'][field] == quote


def test_exclusion_without_support_is_uncertain_not_a_negative():
    raw = {**RELEVANCE, 'label': 'exclude', 'exclude_reason': 'not_persistent'}
    result = guard_scope(ITEM['abstract'], raw)
    assert result['label'] == 'borderline' and result['exclude_reason'] is None


def test_general_study_has_its_own_support_without_invented_method_quotes():
    abstract = 'We survey persistent self-improvement across models and experience stores.'
    relevance = {**RELEVANCE, 'scope_kind': 'theory',
                 'scope_support': {key: None for key in RELEVANCE['scope_support']}}
    relevance['scope_support']['study_quote'] = abstract
    assert guard_scope(abstract, relevance)['label'] == 'include'
    relevance['scope_support']['study_quote'] = None
    assert guard_scope(abstract, relevance)['label'] == 'borderline'


def test_errors_enter_manual_queue():
    result = judge_item(ITEM, Client([LLMError('relevance invalid after one retry')]))
    assert result['label'] == 'error'
    assert result['review_required']
    assert result['llm']['error']['stage'] == 'relevance'


def test_unhydrated_metadata_never_goes_to_model():
    client = Client([])
    result = judge_item({**ITEM, 'metadata_pending': True, 'abstract': ''}, client)
    assert result['label'] == 'error' and result['llm']['error']['stage'] == 'metadata'
    assert not client.calls


def test_numeric_retry_recovers_and_records_initial_failure():
    client = Client([{'summary_zh': '提升14%'}, {'summary_zh': '提升12.5%'},
                     {'summary_en': 'Improves 12.5%'}])
    result = summarize_item({**ITEM, 'label': 'include'}, client)
    assert result['summary_zh'] == '提升12.5%'
    assert result['initial_guard_failed'] and not result['guard_failed']
    assert '14%' in client.calls[1][1]['feedback']


def test_second_number_failure_clears_both_languages():
    client = Client([{'summary_zh': '提升12.5%'}, {'summary_en': 'Improves 14%'},
                     {'summary_zh': '提升12.5%'}, {'summary_en': 'Improves 14%'}])
    result = summarize_item({**ITEM, 'label': 'borderline'}, client)
    assert result['guard_failed'] and result['initial_guard_failed']
    assert result['summary_zh'] == result['summary_en'] == ''
    assert result['review_required']


def test_translation_error_clears_both_languages_and_queues():
    result = summarize_item({**ITEM, 'label': 'include'}, Client([
        {'summary_zh': '提升12.5%'}, LLMError('translate failed')]))
    assert result['label'] == 'error'
    assert result['summary_zh'] == result['summary_en'] == ''
