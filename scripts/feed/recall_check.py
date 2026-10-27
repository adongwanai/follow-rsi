"""Compare discovery against public reference lists without editing search terms."""
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import requests
import yaml
from scripts.common import read_yaml
from .normalize import arxiv_ids, title_tokens
from .storage import load_items, write_json
from .health import timestamp, week_of

REFERENCES = {
    'Harness-RSI': 'https://raw.githubusercontent.com/zgcagi/Harness-RSI/main/README.md',
    'awesome-rsi-papers': 'https://raw.githubusercontent.com/Prism-Shadow/awesome-rsi/main/site/src/data/papers.js',
    'awesome-rsi-methods': 'https://raw.githubusercontent.com/Prism-Shadow/awesome-rsi/main/site/src/data/methods.js',
}


def compare(reference_metadata, items, cutoff):
    by_arxiv = {p['arxiv_id']: p for p in items if p.get('arxiv_id')}
    misses, pending = [], []
    for ref in reference_metadata:
        if not ref.get('published') or ref['published'][:10] < cutoff:
            continue
        item = by_arxiv.get(ref['arxiv_id'])
        reason = None
        if item is None:
            reason = 'never_fetched'
        elif item.get('llm', {}).get('label') == 'exclude':
            reason = 'excluded'
        elif item.get('llm', {}).get('label') == 'borderline' and item.get('review', {}).get('decision') == 'reject':
            reason = 'borderline_rejected'
        elif item.get('review', {}).get('decision') not in {'accept', 'move'} and not item.get('in_repo'):
            pending.append(ref['arxiv_id'])
        if reason:
            misses.append({'arxiv_id': ref['arxiv_id'], 'title': ref['title'], 'published': ref['published'],
                           'reason': reason, 'references': ref.get('references', [])})
    return misses, pending


def suggest_keywords(misses):
    stop = {'the', 'and', 'for', 'with', 'from', 'toward', 'towards', 'through', 'using', 'agent', 'agents',
            'learning', 'language', 'model', 'models', 'large', 'self', 'based', 'improving', 'recursive'}
    words = Counter(word for item in misses if item['reason'] == 'never_fetched'
                    for word in title_tokens(item['title']) if len(word) >= 5 and word not in stop and not word.isdigit())
    return [word for word, _ in words.most_common(8)]


def run(root, week=None, now=None, reference_texts=None, metadata=None, session=None):
    from .fetch_arxiv import USER_AGENT, fetch_ids
    import json
    current = now or datetime.now(timezone.utc)
    if isinstance(current, str):
        current = timestamp(current)
    week = week or week_of(current.isoformat())
    cutoff = (current - timedelta(days=60)).date().isoformat()
    reports, references = {}, {}
    if reference_texts is None:
        reference_texts = {}
        for name, url in REFERENCES.items():
            try:
                response = (session or requests).get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
                response.raise_for_status()
                reference_texts[name] = response.text
                reports[name] = {'ok': True, 'url': url}
            except requests.RequestException as error:
                reports[name] = {'ok': False, 'url': url, 'error': str(error)}
    for name, text in reference_texts.items():
        ids = arxiv_ids(text)
        reports.setdefault(name, {'ok': True})['ids'] = len(ids)
        for ident in ids:
            references.setdefault(ident, []).append(name)
    papers = read_yaml(Path(root) / 'data' / 'papers.yaml')['papers']
    for paper in papers:
        if paper.get('arxiv'):
            references.setdefault(paper['arxiv'], []).append('local-papers.yaml')
    # Numeric arXiv prefixes allow us to avoid fetching old foundations; exact
    # day inclusion still uses the API's first-submission date below.
    prefix_floor = (current - timedelta(days=60)).strftime('%y%m')
    candidates = [ident for ident in references if re.match(r'^\d{4}\.', ident) and ident[:4] >= prefix_floor]
    if metadata is None:
        metadata = fetch_ids(candidates, session=session, now=current.isoformat())
    metadata = [{**p, 'references': references.get(p['arxiv_id'], [])} for p in metadata if p['arxiv_id'] in references]
    unavailable = sorted(set(candidates) - {p['arxiv_id'] for p in metadata})
    misses, pending = compare(metadata, load_items(root), cutoff)
    counts = dict(Counter(item['reason'] for item in misses))
    suggestions = suggest_keywords(misses)
    report = {'week': week, 'checked_at': current.isoformat(), 'cutoff': cutoff,
              'reference_status': reports, 'metadata_unavailable': unavailable,
              'misses': misses, 'pending_review': pending, 'suggested_keywords': suggestions,
              'summary': f"本周漏判 {len(misses)} 篇，其中 {counts.get('never_fetched', 0)} 篇从未被抓到 → 建议新增关键词：{'、'.join(suggestions) or '暂无'}"}
    path = Path(root) / 'review' / f'{week}.misses.yaml'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(report, allow_unicode=True, sort_keys=False), encoding='utf-8')
    metrics_path = Path(root) / 'data' / 'feed' / 'metrics.json'
    metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {'weeks': {}}
    metrics.setdefault('weeks', {}).setdefault(week, {})['recall_vs_reference'] = {
        'missed': len(misses), 'reasons': counts, 'pending_review': len(pending),
        'metadata_unavailable': len(unavailable), 'references_failed': sum(not r['ok'] for r in reports.values())}
    write_json(metrics_path, metrics)
    return report
