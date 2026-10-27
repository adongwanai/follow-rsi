"""Follow RSI stages, resumable processing, and the owner publication gate."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path

from scripts.common import ROOT, read_yaml
from scripts.feed.storage import load_items, save_items, write_json

STAGES = ('fetch', 'normalize', 'dedupe', 'judge', 'summarize', 'queue', 'publish')


def configure(root, env_file=None):
    """Read only an explicitly named local key/value file; never evaluate shell text."""
    if env_file:
        allowed = {'LLM_PROVIDER', 'LLM_MODEL', 'LLM_BASE_URL', 'LLM_API_KEY', 'S2_API_KEY', 'GITHUB_TOKEN', 'GH_TOKEN'}
        for number, line in enumerate(Path(env_file).read_text().splitlines(), 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, separator, value = line.partition('=')
            key = key.removeprefix('export ').strip()
            if not separator or key not in allowed:
                raise ValueError(f'Unsupported environment assignment at line {number}')
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            os.environ[key] = value
    config = read_yaml(Path(root) / 'feed/model.yaml')
    for field, key in [('provider','LLM_PROVIDER'),('model','LLM_MODEL'),('base_url','LLM_BASE_URL')]:
        if config.get(field) and not os.environ.get(key):
            os.environ[key] = config[field]


def current_week():
    year, week, _ = datetime.now(timezone.utc).isocalendar()
    return f'{year}-W{week:02d}'


def current_date():
    return datetime.now(timezone.utc).date().isoformat()


def issue_client(enabled):
    if not enabled:
        return None
    from scripts.feed.health import GithubIssues
    return GithubIssues(os.environ['GITHUB_REPOSITORY'])


def process_items(root, stage, workers=4, client=None):
    from scripts.feed.judge import judge_item, summarize_item
    from scripts.feed.llm import FeedLLM
    items = load_items(root)
    if stage == 'judge':
        todo = [item for item in items if item['kind'] == 'paper' and not item.get('in_repo')
                and not item.get('llm', {}).get('label')]
        operation = judge_item
    else:
        todo = [item for item in items if item.get('label') in ('include','borderline')
                and not item.get('in_repo') and 'summary_zh' not in item]
        operation = summarize_item
    if not todo:
        return {'stage':stage, 'processed':0}
    client = client or FeedLLM.from_env(root)
    counts = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(operation, item, client, root): item['id'] for item in todo}
        for index, future in enumerate(as_completed(pending), 1):
            result = future.result()
            save_items(root, [result])
            label = result.get('label', 'unjudged')
            counts[label] = counts.get(label, 0) + 1
            if index == 1 or index % 10 == 0 or index == len(todo):
                print(f'{stage}: {index}/{len(todo)} processed; {counts}', flush=True)
    return {'stage':stage, 'processed':len(todo), 'labels':counts}


def run_stage(root, stage, *, schedule='daily', days=3, sources=None, week=None, date=None,
              workers=4, issues=False, client=None):
    root = Path(root)
    week = week or current_week()
    date = date or current_date()
    directory = root / 'data/feed'
    if stage == 'fetch':
        from scripts.feed.fetch_arxiv import fetch_sources
        from scripts.feed.health import update_health
        result = fetch_sources(root, schedule=schedule, days=days, source_ids=sources)
        write_json(directory/'last-fetch.json', result)
        update_health(root, result['outcomes'], issue_client=issue_client(issues))
        return {'stage':stage, 'records':len(result['records']),
                'sources':[{k:v for k,v in entry.items() if k!='ids'} for entry in result['outcomes']]}
    if stage == 'normalize':
        from scripts.feed.normalize import normalize_records
        fetched = json.loads((directory/'last-fetch.json').read_text())
        records = normalize_records(fetched['records'])
        write_json(directory/'normalized.json', records)
        return {'stage':stage, 'records':len(records)}
    if stage == 'dedupe':
        from scripts.feed.dedupe import dedupe_items
        records = json.loads((directory/'normalized.json').read_text())
        items = dedupe_items(records, load_items(root), read_yaml(root/'data/papers.yaml')['papers'])
        return {'stage':stage, 'unique':len(items), 'appended':save_items(root,items)}
    if stage in ('judge','summarize'):
        return process_items(root, stage, workers=workers, client=client)
    if stage == 'queue':
        from scripts.feed.review import queue_daily_review
        result = queue_daily_review(root, date)
        return {'stage':stage, 'date':date, 'pending':sum(row['decision']=='pending' for row in result['items']),
                'items':len(result['items']), 'path':str(root/'review/daily'/f'{date}.yaml')}
    if stage == 'publish':
        from scripts.feed.review import apply_daily_review
        from scripts.feed.digest import publish_day
        apply_daily_review(root, date)
        return publish_day(root, date)
    raise ValueError(f'Unknown pipeline stage: {stage}')


def run_pipeline(root=ROOT, stage='all', until=None, **options):
    from scripts.feed.digest import initialize_public
    from scripts.feed.health import compute_metrics
    initialize_public(root)
    stages = list(STAGES) if stage == 'all' else [stage]
    if until:
        if stage != 'all':
            raise ValueError('--until applies only to --stage all')
        stages = stages[:stages.index(until)+1]
    results = []
    for name in stages:
        if name == 'publish' and stage == 'all':
            review = read_yaml(Path(root)/'review/daily'/f"{options.get('date') or current_date()}.yaml")
            rows = review['items']+review['lab_updates']
            if any(row['decision']=='pending' for row in rows):
                results.append({'stage':'publish','status':'awaiting_owner_review'})
                break
            if not any(row['decision'] in ('accept','move') for row in rows):
                results.append({'stage':'publish','status':'no_approved_items'})
                break
        result = run_stage(root,name,**options)
        results.append(result)
        print(json.dumps(result,ensure_ascii=False),flush=True)
    compute_metrics(root,week=options.get('week'))
    return results


def check_versions(root, issues=False):
    from scripts.feed.fetch_arxiv import fetch_ids
    from scripts.feed.dedupe import dedupe_items
    from scripts.feed.health import version_alerts
    from scripts.feed.digest import remove_retracted
    papers = read_yaml(Path(root)/'data/papers.yaml')['papers']
    existing = load_items(root)
    ids = [p['arxiv'] for p in papers if p.get('arxiv')]
    ids += [p['arxiv_id'] for p in existing if p.get('arxiv_id')]
    fresh = fetch_ids(ids)
    merged = dedupe_items(fresh,existing,papers)
    save_items(root,merged)
    alerts = version_alerts(root,merged,issue_client=issue_client(issues))
    remove_retracted(root)
    return {'checked':len(fresh),'alerts':alerts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--env-file',type=Path)
    commands = parser.add_subparsers(dest='command',required=True)
    run = commands.add_parser('run')
    run.add_argument('--stage',choices=(*STAGES,'all'),default='all')
    run.add_argument('--until',choices=STAGES)
    run.add_argument('--schedule',choices=['daily','weekly','all'],default='daily')
    run.add_argument('--days',type=int,default=3)
    run.add_argument('--sources',nargs='+')
    run.add_argument('--week')
    run.add_argument('--date',default=current_date())
    run.add_argument('--workers',type=int,default=4)
    run.add_argument('--issues',action='store_true')
    for name in ('queue','picks','review','check-review','recall','promote','publish'):
        command = commands.add_parser(name)
        period = command.add_mutually_exclusive_group()
        period.add_argument('--week')
        period.add_argument('--date')
        if name == 'publish':
            command.add_argument('--render-card',action='store_true')
            command.add_argument('--demo',action='store_true')
    version = commands.add_parser('versions')
    version.add_argument('--issues',action='store_true')
    commands.add_parser('health')
    args = parser.parse_args()
    configure(args.root,args.env_file)
    if args.command == 'run':
        if args.days < 1 or args.workers < 1:
            parser.error('--days and --workers must be positive')
        run_pipeline(args.root,args.stage,args.until,schedule=args.schedule,days=args.days,
                     sources=args.sources,week=args.week,date=args.date,workers=args.workers,issues=args.issues)
        return
    date = getattr(args,'date',None) or current_date()
    week = getattr(args,'week',None) or current_week()
    if args.command == 'picks' or (args.command == 'queue' and args.week):
        from scripts.feed.review import queue_weekly_picks
        queue_weekly_picks(args.root,week)
        result = {'week':week,'path':str(args.root/'review'/f'{week}.yaml')}
    elif args.command == 'queue':
        result = run_stage(args.root,'queue',date=date)
    elif args.command in ('review','check-review'):
        from scripts.feed.review import interactive_daily_review,validate_daily_review,validate_weekly_picks
        if args.week:
            validate_weekly_picks(args.root,week)
            result = {'week':week,'status':'validated','path':str(args.root/'review'/f'{week}.yaml')}
        else:
            (interactive_daily_review if args.command=='review' else validate_daily_review)(args.root,date)
            result = {'date':date,'status':'validated' if args.command=='check-review' else 'saved'}
    elif args.command == 'publish':
        from scripts.feed.digest import publish_week,publish_day,publish_demo
        from scripts.feed.review import apply_daily_review,validate_weekly_picks
        if args.demo:
            result = publish_demo(args.root,week,render_card=args.render_card)
        elif args.week:
            validate_weekly_picks(args.root,week)
            result = publish_week(args.root,week,render_card=args.render_card)
        else:
            apply_daily_review(args.root,date)
            result = publish_day(args.root,date)
    elif args.command == 'promote':
        from scripts.feed.promote import promote_candidates
        result = promote_candidates(args.root,week=week) if args.week else promote_candidates(args.root,date=date)
    elif args.command == 'versions':
        result = check_versions(args.root,args.issues)
    elif args.command == 'recall':
        from scripts.feed.recall_check import run
        result = run(args.root,week=week)
    else:
        from scripts.feed.health import update_health,compute_metrics
        status = update_health(args.root,[])
        result = {'last_success':status['last_success'],'metrics':compute_metrics(args.root)}
    print(json.dumps(result,ensure_ascii=False,default=str,indent=2))


if __name__ == '__main__':
    main()
