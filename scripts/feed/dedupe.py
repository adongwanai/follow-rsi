"""Merge arXiv versions and near-identical titles without erasing human decisions."""
from copy import deepcopy
from .normalize import split_arxiv, title_tokens

LIST_FIELDS = ('source_hits', 'seed_hits', 'code_links', 'categories', 'aliases', 'hf_daily_dates')


def similar_titles(left, right):
    a, b = title_tokens(left), title_tokens(right)
    return bool(a and b) and len(a & b) / len(a | b) >= .9


def merge_item(old, new):
    merged = deepcopy(old)
    newer = new['version'] > old['version']
    # Non-empty source metadata may supplement existing records. Judgement and
    # review belong to their own stages, so fetching cannot overwrite them.
    for key in ('title', 'authors', 'abstract', 'comments', 'published', 'updated'):
        if new.get(key) and (newer or old.get('metadata_pending') or not old.get(key)):
            merged[key] = new[key]
    for key in LIST_FIELDS:
        merged[key] = sorted(set(old.get(key, [])) | set(new.get(key, [])))
    if new['id'] != old['id']:
        merged['aliases'] = sorted(set(merged['aliases']) | {new['id']})
    if 'metadata_pending' in new:
        merged['metadata_pending'] = new['metadata_pending']
    if old['title'] != new['title']:
        merged['aliases'] = sorted(set(merged['aliases']) | {old['title'], new['title']})
    merged['links'] = {**old.get('links', {}), **new.get('links', {})}
    merged['hf_upvotes'] = max(old.get('hf_upvotes', 0), new.get('hf_upvotes', 0))
    merged['in_repo'] = old.get('in_repo', False) or new.get('in_repo', False)
    merged['retracted'] = old.get('retracted', False) or new.get('retracted', False)
    merged['author_tracked'] = old.get('author_tracked', False) or new.get('author_tracked', False)
    if newer:
        merged['previous_version'] = old['version']
        merged['version'] = new['version']
        merged['version_changed'] = True
    if not old.get('arxiv_id') and new.get('arxiv_id'):
        merged['arxiv_id'] = new['arxiv_id']
        # Keep original stable id once an item has entered review/cache.
        merged['aliases'] = sorted(set(merged['aliases']) | {new['id']})
    if new.get('repo_id'):
        merged['repo_id'] = new['repo_id']
    return merged


def dedupe_items(incoming, existing=(), repo_papers=()):
    items = [deepcopy(item) for item in existing]
    repo_ids = {split_arxiv(p['arxiv'])[0]: p['id'] for p in repo_papers if p.get('arxiv')}
    for raw in incoming:
        item = deepcopy(raw)
        if item.get('arxiv_id') in repo_ids:
            item['in_repo'] = True
            item['repo_id'] = repo_ids[item['arxiv_id']]
        match = next((i for i, old in enumerate(items) if old['id'] == item['id'] or
                      (item.get('arxiv_id') and old.get('arxiv_id') == item['arxiv_id'])), None)
        if match is None and item['kind'] == 'paper':
            match = next((i for i, old in enumerate(items) if old['kind'] == 'paper' and
                          any(similar_titles(title, item['title']) for title in [old['title'], *old.get('aliases', [])])), None)
        if match is None:
            items.append(item)
        else:
            items[match] = merge_item(items[match], item)
    # Also mark already stored records when a paper was subsequently promoted.
    for item in items:
        if item.get('arxiv_id') in repo_ids:
            item['in_repo'], item['repo_id'] = True, repo_ids[item['arxiv_id']]
    return items
