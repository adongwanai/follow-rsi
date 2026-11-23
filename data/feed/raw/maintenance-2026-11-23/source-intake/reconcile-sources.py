"""Reconcile saved free-source responses; writes only this isolated directory."""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys

import yaml

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from scripts.feed import fetch_arxiv, fetch_github, fetch_hf, fetch_rss, fetch_s2
from scripts.feed.dedupe import similar_titles
from scripts.feed.review import source_hash

WORK = ROOT / 'build/maintenance-2026-11-23/source-intake'
DAY = '2026-11-23'
NOW = datetime.now(timezone.utc)
assert NOW.date().isoformat() == DAY


def save(name, value):
    (WORK / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


base = {x['id']: x for x in map(json.loads, (WORK / 'canonical-baseline.jsonl').read_text().splitlines())}
prior_observations = {}
watch_path = WORK.parent / 'pr-audit/issue-canonical-mapping.json'
if watch_path.exists():
    for issue in json.loads(watch_path.read_text()):
        for aid in issue['arxiv_ids']:
            ident = 'arxiv:' + aid
            known = prior_observations.get(ident)
            if not known or issue['created_at'] < known['observed_at']:
                prior_observations[ident] = {'observed_at': issue['created_at'],
                    'source': 'repository arxiv-watch issue', 'url': issue['url'],
                    'evidence_path': str(watch_path.relative_to(ROOT)), 'evidence_sha256': sha(watch_path)}


def first_seen(ident, collected_at):
    if ident in base:
        return base[ident]['first_seen']
    prior = prior_observations.get(ident)
    return min(prior['observed_at'], collected_at) if prior else collected_at

sources = [x for x in yaml.safe_load((WORK / 'feed/sources.yaml').read_text())['sources'] if x['enabled']]
seed_ids = {x['arxiv']: x['id'] for x in fetch_s2.seed_papers(yaml.safe_load((WORK / 'data/papers.yaml').read_text())['papers'])}
official = {}
for path in [WORK / 'official-metadata/records.json', WORK / 'official-metadata/extra/records.json']:
    if path.exists():
        official.update({x['arxiv_id']: x for x in json.loads(path.read_text())['records']})
raw_rows, eligible, receipts_by_source, source_summaries = [], [], {}, []
observed = {}
for source in sources:
    sid, kind = source['id'], source['kind']
    checkpoint = WORK / 'source-results' / f'{sid}.json'
    result = json.loads(checkpoint.read_text()) if checkpoint.exists() else None
    receipt_path = WORK / 'network' / sid / 'attempts.jsonl'
    receipts = [json.loads(x) for x in receipt_path.read_text().splitlines()] if receipt_path.exists() else []
    receipts_by_source[sid] = receipts
    source_raw, source_eligible = [], []
    dispositions = Counter()
    for receipt in receipts:
        if receipt.get('http_status') != 200:
            continue
        path = ROOT / receipt['body_path']
        assert sha(path) == receipt['body_sha256'], path
        now, url = receipt['requested_at'], receipt['request_url']
        if kind == 'hf_daily':
            records = fetch_hf.parse_json(json.loads(path.read_text()), sid, keywords=[], now=now,
                                         daily_date=receipt['params']['date'])
        elif kind == 'arxiv_query':
            if url.startswith('https://rss.arxiv.org/'):
                records = fetch_rss.parse_feed(path.read_bytes(), sid, now=now, feed_url=receipt['final_url'])
            else:
                records = fetch_arxiv.parse_atom(path.read_text(), sid, now=now)
        elif kind == 'rss':
            records = fetch_rss.parse_feed(path.read_bytes(), sid, now=now, feed_url=receipt['final_url'])
        elif kind == 'github_releases':
            repository = url.split('/repos/', 1)[1].removesuffix('/releases')
            records = fetch_github.parse_json(json.loads(path.read_text()), repository, sid, now=now)
        elif url.endswith(('/citations', '/papers')):
            seed_id = seed_ids.get(url.split('paper/arXiv:', 1)[1].removesuffix('/citations')) if '/citations' in url else None
            records = fetch_s2.parse_json(json.loads(path.read_text()), sid,
                                         seed_id=seed_id,
                                         author_tracked=kind == 's2_authors', now=now)
        else:
            # S2 seed author metadata is coverage evidence, not a discovered paper page.
            continue
        for index, record in enumerate(records):
            ident = record['id']
            observed[ident] = min(observed.get(ident, now), now)
            record['source_observed_at'] = now
            record['first_seen'] = first_seen(ident, now)
            record['first_seen_policy'] = 'preserve_canonical' if ident in base else 'earliest_verified_repository_observation' if ident in prior_observations else 'actual_source_observation'
            if ident in prior_observations and ident not in base:
                record['first_seen_evidence'] = prior_observations[ident]
            date = str(record.get('source_published') or record['published'])[:10]
            if kind in {'hf_daily', 'arxiv_query'}:
                disposition = 'within_requested_source_window'
            elif kind in {'s2_citations', 's2_authors'}:
                cutoff = (NOW - timedelta(days=30)).date().isoformat()
                disposition = ('missing_publication_date' if not date else 'before_source_window' if date < cutoff
                               else 'after_target_date' if date > DAY else 'within_requested_source_window')
            else:
                cutoff = (NOW - timedelta(days=source['params'].get('lookback_days', 14) - 1)).date().isoformat()
                disposition = ('needs_official_metadata' if not date and record.get('arxiv_id')
                               else 'missing_publication_date' if not date else 'before_source_window' if date < cutoff
                               else 'after_target_date' if date > DAY else 'within_requested_source_window')
            evidence = {key: receipt[key] for key in ('requested_at', 'finished_at', 'request_url', 'body_path', 'body_sha256')}
            evidence.update(params=receipt.get('params'), normalized_record_index=index)
            row = {'source_id': sid, 'id': ident, 'title': record['title'], 'published_as_reported': record['published'],
                   'disposition': disposition, 'new_to_canonical': ident not in base, 'record': record, 'evidence': evidence}
            raw_rows.append(row)
            source_raw.append(row)
            dispositions[disposition] += 1
            if disposition in {'within_requested_source_window', 'needs_official_metadata'}:
                eligible.append(row)
                source_eligible.append(row)
    today = result.get('hf_today') if result and kind == 'hf_daily' else None
    status = 'pending' if result is None else 'partial' if result.get('error') and source_raw else 'error' if result.get('error') else 'ok'
    if today and today.get('request_status') == 'not_ready':
        status = 'historical_boards_ok_today_not_ready'
    source_summaries.append({'source_id': sid, 'kind': kind, 'status': status,
        'started_at': result['started_at'] if result else receipts[0]['requested_at'] if receipts else None,
        'finished_at': result['finished_at'] if result else None, 'request_count': len(receipts),
        'http_status_counts': dict(Counter(str(r.get('http_status', 'network_error')) for r in receipts)),
        'raw_records_from_successful_responses': len(source_raw), 'raw_unique_ids': len({x['id'] for x in source_raw}),
        'configured_window_records': len(source_eligible), 'configured_window_unique_ids': len({x['id'] for x in source_eligible}),
        'original_collector_count': result['count'] if result else None,
        'window_dispositions': dict(dispositions), 'error': result.get('error') if result else None,
        'source_traversal_complete': result.get('source_traversal_complete', not bool(result.get('error'))) if result else False,
        'hf_today': today, 'network_attempts': str(receipt_path.relative_to(ROOT))})

# Only exact stable identities are coalesced here. Any approximate-title collision is held for review.
incoming = {}
bindings = defaultdict(list)
for row in eligible:
    r = deepcopy(row['record'])
    ident = r['id']
    bindings[ident].append(row['evidence'])
    if ident not in incoming:
        incoming[ident] = r
    else:
        for field in ['source_hits', 'seed_hits', 'code_links', 'categories', 'hf_daily_dates']:
            incoming[ident][field] = sorted(set(incoming[ident].get(field, [])) | set(r.get(field, [])))
        incoming[ident]['links'].update(r['links'])
    incoming[ident]['first_seen'] = first_seen(ident, observed[ident])
    incoming[ident]['source_observed_at'] = observed[ident]

new_items, metadata_changes, provenance_updates, collisions = [], [], [], []
for ident, record in incoming.items():
    old = base.get(ident)
    authority = official.get(record.get('arxiv_id'))
    if authority:
        fields = ['title', 'abstract', 'authors', 'published', 'updated', 'version', 'published_source',
                  'announced', 'announced_source', 'comments']
        if old:
            differences = {k: {'before': old.get(k), 'official': authority.get(k)} for k in fields
                           if old.get(k) != authority.get(k)}
            if differences:
                metadata_changes.append({'id': ident, 'existing_source_hash': source_hash(old),
                    'official_arxiv_id': authority['arxiv_id'], 'differences': differences,
                    'automatically_applied': False, 'review_required': True})
        else:
            for k in fields:
                record[k] = authority[k]
            record['links'].update(authority['links'])
            record['metadata_pending'] = False
            record['official_metadata_verified'] = True
            record['official_metadata_record_id'] = authority['id']
            if authority.get('metadata_evidence'):
                record['official_metadata_evidence'] = authority['metadata_evidence']
    if old:
        updates = {k: sorted(set(record.get(k, [])) - set(old.get(k, [])))
                   for k in ['source_hits', 'hf_daily_dates']}
        updates = {k: v for k, v in updates.items() if v}
        if updates:
            provenance_updates.append({'id': ident, 'existing_source_hash': source_hash(old),
                'existing_first_seen': old['first_seen'], 'observed_source_hash_is_not_apply_precondition': True,
                'apply_validation': 'Check baseline first_seen then union source_hits and hf_daily_dates only; retain all science and decisions.',
                'add_to_sets': updates, 'bindings': bindings[ident],
                'scientific_fields_and_decisions_must_remain_unchanged': True})
    else:
        same = [x['id'] for x in base.values() if x['kind'] == record['kind'] and (
            record.get('arxiv_id') and x.get('arxiv_id') == record['arxiv_id'] or
            record['kind'] == 'paper' and similar_titles(x['title'], record['title']))]
        if same:
            collisions.append({'incoming_id': ident, 'possible_existing_ids': same, 'title': record['title'],
                               'proposed_record': record, 'action': 'hold_for_identity_reconciliation'})
        else:
            record['intake_review_status'] = 'unreviewed_free_source_candidate'
            new_items.append({'id': ident, 'record': record, 'bindings': bindings[ident],
                              'formal_decision': 'defer', 'paid_stages_run': False})

for item in new_items:
    assert item['record']['first_seen'] == first_seen(item['id'], observed[item['id']])
assert all(incoming[k]['first_seen'] == base[k]['first_seen'] for k in incoming.keys() & base.keys())
summary = {'generated_at': datetime.now(timezone.utc).isoformat(), 'target_day': DAY,
    'canonical_baseline': json.loads((WORK / 'canonical-baseline.json').read_text()),
    'enabled_sources': len(sources), 'sources_finished': sum(x['status'] != 'pending' for x in source_summaries),
    'all_sources_attempted_and_finished': all(x['status'] != 'pending' for x in source_summaries),
    'sources': source_summaries, 'raw_occurrences': len(raw_rows), 'raw_unique_ids': len({x['id'] for x in raw_rows}),
    'configured_window_occurrences': len(eligible), 'configured_window_unique_ids': len(incoming),
    'proposed_new_ids': [x['id'] for x in new_items], 'new_items': len(new_items),
    'new_items_by_kind': dict(Counter(x['record']['kind'] for x in new_items)),
    'existing_provenance_updates': len(provenance_updates),
    'existing_hf_membership_updates': sum('hf_daily_dates' in x['add_to_sets'] for x in provenance_updates),
    'official_metadata_change_candidates': len(metadata_changes), 'identity_collisions': len(collisions),
    'missing_official_metadata_new_papers': [x['id'] for x in new_items if x['record']['kind'] == 'paper'
                                           and x['record'].get('arxiv_id') and not x['record'].get('official_metadata_verified')],
    'known_first_seen_preserved': True, 'production_writes': 0, 'paid_calls': 0,
    'scope_review_boundary': 'Free discovery and metadata only. No per-paper final review, paid judge, acceptance, or publication.'}
save('all-source-snapshot.json', summary)
save('integration-proposal.json', {'generated_at': summary['generated_at'], 'target_day': DAY,
    'canonical_baseline': summary['canonical_baseline'], 'new_items': new_items,
    'existing_provenance_updates': provenance_updates, 'official_metadata_change_candidates': metadata_changes,
    'identity_collisions': collisions, 'applied': False, 'production_writes': 0, 'paid_calls': 0})
(WORK / 'raw-source-id-reconciliation.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True) + '\n' for x in raw_rows))
(WORK / 'candidate-records.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True) + '\n' for x in incoming.values()))
lines = [f'# {DAY} 免费来源快照', '',
    f"生成时间 {summary['generated_at']}；12 路中 {summary['sources_finished']} 路已结束。本报告只涵盖实际请求得到的响应，失败源未覆盖部分保持未知。", '',
    '| 来源 | 状态 | 全部原始记录 | 窗口内记录 | 请求/HTTP |', '|---|---|---:|---:|---|']
for x in source_summaries:
    lines.append(f"| {x['source_id']} | {x['status']} | {x['raw_records_from_successful_responses']} | {x['configured_window_records']} | {x['request_count']} / {x['http_status_counts']} |")
hf_result = next(x for x in source_summaries if x['source_id'] == 'hf-daily')
hf_board_receipts = receipts_by_source['hf-daily']
hf_board_counts = {x['params']['date']: len(json.loads((ROOT / x['body_path']).read_text()))
                   for x in hf_board_receipts if x.get('http_status') == 200}
lines += ['', f"HF 当日状态：{hf_result['hf_today']['request_status']}；API 给出的 available_through：{hf_result['hf_today']['available_through']}。实际成功响应完整榜单及篇数：{hf_board_counts}。空数组仅说明该次请求返回空榜，不代表全部来源没有更新。",
          '', f"相对 {len(base)} 条 canonical 基线，提议新增 {len(new_items)} 条；{len(provenance_updates)} 条已知记录有来源/日期补记，{len(metadata_changes)} 条有官方元数据差异需审，{len(collisions)} 条身份冲突待核对。",
          '', '全部 raw ID、出处 hash 和时间见 raw-source-id-reconciliation.jsonl。可应用清单见 integration-proposal.json；该清单尚未应用，保留所有旧 first_seen、科学字段、审核和发表状态。', '',
          '失败或范围限制：']
for x in source_summaries:
    if x['error']:
        lines.append(f"- {x['source_id']}: {x['error']}")
lines += ['', '0 付费调用；未运行 judge、summarize 或 evaluate；未修改 production、commit、push 或 GitHub。', '']
(WORK / 'all-source-snapshot.md').write_text('\n'.join(lines))
print(json.dumps({k: summary[k] for k in ['generated_at', 'sources_finished', 'raw_occurrences', 'raw_unique_ids',
    'configured_window_unique_ids', 'new_items', 'new_items_by_kind', 'existing_provenance_updates',
    'existing_hf_membership_updates', 'official_metadata_change_candidates', 'identity_collisions',
    'missing_official_metadata_new_papers']}, ensure_ascii=False))
