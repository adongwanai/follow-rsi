"""GitHub Actions orchestration. External writes are disabled outside its runner."""
import argparse
import base64
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from jinja2 import Environment, nodes
from scripts.common import ROOT, read_yaml

REVIEW_PATH = re.compile(r'^review/(\d{4}-W\d{2})\.yaml$')
DAILY_PATH = re.compile(r'^review/daily/(\d{4}-\d{2}-\d{2})\.yaml$')
DAILY_BRANCH = re.compile(r'^feed/review-(\d{4}-\d{2}-\d{2})$')
PICKS_BRANCH = re.compile(r'^feed/picks-(\d{4})-w(\d{2})$')
PROMPT_NAMES = {'relevance', 'classify', 'evidence', 'summarize', 'translate', 'digest_intro'}
EVAL_MARKER = '<!-- follow-rsi-eval -->'
STATE_PATHS = ['data/feed', 'site/feed/status.json', 'badges/feed-updated.json', 'site/badges/feed-updated.json', 'review']
PUBLIC_PATHS = ['data/feed', 'feed/eval/labeled.yaml', 'daily', 'digests', 'README.md', 'README_zh.md',
                'README_en.md', 'stats.json', 'papers', 'site', 'assets', 'badges']


def valid_week(value):
    if not re.fullmatch(r'\d{4}-W\d{2}', value):
        raise ValueError(f'Invalid ISO week: {value}')
    year, week = value.split('-W')
    date.fromisocalendar(int(year), int(week), 1)
    return value


def current_week():
    year, week, _ = datetime.now(timezone.utc).isocalendar()
    return f'{year}-W{week:02d}'


def review_weeks(paths):
    """Ignore excluded/misses reports and arbitrary similarly named files."""
    return sorted({valid_week(match.group(1)) for path in paths if (match := REVIEW_PATH.fullmatch(path))})


def require_ci(root=ROOT):
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise RuntimeError('External writes and branch operations require a GitHub Actions runner')
    workspace = os.environ.get('GITHUB_WORKSPACE')
    if not workspace or Path(workspace).resolve() != Path(root).resolve():
        raise RuntimeError('CI root must be the checked-out GITHUB_WORKSPACE')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', os.environ.get('GITHUB_REPOSITORY', '')):
        raise RuntimeError('GITHUB_REPOSITORY must identify the current repository')


def run(args, root=ROOT, check=True):
    return subprocess.run(args, cwd=root, check=check, capture_output=True, text=True)


def gh(args, root=ROOT):
    require_ci(root)
    return run(['gh', *args], root).stdout.strip()


def default_branch(root):
    return gh(['repo', 'view', os.environ['GITHUB_REPOSITORY'], '--json', 'defaultBranchRef',
               '--jq', '.defaultBranchRef.name'], root)


def configure_model(root=ROOT):
    config = read_yaml(Path(root) / 'feed/model.yaml')
    for key, environment in [('provider', 'LLM_PROVIDER'), ('model', 'LLM_MODEL'), ('base_url', 'LLM_BASE_URL')]:
        if config.get(key) and not os.environ.get(environment):
            os.environ[environment] = config[key]


def commit_paths(root, message, paths, push=True):
    require_ci(root)
    selected = [path for path in paths if (Path(root) / path).exists() or run(['git', 'ls-files', '--', path], root).stdout.strip()]
    if not selected:
        return False
    run(['git', 'config', 'user.name', 'github-actions[bot]'], root)
    run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], root)
    run(['git', 'add', '--', *selected], root)
    result = run(['git', 'diff', '--cached', '--quiet'], root, check=False)
    if result.returncode == 0:
        return False
    if result.returncode != 1:
        raise RuntimeError(result.stderr)
    run(['git', 'commit', '-m', message], root)
    if push:
        run(['git', 'push', 'origin', 'HEAD'], root)
    return True


def switch_review_branch(root, branch, base):
    require_ci(root)
    if run(['git', 'status', '--porcelain', '--untracked-files=no'], root).stdout.strip():
        raise RuntimeError('Branch preparation requires a clean tracked checkout')
    run(['git', 'config', 'user.name', 'github-actions[bot]'], root)
    run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], root)
    run(['git', 'fetch', 'origin', base], root)
    existing = run(['git', 'ls-remote', '--heads', 'origin', branch], root).stdout.strip()
    if existing:
        run(['git', 'fetch', 'origin', branch], root)
        run(['git', 'switch', '-C', branch, 'origin/' + branch], root)
        # Existing owner decisions are merged, never replaced by a force push.
        run(['git', 'merge', '--no-edit', 'origin/' + base], root)
    else:
        run(['git', 'switch', '-c', branch, 'origin/' + base], root)


