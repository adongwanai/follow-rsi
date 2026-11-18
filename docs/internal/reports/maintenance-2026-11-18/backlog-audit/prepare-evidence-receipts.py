"""Freeze source-identity reuse and bounded new-version readbacks, without adoption."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from difflib import SequenceMatcher, unified_diff

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[5]
REPORT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/backlog-audit'
RAW = ROOT / 'data/feed/raw/maintenance-2026-11-18/backlog-audit'
REFRESH = RAW / 'remote-refresh-v1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def ref(path):
    return {'path': str(path.relative_to(ROOT)), 'sha256': sha(path.read_bytes())}


def dump(name, value):
    path = REPORT / name
    assert not path.exists(), 'Do not replace a frozen evidence receipt.'
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


old_path = ROOT / 'data/feed/raw/maintenance-2026-11-15/publication-final/backlog-audit/four-issue-evidence-review.json'
old = json.loads(old_path.read_text())
four = []
for prior in old['items']:
    aid = prior['id'].split(':')[1]
    comparisons = []
    for earlier in prior['source_comparison']:
        path = REFRESH / (aid + ('-abs.html' if '/abs/' in earlier['url'] else '-current.html'))
        comparisons.append({**ref(path), 'url': earlier['url'], 'prior_sha256': earlier['sha256'], 'byte_identical': sha(path.read_bytes()) == earlier['sha256']})
    assert all(r['byte_identical'] for r in comparisons)
    repository = None
    if aid in {'2610.39714', '2610.36013'}:
        name, expected = {'2610.39714': ('molrsi', 'ded9761ebc65624de0a7639e6b2865457d6543ca'), '2610.36013': ('omnibrain', '58915ee619f78f59aaa5db04c074565b3b97d380')}[aid]
        tree = json.loads((REFRESH / (name + '-tree.json')).read_text())
        assert tree['sha'] == expected
        repository = {'tree_sha': tree['sha'], 'prior_tree_sha': expected, 'unchanged': True, 'receipt': ref(REFRESH / (name + '-tree.json')), 'files': [r['path'] for r in tree['tree']]}
    four.append({'id': prior['id'], 'issue': prior['issue'], 'source_hash': prior['source_hash'], 'status': 'unchanged_original_body_and_artifact_gap_reconfirmed', 'scope_recommendation': prior['suggestion'], 'reason_zh': prior['pending_evidence'], 'source_comparison': comparisons, 'repository': repository, 'previous_valid_review': ref(old_path), 'prior_item_id': prior['id'], 'new_body_review_performed': False, 'scope_or_formal_decision_changed': False, 'recommend_close': False})
dump('four-issue-evidence-v1.json', {'reviewed_on': '2026-11-18', 'review_level': 'byte_hash_reuse_of_saved_source_review', 'items': four, 'paid_requests': 0})

version_rows = []
for aid, issue in [('2609.38372', 115), ('2609.34924', 116)]:
    pair = []
    for version in [1, 2]:
        path = REFRESH / f'{aid}v{version}.html'
        soup = BeautifulSoup(path.read_bytes(), 'html.parser')
        whole = soup.get_text(' ', strip=True)
        watermark = re.search(r'arXiv:' + re.escape(aid) + rf'v{version}\s+\[[^\]]+\]\s+\d+\s+\w+\s+\d{{4}}', whole)
        assert watermark is not None and soup.find('article') is not None
        article = soup.find('article')
        text = article.get_text(' ', strip=True)
        tables = [table.get_text(' ', strip=True) for table in article.select('table.ltx_tabular')]
        math = [m.get('alttext', m.get_text(' ', strip=True)) for m in article.select('math')]
        paragraphs = [p.get_text(' ', strip=True) for p in article.select('.ltx_para')]
        side = {'version': version, 'url': f'https://arxiv.org/html/{aid}v{version}', 'source': ref(path), 'watermark': watermark.group(0), 'title': article.h1.get_text(' ', strip=True), 'article_text_sha256': sha(text.encode()), 'article_characters': len(text), 'abstract': article.select_one('.ltx_abstract').get_text(' ', strip=True), 'tables': tables, 'math': math, 'paragraphs': paragraphs, 'text': text}
        pair.append(side)
    old_side, new_side = pair
    delta_path = RAW / f'{aid}-v1-v2-paragraph-diff.txt'
    assert not delta_path.exists()
    delta_path.write_text('\n'.join(unified_diff(old_side['paragraphs'], new_side['paragraphs'], fromfile=f'{aid}v1', tofile=f'{aid}v2', lineterm='')) + '\n')
    if issue == 115:
        quotes = [
            'the same frozen model, on the same version of the harness, first solves tasks as the solver and then, as the proposer, reads the complete run records and directly edits the harness that runs it.',
            'the harnesses evolved by GLM-5.3 and GPT-5.6 Sol gain about 5 points on the in-distribution benchmarks',
            'Code and the evolved harnesses are available at this link .',
        ]
        conclusion = 'v2改标题并扩展多模型及重复运行/区间结果；摘要不再复用v1的4.48、12.64与66.17→68.06单版叙述。反馈编辑自身Harness的范围依据仍可见，但本次只是版本身份和指定段落读回，不能视为完整候选版本或新版数字已审核。'
        next_actions = ['review_v2_added_model_conditions_and_all_publicly_quoted_numbers_against_tables', 'independent_version_crosscheck_before_updating_catalog_title_or_summary', 'preserve_v1_scientific_snapshot_until_exact_version_dated_receipt']
    else:
        quotes = [
            'we propose, but do not run, the experiment that would test the argument.',
            'Our evidence is descriptive.',
            'These are not SWE-bench resolve rates',
            'the set of tasks still able to improve shrinks and gets harder with each round.',
        ]
        conclusion = 'v2明确把scaffold可扩张的主张写为待实验检验的假说，并展开幸存任务选择与成功后停止两项混杂。已核摘要与5.1节及表格文本指纹；没有进行全论文证明、图像、全部数字的独立复审，不应自动刷新旧证据卡或关闭版本issue。'
        next_actions = ['review_v2_claim_qualification_and_theorem_assumptions', 'independent_check_of_existing_catalog_summary_against_v2_limitations', 'separate_descriptive_saturation_from_empirically_verified_scaffold_expansion', 'obtain_exact_version_dated_receipt_before_adoption']
    for quote in quotes:
        assert quote in new_side['text'], quote
    row = {'id': 'arxiv:' + aid, 'issue': issue, 'current_version': 1, 'candidate_version': 2, 'status': 'version_pair_recovered_partial_readback_full_review_pending', 'source_identity_verified': True, 'source_files': [{k: v for k, v in side.items() if k not in {'tables', 'math', 'paragraphs', 'text'}} for side in pair], 'article_text_identical': old_side['article_text_sha256'] == new_side['article_text_sha256'], 'tables_exactly_identical': old_side['tables'] == new_side['tables'], 'tables_count': [len(s['tables']) for s in pair], 'math_exactly_identical': old_side['math'] == new_side['math'], 'math_count': [len(s['math']) for s in pair], 'paragraph_diff': ref(delta_path), 'verified_v2_quotes': quotes, 'reason_zh': conclusion, 'next_actions': next_actions, 'fulltext_review_required': True, 'scope_review_complete': False, 'independent_cross_review_complete': False, 'formal_version_adopted': False, 'catalog_changed': False, 'experiments_reproduced': False, 'binary_figure_assets_checked': False, 'recommend_close': False}
    version_rows.append(row)
dump('new-version-readback-v1.json', {'observed_on': '2026-11-18', 'items': version_rows, 'paid_requests': 0})

retry = json.loads((REPORT / 'blocker-retry-v1.json').read_text())
groups = {}
for attempt in retry['requests']:
    groups.setdefault(attempt['id'], []).append(attempt)
blockers = []
for ident, attempts in sorted(groups.items()):
    metadata = []
    for attempt in attempts:
        assert not attempt['recovered_body'], 'Recovered fulltext needs a separate scope review.'
        if attempt.get('http_status') == 200 and 'ieee' in attempt['url']:
            path = ROOT / attempt['body_path']
            match = re.search(r'xplGlobal\.document\.metadata\s*=\s*(\{.*?\});', path.read_text(errors='replace'), re.S)
            assert match, 'Expected the returned IEEE subscription metadata HTML.'
            data = json.loads(match.group(1))
            metadata.append({'source': ref(path), 'abstract': data.get('abstract'), 'doi': data.get('doi'), 'authors': [author['name'] for author in data.get('authors', [])], 'publication_date_raw': data.get('publicationDate'), 'display_publication_date_raw': data.get('displayPublicationDate'), 'online_date_raw': data.get('onlineDate'), 'is_open_access': data.get('isOpenAccess'), 'fulltext_recovered': False})
    if ident == 's2:4f0054281e9d9be28b7740765b426b0a125aad68':
        reason = 'IEEE页面202空体；旧PDF地址这次HTTP200但实际返回订阅元数据HTML。已恢复官方摘要、DOI与作者，明确缓存结构迁移及meta-skill晋升；仍缺正文以区分内容积累、参数槽位与Harness工件更新。05–07 Oct为会议区间，首次上线日unknown。'
    elif ident == 's2:7872d98d7366afe3ac62a134eb74aa3efdf3018b':
        reason = 'IEEE页面202空体，stamp端点200实际为订阅元数据HTML；官方摘要可读但正文未恢复。显示/插入日期08/31与刊期11/15仍须分开，首次上线日期unknown。需核机制更新与持久知识内容边界。'
    elif any('elsevier' in a['url'] for a in attempts):
        reason = 'ScienceDirect页面403；Elsevier API200 XML仅元数据，abstract/description/body/originalText均无非空内容。未恢复所需原始摘要或方法正文。'
    else:
        reason = 'ACM DOI页面和PDF端点均403，HTML为Just a moment访问挑战。未取得PDF或可核方法正文。'
    blockers.append({'id': ident, 'status': 'official_metadata_recovered_fulltext_still_blocked' if metadata else 'source_blocker_reconfirmed_2026_11_18', 'reason_zh': reason, 'attempts': attempts, 'official_metadata': metadata, 'fulltext_recovered': False, 'scope_decision_changed': False, 'required_actions': ['obtain_official_fulltext_or_author_method_artifact', 'complete_identity_date_scope_review_before_acceptance'], 'paid_requests': 0})
assert len(blockers) == 13
dump('source-blocker-assessments-v1.json', {'observed_on': '2026-11-18', 'items': blockers, 'request_count': len(retry['requests']), 'fulltext_recovered': 0, 'paid_requests': 0})
print(json.dumps({'four_body_reviews_reused': len(four), 'new_version_pairs_partial': len(version_rows), 'source_blockers': len(blockers), 'version_table_equality': {r['id']: r['tables_exactly_identical'] for r in version_rows}}, ensure_ascii=False))
