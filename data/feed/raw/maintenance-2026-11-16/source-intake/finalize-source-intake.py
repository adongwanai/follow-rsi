"""Freeze the November 16 free-source intake, preserving evidence and uncertainty."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
WORK = ROOT / 'build/maintenance-2026-11-16/source-intake'
sys.path.insert(0, str(ROOT))
from scripts.feed.review import source_hash


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((WORK / name).read_text())


def save(name, value):
    (WORK / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def relative(path):
    return str(path.relative_to(ROOT))


def evidence(path):
    return {'path': relative(path), 'sha256': sha(path)}


now = datetime.now(timezone.utc).isoformat()
snapshot = read('all-source-snapshot.json')
run = read('run-state.json')
assert run['status'] == 'source_collection_complete'
assert snapshot['all_sources_attempted_and_finished']
base_file = WORK / 'canonical-baseline.jsonl'
baseline = read('canonical-baseline.json')
assert sha(base_file) == baseline['canonical_sha256']
base = {row['id']: row for row in map(json.loads, base_file.read_text().splitlines())}
proposal = read('integration-proposal.json')
effective = deepcopy(proposal)
post_audits = {row['id']: row for row in read('post-identity-date-audit.json')['records']}
doi_audits = {row['id']: row for row in read('doi-identity-date-audit.json')['records']}
assert {row['id'] for row in proposal['new_items']} == set(post_audits) | set(doi_audits)
corrections, source_index = [], []
for item in effective['new_items']:
    record = item['record']
    before = deepcopy(record)
    record.update(updated='', updated_source='unknown', version_status='unknown',
                  stored_version_placeholder=0)
    assert record['version'] == 0
    if record['kind'] == 'post':
        audit = post_audits[item['id']]
        record.update(published_source='official_publisher_rss',
                      source_reported_updated=before['updated'],
                      source_reported_updated_is_normalizer_default=True,
                      official_page_header_date=audit['official_page_header_date'],
                      official_post_body_verified=True,
                      official_metadata_verified=True)
        if audit['primary_paper_link']:
            record['referenced_arxiv_ids'] = ['2610.09093']
            record['referenced_paper_boundary'] = 'A linked external research paper, not a newly discovered HF-recommended paper in this intake.'
        record['official_metadata_evidence'] = {
            'source_url': audit['source_url'], 'body_path': audit['body_path'],
            'body_sha256': audit['body_sha256'], 'requested_at': audit['source_requested_at'],
            'receipt_path': audit['receipt_path'], 'receipt_sha256': audit['receipt_sha256'],
            'authority': 'Official publisher article header and feed; revision date unknown.',
        }
        fulltext = {
            'fulltext_available': True, 'scope_source_kind': 'official publisher article',
            'fulltext_body_path': audit['body_path'], 'fulltext_body_sha256': audit['body_sha256'],
            'text_path': audit['text_path'], 'text_sha256': audit['text_sha256'],
            'fulltext_url': audit['source_url'], 'fulltext_fetched_at': audit['source_requested_at'],
            'identity_date_audit': evidence(WORK / 'post-identity-date-audit.json'),
            'fulltext_blocker': None,
        }
    else:
        audit = doi_audits[item['id']]
        official_receipt_path = WORK / 'additional-official-sources/household-publisher-linked-1.receipt.json'
        official_receipt = json.loads(official_receipt_path.read_text())
        record.update(
            doi=audit['doi'], authors=audit['crossref_authors'],
            published=audit['proposed_original_publication_date'],
            announced=audit['proposed_original_publication_date'],
            published_source='elsevier:coverDisplayDate_available_online',
            announced_source='elsevier:coverDisplayDate_available_online',
            publication_precision='day', metadata_pending=True, official_metadata_verified=False,
            s2_reported_authors=before['authors'], s2_reported_published=before['published'],
            source_publication_date_parts=audit['crossref_date_parts'],
            publisher_available_online_text=audit['publisher_available_online_text'],
            publisher_abstract_available=False, abstract_verified_against_original_body=False,
            identity_status='doi_and_title_confirmed; unresolved_author_variant; body_missing',
            source_blockers=audit['blockers'],
        )
        record['links'].update(doi='https://doi.org/' + audit['doi'],
                               url='https://www.sciencedirect.com/science/article/pii/S0957417426039850?v=s5')
        record['official_metadata_evidence'] = {
            'source_url': official_receipt['request_url'], 'requested_at': official_receipt['requested_at'],
            'body_path': official_receipt['body_path'], 'body_sha256': official_receipt['body_sha256'],
            'receipt_path': relative(official_receipt_path), 'receipt_sha256': sha(official_receipt_path),
            'authority': 'Official publisher XML coredata; explicit available-online date, not article fulltext.',
        }
        fulltext = {
            'fulltext_available': False, 'scope_source_kind': 'publisher identity/date metadata only',
            'fulltext_body_path': None, 'fulltext_body_sha256': None,
            'text_path': None, 'text_sha256': None,
            'identity_date_audit': evidence(WORK / 'doi-identity-date-audit.json'),
            'fulltext_blocker': ' '.join(audit['blockers']),
        }
    assert record['first_seen'] == before['first_seen']
    corrections.append({'id': item['id'], 'before_source_hash': source_hash(before),
                        'after_source_hash': source_hash(record),
                        'changes': {key: {'before': before.get(key), 'after': record.get(key)}
                                    for key in sorted(set(before) | set(record))
                                    if before.get(key) != record.get(key)},
                        'first_seen_unchanged': True, 'raw_discovery_record_preserved': True,
                        'formal_decision': item['formal_decision'], 'scope_review_performed': False})
    source_index.append({
        'id': item['id'], 'kind': record['kind'], 'title': record['title'],
        'first_seen': record['first_seen'], 'source_observed_at': record['source_observed_at'],
        'source_hits': record['source_hits'], 'hf_daily_dates': record['hf_daily_dates'],
        'published_as_proposed': record['published'], 'updated_as_proposed': record['updated'],
        'version': 'unknown', 'stored_version_placeholder': 0,
        'source_hash_of_proposed_record': source_hash(record),
        'discovery_bindings': item['bindings'], 'official_metadata_evidence': record['official_metadata_evidence'],
        'formal_decision': item['formal_decision'], **fulltext,
    })
save('source-metadata-corrections.json', {'generated_at': now, 'items': corrections,
                                       'original_discovery_proposal': evidence(WORK / 'integration-proposal.json')})
effective.update(enriched_at=now,
                 unmodified_discovery_proposal=evidence(WORK / 'integration-proposal.json'),
                 source_corrections=evidence(WORK / 'source-metadata-corrections.json'),
                 enrichment_boundary='Identity/date enrichment only; original S2 and RSS data retained. No scope acceptance or production apply.')
save('effective-integration-proposal.json', effective)
save('source-evidence-index.json', {'generated_at': now, 'new_items': len(source_index),
     'records': source_index, 'effective_proposal_path': relative(WORK / 'effective-integration-proposal.json'),
     'effective_proposal_sha256': sha(WORK / 'effective-integration-proposal.json'),
     'source_identity_only_not_final_acceptance': True})

hf_delta = read('hf-board-source-delta.json')
hf_result = read('source-results/hf-daily.json')
hf_attempts = [json.loads(line) for line in (WORK / 'network/hf-daily/attempts.jsonl').read_text().splitlines()]
boards = []
for observed in hf_delta['boards']:
    board = deepcopy(observed)
    board.update(unique_id_count=len(board['ids']) if board['http_status'] == 200 else None,
                 new_to_canonical_ids=[ident for ident in board['ids'] if ident not in base],
                 missing_membership_after_proposal=board['existing_missing_hf_date_ids'],
                 available_through=hf_result['hf_today']['available_through'] if board['date'] == '2026-11-16' else None)
    assert not board['new_to_canonical_ids'] and not board['missing_membership_after_proposal']
    assert not board['scientific_metadata_deltas']
    boards.append(board)
save('hf-board-reconciliation.json', {
    'generated_at': now, 'target_day': '2026-11-16', 'boards': boards,
    'prior_snapshot': hf_delta['prior_snapshot'], 'canonical_baseline_count': len(base),
    'keyword_prefilter_used': False, 'most_recent_explicit_available_day': '2026-11-13',
    'applied': False, 'boundary': 'not_ready on 11/16 differs from observed empty weekend arrays; 34-member 11/13 list is the latest observed complete board, with no detected late additions.'})
save('cache-reuse-audit.json', {
    'generated_at': now, 'new_source_cache_checks': [evidence(WORK / 'cache-scan-initial.json'), evidence(WORK / 'doi-cache-scan.json')],
    'hf_source_delta': evidence(WORK / 'hf-board-source-delta.json'),
    'existing_hf_records_reused': [{'id': ident, 'canonical_source_hash': source_hash(base[ident]),
                                  'first_seen': base[ident]['first_seen'],
                                  'current_arxiv_version_refetched': False,
                                  'reuse_basis': 'Same HF identity, date membership and observed scientific metadata fields as the verified prior snapshot.'}
                                 for ident in next(b['ids'] for b in boards if b['date'] == '2026-11-13')],
    'historical_478_version_bodies_refetched': False, 'model_cache_reexecuted': False})

raw = [json.loads(line) for line in (WORK / 'raw-source-id-reconciliation.jsonl').read_text().splitlines()]
compact = [{key: row[key] for key in ['source_id', 'id', 'title', 'published_as_reported',
                                    'disposition', 'new_to_canonical', 'evidence']} for row in raw]
compact_path = WORK / 'raw-source-id-index.jsonl'
compact_path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in compact))
save('raw-reconciliation-storage.json', {
    'full_derived_reconciliation': evidence(WORK / 'raw-source-id-reconciliation.jsonl'),
    'full_derived_bytes': (WORK / 'raw-source-id-reconciliation.jsonl').stat().st_size,
    'full_derived_storage': 'local_cache_only; redundant normalized record payloads',
    'public_compact_index': evidence(compact_path), 'rows': len(compact),
    'unique_ids': len({row['id'] for row in compact}),
    'boundary': 'The public index retains every stable ID, window disposition, response hash, query and record index; original network bodies contain the full external records.'})

receipts = []
for path in sorted((WORK / 'network').glob('*/attempts.jsonl')):
    receipts.extend({'source_id': path.parent.name, 'receipt_file_path': relative(path), **json.loads(line)}
                    for line in path.read_text().splitlines())
post_receipts = [json.loads(path.read_text()) for path in sorted((WORK / 'post-fulltexts').glob('*.receipt.json'))]
doi_receipts = [json.loads(path.read_text()) for path in sorted((WORK / 'additional-official-sources').glob('*.receipt.json'))]
all_receipts = receipts + post_receipts + doi_receipts
local_only_responses = {name for audit in doi_audits.values() for name in audit['local_only_external_response_paths']}
body_files = {row['body_path']: row['body_sha256'] for row in all_receipts if row.get('body_path')}
for name, expected in body_files.items():
    assert sha(ROOT / name) == expected, name
for row in post_receipts:
    assert sha(ROOT / row['text_path']) == row['text_sha256']

# Reuse byte-identical public responses without pretending today's request did not occur.
public_candidates = [ROOT / name for name in subprocess.run(
    ['rg', '--files', 'data/feed/raw'], check=True, capture_output=True, text=True).stdout.splitlines()]
required_sizes = {(ROOT / name).stat().st_size for name in body_files if name not in local_only_responses}
existing_by_hash = {}
for path in public_candidates:
    if path.suffix not in {'.body', '.html', '.xml'} or path.stat().st_size not in required_sizes:
        continue
    digest = sha(path)
    existing_by_hash.setdefault(digest, relative(path))
body_storage, unique_new_bodies, same_run = [], [], {}
for name, digest in sorted(body_files.items()):
    if name in local_only_responses:
        storage, selected = 'local_cache_only', None
    elif digest in existing_by_hash:
        storage, selected = 'reuse_existing_public_bytes', existing_by_hash[digest]
    elif digest in same_run:
        storage, selected = 'reuse_same_run_response_bytes', same_run[digest]
    else:
        storage, selected = 'new_public_response_bytes', name
        same_run[digest] = name
        unique_new_bodies.append(name)
    body_storage.append({'original_local_path': name, 'sha256': digest,
                         'bytes': (ROOT / name).stat().st_size,
                         'storage': storage, 'selected_evidence_path': selected,
                         'raw_response_bytes_modified': False})
save('response-storage-index.json', {'generated_at': now, 'responses': body_storage,
    'full_original_response_hashes_preserved': True,
    'path_mapping_boundary': 'Original request receipts keep their original local path. Archive new_public_response_bytes once; map references via selected_evidence_path. Local-only redirect/challenge pages are not public body evidence.'})
save('request-evidence-index.json', {'generated_at': now, 'registry_route_requests': len(receipts),
    'post_body_requests': len(post_receipts), 'doi_identity_and_publisher_requests': len(doi_receipts),
    'total_actual_free_http_requests': len(all_receipts), 'requests': all_receipts,
    'response_storage': evidence(WORK / 'response-storage-index.json'), 'paid_requests': 0})
save('source-health.json', {'generated_at': now, 'sources': snapshot['sources'],
                          'configured_sources': 12, 'all_sources_attempted': True,
                          'raw_counts_are_observed_not_global_coverage': True,
                          'registry_route_request_count': len(receipts), 'paid_calls': 0})

checks = []
def check(name, passed, details):
    checks.append({'check': name, 'passed': bool(passed), 'details': details})
check('frozen_baseline_identity_and_count', len(base) == baseline['count'] == 2090,
      {'count': len(base), 'sha256': sha(base_file)})
check('all_twelve_sources_attempted', len(snapshot['sources']) == 12 and all(
    row['request_count'] > 0 and row['finished_at'] for row in snapshot['sources']), len(receipts))
check('every_original_id_accounted', len(raw) == snapshot['raw_occurrences'] and
      len({row['id'] for row in raw}) == snapshot['raw_unique_ids'],
      {'raw_occurrences': len(raw), 'raw_unique_ids': len({row['id'] for row in raw})})
check('full_hf_cross_weekend_board_reconciliation', {row['date'] for row in boards} ==
      {'2026-11-16', '2026-11-15', '2026-11-14', '2026-11-13'} and
      all(not row['missing_membership_after_proposal'] for row in boards),
      [{'date': row['date'], 'state': row['observation_status'], 'members': row['raw_member_count']} for row in boards])
check('existing_first_seen_preserved', all(row['record']['first_seen'] == base[row['id']]['first_seen']
      for row in raw if row['id'] in base), len({row['id'] for row in raw if row['id'] in base}))
check('new_first_seen_bound_to_actual_request', all(item['record']['first_seen'] ==
      min(binding['requested_at'] for binding in item['bindings']) for item in effective['new_items']), len(source_index))
check('no_existing_science_or_review_change', not effective['official_metadata_change_candidates']
      and not effective['existing_provenance_updates'], {'production_writes': 0, 'source_hashes_preserved': True})
check('new_unknown_revision_fields_preserved', all(item['record']['updated'] == '' and
      item['record']['version_status'] == 'unknown' and item['record']['version'] == 0
      for item in effective['new_items']), '0 is a storage placeholder, not arXiv version 0.')
check('new_identity_sources_and_limits_explicit', len(source_index) == 3 and
      sum(row['fulltext_available'] for row in source_index) == 2 and all(
      row['official_metadata_evidence'] for row in source_index), {'post_bodies': 2, 'doi_metadata_only': 1})
check('raw_and_extracted_hashes_verified', True, {'response_files': len(body_files), 'text_files': len(post_receipts)})
s2 = sorted((row for row in receipts if row['source_id'].startswith('s2-')),
            key=lambda row: row['dispatch_monotonic_ns'])
gaps = [(b['dispatch_monotonic_ns'] - a['dispatch_monotonic_ns']) / 1e9 for a, b in zip(s2, s2[1:])]
check('s2_request_spacing', all(gap >= run['auth']['semantic_scholar_interval_seconds'] for gap in gaps),
      {'minimum_seconds': min(gaps), 'required_seconds': run['auth']['semantic_scholar_interval_seconds'], 'requests': len(s2)})
check('source_failures_not_counted_as_full_coverage', all(not row['source_traversal_complete']
      for row in snapshot['sources'] if row['source_id'].startswith(('s2-', 'arxiv-'))),
      'arXiv 429 and bounded S2 traversals remain incomplete, with successful pages retained.')
check('no_paid_scope_acceptance_or_publication', all(item['formal_decision'] == 'defer' and
      item['paid_stages_run'] is False for item in effective['new_items']) and not effective['applied'],
      {'paid_calls': 0, 'canonical_writes': 0, 'scope_reviews_completed': 0})
qa = {'generated_at': now, 'all_checks_passed': all(row['passed'] for row in checks), 'checks': checks,
      'boundary': 'Source identity/date/reconciliation QA only; not paper acceptance, experiment reproduction, or proof of public deployment.'}
save('intake-qa.json', qa)
assert qa['all_checks_passed'], qa

lines = ['# 2026-11-16 免费来源交接', '',
         '这是来源身份、日期和对账结果；未修改 canonical、审核决定、Git 或出版物，未调用付费模型。', '',
         f'- 12 路全部实际尝试，路由请求 {len(receipts)} 次，补充公告正文/DOI 官方请求 {len(post_receipts) + len(doi_receipts)} 次。',
         f'- 全量原始出现 {len(raw)} 条 / {snapshot["raw_unique_ids"]} 个 ID；配置窗口内 {snapshot["configured_window_occurrences"]} 条 / {snapshot["configured_window_unique_ids"]} 个 ID。',
         '- 相对 2090 条基线，提议新增 3 条：2 个 OpenAI 公告，1 个 S2/DOI 论文身份；0 旧来源/推荐日补记，0 模糊身份归并。',
         '- HF 11/16 为 HTTP 400 not_ready，API 明确 available_through=11/13；11/15、11/14 分别为 HTTP 200 空数组；11/13 完整 34 条与前次成员及科学字段一致，无晚到成员或漏记推荐日。三种状态不混同。',
         '- 3 路 arXiv 查询均为 HTTP 429；S2 引用保留 20 个成功页，S2 作者保留 10 份种子作者元数据、未走到作者论文页；两路均在 180 秒边界结束，未访问覆盖为 unknown。',
         '- 两篇新公告官方正文、H1 与页头日期已核：页头 11/15，RSS 11/15 22:00 UTC，实际 first_seen 11/16。updated 为空、version=0 仅表示 unknown 占位；2610.09093 只作为公告引用论文，不转为今天新增。',
         '- 新 DOI 10.1016/j.eswa.2026.135083 的官方 XML 明示 Available online 13 November 2026；并列保留 S2 11/01、Crossref 仅 11 月及第二作者 Yan-Qing Cai / Yanchang Cai 冲突。没有摘要或正文；ScienceDirect 403、text/plain 400，XML 200 只有 coredata。',
         '- 原始字节和 SHA 全部保留；含匿名路由字段的 DOI 跳转页及拦截页仅本地。公开清单不含完整 canonical/重复派生快照，原始相同响应按哈希复用既有归档。',
         '- source-evidence-index.json 是逐项主审入口；effective-integration-proposal.json 是最小规范记录提议；source-metadata-corrections.json 保留规范化前后差异。',
         f'- 来源 QA {len(checks)} / {len(checks)} 通过。这不代表三轮范围审查或发布完成。', '',
         '最小归档以 minimal-publication-files.json 为准；response-storage-index.json 明确原路径、可复用公共路径和本地限定正文，不能把本地文件称为公开附件。', '']
(WORK / 'HANDOFF.md').write_text('\n'.join(lines))

metadata_names = ['HANDOFF.md', 'setup-receipt.json', 'canonical-baseline.json',
    'run-state.json', 'auth-presence.json', 'all-source-snapshot.json', 'all-source-snapshot.md',
    'integration-proposal.json', 'effective-integration-proposal.json', 'source-metadata-corrections.json',
    'source-evidence-index.json', 'post-identity-date-audit.json', 'doi-identity-date-audit.json',
    'cache-scan-initial.json', 'doi-cache-scan.json', 'cache-reuse-audit.json',
    'hf-board-source-delta.json', 'hf-board-reconciliation.json', 'source-health.json',
    'raw-source-id-index.jsonl', 'raw-reconciliation-storage.json', 'request-evidence-index.json',
    'response-storage-index.json', 'intake-qa.json', 'feed/sources.yaml',
    'fetch-free-sources.py', 'reconcile-sources.py', 'fetch-new-posts.py', 'fetch-new-doi.py',
    'finalize-source-intake.py', 'minimal-publication-files.json', 'manifest.json', 'freeze-receipt.json']
metadata_names += [str(path.relative_to(WORK)) for path in sorted((WORK / 'network').glob('*/attempts.jsonl'))]
metadata_names += [str(path.relative_to(WORK)) for path in sorted((WORK / 'post-fulltexts').glob('*.receipt.json'))]
metadata_names += [str(path.relative_to(WORK)) for path in sorted((WORK / 'post-fulltexts').glob('*.txt'))]
metadata_names += [str(path.relative_to(WORK)) for path in sorted((WORK / 'additional-official-sources').glob('*.receipt.json'))]
publication_names = metadata_names + [str((ROOT / name).relative_to(WORK)) for name in unique_new_bodies]
assert len(publication_names) == len(set(publication_names))
save('minimal-publication-files.json', {
    'generated_at': now, 'public_files_relative_to_intake': publication_names,
    'new_body_files': unique_new_bodies,
    'existing_body_references': [row for row in body_storage if row['storage'] == 'reuse_existing_public_bytes'],
    'same_run_body_references': [row for row in body_storage if row['storage'] == 'reuse_same_run_response_bytes'],
    'local_only_responses': [row for row in body_storage if row['storage'] == 'local_cache_only'],
    'additional_local_only': ['canonical-baseline.jsonl', 'raw-source-id-reconciliation.jsonl',
                              'candidate-records.jsonl', 'source-results/', 'data/feed/raw/', 'data/papers.yaml', 'data/feed/state.json'],
    'instructions': 'Copy only public_files_relative_to_intake byte-for-byte. Original responses already archived under existing_body_references are reused by SHA, not recopied. Derived links can be mapped separately, but raw external response bytes/hashes must not change. Original local-only response bytes remain private local cache.'})
manifest_files = [{'path': relative(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}
                  for path in sorted(WORK.rglob('*')) if path.is_file() and path.name not in {'manifest.json', 'freeze-receipt.json'}]
save('manifest.json', {'generated_at': datetime.now(timezone.utc).isoformat(), 'frozen': True,
                      'files': manifest_files, 'file_count': len(manifest_files),
                      'bytes': sum(row['bytes'] for row in manifest_files),
                      'excludes': ['manifest.json', 'freeze-receipt.json'],
                      'publication_boundary': 'This manifest covers local cache too; presence here does not mean public upload.'})
freeze = {'frozen_at': datetime.now(timezone.utc).isoformat(), 'file_count_in_manifest': len(manifest_files),
          'manifest_sha256': sha(WORK / 'manifest.json'),
          'effective_proposal_sha256': sha(WORK / 'effective-integration-proposal.json'),
          'source_index_sha256': sha(WORK / 'source-evidence-index.json'),
          'qa_sha256': sha(WORK / 'intake-qa.json'), 'handoff_sha256': sha(WORK / 'HANDOFF.md'),
          'minimal_publication_list_sha256': sha(WORK / 'minimal-publication-files.json'),
          'public_file_count': len(publication_names),
          'raw_occurrences': len(raw), 'raw_unique_ids': snapshot['raw_unique_ids'],
          'new_candidates': 3, 'registry_requests': len(receipts),
          'actual_free_http_requests': len(all_receipts), 'paid_requests': 0,
          'production_writes': 0, 'new_scope_reviews_completed': 0}
save('freeze-receipt.json', freeze)
print(json.dumps(freeze, ensure_ascii=False))