def upsert_pr(root, branch, base, title, body):
    require_ci(root)
    repository = os.environ['GITHUB_REPOSITORY']
    prs = json.loads(gh(['pr', 'list', '--repo', repository, '--head', branch, '--state', 'open',
                         '--json', 'number,url'], root))
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'body.md'
        path.write_text(body, encoding='utf-8')
        if prs:
            gh(['pr', 'edit', str(prs[0]['number']), '--repo', repository, '--title', title, '--body-file', str(path)], root)
            return prs[0]['url']
        return gh(['pr', 'create', '--repo', repository, '--head', branch, '--base', base,
                   '--title', title, '--body-file', str(path)], root)


def valid_date(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError(f'Invalid review date: {value}')
    date.fromisoformat(value)
    return value


def review_requests(paths):
    requests = []
    for path in sorted(set(paths)):
        if match := DAILY_PATH.fullmatch(path):
            requests.append({'kind': 'daily', 'date': valid_date(match.group(1)), 'path': path})
        elif match := REVIEW_PATH.fullmatch(path):
            requests.append({'kind': 'weekly', 'week': valid_week(match.group(1)), 'path': path})
    return requests


def branch_request(branch):
    if match := DAILY_BRANCH.fullmatch(branch):
        value = valid_date(match.group(1))
        return {'kind': 'daily', 'date': value, 'path': f'review/daily/{value}.yaml'}
    if match := PICKS_BRANCH.fullmatch(branch):
        value = valid_week(match.group(1) + '-W' + match.group(2))
        return {'kind': 'weekly', 'week': value, 'path': f'review/{value}.yaml'}
    return None


def remote_file(root, path, ref):
    repository = os.environ['GITHUB_REPOSITORY']
    payload = json.loads(gh(['api', f'repos/{repository}/contents/{path}?ref={ref}'], root))
    return base64.b64decode(payload['content']).decode('utf-8')


def dispatch_pr_check(root, number, base):
    # workflow_dispatch is one of GitHub's allowed GITHUB_TOKEN event exceptions.
    gh(['workflow', 'run', 'feed-review.yml', '--repo', os.environ['GITHUB_REPOSITORY'], '--ref', base,
        '-f', 'mode=check', '-f', f'pr_number={number}'], root)


def daily_pr_history(root):
    history = json.loads(gh(['pr', 'list', '--repo', os.environ['GITHUB_REPOSITORY'], '--state', 'all',
                            '--limit', '1000', '--json', 'number,headRefName,headRefOid,url,state,createdAt,mergedAt'], root))
    return [pr for pr in history if DAILY_BRANCH.fullmatch(pr['headRefName'])]


def review_stall_days(history, current_date):
    current = date.fromisoformat(valid_date(current_date))
    merged = [date.fromisoformat(pr['mergedAt'][:10]) for pr in history if pr.get('mergedAt')]
    if merged:
        return max(0, (current - max(merged)).days)
    queued = [date.fromisoformat(pr['createdAt'][:10]) for pr in history]
    return max(0, (current - min(queued)).days + 1) if queued else 0


def update_review_stall(root, current_date, backlog, history):
    title = 'Review stalled: Follow RSI'
    repository = os.environ['GITHUB_REPOSITORY']
    issues = json.loads(gh(['issue', 'list', '--repo', repository, '--state', 'open', '--search', title + ' in:title',
                           '--json', 'number,title'], root))
    previous = next((row['number'] for row in issues if row['title'] == title), None)
    days = review_stall_days(history, current_date)
    if days < 3:
        if previous:
            gh(['issue', 'close', str(previous), '--repo', repository], root)
        return {'consecutive_days_without_merge': days, 'backlog': backlog}
    body = (f'No daily owner-review PR has merged for {days} calendar days.\n\n'
            f'Current unpublished review queue: {backlog} items.\n\n'
            'No daily edition or public feed item is published automatically. Decisions remain in the latest daily review PR.\n')
    if backlog > 60:
        body += f'\nThe backlog exceeds 60 items: {backlog} need an owner decision or merge.\n'
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'body.md'
        path.write_text(body, encoding='utf-8')
        if previous:
            gh(['issue', 'edit', str(previous), '--repo', repository, '--body-file', str(path)], root)
        else:
            gh(['issue', 'create', '--repo', repository, '--title', title, '--body-file', str(path)], root)
    return {'consecutive_days_without_merge': days, 'backlog': backlog, 'issue': title}


def queue_daily_pr(root=ROOT, review_date=None):
    from .review import queue_daily_review
    import yaml
    from scripts.common import DataLoader
    require_ci(root)
    review_date = valid_date(review_date or datetime.now(timezone.utc).date().isoformat())
    base, branch = default_branch(root), 'feed/review-' + review_date
    history = daily_pr_history(root)
    previous = sorted([pr for pr in history if pr['state'] == 'OPEN'
                       and DAILY_BRANCH.fullmatch(pr['headRefName']).group(1) < review_date],
                      key=lambda pr: pr['headRefName'])
    carried = []
    for pr in previous:
        old_date = DAILY_BRANCH.fullmatch(pr['headRefName']).group(1)
        source = remote_file(root, f'review/daily/{old_date}.yaml', pr['headRefOid'])
        carried.append(yaml.load(source, Loader=DataLoader))
    switch_review_branch(root, branch, base)
    review = queue_daily_review(root, review_date, carried_reviews=carried)
    commit_paths(root, f'Queue Follow RSI daily owner review {review_date}',
                 [f'review/daily/{review_date}.yaml', f'review/daily/{review_date}.excluded.yaml'], push=False)
    run(['git', 'push', '--set-upstream', 'origin', branch], root)
    rows = [*review['items'], *review['lab_updates']]
    pending = sum(row['decision'] in {'pending', 'defer'} for row in rows)
    body = (f'Daily owner review for Follow RSI {review_date}: {len(review["items"])} papers and {len(review["lab_updates"])} lab updates.\n\n'
            f'{pending} decisions remain pending/deferred. Set decisions to accept, reject, move or defer. Pending blocks merging; defer rolls forward without publishing.\n\n'
            'The queue preserves owner edits from the open reviews below. No decision is published until this PR receives owner approval and is merged.\n\n')
    body += '\n'.join('- ' + pr['url'] for pr in previous) + '\n'
    url = upsert_pr(root, branch, base, f'Review: Follow RSI {review_date}', body)
    # The replacement exists before any previous queue is closed.
    for pr in previous:
        gh(['pr', 'close', str(pr['number']), '--repo', os.environ['GITHUB_REPOSITORY']], root)
    number = int(url.rstrip('/').rsplit('/', 1)[-1])
    dispatch_pr_check(root, number, base)
    if not any(pr['headRefName'] == branch for pr in history):
        history.append({'headRefName': branch, 'state': 'OPEN', 'createdAt': review_date + 'T03:17:00Z', 'mergedAt': None})
    health = update_review_stall(root, review_date, len(rows), history)
    return {'date': review_date, 'url': url, 'rolled_prs': [pr['number'] for pr in previous], 'health': health}


def queue_picks_pr(root=ROOT, week=None):
    from .review import queue_weekly_picks
    require_ci(root)
    week = valid_week(week or current_week())
    base, branch = default_branch(root), 'feed/picks-' + week.lower()
    switch_review_branch(root, branch, base)
    queue_weekly_picks(root, week)
    commit_paths(root, f'Queue Follow RSI weekly picks {week}', [f'review/{week}.yaml'], push=False)
    run(['git', 'push', '--set-upstream', 'origin', branch], root)
    misses_path = Path(root) / 'review' / f'{week}.misses.yaml'
    recall = read_yaml(misses_path).get('summary', '') if misses_path.exists() else ''
    body = (f'Weekly picks for Follow RSI {week}. Choose up to three papers already accepted in this week\'s daily reviews.\n\n'
            'Picks, reasons and optional editorial notes are written by the owner. An empty picks list produces a weekly summary without a picks section.\n\n' + recall + '\n')
    url = upsert_pr(root, branch, base, f'Weekly picks: Follow RSI {week}', body)
    dispatch_pr_check(root, int(url.rstrip('/').rsplit('/', 1)[-1]), base)
    return {'week': week, 'url': url}


def queue_pr(root=ROOT, week=None):
    return queue_picks_pr(root, week)


def validate_request(root, request):
    from .review import validate_daily_review, validate_weekly_picks
    if not (Path(root) / request['path']).exists():
        raise ValueError('Review deletion is not a publishable owner decision')
    if request['kind'] == 'daily':
        return validate_daily_review(root, request['date'])
    return validate_weekly_picks(root, request['week'])


def changed_review_weeks(root, base, head):
    paths = run(['git', 'diff', '--name-only', base, head, '--', 'review'], root).stdout.splitlines()
    return review_weeks(paths)


def check_review_diff(root, base, head):
    paths = run(['git', 'diff', '--name-only', base, head, '--', 'review'], root).stdout.splitlines()
    requests = review_requests(paths)
    for request in requests:
        validate_request(root, request)
    return requests


def merged_review_requests(event, paths, repository):
    pr = event.get('pull_request', {})
    if not pr.get('merged') or pr.get('head', {}).get('repo', {}).get('full_name') != repository:
        return []
    expected = branch_request(pr.get('head', {}).get('ref', ''))
    if expected is None:
        return []
    if review_requests(paths) != [expected]:
        raise ValueError('Merged review PR must modify exactly the date/week identified by its branch')
    return [expected]


def merged_review_weeks(event, paths, repository):
    return [request['week'] for request in merged_review_requests(event, paths, repository) if request['kind'] == 'weekly']


def human_owner_review(pr, reviews, repository):
    owner = repository.split('/')[0].casefold()
    merger = pr.get('merged_by') or {}
    if merger.get('type') == 'User' and merger.get('login', '').casefold() == owner:
        return merger['login']
    owner_reviews = [review for review in reviews if review['user'].get('type') == 'User'
                     and review['user']['login'].casefold() == owner
                     and review['state'] in {'APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'}]
    if owner_reviews and owner_reviews[-1]['state'] == 'APPROVED' and owner_reviews[-1]['commit_id'] == pr['head']['sha']:
        return owner_reviews[-1]['user']['login']
    raise ValueError('Publishing requires a human repository-owner merge or owner approval of the exact PR revision')


def verify_merged_review(root, pr, paths):
    repository = os.environ['GITHUB_REPOSITORY']
    requests = merged_review_requests({'pull_request': pr}, paths, repository)
    if not requests:
        raise ValueError('PR is not a merged daily review or weekly-picks PR from this repository')
    if pr['base']['ref'] != default_branch(root):
        raise ValueError('Review must have merged into the default branch')
    pages = json.loads(gh(['api', '--paginate', '--slurp', f'repos/{repository}/pulls/{pr["number"]}/reviews?per_page=100'], root))
    owner = human_owner_review(pr, [review for page in pages for review in page], repository)
    for request in requests:
        approved = run(['git', 'show', f'{pr["merge_commit_sha"]}:{request["path"]}'], root).stdout
        if (Path(root) / request['path']).read_text(encoding='utf-8') != approved:
            raise ValueError('Current review content differs from the owner-approved merge; review the change in a new PR')
    return requests, owner


def set_pr_status(root, sha, state, context):
    repository = os.environ['GITHUB_REPOSITORY']
    url = f'{os.environ.get("GITHUB_SERVER_URL", "https://github.com")}/{repository}/actions/runs/{os.environ["GITHUB_RUN_ID"]}'
    gh(['api', '--method', 'POST', f'repos/{repository}/statuses/{sha}', '-f', 'state=' + state,
        '-f', 'context=' + context, '-f', 'target_url=' + url,
        '-f', 'description=Validated with trusted default-branch code'], root)


def check_pr(root, number):
    require_ci(root)
    repository = os.environ['GITHUB_REPOSITORY']
    pr = json.loads(gh(['api', f'repos/{repository}/pulls/{number}'], root))
    if pr['head']['repo']['full_name'] != repository:
        raise ValueError('Automated review checks only stage data from same-repository review PRs')
    expected = branch_request(pr['head']['ref'])
    candidate = pr['head']['ref'].startswith('feed/candidates-')
    if expected is None and not candidate:
        raise ValueError('Unsupported automated review branch')
    context = 'Follow RSI candidate integrity' if candidate else 'Follow RSI owner decisions'
    set_pr_status(root, pr['head']['sha'], 'pending', context)
    success = False
    try:
        if candidate:
            path = Path(root) / 'data/papers.yaml'
            path.write_text(remote_file(root, 'data/papers.yaml', pr['head']['sha']), encoding='utf-8')
            from scripts.validate import validate
            validate(root)
        else:
            paths = gh(['api', '--paginate', f'repos/{repository}/pulls/{number}/files', '--jq', '.[].filename'], root).splitlines()
            if review_requests(paths) != [expected]:
                raise ValueError('PR must contain exactly its dated owner review')
            path = Path(root) / expected['path']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(remote_file(root, expected['path'], pr['head']['sha']), encoding='utf-8')
            validate_request(root, expected)
        success = True
    finally:
        set_pr_status(root, pr['head']['sha'], 'success' if success else 'failure', context)
    return {'pr_number': number, 'status': 'success', 'context': context}


def candidate_pr(root, proposal, base):
    if not proposal['count']:
        return {'status': 'empty', 'count': 0}
    repository, branch = os.environ['GITHUB_REPOSITORY'], proposal['branch']
    prs = json.loads(gh(['pr', 'list', '--repo', repository, '--head', branch, '--state', 'open', '--json', 'url'], root))
    if prs:
        # Rerunning publication must not overwrite edits on an owner's open candidate PR.
        return {'status': 'already_open', 'url': prs[0]['url'], 'count': proposal['count']}
    if run(['git', 'status', '--porcelain', '--untracked-files=no'], root).stdout.strip():
        raise RuntimeError('Candidate proposal requires a clean committed public checkout')
    run(['git', 'switch', '-C', branch, 'origin/' + base], root)
    shutil.copyfile(proposal['papers_path'], Path(root) / 'data/papers.yaml')
    run(['python', 'scripts/build.py'], root)
    run(['python', 'scripts/render_cards.py', '--ids', *proposal['candidate_ids']], root)
    commit_paths(root, proposal['title'], ['data/papers.yaml', 'README.md', 'README_zh.md', 'README_en.md',
                                         'stats.json', 'papers', 'site', 'assets', 'badges'], push=False)
    # A previous merged proposal can leave a remote branch. No force push is used.
    run(['git', 'push', '--set-upstream', 'origin', branch], root)
    body = Path(proposal['body_path']).read_text(encoding='utf-8')
    url = upsert_pr(root, branch, base, proposal['title'], body)
    run(['git', 'switch', base], root)
    dispatch_pr_check(root, int(url.rstrip('/').rsplit('/', 1)[-1]), base)
    return {'status': 'opened', 'url': url, 'count': proposal['count']}


def publication_pr(root, review_date=None, week=None, pr_number=None):
    """Manual reruns resolve the same merged PR and never bypass the owner gate."""
    repository = os.environ['GITHUB_REPOSITORY']
    if review_date or week:
        branch = 'feed/review-' + valid_date(review_date) if review_date else 'feed/picks-' + valid_week(week).lower()
        merged = json.loads(gh(['pr', 'list', '--repo', repository, '--head', branch, '--state', 'merged',
                                '--limit', '100', '--json', 'number,mergedAt'], root))
        if not merged:
            raise ValueError('Manual publishing requires an owner-approved, merged review PR')
        pr_number = max(merged, key=lambda pr: pr['mergedAt'])['number']
    if pr_number is None:
        event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text(encoding='utf-8'))
        pr_number = event.get('pull_request', {}).get('number')
        if pr_number is None:
            raise ValueError('Select --date, --week or --pr-number for a manual publication')
    pr = json.loads(gh(['api', f'repos/{repository}/pulls/{pr_number}'], root))
    paths = gh(['api', '--paginate', f'repos/{repository}/pulls/{pr_number}/files',
                '--jq', '.[].filename'], root).splitlines()
    requests, owner = verify_merged_review(root, pr, paths)
    if review_date and requests[0].get('date') != review_date or week and requests[0].get('week') != week:
        raise ValueError('Merged PR does not match the requested edition')
    return pr, requests, owner


