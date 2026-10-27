from copy import deepcopy

from scripts.feed.guard import unknown_evidence
from scripts.feed.judge import judge_item, summarize_item
from scripts.feed.llm import LLMError

ITEM = {'id': 'arxiv:2610.12345', 'arxiv_id': '2610.12345', 'version': 1,
        'kind': 'paper', 'title': 'Iterative agents', 'abstract':
        'We retain changes across tasks and test held-out benchmarks, improving 12.5%.',
        'comments': 'Code: https://github.com/example/agent', 'in_repo': False}
RELEVANCE = {'label': 'include', 'exclude_reason': None, 'reason_zh': '修改保留到后续任务', 'confidence': 0.9}
CLASSIFY = {'primary': 'harness', 'harness_sub': 'evolve_main', 'secondary': [],
            'improved_object_zh': '工作流', 'confidence': 0.8}


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
    client = Client([RELEVANCE, CLASSIFY, evidence])
    result = judge_item(ITEM, client)
    assert [name for name, _ in client.calls] == ['relevance', 'classify', 'evidence']
    assert result['primary'] == result['llm']['primary'] == 'harness'
    assert result['confidence'] == 0.8
    assert result['llm']['relevance']['model'] == 'fake'
    assert result['evidence_quick']['held_out']['value'] == 'yes'
    assert result['evidence_quick']['code_released']['value'] == 'unknown'
    assert result['evidence_notice']['zh'] == '自动判断，未核实'
    assert 'llm' not in ITEM


def test_borderline_classified_but_not_quick_evidence_and_exclude_stops():
    client = Client([{**RELEVANCE, 'label': 'borderline'}, CLASSIFY])
    result = judge_item(ITEM, client)
    assert [name for name, _ in client.calls] == ['relevance', 'classify']
    assert result['review_required']
    assert result['evidence_quick'] == unknown_evidence()
    client = Client([{**RELEVANCE, 'label': 'exclude', 'exclude_reason': 'off_topic'}])
    assert judge_item(ITEM, client)['label'] == 'exclude'
    assert len(client.calls) == 1


def test_existing_repo_and_lab_updates_never_judged():
    client = Client([])
    assert judge_item({**ITEM, 'in_repo': True}, client)['in_repo']
    assert judge_item({**ITEM, 'kind': 'post'}, client)['kind'] == 'post'
    assert not client.calls


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
