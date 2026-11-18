"""Bind the corrected review and replay persistence in a disposable local fixture."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast
import hashlib
import json
import shutil
import subprocess
import tempfile

import yaml

from scripts.feed.guard import check_summary
from scripts.feed.review import (
    apply_daily_review, approved_weekly_backlog, source_hash, validate_daily_review,
)
from scripts.feed.storage import load_items, save_items

ROOT = Path('.').resolve()
OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/independent-recovery'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/independent-recovery'
sha = lambda content: hashlib.sha256(content).hexdigest()
relative = lambda path: str(path.relative_to(ROOT))
stamp = datetime.now(timezone.utc).isoformat()

initial_path = OUT / 'review-findings-initial.json'
initial = json.loads(initial_path.read_text())
index = json.loads((OUT / 'source-recovery-index.json').read_text())
amendments = json.loads((OUT / 'amendments-proposed.json').read_text())
previous_path = OUT.parent / 'previous-review/2026-11-16.before-recovery.yaml'
corrected_path = OUT / 'review-2026-11-16.corrected.yaml'
previous = yaml.safe_load(previous_path.read_bytes())
corrected = yaml.safe_load(corrected_path.read_bytes())
assert sha(previous_path.read_bytes()) == initial['review_sha256'] == index['review_sha256']
assert sha(corrected_path.read_bytes()) == 'c2d0199d7f9e43817eb05c83e85a0b6e8a8f7895628c0546b76324830fe7a473'
assert previous['date'] == corrected['date'] == '2026-11-16'
assert previous['reviewed_on'] == '2026-11-17'
assert corrected['reviewed_on'] == '2026-11-18'
assert set(previous) == set(corrected)
assert {k: v for k, v in previous.items() if k not in ('items', 'lab_updates', 'reviewed_on')} == {
    k: v for k, v in corrected.items() if k not in ('items', 'lab_updates', 'reviewed_on')}

before = {row['id']: row for row in previous['items'] + previous['lab_updates']}
after = {row['id']: row for row in corrected['items'] + corrected['lab_updates']}
assert list(before) == list(after)
changes = []
for key, old in before.items():
    new = after[key]
    fields = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    allowed = {'arxiv:2610.09832': ['note', 'summary_override'],
               'arxiv:2610.24453': ['evidence_quick', 'note']}.get(key, [])
    assert fields == allowed, (key, fields)
    if fields:
        assert new['note'].startswith(old['note'])
        changes.append({'id': key, 'fields': fields, 'previous_note_preserved_with_explicit_correction': True})
for change in amendments['items']:
    row = after[change['id']]
    actual = (row['summary_override'] if change['field'] == 'summary_override'
              else row['evidence_quick']['cross_model'])
    assert actual == change['proposed']

canonical_snapshot = json.loads((OUT / 'canonical-source-bindings.json').read_text())
canonical = {row['id']: row for row in canonical_snapshot['items']}
assert set(canonical) == set(after)
assert all(source_hash(canonical[key]) == row['source_hash'] for key, row in after.items())
assert all(not row.get('in_repo') for row in canonical.values())
recovered_sources = {row['id']: row['source'] for row in index['items']}
body_checks = []
for key, source in recovered_sources.items():
    body_path = ROOT / source['path']
    text_path = ROOT / source['text_path']
    body_sha = sha(body_path.read_bytes())
    text_sha = sha(text_path.read_bytes())
    reviewed_source = after[key]['source_review_evidence']
    assert body_sha == source['sha256'] == reviewed_source['body_sha256']
    assert text_sha == source['text_sha256'] == reviewed_source['extracted_text_sha256']
    assert source['identity_found']
    body_checks.append({'id': key, 'body_sha256': body_sha, 'text_sha256': text_sha,
                        'matches_corrected_review': True, 'version_identity_matches': True})
for key, row in after.items():
    if key in recovered_sources:
        continue
    for entry in row['source_review_evidence']['evidence']:
        content = (ROOT / entry['archived_path']).read_bytes()
        assert sha(content) == entry['sha256']
        assert not entry.get('quote') or entry['quote'] in content.decode()

guards = []
for key, row in after.items():
    if row.get('summary_override'):
        summary = row['summary_override']
        result = check_summary(row['title'], row.get('abstract', ''),
                               summary['summary_zh'], summary['summary_en'])
        assert result['ok']
        guards.append({'id': key, **result})

code_files = ['scripts/feed/review.py', 'scripts/feed/storage.py', 'scripts/feed/guard.py',
              'tests/feed/test_daily.py', 'tests/feed/test_review.py']
code_bindings = {name: sha((ROOT / name).read_bytes()) for name in code_files}
old_code = subprocess.check_output(['git', 'show',
    'a2572651ccca1473cb988e5e2f2ccae7450c7a8a:scripts/feed/review.py']).decode()
new_code = (ROOT / 'scripts/feed/review.py').read_text()
function_ast = lambda code, name: ast.dump(next(
    node for node in ast.parse(code).body if isinstance(node, ast.FunctionDef) and node.name == name))
assert function_ast(old_code, 'source_hash') == function_ast(new_code, 'source_hash')

# Copy only the exact reviewed records into the fixture. No production apply occurs.
with tempfile.TemporaryDirectory(prefix='replay-fixture-', dir=OUT) as directory:
    fixture = Path(directory)
    inputs = {}
    paths = [ROOT / 'feed/sources.yaml', ROOT / 'feed/taxonomy.yaml']
    for folder, pattern in [('daily', '????-??-??.json'), ('recaps', '????-??-??--????-??-??.json')]:
        paths += sorted((ROOT / 'site' / folder).glob(pattern))
    for path in paths:
        target = fixture / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        inputs[relative(path)] = sha(target.read_bytes())
    review_target = fixture / 'review/daily/2026-11-16.yaml'
    review_target.parent.mkdir(parents=True)
    review_target.write_bytes(corrected_path.read_bytes())
    save_items(fixture, canonical.values())
    validate_daily_review(fixture, '2026-11-16')
    applied = apply_daily_review(fixture, '2026-11-16', now=stamp)
    stored = {row['id']: row for row in load_items(fixture)}
    preservation = []
    for key, original in canonical.items():
        current = stored[key]
        assert {k: v for k, v in current.items() if k != 'review'} == {
            k: v for k, v in original.items() if k != 'review'}
        assert source_hash(current) == source_hash(original)
        if 'evidence_quick' in after[key]:
            assert current['review']['evidence_quick'] == after[key]['evidence_quick']
        else:
            assert 'evidence_quick' not in current['review']
        preservation.append({'id': key, 'all_nonreview_fields_unchanged': True,
                             'canonical_source_hash_unchanged': True,
                             'reviewed_evidence_matches_yaml': True})
    backlog = {row['id']: row for row in approved_weekly_backlog(fixture, '2026-W47')}
    assert len(backlog) == 8
    cross_model_checks = []
    for key in ['arxiv:2610.22686', 'arxiv:2610.04008', 'arxiv:2610.24453']:
        assert stored[key]['evidence_quick']['cross_model']['value'] == 'yes'
        assert stored[key]['review']['evidence_quick']['cross_model'] == {'value': 'unknown', 'quote': None}
        if key in backlog:
            assert backlog[key]['evidence_quick']['cross_model'] == {'value': 'unknown', 'quote': None}
        cross_model_checks.append({'id': key, 'canonical_original': 'yes', 'review_override': 'unknown',
                                   'weekly_output': 'unknown' if key in backlog else 'excluded_by_reject'})
    second_apply = apply_daily_review(fixture, '2026-11-16', now=stamp)
    assert second_apply == 0
assert code_bindings == {name: sha((ROOT / name).read_bytes()) for name in code_files}

test_log = ROOT / 'build/maintenance-2026-11-18/evidence-regression-tests.log'
test_text = test_log.read_text()
assert '51 passed' in test_text
persistence = {
    'checked_at': stamp, 'reviewer': '/root/nov18_independent_recovery',
    'result': 'passed_for_this_recovery_batch',
    'code_file_sha256': code_bindings, 'source_hash_function_ast_unchanged': True,
    'parent_test_log': {'path': relative(test_log), 'sha256': sha(test_log.read_bytes()),
                        'observed_result': test_text.strip(),
                        'provenance': 'Existing parent-run offline test log inspected; full suite was not independently rerun.'},
    'independent_actual_record_fixture': {
        'input_review_sha256': sha(corrected_path.read_bytes()),
        'input_canonical_commit': canonical_snapshot['source_commit'],
        'input_record_count': len(canonical), 'supporting_input_hashes': inputs,
        'validation_passed': True, 'applied_count': applied,
        'second_apply_count': second_apply, 'weekly_backlog_count': len(backlog),
        'cross_model_checks': cross_model_checks, 'preservation_checks': preservation,
        'fixture_removed': True, 'production_canonical_writes': 0,
    },
    'static_findings': [
        'OWNER_FIELDS now includes evidence_quick, so apply persists the correction under item.review.',
        'Both queues reuse reviewed evidence only when the prior source_hash is unchanged.',
        'Weekly backlog combines the original source with the persisted review before effective_item applies the guard.',
        'Fields absent from lab rows are omitted rather than writing evidence_quick=null.',
    ],
    'limits': [
        'All 15 recovery records have in_repo=false; pre-existing in_repo behavior is unchanged and is outside this batch.',
        'The pre-existing abstract quote guard and code-release handling are unchanged; this check covers the supplied unknown corrections.',
        'No production apply, merged-owner proof, CI environment, rendered deployment or model-quality evaluation is asserted by this receipt.',
    ],
}
(OUT / 'evidence-persistence-crosscheck.json').write_text(json.dumps(persistence, ensure_ascii=False, indent=2) + '\n')

final = deepcopy(initial)
final.update(generated_at=stamp, review_sha256=sha(corrected_path.read_bytes()),
    review_snapshot=relative(corrected_path), review_git_commit=canonical_snapshot['source_commit'],
    original_review_sha256=initial['review_sha256'], original_reviewed_on='2026-11-17',
    actual_cross_review_date='2026-11-18', reviewed_on='2026-11-18',
    summary_and_evidence_ready=True, amendments_applied_and_rechecked=True,
    original_review_path=relative(previous_path), initial_receipt_sha256=sha(initial_path.read_bytes()),
    scope_decisions=dict(Counter(row['decision'] for row in after.values())),
    corrected_fields=changes, summary_guards=guards, recovered_body_checks=body_checks,
    persistence_crosscheck=relative(OUT / 'evidence-persistence-crosscheck.json'),
    readiness_boundary='Source, scope, bilingual summaries, selected numeric boundaries and local reviewed-evidence persistence passed. Publication still requires the parent to verify merged approval, CI, rendering and live deployment.')
for row in final['items']:
    row['amendment_required'] = False
    if row['id'] == 'arxiv:2610.09832':
        row['facts']['limits'][0] = 'Trial-to-active transition is usage-count gated in Eq.9. The corrected bilingual summary now states this explicitly.'
        row['amendment_resolution'] = 'Approved proposed summary applied exactly; qualitative mechanism and limitation statements remain equivalent across languages.'
    if row['id'] == 'arxiv:2610.24453':
        row['facts']['limits'][1] = 'Each run uses one model and starts with an empty memory bank; reviewed cross_model=unknown now correctly records the lack of demonstrated cross-model transfer.'
        row['amendment_resolution'] = 'Review-only cross_model override is unknown; canonical original yes and the reject decision remain unchanged.'
(OUT / 'review-findings-final.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')

readme = OUT / 'README.md'
readme.write_text(readme.read_text() + '''
## 最终修正复核

修正版审核单已绑定到 `31e46a809ca2f542502d5e7174b5fade803e52a0`，SHA256 为 `c2d0199d7f9e43817eb05c83e85a0b6e8a8f7895628c0546b76324830fe7a473`。原审核单及初始独立回执保留；正式 `reviewed_on` 为 11/18。两处提案已精确落实，除真实审核日、修正摘要、Hippo 审核证据及追加纠正说明外，其余 15 条字段不变。8 份中英摘要数字检查通过，12 份正文与抽取文本的哈希再次匹配。

只读代码审查及独立临时副本回放确认：全部 15 条非 `review` 字段原样保留，`source_hash` 不变；MFM、SkillScriptBench 与 Hippo 顶层原自动 `yes` 保留，审核层 `unknown` 正确持久化；前两项的周刊 backlog 输出也保持 `unknown`，Hippo 保持排除。第一次副本 apply 记录 15 条，第二次 0 条；正式 canonical 未写入。主任务提供的 51 项离线测试日志已核对，其全套测试未由本复核者重复运行。

最终回执见 [review-findings-final.json](review-findings-final.json)，代码与证据一致性见 [evidence-persistence-crosscheck.json](evidence-persistence-crosscheck.json)。Reward Engine 的 104/68 与 104/67 反证、DOI 正文与作者身份缺口仍保留。该回执确认来源、范围、摘要与副本持久化，不代表 owner 合并、CI 或线上出版完成。
''')
manifest = []
for path in sorted([*OUT.glob('*'), *RAW.glob('*')]):
    if path.is_file() and path.name != 'file-manifest.json':
        manifest.append({'path': relative(path), 'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())})
(OUT / 'file-manifest.json').write_text(json.dumps({'files': manifest}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'final_review_sha256': final['review_sha256'],
    'decisions': final['scope_decisions'], 'summary_and_evidence_ready': True,
    'independent_fixture': {'first_apply': applied, 'second_apply': second_apply,
                            'backlog_count': len(backlog), 'nonreview_fields_unchanged': len(preservation)},
    'manifest_count': len(manifest)}, ensure_ascii=False, indent=2))