def dispatch_pages(root, base):
    gh(['workflow', 'run', 'pages.yml', '--repo', os.environ['GITHUB_REPOSITORY'], '--ref', base], root)


def weekly_release(root, week, commit):
    """One tag per owner-approved weekly edition; retries update the same release."""
    require_ci(root)
    week = valid_week(week)
    repository, tag = os.environ['GITHUB_REPOSITORY'], 'follow-rsi-' + week
    notes = Path(root) / 'digests' / f'{week}.md'
    card = Path(root) / 'site' / 'cards' / f'digest-{week}.png'
    if not notes.is_file() or not card.is_file():
        raise ValueError('A weekly Release requires the rendered digest and share image')
    result = run(['gh', 'api', f'repos/{repository}/releases/tags/{tag}'], root, check=False)
    title = f'Follow RSI · {week}'
    if result.returncode:
        if 'HTTP 404' not in result.stderr:
            raise RuntimeError(result.stderr.strip() or 'GitHub Release lookup failed')
        url = gh(['release', 'create', tag, '--repo', repository, '--target', commit,
                  '--title', title, '--notes-file', str(notes), '--latest=false', str(card)], root)
        return {'week': week, 'tag': tag, 'url': url, 'status': 'created'}
    release = json.loads(result.stdout)
    gh(['release', 'edit', tag, '--repo', repository, '--title', title, '--notes-file', str(notes)], root)
    gh(['release', 'upload', tag, str(card), '--repo', repository, '--clobber'], root)
    return {'week': week, 'tag': tag, 'url': release['html_url'], 'status': 'updated'}


