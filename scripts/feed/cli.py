"""Follow RSI stages, resumable processing, and the owner publication gate."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
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


def _needs_gate_migration(item):
    decision = item.get('llm', {})
    if (decision.get('label') not in ('include', 'borderline')
            or (decision.get('primary') not in ('harness', 'evaluation_benchmark', 'theory_survey')
                and 'harness' not in decision.get('secondary', []))):
        return False
    gate = item.get('gate', {})
    fields = {'verdict', 'improved_object', 'improved_object_zh', 'harness_specific',
              'feedback_driven', 'persists_across_tasks', 'why_zh'}
    return not (fields <= gate.keys() and all(
        isinstance(gate[field], dict) and {'value', 'quote'} <= gate[field].keys()
        for field in ('feedback_driven', 'persists_across_tasks')))


def _needs_prompt_migration(item, root):
    for stage in ('relevance', 'classify', 'harness_gate'):
        previous = item.get('llm', {}).get(stage, {})
        responses = previous.get('samples', []) if stage == 'harness_gate' else [previous]
        for response in responses:
            recorded = response.get('template_hash')
            if recorded and recorded != hashlib.sha256(
                    (Path(root) / 'feed/prompts' / f'{stage}.md').read_bytes()).hexdigest():
                return True
    return False


def _backfill_items(root, items):
    from scripts.feed.window import published_editions
    editions = published_editions(root)
    editions += [json.loads(path.read_text()) for path in
                 (Path(root) / 'site/weekly').glob('????-W??.json')]
    published = {row['id'] for edition in editions
                 for row in [*edition['items'], *edition.get('lab_updates', []),
                             *edition.get('backlog', [])]}
    for item in items:
        if item['id'] not in published:
            item['backfill_only'] = True
    return items


def process_items(root, stage, workers=4, client=None):
    from scripts.feed.judge import judge_item, summarize_item
    from scripts.feed.library import curated_item
    from scripts.feed.llm import FeedLLM, LLMConfigurationError
    from scripts.feed.scope import archive_out_of_scope
    items = load_items(root)
    refreshed = {}
    for item in items:
        if (item['kind'] == 'paper' and item.get('in_repo')
                and item.get('review', {}).get('kind') != 'correction'):
            curated = curated_item(item, root)
            if curated != item:
                refreshed[item['id']] = curated
    if refreshed:
        save_items(root, refreshed.values())
        items = [refreshed.get(item['id'], item) for item in items]
    automatic = [item for item in items if not item.get('in_repo')
                 and item.get('review', {}).get('kind') != 'correction']
    if stage == 'judge':
        todo = [item for item in automatic if item['kind'] == 'paper'
                and (item.get('llm', {}).get('label') in (None, '', 'error')
                     or _needs_gate_migration(item) or _needs_prompt_migration(item, root))]
        for item in todo:
            if item.get('llm', {}).get('label'):
                # Reclassification must not retain a legacy gate or summary.
                for field in ('gate', 'summary_zh', 'summary_en'):
                    item.pop(field, None)
        operation = judge_item
    else:
        todo = [item for item in automatic if item.get('llm', {}).get('label') in ('include','borderline')
                and 'summary_zh' not in item]
        operation = summarize_item
    if not todo:
        return {'stage':stage, 'processed':len(refreshed),
                'archived':archive_out_of_scope(root) if stage == 'summarize' else 0}
    client = client or FeedLLM.from_env(root)
    counts = {}
    configuration_error = None
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(operation, item, client, root): item['id'] for item in todo}
        for future in as_completed(pending):
            if future.cancelled():
                continue
            try:
                result = future.result()
            except LLMConfigurationError as error:
                if configuration_error is None:
                    configuration_error = error
                for queued in pending:
                    queued.cancel()
                continue
            save_items(root, [result])
            label = result.get('label', 'unjudged')
            counts[label] = counts.get(label, 0) + 1
            processed = sum(counts.values())
            if processed == 1 or processed % 10 == 0 or processed == len(todo):
                print(f'{stage}: {processed}/{len(todo)} processed; {counts}', flush=True)
    if configuration_error is not None:
        print(f'{stage}: interrupted; {sum(counts.values())}/{len(todo)} results saved; {counts}', flush=True)
        raise configuration_error
    return {'stage':stage, 'processed':len(todo) + len(refreshed), 'labels':counts,
            'archived':archive_out_of_scope(root) if stage == 'summarize' else 0}


def run_stage(root, stage, *, schedule='daily', days=2, sources=None, week=None, date=None,
              workers=4, issues=False, client=None):
    root = Path(root)
    week = week or current_week()
    date = date or current_date()
    directory = root / 'data/feed'
    if stage == 'fetch':
        from scripts.feed.fetch_arxiv import fetch_sources
        result = fetch_sources(root, schedule=schedule, days=days, source_ids=sources,
                               issue_client=issue_client(issues))
        result['batch'] = {'lookback_days': days, 'backfill_only': days > 3}
        write_json(directory/'last-fetch.json', result)
        return {'stage':stage, 'records':len(result['records']),
                'sources':[{k:v for k,v in entry.items() if k!='ids'} for entry in result['outcomes']]}
    if stage == 'normalize':
        from scripts.feed.normalize import normalize_records
        fetched = json.loads((directory/'last-fetch.json').read_text())
        records = normalize_records(fetched['records'])
        batch = fetched.get('batch', {'lookback_days': days, 'backfill_only': days > 3})
        batch['backfill_only'] = batch['backfill_only'] or days > 3
        write_json(directory/'normalized.json', {'records': records, 'batch': batch})
        return {'stage':stage, 'records':len(records)}
    if stage == 'dedupe':
        from scripts.feed.dedupe import dedupe_items
        normalized = json.loads((directory/'normalized.json').read_text())
        records = normalized if isinstance(normalized, list) else normalized['records']
        batch = {} if isinstance(normalized, list) else normalized['batch']
        items = dedupe_items(records, load_items(root), read_yaml(root/'data/papers.yaml')['papers'])
        if days > 3 or batch.get('backfill_only'):
            _backfill_items(root, items)
        return {'stage':stage, 'unique':len(items), 'appended':save_items(root,items)}
    if stage in ('judge','summarize'):
        return process_items(root, stage, workers=workers, client=client)
    if stage == 'queue':
        from scripts.feed.review import queue_daily_review
        fetched_path = directory / 'last-fetch.json'
        fetched = json.loads(fetched_path.read_text()) if fetched_path.exists() else {}
        if days > 3 or fetched.get('batch', {}).get('backfill_only'):
            save_items(root, _backfill_items(root, load_items(root)))
        result = queue_daily_review(root, date)
        return {'stage':stage, 'date':date, 'pending':sum(row['decision'] in ('pending', 'defer') for row in result['items']),
                'items':len(result['items']), 'path':str(root/'review/daily'/f'{date}.yaml')}
    if stage == 'publish':
        from scripts.feed.review import apply_daily_review
        from scripts.feed.digest import publish_day, require_publishable_day
        require_publishable_day(root, date)
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
            if any(row['decision'] in ('pending', 'defer') for row in rows):
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
    run.add_argument('--days',type=int,default=2)
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
        from scripts.feed.digest import publish_week,publish_day,publish_demo,require_publishable_day
        from scripts.feed.review import apply_daily_review,validate_weekly_picks
        if args.demo:
            result = publish_demo(args.root,week,render_card=args.render_card)
        elif args.week:
            validate_weekly_picks(args.root,week)
            result = publish_week(args.root,week,render_card=args.render_card)
        else:
            require_publishable_day(args.root,date)
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
