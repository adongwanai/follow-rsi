"""Publication windows follow observed HF recommendation days, then source dates."""
from datetime import date as parse_date, timedelta
import json
from pathlib import Path


def published_editions(root):
    root = Path(root)
    return [json.loads(path.read_text()) for folder, pattern in (
        ('daily', '????-??-??.json'), ('recaps', '????-??-??--????-??-??.json'))
        for path in sorted((root / 'site' / folder).glob(pattern))]


def review_window(root, day):
    current = parse_date.fromisoformat(day)
    previous = [edition.get('end', edition.get('date')) for edition in published_editions(root)]
    previous = [value for value in previous if value and value < day]
    return max(previous) if previous else str(current - timedelta(days=2))


def publication_dates(item, day, lower, published_ids=()):
    announced = item.get('announced') or str(item.get('published') or item.get('hf_submitted_at') or '')[:10]
    announced_source = item.get('announced_source') or ('published' if item.get('published') else 'hf_submitted_at' if item.get('hf_submitted_at') else 'unknown')
    recommended = sorted(item.get('hf_daily_dates', []))
    observed = [value for value in recommended if value <= day]
    news_date = (observed[-1] if observed else recommended[0]) if recommended else str(item.get('updated') or announced)[:10]
    status = 'backlog'
    if item['id'] in published_ids:
        status = 'already_published'
    elif news_date:
        age = (parse_date.fromisoformat(day) - parse_date.fromisoformat(news_date)).days
        if age > 30:
            status = 'stale'
        elif lower < news_date <= day and not item.get('backfill_only'):
            status = 'in_window'
    return {'announced': announced, 'announced_source': announced_source,
            'news_date': news_date, 'window_status': status}


def daily_metadata(root, item, day):
    seen = {entry['id'] for edition in published_editions(root)
            if edition.get('date') != day or edition.get('kind') == 'retrospective'
            for entry in edition['items']}
    return publication_dates(item, day, review_window(root, day), seen)