def publish(root=ROOT, review_date=None, week=None, pr_number=None):
    from .review import apply_daily_review
    from .digest import publish_day, publish_week
    from .promote import promote_candidates
    from .llm import FeedLLM
    from .storage import write_json
    require_ci(root)
    pr, requests, owner = publication_pr(root, review_date, week, pr_number)
    request = requests[0]
    validate_request(root, request)
    configure_model(root)
    client = FeedLLM.from_env(root) if os.environ.get('LLM_API_KEY') else None
    provenance = {'github_pr': pr['number'], 'owner_login': owner, 'merge_commit': pr['merge_commit_sha']}
    edition = request.get('date') or request['week']
    write_json(Path(root) / 'data/feed/review-provenance' / f'{edition}.json', {**request, **provenance})
    if request['kind'] == 'daily':
        apply_daily_review(root, request['date'], provenance=provenance)
        reports = [publish_day(root, request['date'])]
        proposal = promote_candidates(root, date=request['date'])
    else:
        reports = [publish_week(root, request['week'], client=client, render_card=True)]
    run(['python', 'scripts/build.py'], root)
    base = default_branch(root)
    commit_paths(root, 'Publish owner-reviewed Follow RSI ' + edition, PUBLIC_PATHS)
    commit = run(['git', 'rev-parse', 'HEAD'], root).stdout.strip()
    dispatch_pages(root, base)
    if request['kind'] == 'daily':
        run(['git', 'fetch', 'origin', base], root)
        reports.append(candidate_pr(root, proposal, base))
    else:
        reports.append(weekly_release(root, request['week'], commit))
    return reports


