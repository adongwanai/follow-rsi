import json
import shutil

import yaml

from scripts.common import ROOT, read_yaml
from scripts.feed.eval import (add_owner_labels, cache_metadata, effective_labels,
                               import_repository_labels, run_evaluation, score_predictions,
                               verify_metadata_identity)
from test_judge import CLASSIFY, GATE, ITEM, RELEVANCE


def test_exact_user_seed_labels_and_no_relabeling():
    seeds = read_yaml(ROOT / 'feed/eval/curator-seeds.yaml')
    assert len(seeds) == 27
    assert {x['arxiv'] for x in seeds} == {
        '2609.14858', '2609.15364', '2610.11794', '2610.13912', '2610.20431', '2607.28568',
        '2609.08183', '2610.14118', '2609.36675', '2610.15772', '2610.22192', '2609.39306',
        '2609.30652', '2609.05295', '2609.17523', '2610.18842', '2609.00137', '2609.15802',
        '2610.14625', '2607.21461', '2609.38288', '2608.01964', '2608.05013', '2608.27969',
        '2607.20709', '2607.07007', '2609.27242'}
    assert all(x['labeled_by'] == 'curator-seed' and x['needs_owner_review'] for x in seeds)
    assert sum(x['label'] == 'exclude' for x in seeds) == 8
    labels = read_yaml(ROOT / 'feed/eval/labeled.yaml')
    assert [x for x in labels if x['labeled_by'] == 'curator-seed'] == seeds


def test_repository_import_cutoff_and_sections():
    labels = import_repository_labels()
    assert len(labels) == 83
    evaluation_ids = {row['repo_id'] for row in labels if row['primary'] == 'evaluation_benchmark'}
    assert {'rsihub', 'harnessdev', 'aspire', 's3gym'} <= evaluation_ids
    assert all(x['source_date'][:7] > '2026-04' for x in labels)
    assert all(x['source_section'] not in ('foundations', 'candidates') for x in labels)
    for label in labels:
        if label['source_section'] == 'evaluation':
            assert label['primary'] == 'evaluation_benchmark'
        elif label['source_section'] == 'survey_theory':
            assert label['primary'] == 'theory_survey'
        else:
            assert label['primary'] == 'harness' and label['harness_sub'] == label['source_section']


def case(identity, expected, predicted):
    return {'arxiv': identity, 'expected': expected, 'predicted': predicted}


def test_metrics_count_borderline_as_missed_include_and_report_confusion():
    cases = [case('a', {'label': 'include', 'primary': 'harness'}, {'label': 'include', 'primary': 'harness'}),
             case('b', {'label': 'include', 'primary': 'ai4ai'}, {'label': 'borderline', 'primary': 'harness'}),
             case('c', {'label': 'exclude'}, {'label': 'include', 'primary': 'harness'}),
             case('d', {'label': 'exclude'}, {'label': 'exclude'})]
    metrics = score_predictions(cases)
    assert metrics['include']['precision'] == metrics['include']['recall'] == 0.5
    assert metrics['exclude']['precision'] == 1 and metrics['exclude']['recall'] == 0.5
    assert metrics['primary_accuracy'] == 0.5
    assert metrics['confusion_matrix']['ai4ai']['harness'] == 1
    assert metrics['borderline'] == ['b']
    assert len(metrics['mistakes']) == 2
    assert not metrics['thresholds_passed']


def test_classification_error_preserves_relevance_score():
    metrics = score_predictions([case('a', {'label': 'include', 'primary': 'harness'},
                                     {'label': 'include', 'error': 'classify invalid'})])
    assert metrics['include']['precision'] == metrics['include']['recall'] == 1
    assert metrics['primary_accuracy'] == 0
    assert metrics['errors'] == ['a']


def test_owner_label_append_is_idempotent_and_keeps_seed(tmp_path):
    folder = tmp_path / 'feed/eval'
    folder.mkdir(parents=True)
    seed = {'arxiv': '2610.12345', 'name': 'Sample', 'label': 'include', 'primary': 'harness',
            'harness_sub': 'component', 'labeled_by': 'curator-seed', 'needs_owner_review': True}
    (folder / 'labeled.yaml').write_text(yaml.safe_dump([seed]))
    item = {'arxiv_id': '2610.12345', 'title': 'Sample', 'review': {
        'decision': 'reject', 'week': '2026-W44', 'note': 'Static framework'}}
    assert add_owner_labels(tmp_path, [item]) == 1
    assert add_owner_labels(tmp_path, [item]) == 0
    records = read_yaml(folder / 'labeled.yaml')
    assert records[0] == seed
    active, conflicts = effective_labels(records)
    assert not conflicts and active[0]['label'] == 'exclude' and active[0]['labeled_by'] == 'owner'


def test_conflicting_curator_labels_stay_unresolved():
    records = [{'arxiv': 'x', 'label': 'include', 'primary': 'harness', 'labeled_by': 'repository-import'},
               {'arxiv': 'x', 'label': 'exclude', 'labeled_by': 'curator-seed'}]
    active, conflicts = effective_labels(records)
    assert active == [] and len(conflicts) == 1
    assert records[0]['label'] == 'include'


