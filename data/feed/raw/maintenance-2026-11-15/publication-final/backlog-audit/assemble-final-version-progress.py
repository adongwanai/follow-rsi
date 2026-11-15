"""Integrate the ten source-bound cross reviews after the real dated apply.

Writes audit artifacts only. Frozen earlier stages and production stay unchanged.
"""
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
PRIOR = BASE / 'post-intake'
OUT = BASE / 'post-review'
sys.path.insert(0, str(ROOT))
from scripts.feed.review import source_hash


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def ref(path):
    return {'path': str(Path(path).relative_to(ROOT)), 'sha256': sha(path)}


def lines(path):
    return [json.loads(line) for line in gzip.decompress(Path(path).read_bytes()).splitlines()]


def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


assert (OUT / 'application-observation.json').exists(), 'Formal apply must be observed first'
assert not (OUT / 'version-review-progress.json').exists(), 'Do not replace a completed integration'
assert not (OUT / 'freeze-manifest.json').exists(), 'Do not modify a frozen stage'
for entry in read(PRIOR / 'freeze-manifest.json')['files']:
    assert sha(ROOT / entry['path']) == entry['sha256'], entry['path']

canonical = {row['id']: row for row in map(json.loads, (OUT / 'canonical-snapshot.jsonl').read_text().splitlines())}
prior_canonical = {row['id']: row for row in map(json.loads, (PRIOR / 'canonical-snapshot.jsonl').read_text().splitlines())}
progress = read(PRIOR / 'version-review-progress.json')
by_id = {row['id']: row for row in progress['items']}
primary_paths = sorted((BASE / 'primary-review').glob('*-v*-v*.json'))
assert len(primary_paths) == 10
integrations = []
for primary_path in primary_paths:
    primary = read(primary_path)
    ident = primary['id']
    cross_path = BASE.parent / 'independent' / (primary_path.stem + '-cross-review.json')
    cross = read(cross_path)
    assert cross['id'] == ident
    assert (cross.get('scope_agrees') is True or cross.get('scope_agrees_after_amendment') is True
            or cross.get('result', '').startswith('agree_')
            or (cross.get('status') == 'scope_and_version_comparison_agreed_with_limits'
                and cross.get('unresolved_scope_disagreement') is False)), ident
    references = {}
    for name in ('primary_initial', 'primary', 'primary_review', 'primary_amendment', 'primary_numeric_comparison',
                 'independent_initial', 'initial', 'independent_amendment'):
        if name in cross:
            entry = cross[name]
            assert sha(ROOT / entry['path']) == entry['sha256'], (ident, name)
            references[name] = entry
    primary_binding = cross.get('primary_initial', cross.get('primary', cross.get('primary_review')))
    assert primary_binding == ref(primary_path), ident
    assert primary['current_source_hash'] == source_hash(canonical[ident]), ident

    current_scope = primary.get('current_scope_recommendation',
                                primary.get('current_version_scope_recommendation', primary['scope_recommendation']))
    target_scope = primary['scope_recommendation']
    reason = primary['primary_reason_zh']
    if ident == 'arxiv:2610.28914':
        amendment = read(ROOT / cross['primary_amendment']['path'])
        current_scope = target_scope = amendment['scope_recommendation']
        reason = amendment['revised_reason_zh']
    if ident == 'arxiv:2610.18845':
        assert current_scope == cross['current_scope_recommendation'] == 'exclude'
        assert target_scope == 'include' and cross['candidate_scope_recommendation'] == 'include_qualified_component'

    old = by_id[ident]
    old.setdefault('prior_reason_before_nov15_cross_review', old['reason_zh'])
    if 'pending_reason_zh' in old:
        old['prior_pending_reason_before_nov15_cross_review'] = old.pop('pending_reason_zh')
    old['prior_status_before_nov15_cross_review'] = old['status']
    old.update({
        'status': 'scope_comparison_completed_2026_11_15_independent_crosscheck',
        'scope_recommendation': current_scope,
        'scope_recommendation_applies_to': 'retained_current_version',
        'current_version_scope_recommendation': current_scope,
        'candidate_version_scope_recommendation': target_scope,
        'reason_zh': reason,
        'fulltext_review_required': False,
        'independent_status': 'frozen_initial_then_source_bound_crosscheck',
        'primary_review': ref(primary_path),
        'independent_cross_review': ref(cross_path),
        'review_reference_hashes_verified': references,
        'current_formal_decision': canonical[ident].get('review', {}).get('decision'),
        'parent_formal_decision_changed_since_post_intake': (
            canonical[ident].get('review') != prior_canonical[ident].get('review')),
        'formal_decision_changed_by_this_audit': False,
        'version_adopted': False,
        'new_public_numeric_summary_approved': False,
        'next_actions': ['retain_current_formal_version',
                         'separate_version_specific_date_and_summary_review_before_adoption'],
        'coverage': primary.get('coverage', primary.get('method_sections_read')),
        'independent_additional_limits': {key: cross[key] for key in
            ('boundary', 'boundaries', 'shared_findings', 'additional_limits', 'additional_guardrails', 'numeric_claims_scope')
            if key in cross},
        'experiments_reproduced': False,
        'binary_figure_assets_checked': False,
    })
    if ident == 'arxiv:2610.18845':
        old['candidate_scope_boundary_zh'] = primary['scope_boundary_zh']
        old['next_actions'].append('retain_v1_exclusion_until_separate_v2_training_free_branch_review')
    integrations.append({
        'id': ident, 'current_version': primary['current_version'],
        'candidate_version': primary['candidate_version'],
        'current_source_hash': primary['current_source_hash'],
        'current_scope_recommendation': current_scope,
        'candidate_scope_recommendation': target_scope,
        'reason_zh': reason, 'primary_review': ref(primary_path),
        'independent_cross_review': ref(cross_path),
        'reference_hashes_verified': references,
        'independent_additional_limits': old['independent_additional_limits'],
        'official_version_adopted': False,
        'new_public_numeric_summary_approved': False,
    })