def safe_prompt_template(source):
    """PR prompt files are data; allow interpolation, never executable Jinja."""
    tree = Environment().parse(source)
    allowed = (nodes.Template, nodes.Output, nodes.TemplateData, nodes.Name)
    if any(not isinstance(node, allowed) for node in [tree, *tree.find_all(nodes.Node)]):
        raise ValueError('Evaluation prompts may interpolate named variables only; Jinja code is not permitted')


def stage_eval_inputs(root, number, head_sha):
    repository = os.environ['GITHUB_REPOSITORY']
    paths = gh(['api', '--paginate', f'repos/{repository}/pulls/{number}/files', '--jq', '.[].filename'], root).splitlines()
    config = read_yaml(Path(root) / 'feed/model.yaml')
    for path in paths:
        name = Path(path).stem
        if path == f'feed/prompts/{name}.md' and name in PROMPT_NAMES:
            payload = json.loads(gh(['api', f'repos/{repository}/contents/{path}?ref={head_sha}'], root))
            source = base64.b64decode(payload['content'], validate=False).decode('utf-8')
            safe_prompt_template(source)
            (Path(root) / path).write_text(source, encoding='utf-8')
        elif path == 'feed/model.yaml':
            import yaml
            payload = json.loads(gh(['api', f'repos/{repository}/contents/{path}?ref={head_sha}'], root))
            candidate = yaml.safe_load(base64.b64decode(payload['content']).decode('utf-8'))
            if candidate['provider'] != config['provider'] or candidate.get('base_url') != config.get('base_url'):
                raise ValueError('A provider/base URL change requires trusted default-branch configuration before evaluation')
            if not isinstance(candidate['model'], str) or not candidate['model'].strip():
                raise ValueError('Model name must be a nonempty string')
            os.environ['LLM_MODEL'] = candidate['model']