def test_metadata_cache_uses_actual_fetcher_result_and_reports_absent_records(tmp_path):
    folder = tmp_path / 'feed/eval'
    folder.mkdir(parents=True)
    labels = [{'arxiv': '2610.12345'}, {'arxiv': '2610.99999'}]
    (folder / 'labeled.yaml').write_text(yaml.safe_dump(labels))
    calls = []
    def fetch(ids):
        calls.append(ids)
        return [{'arxiv_id': '2610.12345', 'title': 'Recorded fixture title', 'abstract': 'Recorded fixture abstract'}]
    report = cache_metadata(tmp_path, fetch)
    assert report['status'] == 'incomplete' and report['missing'] == ['2610.99999']
    cache_metadata(tmp_path, fetch)
    assert calls[1] == ['2610.99999']
    assert not (folder / 'metadata/2610.99999.json').exists()


def test_missing_credentials_is_explicit_skipped_not_pass(tmp_path, monkeypatch):
    folder = tmp_path / 'feed/eval'
    folder.mkdir(parents=True)
    (folder / 'labeled.yaml').write_text('[]\n')
    for name in ('LLM_PROVIDER', 'LLM_MODEL', 'LLM_API_KEY'):
        monkeypatch.delenv(name, raising=False)
    report = run_evaluation(tmp_path)
    assert report['status'] == 'skipped' and report['thresholds_passed'] is None
    assert 'eval skipped' in (folder / 'report.md').read_text()


def test_missing_metadata_never_passes_with_mock_model(tmp_path):
    folder = tmp_path / 'feed/eval'
    folder.mkdir(parents=True)
    label = {'arxiv': '2610.12345', 'name': 'Example', 'label': 'include', 'primary': 'harness',
             'labeled_by': 'curator-seed', 'needs_owner_review': True}
    (folder / 'labeled.yaml').write_text(yaml.safe_dump([label]))
    class Client:
        model = 'fixture-model'
        def run(self, *args, **kwargs):
            raise AssertionError('No metadata means no LLM request')
    report = run_evaluation(tmp_path, Client())
    assert report['status'] == 'incomplete'
    assert report['evaluated'] == 0 and not report['thresholds_passed']


def test_complete_fixture_evaluation_runs_relevance_then_classify(tmp_path):
    folder = tmp_path / 'feed/eval'
    (folder / 'metadata').mkdir(parents=True)
    shutil.copyfile(ROOT / 'feed/taxonomy.yaml', tmp_path / 'feed/taxonomy.yaml')
    labels = [{'arxiv': '2610.12345', 'name': 'Offline test fixture', 'label': 'include', 'primary': 'harness', 'labeled_by': 'owner'},
              {'arxiv': '2610.99999', 'name': 'Offline test fixture', 'label': 'exclude', 'labeled_by': 'owner'}]
    (folder / 'labeled.yaml').write_text(yaml.safe_dump(labels))
    for label in labels:
        (folder / 'metadata' / (label['arxiv'] + '.json')).write_text(json.dumps({
            'arxiv_id': label['arxiv'], 'version': 1, 'title': 'Offline test fixture',
            'abstract': ITEM['abstract'] if label['label'] == 'include' else 'We study galaxy formation.'}))
    class Client:
        model = 'fixture-model'
        def __init__(self):
            self.calls = []
        def run(self, name, item, **kwargs):
            self.calls.append((name, item['arxiv_id']))
            if name == 'classify':
                data = CLASSIFY
            elif name == 'harness_gate':
                data = GATE
            else:
                data = RELEVANCE if item['arxiv_id'] == '2610.12345' else {
                    **RELEVANCE, 'label': 'exclude', 'exclude_reason': 'off_topic',
                    'scope_support': {**RELEVANCE['scope_support'], 'exclusion_quote': 'We study galaxy formation.'}}
            return {'data': data, 'model': self.model, 'prompt_hash': name, 'cache_key': name + item['arxiv_id']}
    client = Client()
    report = run_evaluation(tmp_path, client)
    assert client.calls == [('relevance', '2610.12345'), ('classify', '2610.12345'),
                            ('harness_gate', '2610.12345'), ('relevance', '2610.99999')]
    assert report['status'] == 'complete' and report['thresholds_passed']
    assert report['metrics']['include']['precision'] == report['metrics']['include']['recall'] == 1


def test_arxiv_identity_mismatch_cannot_score_curated_label(tmp_path):
    assert verify_metadata_identity({'name': 'Dream-RSI'}, {'title': 'Dream-RSI: a study', 'abstract': 'Test fixture.'})['ok']
    assert verify_metadata_identity({'name': 'Memento 3'}, {'title': 'Memento-3: Memory', 'abstract': 'Test fixture.'})['ok']
    assert not verify_metadata_identity({'name': 'Dream-RSI'}, {'title': 'Galaxy Formation', 'abstract': 'Test fixture.'})['ok']
    assert not verify_metadata_identity({'name': 'Dream-RSI'}, {'title': 'Dream-RSI', 'abstract': ''})['ok']
    folder = tmp_path / 'feed/eval'
    (folder / 'metadata').mkdir(parents=True)
    (folder / 'labeled.yaml').write_text(yaml.safe_dump([{'arxiv': '2610.12345', 'name': 'Dream-RSI',
        'label': 'include', 'primary': 'experience_world_model', 'labeled_by': 'curator-seed'}]))
    (folder / 'metadata/2610.12345.json').write_text(json.dumps({'title': 'Galaxy Formation', 'abstract': 'A real but unrelated paper.'}))
    class Client:
        model = 'fixture-model'
        def run(self, *args, **kwargs):
            raise AssertionError('Wrong paper identity must never be scored')
    report = run_evaluation(tmp_path, Client())
    assert report['status'] == 'incomplete' and report['evaluated'] == 0
    assert len(report['invalid_metadata']) == 1 and not report['thresholds_passed']