source_observation = read(OUT / 'source-recovery-observation.json')
source_rows = {row['id']: (index, row) for index, row in enumerate(source_observation['rows'])}
completed = {row['id'] for row in integrations}
tables = {}
for name in ('progress-version-review-tasks.jsonl.gz', 'progress-daily-metadata-review-tasks.jsonl.gz'):
    rows = lines(PRIOR / name)
    for row in rows:
        ident = row['id']
        if ident in completed:
            finding = by_id[ident]
            row.update({
                'prior_status_before_nov15_cross_review': row['status'],
                'status': finding['status'], 'fulltext_review_required': False,
                'required_actions': finding['next_actions'],
                'version_comparison_ref': {'path': str((OUT / 'version-review-progress.json').relative_to(ROOT)), 'id': ident},
            })
        if ident in source_rows:
            index, observed = source_rows[ident]
            row['version_source_recovery'] = {
                'path': str((OUT / 'source-recovery-observation.json').relative_to(ROOT)),
                'index': index, 'status': observed['recovery_status'],
                'queue_processing_complete': observed['queue_processing_complete'],
                'scope_review_completed': False, 'version_adopted': False,
            }
    tables[name] = rows
weekly_pending = {row['id'] for row in tables['progress-version-review-tasks.jsonl.gz'] if row.get('fulltext_review_required')}
daily_pending = {row['id'] for row in tables['progress-daily-metadata-review-tasks.jsonl.gz'] if row.get('fulltext_review_required')}
pending = weekly_pending | daily_pending
assert pending == set(source_rows) and len(pending) == 337
done_count = sum(not row['fulltext_review_required'] for row in progress['items'])
assert done_count == 39
progress.update({
    'stage': 'post-review', 'generated_at': datetime.now(timezone.utc).isoformat(),
    'prior_progress': ref(PRIOR / 'version-review-progress.json'),
    'today_completed_ids': sorted(completed), 'today_scope_comparisons_completed': len(completed),
    'scope_comparisons_completed': done_count,
    'substantive_comparisons_independently_reviewed': done_count - progress['unchanged_scope_reuse'],
    'changed_pairs_still_requiring_review': 0,
    'remaining_weekly_fulltext': len(weekly_pending),
    'remaining_daily_fulltext': len(daily_pending),
    'weekly_daily_overlap': len(weekly_pending & daily_pending),
    'remaining_fulltext_union': len(pending),
    'required_pair_not_yet_available': 196,
    'body_pairs_ready_for_scope_review': 141,
    'source_recovery_status': 'known_versions_complete_original_identity_gap_retained',
    'source_recovery_observation': ref(OUT / 'source-recovery-observation.json'),
    'current_formal_versions_adopted': 0,
    'boundaries_zh': [
        '正式apply后冻结规范库；十对版本的主审与独立初稿/交叉回执按SHA整合，旧初稿与纠正均保留。',
        '范围比较累计39项：24项无实质范围变化可复用、15项有独立实质比较；本日完成10项。',
        '337项来源处理完成不代表内容完成：141对可开始正文比较，196项已核旧HF原文但仍缺原版身份。',
        'D-Skill依现行判据纠正当前范围；RSI4EO仅候选v2训练禁用分支可纳，当前v1仍exclude。',
        '范围完成不等于实验复现、全部表/图重新核算、公共数字摘要批准或正式版本采纳。',
    ],
})
dump(OUT / 'version-pair-adjudication.json', {
    'created_at': progress['generated_at'], 'count': len(integrations),
    'current_version_scope_counts': dict(Counter(row['current_scope_recommendation'] for row in integrations)),
    'candidate_version_scope_counts': dict(Counter(row['candidate_scope_recommendation'] for row in integrations)),
    'items': integrations, 'formal_versions_adopted': 0,
    'paid_calls': 0, 'production_writes': 0,
})
dump(OUT / 'version-review-progress.json', progress)
for name, rows in tables.items():
    payload = ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows).encode()
    (OUT / name).write_bytes(gzip.compress(payload, mtime=0))
(OUT / 'current-scope-resolutions.json').write_bytes((PRIOR / 'current-scope-resolutions.json').read_bytes())
print(json.dumps({key: progress[key] for key in (
    'today_scope_comparisons_completed', 'scope_comparisons_completed',
    'substantive_comparisons_independently_reviewed', 'remaining_fulltext_union',
    'remaining_weekly_fulltext', 'remaining_daily_fulltext', 'weekly_daily_overlap',
    'body_pairs_ready_for_scope_review', 'required_pair_not_yet_available',
)}, ensure_ascii=False, indent=2))