def comment_eval(root, number, report):
    repository = os.environ['GITHUB_REPOSITORY']
    comments = json.loads(gh(['api', f'repos/{repository}/issues/{number}/comments?per_page=100'], root))
    previous = next((row['id'] for row in comments if row['body'].startswith(EVAL_MARKER)
                     and row['user']['login'] == 'github-actions[bot]'), None)
    body = EVAL_MARKER + '\n' + report
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'comment.md'
        path.write_text(body, encoding='utf-8')
        if previous:
            payload = Path(directory) / 'comment.json'
            payload.write_text(json.dumps({'body': body}), encoding='utf-8')
            gh(['api', '--method', 'PATCH', f'repos/{repository}/issues/comments/{previous}', '--input', str(payload)], root)
        else:
            gh(['pr', 'comment', str(number), '--repo', repository, '--body-file', str(path)], root)


def evaluate(root=ROOT):
    from .eval import cache_metadata, run_evaluation
    require_ci(root)
    configure_model(root)
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    pr = event.get('pull_request')
    if pr and pr['head']['repo']['full_name'] == os.environ['GITHUB_REPOSITORY'] and os.environ.get('LLM_API_KEY'):
        stage_eval_inputs(root, pr['number'], pr['head']['sha'])
    if os.environ.get('LLM_API_KEY'):
        cache_metadata(root)
    report = run_evaluation(root)
    markdown = (Path(root) / 'feed/eval/report.md').read_text(encoding='utf-8')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a', encoding='utf-8') as handle:
            handle.write(markdown + '\n')
    if pr:
        comment_eval(root, pr['number'], markdown)
    if report['status'] != 'skipped' and not report['thresholds_passed']:
        raise SystemExit(1)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    commands = parser.add_subparsers(dest='command', required=True)
    commit = commands.add_parser('commit')
    commit.add_argument('--message', required=True)
    commit.add_argument('--paths', nargs='+', default=STATE_PATHS)
    commit.add_argument('--deploy-pages', action='store_true')
    queue = commands.add_parser('queue-pr')
    queue.add_argument('--week')
    daily = commands.add_parser('queue-daily-pr')
    daily.add_argument('--date')
    picks = commands.add_parser('queue-picks-pr')
    picks.add_argument('--week')
    pr_check = commands.add_parser('check-pr')
    pr_check.add_argument('--pr-number', type=int, required=True)
    check = commands.add_parser('check-review-diff')
    check.add_argument('--base', required=True)
    check.add_argument('--head', required=True)
    publication = commands.add_parser('publish')
    selector = publication.add_mutually_exclusive_group()
    selector.add_argument('--date')
    selector.add_argument('--week')
    selector.add_argument('--pr-number', type=int)
    commands.add_parser('evaluate')
    args = parser.parse_args()
    if args.command == 'commit':
        result = commit_paths(args.root, args.message, args.paths)
        if result and args.deploy_pages:
            dispatch_pages(args.root, default_branch(args.root))
    elif args.command == 'queue-pr':
        result = queue_pr(args.root, args.week)
    elif args.command == 'queue-daily-pr':
        result = queue_daily_pr(args.root, args.date)
    elif args.command == 'queue-picks-pr':
        result = queue_picks_pr(args.root, args.week)
    elif args.command == 'check-pr':
        result = check_pr(args.root, args.pr_number)
    elif args.command == 'check-review-diff':
        result = check_review_diff(args.root, args.base, args.head)
    elif args.command == 'publish':
        result = publish(args.root, args.date, args.week, args.pr_number)
    else:
        result = evaluate(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
