"""Curator-label regression evaluation; metadata fetch is an explicit operation."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET

import requests

import yaml

from scripts.common import ROOT, read_yaml
from scripts.feed.judge import judge_item
from scripts.feed.llm import FeedLLM, LLMConfigurationError, stage_settings

THRESHOLDS = {'include_recall': 0.90, 'include_precision': 0.80, 'primary_accuracy': 0.75}
GATE_THRESHOLDS = {'harness_precision': 0.85, 'harness_recall': 0.90}
HARNESS_SECTIONS = {'evolve_main', 'generalize', 'evidence_selection',
                    'improver', 'component', 'coevolution'}


def import_repository_labels(root=ROOT):
    """Interpret 'after 2026-04' as 2026-05 onward; never import candidates."""
    labels = []
    for paper in read_yaml(Path(root) / 'data/papers.yaml')['papers']:
        section = paper['section']
        if section in ('foundations', 'candidates') or paper['date'][:7] <= '2026-04' or not paper.get('arxiv'):
            continue
        primary = 'harness' if section in HARNESS_SECTIONS else {
            'evaluation': 'evaluation_benchmark', 'survey_theory': 'theory_survey'}[section]
        record = {'arxiv': paper['arxiv'], 'name': paper['title'], 'label': 'include', 'primary': primary}
        if primary == 'harness':
            record['harness_sub'] = section
        record.update(labeled_by='repository-import', repo_id=paper['id'],
                      source_section=section, source_date=paper['date'])
        labels.append(record)
    return labels


def initialize_labels(root=ROOT):
    root = Path(root)
    path = root / 'feed/eval/labeled.yaml'
    existing = read_yaml(path) if path.exists() else []
    owners = [record for record in existing if record['labeled_by'] == 'owner']
    records = import_repository_labels(root) + read_yaml(root / 'feed/eval/curator-seeds.yaml') + owners
    path.write_text('# Imported dates: 2026-05 onward. Curator-seed labels are unverified.\n'
                    + yaml.safe_dump(records, allow_unicode=True, sort_keys=False), encoding='utf-8')
    return records


def metadata_path(arxiv_id, root=ROOT):
    return Path(root) / 'feed/eval/metadata' / (arxiv_id.replace('/', '_') + '.json')


def cache_metadata(root=ROOT, fetcher=None):
    """Fetch metadata only, explicitly. Shared arXiv adapter enforces <=1/3sec."""
    if fetcher is None:
        from scripts.feed.fetch_arxiv import parse_atom, request
        def fetcher(ids):
            body = request({'id_list': ','.join(ids), 'max_results': 100})
            raw = Path(root) / 'feed/eval/raw'
            raw.mkdir(parents=True, exist_ok=True)
            batch_hash = hashlib.sha256(','.join(ids).encode()).hexdigest()[:16]
            date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            (raw / (date + '-' + batch_hash + '.atom')).write_text(body, encoding='utf-8')
            return parse_atom(body, source_id='arxiv-eval-metadata')
    labels = read_yaml(Path(root) / 'feed/eval/labeled.yaml')
    missing = sorted({record['arxiv'] for record in labels if not metadata_path(record['arxiv'], root).exists()})
    fetched, errors = [], []
    for start in range(0, len(missing), 100):
        batch = missing[start:start + 100]
        try:
            items = fetcher(batch)
        except (requests.RequestException, ET.ParseError, ValueError) as error:
            errors.append({'ids': batch, 'error': str(error)})
            continue
        for item in items:
            # API metadata is never synthesized from curated summaries.
            if not isinstance(item['title'], str) or not isinstance(item['abstract'], str):
                raise ValueError('arXiv metadata title and abstract must be strings')
            path = metadata_path(item['arxiv_id'], root)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(item, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
            fetched.append(item['arxiv_id'])
    still_missing = [arxiv_id for arxiv_id in missing if not metadata_path(arxiv_id, root).exists()]
    report = {'fetched': fetched, 'missing': still_missing, 'errors': errors,
              'status': 'complete' if not still_missing and not errors else 'incomplete'}
    (Path(root) / 'feed/eval/metadata-fetch.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def verify_metadata_identity(label, item):
    """Conservative title/name matching; ambiguous identifiers need owner review."""
    if not item.get('abstract', '').strip():
        return {'ok': False, 'expected_name': label['name'], 'returned_title': item['title'],
                'match_method': None, 'quote': None,
                'reason': 'Original arXiv abstract is empty; example cannot be judged'}
    def compact(value):
        value = unicodedata.normalize('NFKC', value).casefold()
        value = re.sub(r'\brsi\b', 'recursive self improvement', value)
        return ''.join(re.findall(r'\w+', value))
    expected, actual = compact(label['name']), compact(item['title'])
    # Curators sometimes add a short method name before a colon or in a suffix.
    aliases = [(expected, 'title')]
    if ':' in label['name']:
        prefix, suffix = label['name'].split(':', 1)
        aliases += [(compact(prefix), 'title-prefix'), (compact(suffix), 'title-without-curator-prefix')]
    aliases.append((compact(re.sub(r'\s*\([^()]+\)\s*$', '', label['name'])), 'title-without-nickname'))
    method = next((method for alias, method in aliases if alias and alias in actual), None)
    if method is None:
        ignored = {'a', 'an', 'the', 'and', 'of', 'for', 'with', 'via', 'through', 'from', 'to', 'in', 'on'}
        expected_tokens = set(re.findall(r'\w+', re.sub(r'\s*\([^()]+\)\s*$', '', label['name']).casefold())) - ignored
        title_tokens = set(re.findall(r'\w+', item['title'].casefold())) - ignored
        if len(expected_tokens) >= 3 and expected_tokens <= title_tokens:
            method = 'title-content-words'
    quote = None
    if method is None and re.fullmatch(r'[\w-]{3,}', label['name']):
        # A case-preserving named method in the abstract can verify a short
        # curator alias absent from the formal title (e.g. Recuris or MASS).
        match = re.search(r'(?<!\w)' + re.escape(label['name']) + r'(?!\w)', item.get('abstract', ''))
        if match:
            method = 'abstract-named-method'
            quote = item['abstract'][max(0, match.start() - 35):match.end() + 35]
    return {'ok': method is not None, 'expected_name': label['name'], 'returned_title': item['title'],
            'match_method': method, 'quote': quote,
            'reason': None if method else 'Curated name/title does not match returned arXiv title; owner verification required'}


def _label_signature(record):
    return tuple(record.get(key) for key in ('label', 'primary', 'harness_sub', 'exclude_reason'))


def effective_labels(records):
    """Keep historical labels on disk; latest explicit owner labels take precedence."""
    grouped = defaultdict(list)
    for record in records:
        grouped[record['arxiv']].append(record)
    active, conflicts = [], []
    for arxiv_id, history in grouped.items():
        owner = [record for record in history if record['labeled_by'] == 'owner']
        if owner:
            active.append(owner[-1])
        elif len({_label_signature(record) for record in history}) > 1:
            conflicts.append({'arxiv': arxiv_id, 'labels': history})
        else:
            active.append(history[-1])
    return active, conflicts


def add_owner_labels(root, items):
    path = Path(root) / 'feed/eval/labeled.yaml'
    records = read_yaml(path) if path.exists() else []
    signatures = {record.get('owner_decision_hash') for record in records}
    added = 0
    for item in items:
        review = item['review']
        if not item.get('arxiv_id') or (review['decision'] != 'reject'
                and not review.get('direction_override') and not review.get('summary_override')):
            continue
        fingerprint = hashlib.sha256(json.dumps(
            [item['arxiv_id'], review], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        if fingerprint in signatures:
            continue
        label = {'arxiv': item['arxiv_id'], 'name': item['title'],
                 'label': 'exclude' if review['decision'] == 'reject' else 'include',
                 'labeled_by': 'owner', 'needs_owner_review': False,
                 'owner_decision_hash': fingerprint, 'owner_review': deepcopy(review)}
        if label['label'] == 'include':
            override = review.get('direction_override')
            direction = override if isinstance(override, dict) else {'primary': override or item['primary']}
            label['primary'] = direction['primary']
            if label['primary'] == 'harness':
                label['harness_sub'] = direction.get('harness_sub', item.get('harness_sub'))
            label['secondary'] = direction.get('secondary', item.get('secondary', []))
        records.append(label)
        signatures.add(fingerprint)
        added += 1
    if added:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(records, allow_unicode=True, sort_keys=False), encoding='utf-8')
    return added


def append_owner_labels(items, root=ROOT):
    return add_owner_labels(root, items)


def harness_metrics(cases):
    positive = [case for case in cases if case['expected'].get('verdict') == 'harness']
    admitted = [case for case in cases if case['predicted'].get('gate', {}).get('verdict') == 'harness'
                and case['predicted'].get('label') == 'include']
    correct = sum(case['expected'].get('verdict') == 'harness' for case in admitted)
    return {'precision': correct / len(admitted) if admitted else None,
            'recall': correct / len(positive) if positive else None,
            'true_positive': correct, 'predicted': len(admitted), 'support': len(positive),
            'evaluated': len(cases)}


def score_predictions(cases):
    metrics = {}
    for label in ('include', 'exclude'):
        tp = sum(case['expected']['label'] == label and case['predicted'].get('label') == label for case in cases)
        predicted = sum(case['predicted'].get('label') == label for case in cases)
        support = sum(case['expected']['label'] == label for case in cases)
        metrics[label] = {'precision': tp / predicted if predicted else None,
                          'recall': tp / support if support else None,
                          'true_positive': tp, 'predicted': predicted, 'support': support}
    confusion = defaultdict(Counter)
    primary_cases = [case for case in cases if case['expected'].get('primary')]
    for case in primary_cases:
        confusion[case['expected']['primary']][case['predicted'].get('primary', '<not-classified>')] += 1
    primary_correct = sum(case['expected']['primary'] == case['predicted'].get('primary') for case in primary_cases)
    metrics['primary_accuracy'] = primary_correct / len(primary_cases) if primary_cases else None
    metrics['primary_support'] = len(primary_cases)
    metrics['confusion_matrix'] = {key: dict(value) for key, value in sorted(confusion.items())}
    metrics['borderline'] = [case['arxiv'] for case in cases if case['predicted'].get('label') == 'borderline']
    metrics['errors'] = [case['arxiv'] for case in cases if case['predicted'].get('label') == 'error'
                        or case['predicted'].get('error')]
    metrics['mistakes'] = [case for case in cases if case['expected']['label'] != case['predicted'].get('label')
                           or (case['expected'].get('primary') and case['expected']['primary'] != case['predicted'].get('primary'))]
    measured = {'include_recall': metrics['include']['recall'],
                'include_precision': metrics['include']['precision'],
                'primary_accuracy': metrics['primary_accuracy']}
    thresholds = THRESHOLDS
    gate_cases = [case for case in cases if 'verdict' in case['expected']]
    if gate_cases:
        metrics['harness'] = harness_metrics(gate_cases)
        metrics['harness_mistakes'] = [case for case in gate_cases
            if (case['expected']['verdict'] == 'harness') != (
                case['predicted'].get('gate', {}).get('verdict') == 'harness'
                and case['predicted'].get('label') == 'include')]
        metrics['harness_without_prompt_examples'] = harness_metrics(
            [case for case in gate_cases if not case['expected'].get('in_prompt_example')])
        metrics['harness_owner_review'] = harness_metrics(
            [case for case in gate_cases if case['expected'].get('labeled_by') == 'owner'])
        measured = {'harness_precision': metrics['harness']['precision'],
                    'harness_recall': metrics['harness']['recall']}
        thresholds = GATE_THRESHOLDS
    metrics['threshold_results'] = {name: {'value': measured[name], 'minimum': minimum,
                                         'passed': measured[name] is not None and measured[name] >= minimum}
                                   for name, minimum in thresholds.items()}
    metrics['thresholds_passed'] = all(result['passed'] for result in metrics['threshold_results'].values())
    return metrics


def report_markdown(report):
    text = ['# Follow RSI prompt evaluation', '', '**Status: ' + report['status'] + '**', '']
    if report['status'] == 'skipped':
        return '\n'.join(text + ['eval skipped — ' + report['reason'],
                                 '', 'No quality threshold has been measured or claimed to pass.', ''])
    text += [f"Evaluated: {report['evaluated']} / {report['total']}; missing metadata: {len(report['missing_metadata'])}; identity mismatches: {len(report['invalid_metadata'])}.",
             f"Curator seeds awaiting owner review: {report['needs_owner_review']}.", '',
             '| Metric | Measured | Required | Result |', '| --- | ---: | ---: | --- |']
    for name, result in report['metrics']['threshold_results'].items():
        value = 'unmeasured' if result['value'] is None else f"{result['value']:.3f}"
        text.append(f"| {name} | {value} | {result['minimum']:.2f} | {'pass' if result['passed'] else 'fail'} |")
    text += ['', 'Borderline predictions: ' + str(len(report['metrics']['borderline'])),
             'API/schema errors: ' + str(len(report['metrics']['errors'])), '', '## Direction confusion matrix', '',
             '```json', json.dumps(report['metrics']['confusion_matrix'], ensure_ascii=False, indent=2), '```', '',
             '## Mistakes', '']
    if 'harness' in report['metrics']:
        text += ['Baseline: owner re-review retained 8 of the 20 original Harness labels (precision 0.40).',
                 'The new set contains 25 owner decisions plus 20 preselected library positives. Ten calibration examples are visible in the gate prompt; the full-set result is not a blind holdout score.',
                 'Library labels are evaluation targets, not new full-text audits. HARBOR remains an owner-flagged scope ambiguity; its preselected positive label has not been changed to improve this score.',
                 'The 45-case set has more positives than the historical daily batch; compare the owner-only subset separately.', '',
                 '| Subset | Cases | Precision | Recall | True positives / target positives |',
                 '| --- | ---: | ---: | ---: | ---: |']
        for label, key in (('Full set', 'harness'), ('Owner-reviewed batch', 'harness_owner_review'),
                           ('Excluding prompt examples', 'harness_without_prompt_examples')):
            metric = report['metrics'][key]
            precision = 'unmeasured' if metric['precision'] is None else f"{metric['precision']:.3f}"
            recall = 'unmeasured' if metric['recall'] is None else f"{metric['recall']:.3f}"
            text.append(f"| {label} | {metric['evaluated']} | {precision} | {recall} | {metric['true_positive']} / {metric['support']} |")
        text += ['', '### Harness gate errors', '']
        for case in report['metrics']['harness_mistakes']:
            predicted = case['predicted']
            gate = predicted.get('gate', {})
            issues = predicted.get('scope_guard', {}).get('issues', [])
            text.append(f"- {case['arxiv']} ({case['expected']['name']}): expected {case['expected']['verdict']}; "
                        f"predicted {predicted.get('label')} / {gate.get('verdict', 'not run')}. "
                        + gate.get('why_zh', predicted.get('reason_zh', predicted.get('error', '')))
                        + (' Source guard: ' + ', '.join(issues) + '.' if issues else ''))
        if not report['metrics']['harness_mistakes']:
            text.append('No Harness gate errors in the evaluated subset.')
        text += ['', '### Scope and direction errors', '']
    for case in report['metrics']['mistakes']:
        expected = case['expected']
        predicted = case['predicted']
        text.append(f"- {case['arxiv']}: expected {expected['label']} / {expected.get('primary', '—')}; "
                    f"predicted {predicted.get('label')} / {predicted.get('primary', '—')}. "
                    + predicted.get('reason_zh', predicted.get('error', '')))
    if not report['metrics']['mistakes']:
        text.append('No mistakes in the evaluated subset.' if report['evaluated'] else 'No examples evaluated.')
    if report['missing_metadata']:
        text += ['', 'Missing metadata (not synthesized): ' + ', '.join(report['missing_metadata'])]
    if report['invalid_metadata']:
        text += ['', '## Metadata identity mismatches', '']
        for item in report['invalid_metadata']:
            text.append(f"- {item['arxiv']}: expected **{item['expected_name']}**, returned **{item['returned_title']}**. No label changed; example not scored.")
    if report['conflicting_labels']:
        text += ['', 'Conflicting curator/import labels remain unchanged and require owner resolution.']
    if report['status'] == 'incomplete':
        text += ['', 'Incomplete evaluation is not a passing quality gate.']
    text += ['', 'Recommendations: inspect false negatives for persistence/RSI scope, false positives for static or single-round systems, and direction errors for the object retained between rounds. Keep labels unchanged unless the owner explicitly corrects them.', '']
    return '\n'.join(text)


def run_evaluation(root=ROOT, client=None, workers=1, *, label_file='labeled.yaml', report_prefix='report'):
    root = Path(root)
    labels, conflicts = effective_labels(read_yaml(root / 'feed/eval' / label_file))
    report = {'generated_at': datetime.now(timezone.utc).isoformat(), 'total': len(labels),
              'needs_owner_review': sum(bool(label.get('needs_owner_review')) for label in labels),
              'conflicting_labels': conflicts,
              'thresholds': GATE_THRESHOLDS if any('verdict' in label for label in labels) else THRESHOLDS}
    if client is None:
        try:
            client = FeedLLM.from_env(root)
        except LLMConfigurationError as error:
            report.update(status='skipped', reason=str(error), evaluated=0, thresholds_passed=None)
            _write_report(root, report, report_prefix)
            return report
    report['model'] = client.model
    report['stage_models'] = {stage: stage_settings(stage, root, client.model)['model']
                              for stage in ('relevance', 'classify', 'harness_gate')}
    cases, missing, invalid, ready = [], [], [], []
    for label in labels:
        path = metadata_path(label['arxiv'], root)
        if not path.exists():
            missing.append(label['arxiv'])
            continue
        item = json.loads(path.read_text(encoding='utf-8'))
        identity = verify_metadata_identity(label, item)
        if not identity['ok']:
            invalid.append({'arxiv': label['arxiv'], **identity})
            continue
        item.setdefault('id', 'arxiv:' + label['arxiv'])
        item['eval_identity'] = identity
        ready.append((label, item))

    def evaluate_one(pair):
        label, item = pair
        # Library labels are evaluation targets, not input features. Exercise the
        # same model/quote/gate path as an uncurated discovery, without code reads.
        result = judge_item({**item, 'in_repo': False}, client, root, include_evidence=False)
        fields = ('label', 'exclude_reason', 'reason_zh', 'scope_kind', 'scope_support', 'scope_guard',
                  'primary', 'harness_sub', 'secondary', 'confidence', 'improved_object_zh', 'gate')
        prediction = {field: result[field] for field in fields if field in result}
        provenance = result['llm']
        if 'error' in provenance:
            prediction['error'] = provenance['error']['message']
        return {'arxiv': label['arxiv'], 'expected': label,
                'predicted': prediction, 'provenance': provenance, 'identity': item['eval_identity']}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        cases = list(executor.map(evaluate_one, ready))
    metrics = score_predictions(cases)
    report.update(status='incomplete' if missing or invalid or conflicts or metrics['errors'] else 'complete',
                  evaluated=len(cases), missing_metadata=missing, invalid_metadata=invalid, metrics=metrics,
                  cases=cases, thresholds_passed=metrics['thresholds_passed'] and not missing and not invalid and not conflicts and not metrics['errors'])
    _write_report(root, report, report_prefix)
    return report


def _write_report(root, report, prefix='report'):
    folder = root / 'feed/eval'
    (folder / (prefix + '.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    (folder / (prefix + '.md')).write_text(report_markdown(report), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch-metadata', action='store_true', help='Explicit network fetch; no PDFs')
    parser.add_argument('--initialize-labels', action='store_true')
    parser.add_argument('--workers', type=int, choices=range(1, 5), default=1,
                        help='Parallel independent LLM examples (1–4); arXiv fetches stay serial')
    args = parser.parse_args()
    if args.initialize_labels:
        initialize_labels()
    if args.fetch_metadata:
        print(json.dumps(cache_metadata(), ensure_ascii=False, indent=2))
        return
    gate_cases = ROOT / 'feed/eval/harness-gate-cases.yaml'
    report = run_evaluation(workers=args.workers,
                            label_file='harness-gate-cases.yaml' if gate_cases.exists() else 'labeled.yaml',
                            report_prefix='gate-report' if gate_cases.exists() else 'report')
    print(report_markdown(report))
    if report['status'] != 'skipped' and not report['thresholds_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
