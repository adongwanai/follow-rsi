"""Bind recorded review phases to a parent-declared frozen canonical snapshot.

This only writes audit advice under build. Required hashes must come from the
completed parent batch and final independent report; do not run while either
is changing. It does not turn a source comparison or model label into approval.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import yaml

from coverage_ledger import (BASE, ROOT, SOURCE_FIELDS, input_fingerprint,
                             new_catalog_provenance, read_json, read_rows,
                             stale_templates, summary_quality)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


verified_files = {}


def verify(relative, expected):
    if relative not in verified_files:
        verified_files[relative] = sha(ROOT / relative)
    if verified_files[relative] != expected:
        raise ValueError(f'Source changed: {relative}')


def phase(ident, number, name, report, source, fields=SOURCE_FIELDS, **details):
    relative = str(report.relative_to(ROOT))
    if relative not in verified_files:
        verified_files[relative] = sha(report)
    return {'id': ident, 'round': number, 'phase': name, 'report_file': relative,
            'report_sha256': verified_files[relative],
            'input_fingerprint_fields': list(fields),
            'input_fingerprint_sha256': input_fingerprint(source, fields),
            'formal_decision': 'defer', 'publication_authorized': False, **details}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canonical-sha256', required=True)
    parser.add_argument('--independent-manifest-sha256', required=True)
    parser.add_argument('--independent-manifest', type=Path,
                        default=ROOT / 'docs/internal/reports/maintenance-2026-10-30/independent/manifest.json')
    args = parser.parse_args()
    current_path = ROOT / 'data/feed/items.jsonl'
    third_path = args.independent_manifest.resolve()
    assert sha(current_path) == args.canonical_sha256, 'Canonical snapshot is not frozen at declared hash'
    assert sha(third_path) == args.independent_manifest_sha256, 'Independent report changed'
    current, _ = read_rows(current_path)
    baseline, _ = read_rows(BASE / 'before/data/feed/items.jsonl')
    assert len(baseline) == 1124 and not baseline.keys() - current.keys()
    third = read_json(third_path)
    if third['status'].startswith('in_progress'):
        raise ValueError('Independent report still in progress; do not freeze advice')
    identity_path = BASE / 'identity-checks.json'
    s2_path = BASE / 's2-primary/verification-ledger.json'
    identity = {row['id']: row for row in read_json(identity_path)}
    s2 = {row['id']: row for row in read_json(s2_path)}
    catalog_path = ROOT / 'data/papers.yaml'
    catalog = {paper['id']: paper for paper in yaml.safe_load(catalog_path.read_text())['papers']}
    catalog_hash = sha(catalog_path)
    advice, skipped_round2 = [], []
    source_fields = ('kind', 'title', 'published', 'updated', 'version')
    for ident, old in baseline.items():
        item = current[ident]
        protected = bool(old.get('review', {}).get('correction_file') or old.get('in_repo'))
        if ident in identity:
            check = identity[ident]
            verify(check['source_file'], check['source_sha256'])
            advice.append(phase(ident, 1, 'identity_original_dates_versions_and_abstract_comparison',
                                identity_path, old, source_fields,
                                verdict=check['status'], reviewer_type='recorded_source_verification',
                                scope_approved=False, abstract_equivalent_to_official=check['abstract_matches'],
                                original_date_matches_official=str(check['previous_published'])[:10] == str(check['official_published'])[:10],
                                original_version_matches_official=check['previous_version'] == check['official_version'],
                                source_file=check['source_file'], source_sha256=check['source_sha256'],
                                limit='Identity/date comparison; does not certify all paper claims or scope.'))
        elif ident in s2:
            check = s2[ident]
            for receipt in check['network_receipts']:
                if receipt.get('sha256'):
                    verify(receipt['body_file'], receipt['sha256'])
            advice.append(phase(ident, 1, 'publisher_identity_dates_and_abstract_availability',
                                s2_path, old, source_fields,
                                verdict=check['abstract_status'], reviewer_type='recorded_source_verification',
                                identity_result=check['identity'], scope_approved=False,
                                limit='Publisher metadata verification; date conflicts and absent abstracts remain recorded.'))
        if item['kind'] != 'paper' or protected:
            continue
        new_catalog = new_catalog_provenance(item, old, catalog, catalog_hash)
        if new_catalog and new_catalog['verified_curated_source']:
            advice.append(phase(ident, 2, 'new_curated_library_text_and_scope_sync',
                                catalog_path, item, verdict=item['label'],
                                reviewer_type='verified_library_copy_not_llm_generation',
                                curated_source=new_catalog,
                                limit='Library sync is not a successful LLM summary and does not authorize publication.'))
            continue
        model = item.get('llm', {})
        quality = summary_quality(item)
        stale, missing = stale_templates(item)
        reasons = []
        if model.get('label') not in ('include', 'borderline', 'exclude') or model.get('error'):
            reasons.append('model_error_or_missing_label')
        if stale or missing or 'relevance' not in model:
            reasons.append('stale_or_unrecorded_model_provenance')
        if not quality['summary_complete']:
            reasons += quality['issues']
        if reasons:
            skipped_round2.append({'id': ident, 'reasons': reasons})
            continue
        advice.append(phase(ident, 2, 'current_prompt_classification_and_required_bilingual_summary',
                            current_path, item, verdict=item['label'], reviewer='follow-rsi-model-pipeline',
                            reviewer_type='llm_pipeline_not_owner',
                            gate_verdict=item.get('gate', {}).get('verdict'),
                            provenance_stages=[stage for stage in ('relevance', 'classify', 'harness_gate', 'evidence', 'summarize', 'translate') if stage in model],
                            scope_guard=item.get('scope_guard'), summary_quality=quality,
                            limit='Relevance/classify/gate count together as one model phase, not three reviews.'))

    post_path = BASE / 'labs/results.json'
    post_index_path = ROOT / 'docs/internal/reports/maintenance-2026-10-30/primary/labs-source-index.json'
    post_source_path = ROOT / 'build/four-paper-review-2026-10-30/primary/labs-scope-review.json'
    source_reviews = read_json(post_source_path)
    post_sources = {row['id']: row for row in source_reviews['reviews']}
    for row in read_json(post_path):
        ident = row['id']
        verify(row['source_file'], row['sha256'])
        verify(row['text_file'], row['text_sha256'])
        body = {'body_file': row['text_file'], 'body_sha256': row['text_sha256']}
        advice.append(phase(ident, 1, 'official_announcement_source_and_original_date',
                            post_index_path, baseline[ident], verdict='source_hash_verified',
                            reviewer_type='recorded_source_verification', scope_approved=False, **body))
        final_source = post_sources.get(ident)
        suggestion = (final_source['recommended_verdict'] if final_source else row['gate']['verdict'])
        quality = summary_quality(current[ident], scope_suggests_retention=suggestion in ('harness', 'borderline'))
        if row['status'] == 'model_scope_reviewed' and quality['summary_complete']:
            advice.append(phase(ident, 2, 'official_post_body_model_scope_review', post_path,
                                baseline[ident], verdict=row['gate']['verdict'],
                                reviewer='follow-rsi-post-body-model', reviewer_type='llm_pipeline_not_owner',
                                summary_quality=quality, provenance=row['provenance'], **body))
        else:
            skipped_round2.append({'id': ident, 'reasons': quality['issues'] or [row['status']]})
        if final_source:
            advice.append(phase(ident, 3, 'separate_agent_official_post_body_scope_review',
                                post_source_path, baseline[ident], verdict=final_source['recommended_verdict'],
                                reviewer=source_reviews['reviewer'], reviewer_type='codex_source_reader_not_owner',
                                source_scope=final_source['recommended_topic'],
                                body_file=final_source['text_file'], body_sha256=final_source['text_sha256']))

    targets = read_json(BASE / 'independent-round3/targets.json')['targets']
    adjudications = {}
    for filename in ('adjudications.jsonl', 'negative-adjudications.jsonl'):
        path = BASE / 'independent-round3' / filename
        for row in read_jsonl(path):
            adjudications.setdefault(row['id'], []).append((path, row))
    for row in third['coverage']:
        if not row['original_source_review_available']:
            continue
        ident, target = row['id'], targets[row['id']]
        assert ident in baseline, 'New HF appendices must not enter fixed backlog'
        abstract_source = target['abstract_source']
        verify(abstract_source['file'], abstract_source['sha256'])
        record_path = BASE / 'independent-round3/records' / (ident.replace(':', '-') + '.json')
        record = read_json(record_path) if record_path.exists() else {}
        body = {}
        excerpt = ''
        receipt_relative = row.get('body_receipt') or record.get('body_receipt')
        if receipt_relative:
            receipt = read_json(ROOT / receipt_relative)
            if receipt.get('text_file'):
                verify(receipt['text_file'], receipt['text_sha256'])
                verify(receipt['excerpt_file'], receipt['excerpt_sha256'])
                if row['review_level'] in ('official_body_selected_passages', 'official_body_excerpt_and_abstract'):
                    excerpt = (ROOT / receipt['excerpt_file']).read_text()
                    body = {'body_file': receipt['text_file'], 'body_sha256': receipt['text_sha256'],
                            'body_receipt': receipt_relative}
        assert hashlib.sha256((target['official_abstract'] + '\n' + excerpt).encode()).hexdigest() == row['source_hash'], ident
        source_item = {'kind': 'paper', 'title': target['title'],
                       'abstract': target['official_abstract'], 'version': target['official_version']}
        fields = ('kind', 'title', 'abstract', 'version') if target['arxiv_id'] else ('kind', 'title', 'abstract')
        source_adjudications = []
        for path, judgment in adjudications.get(ident, []):
            if judgment.get('body_file'):
                verify(judgment['body_file'], judgment['body_sha256'])
                text = (ROOT / judgment['body_file']).read_text()
                assert all(quote in text for quote in judgment['quotes'])
            source_adjudications.append({'report_file': str(path.relative_to(ROOT)),
                                        'report_sha256': sha(path), 'judgment': judgment})
        advice.append(phase(ident, 3, 'separate_source_scope_review_and_recorded_adjudication',
                            third_path, source_item, fields,
                            verdict=row['effective_scope_suggestion'], reviewer=third['reviewer_agent'],
                            reviewer_type=record.get('reviewer_type', 'codex_source_reader_not_owner'),
                            model_status=row['model_status'], model_recommendation=row['model_recommendation'],
                            model_source_hash=row.get('model_source_hash', record.get('source_hash')),
                            api_error_type=row.get('api_error_type'), http_status=row.get('http_status'),
                            source_reading_adjudication=row['source_reading_adjudication'],
                            source_hash=row['source_hash'], prompt_hash=row['prompt_hash'],
                            source_record=str(record_path.relative_to(ROOT)) if record else None,
                            source_record_sha256=sha(record_path) if record else None,
                            source_adjudications=source_adjudications, review_level=row['review_level'],
                            scope_suggestion=(source_adjudications[-1]['judgment'].get('scope')
                                              if source_adjudications else record.get('data', {}).get('scope')),
                            limitations=third['limitations'], **body))

    advice.extend(read_json(BASE / 'hf-today-advice-manifest.json'))
    assert sha(current_path) == args.canonical_sha256
    assert sha(third_path) == args.independent_manifest_sha256
    output = BASE / 'advice-manifest.json'
    output.write_text(json.dumps(advice, ensure_ascii=False, indent=2) + '\n')
    result = {'canonical_sha256': args.canonical_sha256,
              'independent_manifest_sha256': args.independent_manifest_sha256,
              'baseline_unique_ids': len(baseline), 'canonical_unique_ids': len(current),
              'records_by_round': dict(Counter(row['round'] for row in advice)),
              'records_by_phase': dict(Counter(row['phase'] for row in advice)),
              'verified_source_files': len(verified_files),
              'round2_incomplete': skipped_round2,
              'round2_incomplete_reason_counts': dict(Counter(reason for row in skipped_round2 for reason in row['reasons'])),
              'all_formal_decisions_defer': True, 'publication_authorized': False}
    (BASE / 'advice-manifest-validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'round2_incomplete'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
