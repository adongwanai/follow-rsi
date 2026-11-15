"""Freeze source-recovery results, explicitly separate from content review."""
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

ROOT = Path.cwd()
WORK = ROOT / 'build/maintenance-2026-11-15/version-source-recovery'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (WORK / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


state = json.loads((WORK / 'recovery-state.json').read_text())
progress = json.loads((WORK / 'progress.json').read_text())
requests = [json.loads(line) for line in (WORK / 'requests.jsonl').read_text().splitlines()]
assert state.get('finished_at'), 'Recovery process has not finished; do not freeze.'
assert not (WORK / 'active-request.json').exists()
assert progress['queue_items_not_yet_processed'] == 0 or state['stopped_reason']
items = state['items']
identity_reference = json.loads((WORK / 'original-version-identity-audit-reference.json').read_text())
assert sha(ROOT / identity_reference['path']) == identity_reference['sha256']
identity_audit = json.loads((ROOT / identity_reference['path']).read_text())
state['original_version_identity_audit'] = identity_reference
state['bulk_body_storage'] = 'local_cache_only'
state['bulk_body_archive_public_attachment'] = False
for item in items:
    if item['current_version'] == 'unknown':
        item['original_version_identity_audit'] = identity_reference
save('recovery-state.json', state)
recovered_pairs, identity_blocked, failed_versions, not_yet_attempted = [], [], [], []
for item in items:
    entry = {key: item[key] for key in ['id', 'title', 'current_version', 'target_version',
                                       'current_source_hash', 'recovery_status', 'queue_processing_complete']}
    entry['sides'] = item['sides']
    entry['body_review_completed'] = False
    entry['version_adopted'] = False
    if item['current_version'] == 'unknown':
        entry['original_version_identity_audit'] = identity_reference
        identity_blocked.append(entry)
    elif all(side['status'] == 'recovered' for side in item['sides']):
        recovered_pairs.append(entry)
    for side in item['sides']:
        if side['status'] == 'request_failed':
            failed_versions.append({'id': item['id'], **side})
        elif side['attempt_permitted'] and side['status'] == 'not_yet_attempted':
            not_yet_attempted.append({'id': item['id'], **side})
save('recovered-version-pairs.json', {'count': len(recovered_pairs), 'items': recovered_pairs,
                                    'content_review_completed': False, 'version_adopted': False})
save('missing-original-version-identity.json', {'count': len(identity_blocked), 'items': identity_blocked,
                                              'boundary': 'Known target bodies do not identify the original snapshot. No v0 request or v1 assumption.'})
save('request-failures.json', {'count': len(failed_versions), 'items': failed_versions})
save('not-yet-attempted-known-versions.json', {'count': len(not_yet_attempted), 'items': not_yet_attempted})
accounting = {
    'input_items': len(items),
    'paired_bodies_recovered': len(recovered_pairs),
    'single_side_recovered_items': sum(sum(side['status'] == 'recovered' for side in item['sides']) == 1 for item in items),
    'known_pair_single_side_recovered_items': sum(sum(side['status'] == 'recovered' for side in item['sides']) == 1 for item in items if item['current_version'] != 'unknown'),
    'no_side_recovered_items': sum(not any(side['status'] == 'recovered' for side in item['sides']) for item in items),
    'missing_original_version_identity': len(identity_blocked),
    'missing_original_identity_with_recovered_target': sum(any(side['side'] == 'candidate' and side['status'] == 'recovered' for side in item['sides']) for item in identity_blocked),
    'failed_known_versions': len(failed_versions),
    'not_yet_attempted_known_versions': len(not_yet_attempted),
    'unknown_original_sides_not_attempted': len(identity_blocked),
    'queue_items_not_yet_processed': progress['queue_items_not_yet_processed'],
    'boundary': 'One-sided target recovery does not resolve missing original identity. Body acquisition does not advance the separate scope-review completion count.',
}
save('recovery-accounting.json', accounting)

checks = []


def check(name, passed, details, severity='error'):
    checks.append({'check': name, 'passed': bool(passed), 'severity': severity, 'details': details})


check('frozen_worklist_sha', sha(WORK / 'input-worklist.json') == state['input_sha256'], state['input_sha256'])
check('full_337_item_accounting', len(items) == 337 and len({item['id'] for item in items}) == 337,
      {'items': len(items), 'processed': progress['queue_items_processed'],
       'not_yet_processed': progress['queue_items_not_yet_processed']})
check('unknown_originals_not_invented', len(identity_blocked) == 196 and all(
    side['version'] == 'unknown' and side['status'] == 'not_yet_attempted' and not side['attempts']
    for item in identity_blocked for side in item['sides'] if side['side'] == 'current'), len(identity_blocked))
check('unknown_original_identity_audit_bound', identity_audit['summary']['items'] == 196
      and identity_audit['summary']['version_identity_resolved'] == 0
      and identity_audit['summary']['snapshot_abstract_exact_matches'] == 223,
      {'source_path': identity_reference['path'], 'source_sha256': identity_reference['sha256'],
       'raw_memberships_checked_by_backlog_audit': 223, 'explicit_bindings_found': 0})
check('no_v0_requests', all(row['version'] > 0 and 'v0' not in row['request_url'] for row in requests), len(requests))
excluded = json.loads((WORK / 'excluded-ten-pairs.json').read_text())
check('existing_ten_pairs_excluded', len(excluded['items']) == 10 and not (
    {item['id'] for item in excluded['items']} & {item['id'] for item in items}), len(excluded['items']))
verified = 0
for item in items:
    for side in item['sides']:
        if side['status'] != 'recovered':
            continue
        recovery = side['source_recovery']
        assert recovery['usable_versioned_fulltext']
        assert recovery['expected_arxiv_version'] == item['id'].removeprefix('arxiv:') + 'v' + str(side['version'])
        assert sha(ROOT / recovery['body_path']) == recovery['body_sha256']
        assert sha(ROOT / recovery['text_path']) == recovery['text_sha256']
        if recovery.get('receipt_path'):
            assert sha(ROOT / recovery['receipt_path']) == recovery['receipt_sha256']
        verified += 1
check('all_recovered_body_and_text_hashes', verified == sum(
    side['status'] == 'recovered' for item in items for side in item['sides']), verified)
for request in requests:
    if request.get('body_path'):
        assert sha(ROOT / request['body_path']) == request['body_sha256']
check('all_response_body_hashes', True, len(requests))
gaps = [(second['dispatch_monotonic_ns'] - first['dispatch_monotonic_ns']) / 1e9
        for first, second in zip(requests, requests[1:])]
check('requests_do_not_overlap', all(
    datetime.fromisoformat(first['finished_at']) <= datetime.fromisoformat(second['requested_at'])
    for first, second in zip(requests, requests[1:])), len(gaps))
check('sequential_request_spacing_target', not gaps or min(gaps) >= 3.2,
      {'configured_target_seconds': 3.2, 'minimum_recorded_seconds': min(gaps) if gaps else None,
       'gaps_below_target': [{'first_attempt': first['attempt_number'],
                              'second_attempt': second['attempt_number'], 'recorded_seconds': gap}
                             for first, second, gap in zip(requests, requests[1:], gaps) if gap < 3.2],
       'measurement_boundary': 'The limiter timestamp precedes dispatch_monotonic_ns and requests.get. These are pre-request log gaps, not measured socket dispatch times.',
       'disposition': 'Keep the original 3.2-second target and failed result. This agent-chosen pacing target is an operational warning; it does not invalidate recovered payload hashes or assert exact dispatch pacing.'},
      severity='warning')
check('known_version_queue_terminal_or_stopped', not not_yet_attempted or state['stopped_reason'],
      {'known_versions_not_yet_attempted': len(not_yet_attempted), 'stopped_reason': state['stopped_reason']})
check('no_review_or_adoption_claim', all(not item['body_review_completed'] and not item['version_adopted'] for item in items),
      {'content_reviews_completed': 0, 'formal_version_adoptions': 0, 'paid_calls': 0, 'canonical_writes': 0})
archive_members = []
for directory in ['bodies', 'texts', 'receipts']:
    for path in sorted((WORK / directory).iterdir()):
        if path.is_file():
            archive_members.append({'member': str(path.relative_to(WORK)),
                                    'original_path': str(path.relative_to(ROOT)),
                                    'bytes': path.stat().st_size, 'sha256': sha(path)})
archive_members.append({'member': 'requests.jsonl', 'original_path': str((WORK / 'requests.jsonl').relative_to(ROOT)),
                        'bytes': (WORK / 'requests.jsonl').stat().st_size, 'sha256': sha(WORK / 'requests.jsonl')})
archive_path = WORK / 'version-source-bodies.tar.gz'
with archive_path.open('wb') as raw_archive:
    with gzip.GzipFile(filename='', mode='wb', fileobj=raw_archive, mtime=0, compresslevel=6) as compressed:
        with tarfile.open(fileobj=compressed, mode='w') as archive:
            for member in archive_members:
                info = tarfile.TarInfo(member['member'])
                info.size, info.mode, info.mtime = member['bytes'], 0o644, 0
                with (ROOT / member['original_path']).open('rb') as source:
                    archive.addfile(info, source)
member_lookup = {member['member']: member for member in archive_members}
verified_archive_members = 0
with tarfile.open(archive_path, 'r:gz') as archive:
    for member in archive:
        data = archive.extractfile(member).read()
        expected = member_lookup[member.name]
        assert len(data) == expected['bytes']
        assert hashlib.sha256(data).hexdigest() == expected['sha256']
        verified_archive_members += 1
archive_index = {
    'archive_path': str(archive_path.relative_to(ROOT)), 'archive_bytes': archive_path.stat().st_size,
    'archive_sha256': sha(archive_path), 'member_count': len(archive_members),
    'uncompressed_member_bytes': sum(member['bytes'] for member in archive_members),
    'member_payloads_preserved_byte_for_byte': True,
    'archive_metadata_policy': 'Stable order, zero archive mtime and numeric owner metadata; member payload bytes are unchanged.',
    'included_directories': ['bodies', 'texts', 'receipts'], 'additional_members': ['requests.jsonl'],
    'members': archive_members,
}
storage = {
    'storage_class': 'local_cache_only', 'public_attachment': False,
    'full_archive_filename': archive_path.name,
    'full_archive_bytes': archive_index['archive_bytes'], 'full_archive_sha256': archive_index['archive_sha256'],
    'bulk_body_directories': ['bodies', 'texts'],
    'instructions': 'Keep this full archive and source/text cache in the ignored build directory. The metadata and receipt publication list does not publish the bulk body archive. Copy only source bodies actually cited by a completed substantive review or formal adoption, with exact hashes, when the parent selects them.',
    'member_payloads_unchanged': True,
}
save('archive-storage.json', storage)
archive_index['storage_class'] = 'local_cache_only'
archive_index['public_attachment'] = False
archive_index['archive_storage_index'] = 'archive-storage.json'
save('body-archive-members.json', archive_index)
check('body_archive_payload_bytes', verified_archive_members == len(archive_members),
      {'members': verified_archive_members, 'archive_bytes': archive_index['archive_bytes'],
       'uncompressed_member_bytes': archive_index['uncompressed_member_bytes']})
qa = {'generated_at': datetime.now(timezone.utc).isoformat(), 'all_checks_passed': all(c['passed'] for c in checks),
      'all_blocking_checks_passed': all(c['passed'] for c in checks if c['severity'] == 'error'),
      'operational_warnings': [c for c in checks if not c['passed'] and c['severity'] == 'warning'],
      'checks': checks, 'boundary': 'Source-acquisition verification only; no paper-content/scope review or production mutation.'}
save('recovery-qa.json', qa)
assert qa['all_blocking_checks_passed'], qa

lines = ['# 2026-11-15 历史版本正文恢复', '',
         f'本次源文件恢复覆盖冻结清单的 {len(items)} 项；其中 {progress["queue_items_processed"]} 项明确版本请求/缓存处理完毕，{progress["queue_items_not_yet_processed"]} 项尚未处理。', '',
         f'- 实际免费 HTTP 请求：{len(requests)}；HTTP 状态：{dict(Counter(str(row.get("http_status", "network_error")) for row in requests))}。',
         f'- 有效正文响应：{progress["valid_fulltext_responses"]}；新增恢复版本：{progress["newly_fetched_versions"]}；缓存复用版本：{progress["reused_cached_versions"]}。',
         f'- 141 项明确原版/目标版本中，{len(recovered_pairs)} 对正文已齐；失败版本 {len(failed_versions)}，尚未尝试的明确版本 {len(not_yet_attempted)}。',
         f'- 单边正文已恢复的条目：{accounting["single_side_recovered_items"]}；其中原版身份未知但目标正文已恢复：{accounting["missing_original_identity_with_recovered_target"]}。',
         f'- 196 项原始版本身份仍未知；这些条目的目标版本状态见 missing-original-version-identity.json，不假定原版为 v1。',
         '- backlog 子任务已离线复核这 196 项的原始 source_hash 与 223 条 HF 成员/摘要命中，但 0 条具有明确版本字段或带版本 URL；因此它们是身份证据缺口，不是未开展原始来源核对。回执哈希见 original-version-identity-audit-reference.json。',
         '- 既有 10 对正文未重复请求；所有成功必须有完整 arXiv article 与对应页面 watermark，或有效指定版本 PDF（详细版本绑定方式逐项保留）。HTTP 200 元数据页不算正文。',
         f'- 全局停止原因：{state["stopped_reason"] or "none"}。',
         f'- 节流审计：目标仍为 3.2 秒，实际记录的最小间隔 {min(gaps) if gaps else None} 秒，{sum(gap < 3.2 for gap in gaps)} 个间隔未达到目标；该检查明确保留为失败告警，all_checks_passed={str(qa["all_checks_passed"]).lower()}。请求前日志与限流参考计时点不同，不能据此声称精确的网络发出时刻。所有前请求完成均早于下一请求记录；不重写历史日志或降低目标。',
         f'- 原文字节包：version-source-bodies.tar.gz，{archive_index["archive_bytes"]} 字节；展开成员 {archive_index["member_count"]} 个，共 {archive_index["uncompressed_member_bytes"]} 字节。逐成员解包 SHA-256 校验通过，索引见 body-archive-members.json。',
         '- 正文与提取文本、完整 tar.gz 均为 local_cache_only，留在忽略的 build 目录，不是公开附件，也未额外分块。仓库最小归档仅含逐项官方 URL/版本/原始 SHA、请求回执、提取结果索引、冻结核验和本地包 SHA，见 minimal-publication-files.json。',
         '- 本恢复批次 0 项完成实质正文审查，因此本目录没有可自动纳入公开证据的整批正文。正式纳入或实质版本审查确实引用的正文，由整合方按相应完成审核单选择性归档并保持原始字节及 SHA。',
         '- 0 付费调用，0 canonical 修改，0 新内容审查完成，0 正式版本采用。', '',
         '恢复正文仅让后续版本对照成为可能。必须另行完成变更段落/表格/数字核对与独立范围复审；本目录不改变原先审核或发表结论。', '',
         '交接入口：progress.json、recovery-accounting.json、recovery-state.json、recovered-version-pairs.json、missing-original-version-identity.json、request-failures.json、not-yet-attempted-known-versions.json、requests.jsonl、recovery-qa.json。', '']
(WORK / 'HANDOFF.md').write_text('\n'.join(lines))
publication_files = ['archive-storage.json', 'body-archive-members.json',
    'recovery-state.json', 'recovery-accounting.json', 'recovered-version-pairs.json',
    'missing-original-version-identity.json', 'request-failures.json',
    'not-yet-attempted-known-versions.json', 'input-worklist.json', 'excluded-ten-pairs.json',
    'original-version-identity-audit-reference.json', 'requests.jsonl',
    'progress.json', 'recovery-qa.json', 'HANDOFF.md', 'manifest.json', 'freeze-receipt.json',
    'recover-version-bodies.py', 'finalize-recovery.py', 'minimal-publication-files.json']
publication_files += [str(path.relative_to(WORK)) for path in sorted((WORK / 'receipts').iterdir()) if path.is_file()]
save('minimal-publication-files.json', {
    'public_metadata_and_receipts': publication_files,
    'local_cache_only': ['bodies/', 'texts/', archive_path.name, 'recovery.log'],
    'selective_reviewed_body_files_from_this_batch': [],
    'selective_body_boundary': 'Zero substantive content reviews or formal version adoptions completed in this recovery-only batch; the parent selects exact body files actually cited by separate completed reviews.',
    'referenced_external_identity_audit': identity_reference,
})
files = [{'path': str(path.relative_to(ROOT)), 'bytes': path.stat().st_size, 'sha256': sha(path)}
         for path in sorted(WORK.rglob('*')) if path.is_file() and path.name not in {'manifest.json', 'freeze-receipt.json'}]
save('manifest.json', {'generated_at': datetime.now(timezone.utc).isoformat(), 'files': files,
                       'file_count': len(files), 'bytes': sum(row['bytes'] for row in files),
                       'excludes': ['manifest.json', 'freeze-receipt.json'], 'frozen': True})
receipt = {'frozen_at': datetime.now(timezone.utc).isoformat(),
           'manifest_sha256': sha(WORK / 'manifest.json'), 'progress_sha256': sha(WORK / 'progress.json'),
           'state_sha256': sha(WORK / 'recovery-state.json'), 'qa_sha256': sha(WORK / 'recovery-qa.json'),
           'handoff_sha256': sha(WORK / 'HANDOFF.md'), 'file_count_in_manifest': len(files),
           'total_directory_bytes_in_manifest': sum(row['bytes'] for row in files),
           'body_archive_sha256': archive_index['archive_sha256'],
           'body_archive_bytes': archive_index['archive_bytes'],
           'body_archive_member_index_sha256': sha(WORK / 'body-archive-members.json'),
           'archive_storage_index_sha256': sha(WORK / 'archive-storage.json'),
           'bulk_body_storage': 'local_cache_only', 'bulk_body_archive_public_attachment': False,
           'all_checks_passed': qa['all_checks_passed'],
           'all_blocking_checks_passed': qa['all_blocking_checks_passed'],
           'operational_warnings': qa['operational_warnings'],
           'recommended_publication_files': publication_files,
           'summary': progress}
save('freeze-receipt.json', receipt)
print(json.dumps(receipt, ensure_ascii=False))
