from copy import deepcopy
import json
import shutil

import pytest
import yaml

from scripts.common import ROOT
from scripts.feed.judge import apply_gate, guard_harness, run_harness_gate
from scripts.feed.llm import read_prompt, stage_settings, truncate_fields, validate_result
from scripts.feed.eval import score_predictions
from test_judge import Client, GATE, ITEM

RECORDED = json.loads((ROOT / 'tests/feed/fixtures/harness-gate-recorded.json').read_text())


def test_recording_covers_requested_positive_and_negative_boundaries():
    assert {case['arxiv'] for case in RECORDED['cases']} == {
        '2610.06830', '2610.16523', '2610.26453', '2610.17184',
        '2610.15915', '2610.27227', '2610.35434'}
    assert all(case['provenance']['samples'][0]['model'] == 'deepseek-v4-pro'
               for case in RECORDED['cases'])


@pytest.mark.parametrize('case', RECORDED['cases'], ids=lambda case: case['arxiv'])
def test_recorded_gate_responses_preserve_harness_boundary_offline(case):
    response = deepcopy(case['provenance']['samples'][0]['data'])
    _, schema = read_prompt('harness_gate')
    validate_result('harness_gate', response, schema)
    checked = guard_harness(case['abstract'], response)
    assert (checked['verdict'] == 'harness') is case['expected_harness']
    assert checked == case['gate']


@pytest.mark.parametrize('field', ['feedback_driven', 'persists_across_tasks'])
def test_quote_not_in_abstract_downgrades_to_borderline(field):
    gate = deepcopy(GATE)
    gate[field]['quote'] = 'An invented claim that is not in the source.'
    checked = guard_harness(ITEM['abstract'], gate)
    assert checked['verdict'] == 'borderline'
    assert checked[field] == {'value': 'unclear', 'quote': None}
    assert gate[field]['value'] == 'yes'


@pytest.mark.parametrize(('obj', 'primary'), [
    ('model_weights', 'model_weights'), ('training_env_reward', 'data_task'),
    ('external_artifact', 'ai4ai'), ('memory_entries', 'experience_world_model'),
])
def test_other_objects_cannot_pass_even_if_model_calls_them_harness(obj, primary):
    checked = guard_harness(ITEM['abstract'], {**GATE, 'improved_object': obj})
    assert checked['verdict'] == 'other_direction'
    assert checked['suggested_primary'] == primary and checked['harness_specific'] == 'no'


def test_general_rsi_study_cannot_pass_as_harness():
    assert guard_harness(ITEM['abstract'], {**GATE, 'harness_specific': 'no'})['verdict'] == 'borderline'


def test_memory_benchmark_remains_a_study_not_a_memory_method():
    checked = guard_harness(ITEM['abstract'], {**GATE, 'improved_object': 'memory_entries',
                            'suggested_primary': 'evaluation_benchmark',
                            'verdict': 'other_direction', 'harness_specific': 'no'})
    assert checked['suggested_primary'] == 'evaluation_benchmark'
    assert checked['verdict'] == 'other_direction'


def test_gate_cannot_recast_an_evidence_supported_benchmark_as_a_method():
    item = {'label': 'include', 'primary': 'evaluation_benchmark', 'scope_kind': 'evaluation',
            'harness_sub': None, 'secondary': ['harness']}
    gate = {**GATE, 'verdict': 'other_direction', 'suggested_primary': 'ai4ai',
            'improved_object': 'external_artifact', 'harness_specific': 'no'}
    result = apply_gate(item, gate)
    assert result['primary'] == result['gate']['suggested_primary'] == 'evaluation_benchmark'
    assert result['gate']['harness_specific'] == 'no' and result['secondary'] == []


@pytest.mark.parametrize('agree', [True, False])
def test_flash_needs_two_independent_matching_judgements(tmp_path, agree):
    (tmp_path / 'feed').mkdir()
    shutil.copy(ROOT / 'feed/taxonomy.yaml', tmp_path / 'feed/taxonomy.yaml')
    (tmp_path / 'feed/model.yaml').write_text(yaml.safe_dump({
        'model': 'deepseek-flash', 'stages': {'harness_gate': {'model': 'deepseek-flash', 'samples': 1}}}))
    second = deepcopy(GATE)
    if not agree:
        second['verdict'] = 'borderline'
    client = Client([GATE, second])
    gate, provenance = run_harness_gate(ITEM, client, tmp_path)
    assert len(client.calls) == 2
    assert client.calls[0][1]['retry_token'] != client.calls[1][1]['retry_token']
    assert provenance['agreement'] is agree
    assert gate['verdict'] == ('harness' if agree else 'borderline')
    assert stage_settings('harness_gate', tmp_path)['temperature'] > 0


def test_gate_quotes_and_explanations_truncate_to_declared_limits():
    data = {**deepcopy(GATE), 'why_zh': '理' * 75}
    data['feedback_driven']['quote'] = 'q' * 250
    paths = truncate_fields(data)
    assert len(data['why_zh']) == 60 and len(data['feedback_driven']['quote']) == 200
    assert set(paths) == {'why_zh', 'feedback_driven.quote'}


def test_gate_precision_and_recall_do_not_count_classifier_labels():
    cases = [
        {'arxiv': 'a', 'expected': {'label': 'include', 'verdict': 'harness'},
         'predicted': {'label': 'include', 'primary': 'harness', 'gate': {'verdict': 'harness'}}},
        {'arxiv': 'b', 'expected': {'label': 'include', 'verdict': 'harness'},
         'predicted': {'label': 'include', 'primary': 'harness', 'gate': {'verdict': 'borderline'}}},
        {'arxiv': 'c', 'expected': {'label': 'exclude', 'verdict': 'exclude'},
         'predicted': {'label': 'include', 'gate': {'verdict': 'harness'}}},
    ]
    metrics = score_predictions(cases)
    assert metrics['harness']['precision'] == metrics['harness']['recall'] == .5
    assert not metrics['thresholds_passed']
    assert metrics['threshold_results']['harness_precision']['minimum'] == .85
    assert metrics['threshold_results']['harness_recall']['minimum'] == .90
