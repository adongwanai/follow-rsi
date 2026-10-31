#!/usr/bin/env python3
"""Read-only accounting for the fixed 1124-item backlog; never publishes.

Run only after the parent has recorded the model batch's final state:
  .venv/bin/python build/backlog-all-2026-10-30/coverage_ledger.py \
      --model-status blocked --advice-manifest path/to/advice-manifest.json

The optional advice manifest is a JSON list. Each entry has id, round (1-3),
report_file, verdict, and input_fingerprint_sha256, calculated by the public
input_fingerprint function below. Full-body reviews also supply body_file and
body_sha256. A manifest records review provenance, never owner approval.
Historical three-round reuse candidates are reported separately: unchanged
source text alone does not prove their interpretation follows today's rules.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unicodedata

import yaml

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
SOURCE_FIELDS = ('kind', 'title', 'abstract', 'version', 'comments')
ORIGINAL_FACT_FIELDS = ('title', 'abstract', 'version', 'published', 'updated',
                        'authors', 'comments', 'categories', 'links')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalized(value):
    return ' '.join(unicodedata.normalize('NFKC', value).split())


def input_fingerprint(item, fields=SOURCE_FIELDS):
    """Fingerprint model inputs, excluding generated labels, gates and summaries."""
    values = {key: normalized(item[key]) if isinstance(item.get(key), str)
              else item.get(key) for key in fields}
    return digest(json.dumps(values, ensure_ascii=False, sort_keys=True,
                             separators=(',', ':')).encode())


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def relative(path):
    return str(path.resolve().relative_to(ROOT))


def read_rows(path):
    raw = path.read_bytes()
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    result = {row['id']: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f'Duplicate IDs in {path}; resolve explicitly before accounting')
    return result, digest(raw)


def checked_advice(path, current):
    advice = {}
    report_hashes = {}
    manifest = read_json(path)
    if not isinstance(manifest, list):
        raise ValueError('Advice manifest must be a JSON list')
    for entry in manifest:
        ident, round_number = entry['id'], entry['round']
        if ident not in current or type(round_number) is not int or round_number not in (1, 2, 3):
            raise ValueError(f'Unexpected advice identity or round: {ident}, {round_number}')
        report = ROOT / entry['report_file']
        if report not in report_hashes:
            report_hashes[report] = digest(report.read_bytes())
        actual_report_hash = report_hashes[report]
        if entry.get('report_sha256', actual_report_hash) != actual_report_hash:
            raise ValueError(f'Advice report changed after manifest was created: {report}')
        record = {**entry, 'report_sha256': actual_report_hash,
                  'input_matches_current': entry['input_fingerprint_sha256'] == input_fingerprint(
                      current[ident], entry.get('input_fingerprint_fields', SOURCE_FIELDS)),
                  'owner_approval': False}
        if 'body_file' in entry:
            body = ROOT / entry['body_file']
            record['body_hash_matches'] = digest(body.read_bytes()) == entry['body_sha256']
        elif current[ident]['kind'] == 'post':
            record['body_hash_matches'] = False
        advice.setdefault(ident, []).append(record)
    return advice


def stale_templates(item):
    mismatches, unrecorded = [], []
    for stage in ('relevance', 'classify', 'harness_gate', 'evidence', 'summarize', 'translate'):
        previous = item.get('llm', {}).get(stage)
        if not previous:
            continue
        samples = previous.get('samples', []) if stage == 'harness_gate' else [previous]
        expected = digest((ROOT / 'feed/prompts' / f'{stage}.md').read_bytes())
        for index, sample in enumerate(samples):
            name = f'{stage}[{index}]' if stage == 'harness_gate' else stage
            if not sample.get('template_hash'):
                unrecorded.append(name)
            elif sample['template_hash'] != expected:
                mismatches.append(name)
    return mismatches, unrecorded


def summary_quality(item, protected=False, scope_suggests_retention=False):
    """Account for text generation separately from a positive scope label."""
    model = item.get('llm', {})
    error_stage = model.get('error', {}).get('stage')
    required = (scope_suggests_retention or item.get('label') in ('include', 'borderline')
                or error_stage in ('summarize', 'translate'))
    missing = [key for key in ('summary_zh', 'summary_en')
               if not item.get(key, '').strip()]
    number_guard = model.get('number_guard', {})
    issues = []
    if required:
        issues += ['missing_' + key for key in missing]
        if item.get('guard_failed'):
            issues.append('summary_guard_failed')
        if not protected:
            issues += ['missing_' + stage + '_provenance' for stage in ('summarize', 'translate')
                       if stage not in model]
            if number_guard.get('ok') is not True:
                issues.append('summary_number_guard_not_confirmed')
    return {'required': required, 'protected_text': protected,
            'summary_zh_present': 'summary_zh' not in missing,
            'summary_en_present': 'summary_en' not in missing,
            'guard_failed': bool(item.get('guard_failed')),
            'initial_guard_failed': bool(item.get('initial_guard_failed')),
            'number_guard': number_guard or None,
            'issues': issues, 'summary_complete': not required or not issues}


def new_catalog_provenance(item, old, catalog, catalog_hash):
    if not item.get('in_repo') or old.get('in_repo'):
        return None
    paper = catalog[item['repo_id']]
    matches = {field: item.get(field, '') == paper.get(field, '')
               for field in ('summary_zh', 'summary_en')}
    verified = (item.get('llm', {}).get('origin') == 'evidence_library'
                and paper.get('arxiv') == item.get('arxiv_id') and all(matches.values()))
    return {'repo_id': paper['id'], 'source': 'data/papers.yaml',
            'source_sha256': catalog_hash, 'summary_matches': matches,
            'verified_curated_source': verified, 'llm_generation_success': False,
            'new_owner_acceptance': False,
            'limit': 'Current local catalog sync; does not change the fixed baseline partition or historical owner decision.'}


def review_accounting(records):
    valid = [record for record in records if record['input_matches_current']
             and record.get('body_hash_matches', True)]
    rounds = sorted({record['round'] for record in valid})
    reports = sorted({record['report_file'] for record in valid})
    reviewers = sorted({record['reviewer'] for record in valid if record.get('reviewer')})
    return {'rounds_recorded': sorted({record['round'] for record in records}),
            'rounds_with_matching_input': rounds,
            'phase_labels': {str(number): sorted({record['phase'] for record in valid
                             if record['round'] == number and record.get('phase')})
                             for number in rounds},
            'three_rounds_recorded': rounds == [1, 2, 3],
            'three_distinct_round_reports': rounds == [1, 2, 3] and len(reports) >= 3,
            'artifact_count': len(reports), 'artifacts': reports,
            'distinct_reported_reviewer_count': len(reviewers), 'reviewers': reviewers,
            'records_without_reviewer_identity': sum(not record.get('reviewer') for record in valid),
            'advice': records}


def today_hf_coverage(current, baseline, advice):
    path = BASE / 'hf-today-review/manifest.json'
    if not path.exists():
        return {'status': 'source_review_not_recorded', 'items': []}
    manifest = read_json(path)
    snapshot_path = BASE / 'hf-today-normalized.json'
    snapshot = {item['id']: item for item in read_json(snapshot_path)}
    rows = []
    for reviewed in manifest['items']:
        ident = reviewed['id']
        item = current.get(ident)
        fingerprint = input_fingerprint(snapshot[ident])
        rows.append({'id': ident, 'title': reviewed['title'],
                     'hf_daily_date': reviewed['hf_daily_date'],
                     'original_published_at': reviewed['original_published_at'],
                     'in_1124_baseline': ident in baseline,
                     'present_in_current_canonical': item is not None,
                     'source_snapshot_fingerprint_sha256': fingerprint,
                     'current_source_matches_snapshot': input_fingerprint(item) == fingerprint if item else None,
                     'round_1': reviewed['round_1'], 'round_2': reviewed['round_2'],
                     'source_scope_suggestion': reviewed['harness_scope_recommendation'],
                     'current_model_label': item.get('llm', {}).get('label') if item else None,
                     'current_label': item.get('label') if item else None,
                     'current_error': item.get('llm', {}).get('error') if item else None,
                     'summary_quality': summary_quality(item) if item else None,
                     'current_review': review_accounting([
                         record for record in advice.get(ident, [])
                         if record.get('input_snapshot') == relative(snapshot_path)]),
                     'decision': 'defer', 'owner_reviewed_this_run': False,
                     'publication_authorized': False})
    return {'status': 'source_review_recorded_not_publication_approval',
            'manifest': relative(path), 'manifest_sha256': digest(path.read_bytes()),
            'input_snapshot': relative(snapshot_path),
            'input_snapshot_sha256': digest(snapshot_path.read_bytes()),
            'source_review_status': manifest['review_status'],
            'date_rule': manifest['date_rule'], 'total_recommended_today': len(rows),
            'already_in_1124_baseline': sum(row['in_1124_baseline'] for row in rows),
            'new_beyond_1124_baseline': sum(not row['in_1124_baseline'] for row in rows),
            'new_current_canonical': sum(not row['in_1124_baseline'] and row['present_in_current_canonical'] for row in rows),
            'not_yet_in_canonical_ids': [row['id'] for row in rows if not row['present_in_current_canonical']],
            'items': rows}


def post_source_reviews():
    path = BASE / 'labs/results.json'
    independent_path = ROOT / 'build/four-paper-review-2026-10-30/primary/labs-scope-review.json'
    independent = read_json(independent_path)
    second = {row['id']: row for row in independent['reviews']}
    model_report_hash = digest(path.read_bytes())
    independent_report_hash = digest(independent_path.read_bytes())
    if model_report_hash != independent['source_results_sha256']:
        raise ValueError('Official post model results changed after source review')
    result = {}
    for index, row in enumerate(read_json(path)):
        matches = (digest((ROOT / row['source_file']).read_bytes()) == row['sha256']
                   and digest((ROOT / row['text_file']).read_bytes()) == row['text_sha256'])
        review = second.get(row['id'])
        result[row['id']] = {
            'status': row['status'], 'model_gate': row.get('gate'),
            'provenance': row.get('provenance'), 'source_url': row['source_url'],
            'body_file': row['text_file'], 'body_sha256': row['text_sha256'],
            'saved_source_hashes_match': matches,
            'model_report': relative(path), 'model_report_sha256': model_report_hash,
            'independent_source_review': review,
            'independent_report': relative(independent_path) if review else None,
            'independent_report_sha256': independent_report_hash if review else None,
            'model_quote_integrity': {
                field: [check for check in independent['integrity'][field]
                        if check['index'] == index]
                for field in ('hash_checks', 'model_quote_checks', 'raw_quote_failures')},
            'owner_approval': False}
    return result


def build_ledger(model_status, advice_manifest=None):
    inventory_path = BASE / 'inventory-audit.json'
    inventory = read_json(inventory_path)
    baseline_path = BASE / 'before/data/feed/items.jsonl'
    baseline, baseline_hash = read_rows(baseline_path)
    if baseline_hash != inventory['snapshot']['sha256'] or len(baseline) != 1124:
        raise ValueError('Immutable 1124-item baseline differs from the audited inventory')
    previous = {row['id']: row for row in inventory['items']}
    current_path = ROOT / 'data/feed/items.jsonl'
    current, current_hash = read_rows(current_path)
    if baseline.keys() - current.keys():
        raise ValueError('Baseline IDs disappeared: ' + ', '.join(sorted(baseline.keys() - current.keys())))
    identity = {row['id']: row for row in read_json(BASE / 'identity-checks.json')}
    s2 = {row['id']: row for row in read_json(BASE / 's2-primary/verification-ledger.json')}
    advice = checked_advice(advice_manifest, current) if advice_manifest else {}
    posts = post_source_reviews()
    catalog_path = ROOT / 'data/papers.yaml'
    catalog = {paper['id']: paper for paper in yaml.safe_load(catalog_path.read_text())['papers']}
    catalog_hash = digest(catalog_path.read_bytes())
    rows = []
    for ident, old in baseline.items():
        item, prior = current[ident], previous[ident]
        old_fp, new_fp = input_fingerprint(old), input_fingerprint(item)
        same_input = old_fp == new_fp
        owner_protected = prior['partition'] == 'owner_correction_protected'
        catalog_protected = prior['partition'] == 'curated_catalog_protected'
        new_catalog = new_catalog_provenance(item, old, catalog, catalog_hash)
        review_preserved = item.get('review') == old.get('review')
        model = item.get('llm', {})
        model_label = model.get('label')
        source_blockers, audit_gaps, caveats = [], [], []
        current_advice = advice.get(ident, [])
        valid_advice = [record for record in current_advice
                        if record['input_matches_current'] and record.get('body_hash_matches', True)]
        current_review = review_accounting(current_advice)
        current_three_rounds = current_review['three_rounds_recorded']
        post = posts.get(ident)
        post_verified = bool(post and post['saved_source_hashes_match']
                             and post['status'] == 'model_scope_reviewed')
        post_verdict = ((post['independent_source_review'] or {}).get('recommended_verdict',
                         (post['model_gate'] or {}).get('verdict')) if post else None)
        text_quality = summary_quality(item, owner_protected or catalog_protected
                                       or bool(new_catalog and new_catalog['verified_curated_source']),
                                       post_verdict in ('harness', 'borderline'))
        prior_reuse = prior['prior_scope_reusable_candidate'] and same_input
        stale, missing_hashes = stale_templates(item)
        if item['kind'] == 'paper' and not item.get('abstract', '').strip():
            source_blockers.append('missing_original_abstract')
        if item.get('metadata_pending'):
            source_blockers.append('metadata_pending_flag')
        if ident in s2:
            status = s2[ident]['abstract_status']
            if status == 'blocked_missing_abstract':
                source_blockers.append('publisher_abstract_access_blocked')
            elif status == 'editorial_full_text_verified_no_abstract_section':
                caveats.append('editorial_has_official_body_but_no_abstract')
        if ident in identity:
            check = identity[ident]
            if check['status'] != 'matched':
                source_blockers.append('arxiv_identity_not_matched')
            if not check['abstract_matches']:
                caveats.append('saved_abstract_differs_from_official_latest_string')
            if check.get('previous_version') != check.get('official_version'):
                caveats.append('saved_version_differs_from_official_latest')
            if str(check.get('previous_published', ''))[:10] != str(check.get('official_published', ''))[:10]:
                caveats.append('saved_publication_day_differs_from_official')
        if (item['kind'] == 'post' and not post_verified
                and not any(record.get('body_hash_matches') for record in valid_advice)):
            audit_gaps.append('current_official_body_review_not_recorded')
        if prior['prior_all_three_rounds'] and not prior_reuse:
            audit_gaps.append('prior_three_round_source_equivalence_not_established')
        if prior_reuse and not current_three_rounds:
            audit_gaps.append('prior_advice_needs_current_rule_reconciliation')
        if stale:
            audit_gaps.append('model_advice_uses_superseded_prompt')
        if model_label == 'error' or model.get('error'):
            audit_gaps.append('model_processing_error_not_a_scope_decision')
        audit_gaps.extend(text_quality['issues'])
        if owner_protected and not review_preserved:
            audit_gaps.append('protected_owner_review_changed')
        if new_catalog and not new_catalog['verified_curated_source']:
            audit_gaps.append('new_catalog_source_not_verified')
        if current_advice and len(valid_advice) != len(current_advice):
            audit_gaps.append('new_advice_input_or_body_hash_mismatch')
        if owner_protected:
            status = 'protected_owner_correction'
        elif catalog_protected:
            status = 'protected_curated_catalog'
        elif source_blockers:
            status = 'source_blocked'
        elif new_catalog and new_catalog['verified_curated_source']:
            status = 'new_curated_catalog_source'
        elif current_three_rounds:
            status = 'current_three_round_advice'
        elif post_verified:
            status = 'official_body_model_advice'
        elif prior_reuse:
            status = 'prior_three_round_reuse_candidate'
        elif model_label in ('include', 'borderline', 'exclude'):
            status = 'model_advice_only'
        elif model_label == 'error':
            status = 'model_error_pending'
        else:
            status = 'scope_review_pending'
        rows.append({
            'id': ident, 'title': item['title'], 'kind': item['kind'],
            'baseline_partition': prior['partition'], 'coverage_status': status,
            'decision': 'defer', 'owner_reviewed_this_run': False, 'publication_authorized': False,
            'protected_owner_correction': owner_protected, 'protected_catalog': catalog_protected,
            'new_catalog_source': new_catalog,
            'historical_owner_review': old.get('review'), 'historical_owner_review_preserved': review_preserved,
            'baseline_record_unchanged': item == old,
            'original_fact_fields_changed': [key for key in ORIGINAL_FACT_FIELDS if item.get(key) != old.get(key)],
            'source_input': {'baseline_fingerprint_sha256': old_fp, 'current_fingerprint_sha256': new_fp,
                             'same_as_baseline': same_input},
            'source_links': item.get('links', {}), 'source_hits': item.get('source_hits', []),
            'original_published_at': item.get('published'), 'original_updated_at': item.get('updated'),
            'hf_daily_dates': item.get('hf_daily_dates', []),
            'source_identity': {'arxiv': identity.get(ident), 's2_ledger':
                                'build/backlog-all-2026-10-30/s2-primary/verification-ledger.json' if ident in s2 else None},
            'model_advice': {'label': model_label, 'primary': model.get('primary'),
                             'gate_verdict': item.get('gate', {}).get('verdict'),
                             'harness_sample_count': model.get('harness_gate', {}).get('sample_count'),
                             'harness_agreement': model.get('harness_gate', {}).get('agreement'),
                             'error': model.get('error'), 'stale_template_stages': stale,
                             'stages_without_template_hash': missing_hashes,
                             'provenance_stages': [key for key in ('relevance', 'classify', 'harness_gate',
                                                                   'evidence', 'summarize', 'translate') if key in model]},
            'prior_review': {'rounds': prior['prior_review_rounds'], 'reports': prior['prior_reports'],
                             'three_rounds_recorded': prior['prior_all_three_rounds'],
                             'source_reuse_candidate_after_current_input_check': prior_reuse,
                             'original_matching_source_inputs': prior['prior_matching_source_inputs'],
                             'original_differing_source_inputs': prior['prior_differing_source_inputs']},
            'current_review': current_review,
            'official_body_advice': post,
            'summary_quality': text_quality,
            'source_blockers': source_blockers, 'audit_gaps': audit_gaps, 'metadata_caveats': caveats,
        })
    hf_today = today_hf_coverage(current, baseline, advice)
    summary = {
        'baseline_unique_ids': len(rows), 'current_unique_ids': len(current),
        'additional_current_ids_not_in_baseline': sorted(current.keys() - baseline.keys()),
        'by_kind': dict(Counter(row['kind'] for row in rows)),
        'by_coverage_status': dict(Counter(row['coverage_status'] for row in rows)),
        'model_labels': dict(Counter(row['model_advice']['label'] or 'missing' for row in rows)),
        'protected_owner_corrections': sum(row['protected_owner_correction'] for row in rows),
        'protected_catalog': sum(row['protected_catalog'] for row in rows),
        'new_catalog_sources': sum(row['new_catalog_source'] is not None for row in rows),
        'new_catalog_source_ids': [row['id'] for row in rows if row['new_catalog_source']],
        'protected_owner_review_changed_ids': [row['id'] for row in rows if row['protected_owner_correction']
                                              and not row['historical_owner_review_preserved']],
        'original_fact_fields_changed_ids': [row['id'] for row in rows if row['original_fact_fields_changed']],
        'prior_three_rounds_recorded': sum(row['prior_review']['three_rounds_recorded'] for row in rows),
        'prior_three_round_source_reuse_candidates': sum(row['prior_review']['source_reuse_candidate_after_current_input_check'] for row in rows),
        'current_three_distinct_round_advice': sum(row['current_review']['three_distinct_round_reports'] for row in rows),
        'current_three_rounds_recorded': sum(row['current_review']['three_rounds_recorded'] for row in rows),
        'recorded_review_round_counts': {str(number): sum(number in row['current_review']['rounds_recorded']
                                                        for row in rows) for number in (1, 2, 3)},
        'matching_review_round_counts': {str(number): sum(number in row['current_review']['rounds_with_matching_input']
                                                        for row in rows) for number in (1, 2, 3)},
        'official_body_model_advice': sum(row['official_body_advice'] is not None for row in rows),
        'official_body_independent_source_review': sum(bool(row['official_body_advice'] and
              row['official_body_advice']['independent_source_review']) for row in rows),
        'summary_required': sum(row['summary_quality']['required'] for row in rows),
        'required_summary_incomplete_ids': [row['id'] for row in rows
                                           if not row['summary_quality']['summary_complete']],
        'summary_issue_counts': dict(Counter(issue for row in rows for issue in row['summary_quality']['issues'])),
        'guard_failed_ids': [row['id'] for row in rows if row['summary_quality']['guard_failed']],
        'today_hf_total': hf_today.get('total_recommended_today', 0),
        'today_hf_new_beyond_baseline': hf_today.get('new_beyond_1124_baseline', 0),
        'today_hf_new_in_canonical': hf_today.get('new_current_canonical', 0),
        'source_blocker_counts': dict(Counter(blocker for row in rows for blocker in row['source_blockers'])),
        'audit_gap_counts': dict(Counter(gap for row in rows for gap in row['audit_gaps'])),
        'metadata_caveat_counts': dict(Counter(caveat for row in rows for caveat in row['metadata_caveats'])),
        'all_new_formal_decisions_defer': all(row['decision'] == 'defer' for row in rows),
    }
    if summary['protected_owner_corrections'] != 33 or summary['protected_catalog'] != 17:
        raise ValueError('Protected baseline partition counts changed')
    return {'schema_version': 2, 'audit_date': '2026-10-30', 'model_batch_status': model_status,
            'authority': 'audit_advice_only_not_owner_approval_or_publication',
            'sources': {'baseline': relative(baseline_path), 'baseline_sha256': baseline_hash,
                        'inventory': relative(inventory_path), 'inventory_sha256': digest(inventory_path.read_bytes()),
                        'current_items': relative(current_path), 'current_items_sha256': current_hash,
                        'advice_manifest': relative(advice_manifest) if advice_manifest else None,
                        'advice_manifest_sha256': digest(advice_manifest.read_bytes()) if advice_manifest else None},
            'definitions': {'decision': 'All entries defer. Historical owner decisions remain in a separate protected field.',
                            'model_advice_only': 'A label or independent model gate samples do not constitute three scope-review rounds.',
                            'prior_three_round_reuse_candidate': 'Same source input; still requires reconciliation with current scope rules.',
                            'source_blocked': 'Original content or identity is unavailable; never a positive scope decision.',
                            'current_three_round_advice': 'Three recorded phases with matching input fingerprints: source identity/date verification, model classification and text generation, then source-scope re-review. Round 1 does not certify every paper claim. Artifacts and named reviewers are counted separately; still not owner approval.',
                            'official_body_model_advice': 'Official post body reviewed in a separate model/source workflow; never synthesized as canonical paper llm.label.',
                            'distinct_reported_reviewer_count': 'Distinct reviewer identities recorded by manifests; does not independently establish blinding or experimental reproduction.',
                            'summary_complete': 'Required bilingual text and generation guards present; this is a content check, not scope approval or publication authorization.',
                            'input_fingerprint_fields': list(SOURCE_FIELDS)},
            'summary': summary, 'items': rows, 'today_hf': hf_today}


def render_markdown(ledger):
    summary, hf = ledger['summary'], ledger['today_hf']
    rows = ledger['items']
    lines = ['# 2026-10-30 审核覆盖清单', '',
             f"固定基线 {summary['baseline_unique_ids']} 条；当前库存 {summary['current_unique_ids']} 条。"
             f"HF 今日榜 {hf['total_recommended_today']} 篇，其中 {hf['already_in_1124_baseline']} 篇原已在库、"
             f"{hf['new_beyond_1124_baseline']} 篇为基线之外的新附录。新附录不会回填到 1124 的分母。", '',
             '本清单是审核工作记账。所有本轮正式决定均为 defer；来源核验、模型处理和多阶段复核均不等于 owner accept，也不构成发布授权。', '',
             f"Canonical SHA-256：`{ledger['sources']['current_items_sha256']}`。模型批次状态：`{ledger['model_batch_status']}`。", '',
             '| 基线覆盖状态 | 条数 |', '| --- | ---: |']
    lines += [f'| {status} | {count} |' for status, count in summary['by_coverage_status'].items()]
    lines += ['', '| 本轮阶段 | 有记录 | 所核字段与当前输入匹配 |', '| --- | ---: | ---: |']
    names = {1: '来源身份、原日期、版本与摘要差异核对',
             2: '分类与必需双语摘要；文章使用独立正文流程',
             3: '另一个 agent 的来源范围复核及记录的裁定'}
    for number, name in names.items():
        lines.append(f"| {number}. {name} | {summary['recorded_review_round_counts'][str(number)]} | {summary['matching_review_round_counts'][str(number)]} |")
    lines += ['', f"三阶段且所核输入匹配：{summary['current_three_rounds_recorded']} 条；"
              f"其中具有至少 3 个不同报告文件的为 {summary['current_three_distinct_round_advice']} 条。"
              '文件数量不代表独立审核者数量；逐项保留 phase、reviewer、原始输入和正文哈希。第一轮仅核对来源和元数据，不认证论文全部事实。', '',
              f"保留 {summary['protected_owner_corrections']} 条 owner 修正与 {summary['protected_catalog']} 条文献库条目。"
              f"历史三轮记录 {summary['prior_three_rounds_recorded']} 条；当前输入相同的历史复用候选 {summary['prior_three_round_source_reuse_candidates']} 条，均与本轮覆盖分开。", '',
              f"另有 {summary['new_catalog_sources']} 条本轮新增的文献库同步来源；逐字核对文献库双语文本，"
              '单列 provenance，不计为新的 LLM 摘要成功，也不改动历史 owner 决定。', '',
              f"65 篇官方文章：{summary['official_body_model_advice']} 篇有单独的正文模型审查，"
              f"{summary['official_body_independent_source_review']} 篇另有来源复核。没有给这些文章伪造 paper 类型的 llm.label。", '',
              f"需要双语摘要 {summary['summary_required']} 条，当前仍不完整 {len(summary['required_summary_incomplete_ids'])} 条，"
              f"guard_failed {len(summary['guard_failed_ids'])} 条。生成质量与范围建议分别计数。", '',
              '其中模型摘要续跑单为 369 篇论文，另有 Terminal X 这 1 篇公告缺少双语摘要；后者已有正文范围复核，不能笼统记作未审。', '',
              '| 尚存问题 | 条数 |', '| --- | ---: |']
    for group in ('source_blocker_counts', 'audit_gap_counts'):
        lines += [f'| {name} | {count} |' for name, count in summary[group].items()]
    lines += ['', '元数据差异只报告、不由覆盖脚本改动：', '',
              '| 差异或限制 | 条数 |', '| --- | ---: |']
    lines += [f'| {name} | {count} |' for name, count in summary['metadata_caveat_counts'].items()]
    lines += ['', 'HF 今日榜附录（按论文原日期正序；上榜日期单列）：', '',
              '| 论文 | HF 上榜日 | 原始发表日 | 来源范围建议 | 本轮匹配阶段 |',
              '| --- | --- | --- | --- | --- |']
    for row in sorted(hf['items'], key=lambda item: (item['original_published_at'], item['id'])):
        title = row['title'].replace('|', '\\|')
        rounds = ','.join(map(str, row['current_review']['rounds_with_matching_input'])) or '—'
        lines.append(f"| {title} | {row['hf_daily_date']} | {row['original_published_at'][:10]} | {row['source_scope_suggestion']} | {rounds} |")
    lines += ['', '今日 HF 每篇的 primary 第 1、2 阶段共用一份报告，第三阶段来自另一位 agent：真实计为 3 阶段、2 个报告、2 位记录的审核者。第三阶段曾收到主动披露的分类概览，不声称完全盲审。', '',
              '固定 45-case gate 的独立结果见旁边的 harness-gate-eval 报告：运行完整但召回门槛未通过。多轮记录、源码测试或摘要生成完成均不会覆盖这个质量失败。', '',
              '完整逐项证据、原 owner 状态、模型错误和摘要缺口保存在 coverage-ledger.json；数据仅供 owner 审核。', '']
    return '\n'.join(lines)


def build_resume_artifacts(ledger):
    """Expose every frozen ID and an exact, nonpublishing continuation list."""
    current, current_hash = read_rows(ROOT / 'data/feed/items.jsonl')
    state_path = BASE / 'model-run-final-status.json'
    state = read_json(state_path)
    independent_path = ROOT / 'docs/internal/reports/maintenance-2026-10-30/independent/manifest.json'
    independent = read_json(independent_path)
    assert current_hash == ledger['sources']['current_items_sha256'] == state['canonical_sha256']
    summary_ids = set(state['remaining_summary_ids'])
    errors = {row['id']: row for row in state['remaining_errors']}
    metadata_ids = {ident for ident, row in errors.items() if row['stage'] == 'metadata'}
    api_ids = set(errors) - metadata_ids
    assert len(summary_ids) == 369 and len(metadata_ids) == 9 and len(api_ids) == 11
    assert not summary_ids & set(errors)
    independent_missing = {row['id'] for row in independent['coverage']
                           if not row['original_source_review_available']}
    indexed, queues = [], {key: [] for key in (
        'resume_summary', 'retry_model_api', 'retrieve_original_abstract',
        'complete_official_post_summary', 'reconcile_source_version_or_text',
        'independent_source_review_not_yet_recorded')}
    baseline = {row['id']: row for row in ledger['items']}
    hf_new = {row['id']: row for row in ledger['today_hf']['items'] if not row['in_1124_baseline']}
    assert baseline.keys() | hf_new.keys() == current.keys()
    for ident, item in current.items():
        row = baseline.get(ident) or hf_new[ident]
        protected = bool(row.get('protected_owner_correction') or row.get('protected_catalog'))
        review = row['current_review']
        tasks = []
        if ident in summary_ids:
            assert not row['summary_quality']['summary_complete'] and not protected
            tasks.append('resume_summary')
        if ident in api_ids:
            assert item.get('llm', {}).get('error') and not protected
            tasks.append('retry_model_api')
        if ident in metadata_ids:
            assert not item.get('abstract', '').strip() and not protected
            tasks.append('retrieve_original_abstract')
        if item['kind'] == 'post' and not row['summary_quality']['summary_complete']:
            tasks.append('complete_official_post_summary')
        if any(not advice['input_matches_current'] or not advice.get('body_hash_matches', True)
               for advice in review['advice']):
            tasks.append('reconcile_source_version_or_text')
        if ident in independent_missing:
            tasks.append('independent_source_review_not_yet_recorded')
        for task in tasks:
            queues[task].append(ident)
        suggestions = [{'phase': advice['phase'], 'round': advice['round'],
                        'verdict': advice.get('verdict'),
                        'scope': advice.get('scope_suggestion') or advice.get('source_scope'),
                        'input_matches_current': advice['input_matches_current'],
                        'report_file': advice['report_file'], 'report_sha256': advice['report_sha256']}
                       for advice in review['advice'] if advice['round'] in (2, 3)]
        pending = list(dict.fromkeys([*row.get('source_blockers', []), *row.get('audit_gaps', []), *tasks]))
        if not suggestions and not protected and not pending:
            pending.append('scope_review_not_recorded')
        source_files = sorted({advice['report_file'] for advice in review['advice']})
        assert item.get('links') or source_files
        assert suggestions or protected or pending
        indexed.append({
            'id': ident, 'title': item['title'], 'kind': item['kind'],
            'baseline': 'fixed_1124' if ident in baseline else 'hf_2026_10_30_new_15',
            'coverage_status': row.get('coverage_status', 'hf_three_phase_source_advice'),
            'canonical_label': item.get('label'), 'canonical_gate': item.get('gate', {}).get('verdict'),
            'formal_decision': 'defer', 'publication_authorized': False,
            'automatic_edit_protected': protected, 'historical_owner_review': item.get('review'),
            'source_links': item.get('links', {}), 'source_hits': item.get('source_hits', []),
            'original_published_at': item.get('published'), 'hf_daily_dates': item.get('hf_daily_dates', []),
            'source_reports': source_files, 'scope_suggestions': suggestions,
            'rounds_recorded': review['rounds_recorded'],
            'rounds_with_matching_input': review['rounds_with_matching_input'],
            'model_error': item.get('llm', {}).get('error'),
            'pending_reasons': pending, 'resume_tasks': tasks,
            'source_input_sha256': input_fingerprint(item),
            'canonical_record_sha256': digest(json.dumps(item, ensure_ascii=False, sort_keys=True,
                                                         separators=(',', ':')).encode()),
        })
    assert len(indexed) == len({row['id'] for row in indexed}) == 1139
    assert len(queues['complete_official_post_summary']) == 1
    plan = {
        'schema_version': 1, 'audit_date': '2026-10-30', 'status': 'blocked_no_paid_retry_requested',
        'model_batch_status': 'blocked', 'publication_authorized': False,
        'canonical_sha256': current_hash, 'baseline_count': 1124, 'hf_new_count': 15,
        'model_state_file': relative(state_path), 'model_state_sha256': digest(state_path.read_bytes()),
        'independent_manifest_file': relative(independent_path),
        'independent_manifest_sha256': digest(independent_path.read_bytes()),
        'classification_resume': state['classification_resume'],
        'summary_batch': state['summary_batch'],
        'offline_recovered_summary_ids': state['offline_recovery']['recovered_ids'],
        'catalog_sync': state['catalog_sync'],
        'queue_counts': {key: len(ids) for key, ids in queues.items()},
        'queue_overlap_note': 'Queues overlap; do not add queue counts to obtain unique unfinished items.',
        'queues': queues, 'remaining_errors': state['remaining_errors'],
        'protected_owner_count': 33, 'protected_baseline_catalog_count': 17,
        'before_next_model_run': [
            'Confirm model funding and credentials outside chat; no paid call was made by this accounting run.',
            'Prepare only the listed IDs in an isolated output directory; verify each frozen record hash first.',
            'Do not submit missing-abstract records to the model or treat API errors as exclusion decisions.',
            'Review source-version differences and third-round suggestions before any owner decision.',
            'Review generated output before integration; no queue, accept, merge, or publish step is included.',
        ],
    }
    return indexed, plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model-status', required=True, choices=('completed', 'interrupted', 'blocked'))
    parser.add_argument('--advice-manifest', type=Path)
    parser.add_argument('--output', type=Path, default=BASE / 'coverage-ledger.json')
    args = parser.parse_args()
    if not args.output.resolve().is_relative_to(BASE):
        raise ValueError('Coverage artifacts must stay in the backlog audit directory')
    ledger = build_ledger(args.model_status, args.advice_manifest)
    args.output.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    args.output.with_suffix('.md').write_text(render_markdown(ledger), encoding='utf-8')
    indexed, plan = build_resume_artifacts(ledger)
    (args.output.parent / 'item-status.jsonl').write_text(
        ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in indexed), encoding='utf-8')
    (args.output.parent / 'resume-plan.json').write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in ledger['summary'].items()
                      if not key.endswith('_ids') and key != 'additional_current_ids_not_in_baseline'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
