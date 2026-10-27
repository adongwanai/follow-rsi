"""Compare discovery against public reference lists without editing search terms."""
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import json
import ast
import requests
import yaml
from scripts.common import read_yaml
from .normalize import arxiv_ids, title_tokens
from .storage import load_items, write_json
from .health import timestamp, week_of
from .scope import direction_of, load_scope, scope_status

def _literal(text, name, opening):
    """Read one exported literal as data; never execute fetched JavaScript."""
    match = re.search(r'export\s+const\s+' + re.escape(name) + r'\s*=\s*' + re.escape(opening), text)
    if not match:
        raise ValueError(f'Reference is missing exported literal {name}')
    start = match.end() - 1
    closing = {"[": "]", "{": "}"}[opening]
    depth, index, quote, parts = 0, start, None, []
    while index < len(text):
        char = text[index]
        if quote:
            parts.append(char)
            if char == "\\":
                index += 1
                parts.append(text[index])
            elif char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
            parts.append(char)
        elif text.startswith('//', index):
            end = text.find('\n', index)
            index = len(text) if end < 0 else end
            parts.append('\n')
        elif text.startswith('/*', index):
            end = text.find('*/', index + 2)
            if end < 0:
                raise ValueError('Unterminated reference comment')
            index = end + 1
            parts.append(' ')
        else:
            parts.append(char)
            depth += char == opening
            depth -= char == closing
            if depth == 0:
                return ''.join(parts)
        index += 1
    raise ValueError(f'Unterminated reference literal {name}')


def harness_reference_ids(text, taxonomy_text, kind, artifact='Harness code'):
    """Intersect real metadata IDs with explicit upstream artifact labels."""
    taxonomy = _literal(taxonomy_text, 'methodTaxonomy' if kind == 'methods' else 'paperTaxonomy', '{')
    selected = set()
    for match in re.finditer(r'["\']([^"\']+)["\']\s*:\s*\{([^{}]*)\}', taxonomy, re.S):
        field = re.search(r'(?:["\']artifact["\']|\bartifact)\s*:\s*(\[[^\]]*\])', match[2])
        if field and artifact in ast.literal_eval(field[1]):
            selected.add(match[1])
    if not selected:
        raise ValueError(f'No explicitly labelled {artifact} entries found in {kind} taxonomy')
    literal = _literal(text, kind, '[')
    # Metadata entries are flat objects (authors/tags are arrays); string-aware
    # tokenization avoids treating braces or reference URLs in abstracts as rows.
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[{}]|[^{}"\']+', literal, re.S)
    entries, current, depth = [], [], 0
    for token in tokens:
        if token == '{':
            depth += 1
        if depth:
            current.append(token)
        if token == '}':
            depth -= 1
            if depth == 0:
                entries.append(''.join(current))
                current = []
    result = set()
    for entry in entries:
        match = re.search(r'(?:["\']id["\']|\bid)\s*:\s*(["\'])(.*?)\1', entry)
        if not match or match[2] not in selected:
            continue
        arxiv = re.search(r'(?:["\']arxiv["\']|\barxiv)\s*:\s*(null|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')', entry)
        if arxiv and arxiv[1] == 'null':
            continue
        result.update(arxiv_ids(ast.literal_eval(arxiv[1]) if arxiv else match[2]))
    return sorted(result)


def compare(reference_metadata, items, cutoff, scope=None):
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
        elif scope and scope_status(direction_of(item), scope) == 'out_of_scope':
            reason = 'outside_publish_scope'
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


def run(root, week=None, now=None, reference_texts=None, metadata=None, session=None, taxonomy_texts=None):
    from .fetch_arxiv import USER_AGENT, fetch_ids
    current = now or datetime.now(timezone.utc)
    if isinstance(current, str):
        current = timestamp(current)
    week = week or week_of(current.isoformat())
    cutoff = (current - timedelta(days=60)).date().isoformat()
    config = read_yaml(Path(root) / 'feed/sources.yaml')['recall']
    if config['scope'] != 'harness':
        raise ValueError('Recall currently supports only the Harness publication scope')
    registry = config['references']
    reports, references = {}, {}
    supplied = reference_texts is not None
    reference_texts = {} if reference_texts is None else reference_texts
    taxonomy_texts = {} if taxonomy_texts is None else taxonomy_texts
    if not supplied:
        for name, spec in registry.items():
            try:
                response = (session or requests).get(spec['url'], headers={'User-Agent': USER_AGENT}, timeout=30)
                response.raise_for_status()
                reference_texts[name] = response.text
                if spec['selection'] == 'artifact':
                    response = (session or requests).get(spec['taxonomy_url'], headers={'User-Agent': USER_AGENT}, timeout=30)
                    response.raise_for_status()
                    taxonomy_texts[name] = response.text
            except requests.RequestException as error:
                reports[name] = {'ok': False, 'url': spec['url'], 'error': str(error)}
    for name, text in reference_texts.items():
        if name not in registry:
            raise ValueError(f'Unconfigured recall reference: {name}')
        spec = registry[name]
        if name in reports and not reports[name]['ok']:
            continue
        try:
            if spec['selection'] == 'all':
                ids = arxiv_ids(text)
            elif spec['selection'] == 'artifact':
                if name not in taxonomy_texts:
                    raise ValueError('Harness taxonomy unavailable; full-table extraction is not permitted')
                ids = harness_reference_ids(text, taxonomy_texts[name],
                                            'methods' if name.endswith('methods') else 'papers', spec['artifact'])
            else:
                raise ValueError(f'Unsupported recall selection: {spec["selection"]}')
        except (ValueError, SyntaxError) as error:
            reports[name] = {'ok': False, 'url': spec['url'], 'error': str(error)}
            continue
        reports[name] = {'ok': True, 'url': spec['url'], 'selection': spec['selection'],
                         'ids': len(ids), 'all_ids': len(arxiv_ids(text))}
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
    misses, pending = compare(metadata, load_items(root), cutoff, scope=load_scope(root))
    counts = dict(Counter(item['reason'] for item in misses))
    suggestions = suggest_keywords(misses)
    report = {'week': week, 'checked_at': current.isoformat(), 'cutoff': cutoff,
              'scope': 'harness', 'reference_status': reports, 'metadata_unavailable': unavailable,
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
