import base64
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from scripts.common import read_yaml
from scripts.feed import ci

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY = 'owner/follow-rsi'


@pytest.fixture
def ci_environment(tmp_path, monkeypatch):
    monkeypatch.setenv('GITHUB_ACTIONS', 'true')
    monkeypatch.setenv('GITHUB_REPOSITORY', REPOSITORY)
    monkeypatch.setenv('GITHUB_WORKSPACE', str(tmp_path))
    monkeypatch.setenv('GITHUB_RUN_ID', '123')
    return tmp_path


def merged_pr(branch='feed/review-2026-10-27'):
    return {'number': 8, 'merged': True, 'merge_commit_sha': 'merge-sha',
            'merged_by': {'type': 'User', 'login': 'owner'}, 'base': {'ref': 'main'},
            'head': {'ref': branch, 'sha': 'owner-head', 'repo': {'full_name': REPOSITORY}}}


def test_external_writes_fail_before_subprocess_outside_ci(tmp_path, monkeypatch):
    monkeypatch.delenv('GITHUB_ACTIONS', raising=False)
    command = Mock()
    monkeypatch.setattr(ci, 'run', command)
    with pytest.raises(RuntimeError, match='GitHub Actions'):
        ci.commit_paths(tmp_path, 'message', ['data/feed'])
    command.assert_not_called()


def test_ci_guard_requires_current_checkout(ci_environment):
    ci.require_ci(ci_environment)
    with pytest.raises(RuntimeError, match='GITHUB_WORKSPACE'):
        ci.require_ci(ci_environment / 'another-checkout')


def test_only_exact_valid_review_files_are_decisions():
    paths = ['review/2026-W44.yaml', 'review/2026-W44.excluded.yaml', 'review/2026-W44.misses.yaml',
             'docs/review/2026-W44.yaml', 'review/../review/2026-W45.yaml', 'review/2026-W44.yaml',
             'review/daily/2026-10-27.yaml', 'review/daily/2026-10-27.excluded.yaml']
    assert ci.review_weeks(paths) == ['2026-W44']
    assert ci.review_requests(paths) == [
        {'kind': 'weekly', 'week': '2026-W44', 'path': 'review/2026-W44.yaml'},
        {'kind': 'daily', 'date': '2026-10-27', 'path': 'review/daily/2026-10-27.yaml'}]
    with pytest.raises(ValueError):
        ci.review_requests(['review/2026-W54.yaml'])
    with pytest.raises(ValueError):
        ci.review_requests(['review/daily/2026-02-30.yaml'])


@pytest.mark.parametrize('branch,path', [('feed/review-2026-10-27', 'review/daily/2026-10-27.yaml'),
                                        ('feed/picks-2026-w44', 'review/2026-W44.yaml')])
def test_merged_review_requires_origin_branch_and_exact_edition(branch, path):
    event = {'pull_request': merged_pr(branch)}
    assert ci.merged_review_requests(event, [path], REPOSITORY) == ci.review_requests([path])
    assert ci.merged_review_requests(event, [path], 'other/repo') == []
    with pytest.raises(ValueError, match='exactly'):
        ci.merged_review_requests(event, ['review/2026-W45.yaml'], REPOSITORY)
    with pytest.raises(ValueError, match='exactly'):
        ci.merged_review_requests(event, [path, 'review/2026-W45.yaml'], REPOSITORY)
    event['pull_request']['merged'] = False
    assert ci.merged_review_requests(event, [path], REPOSITORY) == []
    assert ci.branch_request('feed/review-2026-w44') is None


def test_pending_review_failure_propagates_through_ci(tmp_path, monkeypatch):
    from scripts.feed import review
    path = tmp_path / 'review/daily/2026-10-27.yaml'
    path.parent.mkdir(parents=True)
    path.write_text('pending owner review')
    monkeypatch.setattr(ci, 'run', Mock(return_value=SimpleNamespace(stdout='review/daily/2026-10-27.yaml\n')))
    validate = Mock(side_effect=ValueError('pending decision blocks publication'))
    monkeypatch.setattr(review, 'validate_daily_review', validate)
    with pytest.raises(ValueError, match='pending'):
        ci.check_review_diff(tmp_path, 'base', 'head')
    validate.assert_called_once_with(tmp_path, '2026-10-27')


def test_owner_merge_or_exact_head_approval_is_required():
    pr = merged_pr()
    pr['merged_by']['login'] = 'OwNeR'
    assert ci.human_owner_review(pr, [], REPOSITORY) == 'OwNeR'
    pr['merged_by'] = {'type': 'Bot', 'login': 'owner'}
    approval = {'state': 'APPROVED', 'commit_id': 'owner-head', 'user': {'type': 'User', 'login': 'owner'}}
    assert ci.human_owner_review(pr, [approval], REPOSITORY) == 'owner'
    for reviews in [[], [{**approval, 'commit_id': 'stale-head'}],
                    [{**approval, 'user': {'type': 'Bot', 'login': 'owner'}}],
                    [approval, {**approval, 'state': 'CHANGES_REQUESTED'}],
                    [approval, {**approval, 'state': 'DISMISSED'}]]:
        with pytest.raises(ValueError, match='human repository-owner'):
            ci.human_owner_review(pr, reviews, REPOSITORY)


def test_merged_yaml_must_match_owner_approved_commit(ci_environment, monkeypatch):
    path = ci_environment / 'review/daily/2026-10-27.yaml'
    path.parent.mkdir(parents=True)
    path.write_text('approved-content')
    monkeypatch.setattr(ci, 'default_branch', lambda root: 'main')
    api = Mock(return_value='[[]]')
    monkeypatch.setattr(ci, 'gh', api)
    monkeypatch.setattr(ci, 'run', Mock(return_value=SimpleNamespace(stdout='approved-content')))
    requests, owner = ci.verify_merged_review(ci_environment, merged_pr(), ['review/daily/2026-10-27.yaml'])
    assert owner == 'owner' and requests[0]['date'] == '2026-10-27'
    assert '--paginate' in api.call_args.args[0] and '--slurp' in api.call_args.args[0]
    path.write_text('modified-after-owner-merge')
    with pytest.raises(ValueError, match='differs'):
        ci.verify_merged_review(ci_environment, merged_pr(), ['review/daily/2026-10-27.yaml'])


def test_manual_publication_requires_a_merged_owner_review(ci_environment, monkeypatch):
    monkeypatch.setattr(ci, 'gh', Mock(return_value='[]'))
    with pytest.raises(ValueError, match='merged review PR'):
        ci.publication_pr(ci_environment, review_date='2026-10-27')
    pr = merged_pr()
    pr['merged_by'] = {'type': 'Bot', 'login': 'github-actions[bot]'}
    replies = [json.dumps([{'number': 8, 'mergedAt': '2026-10-27T12:00:00Z'}]),
               json.dumps(pr), 'review/daily/2026-10-27.yaml', '[[]]']
    monkeypatch.setattr(ci, 'default_branch', lambda root: 'main')
    monkeypatch.setattr(ci, 'gh', Mock(side_effect=replies))
    with pytest.raises(ValueError, match='human repository-owner'):
        ci.publication_pr(ci_environment, review_date='2026-10-27')


def test_rollover_loads_owner_edits_from_remote_head_before_closing_pr(ci_environment, monkeypatch):
    from scripts.feed import review
    events = []
    history = [{'number': 7, 'headRefName': 'feed/review-2026-10-26', 'headRefOid': 'edited-owner-head',
                'url': 'https://github.com/owner/follow-rsi/pull/7', 'state': 'OPEN',
                'createdAt': '2026-10-26T03:17:00Z', 'mergedAt': None}]
    monkeypatch.setattr(ci, 'default_branch', lambda root: 'main')
    monkeypatch.setattr(ci, 'daily_pr_history', lambda root: history)
    remote = Mock(return_value='date: "2026-10-26"\nitems: [{id: paper, decision: accept}]\nlab_updates: []\n')
    monkeypatch.setattr(ci, 'remote_file', remote)
    monkeypatch.setattr(ci, 'switch_review_branch', Mock())
    queue = Mock(return_value={'items': [{'decision': 'accept'}], 'lab_updates': []})
    monkeypatch.setattr(review, 'queue_daily_review', queue)
    monkeypatch.setattr(ci, 'commit_paths', Mock(return_value=True))
    monkeypatch.setattr(ci, 'run', Mock(return_value=SimpleNamespace(stdout='')))
    monkeypatch.setattr(ci, 'upsert_pr', lambda *args: events.append('created') or 'https://github.com/owner/follow-rsi/pull/8')
    monkeypatch.setattr(ci, 'gh', lambda args, root: events.append(args) or '')
    dispatch = Mock()
    monkeypatch.setattr(ci, 'dispatch_pr_check', dispatch)
    monkeypatch.setattr(ci, 'update_review_stall', Mock(return_value={}))
    result = ci.queue_daily_pr(ci_environment, '2026-10-27')
    remote.assert_called_once_with(ci_environment, 'review/daily/2026-10-26.yaml', 'edited-owner-head')
    assert queue.call_args.kwargs['carried_reviews'][0]['items'][0]['decision'] == 'accept'
    assert events[0] == 'created' and events[1][:3] == ['pr', 'close', '7']
    dispatch.assert_called_once_with(ci_environment, 8, 'main')
    assert result['rolled_prs'] == [7]
    events.clear()
    monkeypatch.setattr(ci, 'upsert_pr', Mock(side_effect=RuntimeError('create failed')))
    with pytest.raises(RuntimeError, match='create failed'):
        ci.queue_daily_pr(ci_environment, '2026-10-27')
    assert events == []


def test_review_stall_counts_calendar_days_and_reuses_one_issue(ci_environment, monkeypatch):
    history = [{'createdAt': '2026-10-25T03:17:00Z', 'mergedAt': None}]
    assert ci.review_stall_days(history, '2026-10-26') == 2
    assert ci.review_stall_days(history, '2026-10-27') == 3
    events, opened = [], []
    def api(args, root):
        if args[:2] == ['issue', 'list']:
            return json.dumps(opened)
        body = Path(args[args.index('--body-file') + 1]).read_text() if '--body-file' in args else ''
        events.append((args, body))
        if args[:2] == ['issue', 'create']:
            opened.append({'number': 10, 'title': 'Review stalled: Follow RSI'})
        return ''
    monkeypatch.setattr(ci, 'gh', api)
    ci.update_review_stall(ci_environment, '2026-10-26', 61, history)
    assert events == []
    ci.update_review_stall(ci_environment, '2026-10-27', 61, history)
    ci.update_review_stall(ci_environment, '2026-10-28', 62, history)
    assert [event[0][:2] for event in events] == [['issue', 'create'], ['issue', 'edit']]
    assert 'exceeds 60 items: 61' in events[0][1]
    history[0]['mergedAt'] = '2026-10-28T12:00:00Z'
    ci.update_review_stall(ci_environment, '2026-10-28', 0, history)
    assert events[-1][0][:3] == ['issue', 'close', '10']


@pytest.mark.parametrize('invalid', [False, True])
def test_pr_check_stages_only_yaml_and_reports_status(ci_environment, monkeypatch, invalid):
    def api(args, root):
        if args[-1].endswith('/pulls/8'):
            return json.dumps(merged_pr())
        return 'review/daily/2026-10-27.yaml\nscripts/feed/review.py'
    monkeypatch.setattr(ci, 'gh', api)
    remote = Mock(return_value='owner review yaml')
    monkeypatch.setattr(ci, 'remote_file', remote)
    statuses = Mock()
    monkeypatch.setattr(ci, 'set_pr_status', statuses)
    validate = Mock(side_effect=ValueError('pending') if invalid else None)
    monkeypatch.setattr(ci, 'validate_request', validate)
    command = Mock()
    monkeypatch.setattr(ci, 'run', command)
    if invalid:
        with pytest.raises(ValueError, match='pending'):
            ci.check_pr(ci_environment, 8)
    else:
        assert ci.check_pr(ci_environment, 8)['status'] == 'success'
    assert [call.args[2] for call in statuses.call_args_list] == ['pending', 'failure' if invalid else 'success']
    remote.assert_called_once_with(ci_environment, 'review/daily/2026-10-27.yaml', 'owner-head')
    command.assert_not_called()
    assert not (ci_environment / 'scripts/feed/review.py').exists()


def test_candidate_creation_dispatches_integrity_check_and_keeps_open_edits(ci_environment, monkeypatch):
    (ci_environment / 'data').mkdir()
    papers = ci_environment / 'proposal.yaml'
    papers.write_text('papers: []')
    body = ci_environment / 'proposal.md'
    body.write_text('Candidate proposal')
    proposal = {'count': 1, 'branch': 'feed/candidates-2026-10-27', 'papers_path': papers,
                'body_path': body, 'candidate_ids': ['paper'], 'title': 'Add one candidate'}
    monkeypatch.setattr(ci, 'gh', Mock(return_value='[]'))
    command = Mock(return_value=SimpleNamespace(stdout=''))
    monkeypatch.setattr(ci, 'run', command)
    monkeypatch.setattr(ci, 'commit_paths', Mock())
    monkeypatch.setattr(ci, 'upsert_pr', Mock(return_value='https://github.com/owner/follow-rsi/pull/9'))
    dispatch = Mock()
    monkeypatch.setattr(ci, 'dispatch_pr_check', dispatch)
    assert ci.candidate_pr(ci_environment, proposal, 'main')['status'] == 'opened'
    dispatch.assert_called_once_with(ci_environment, 9, 'main')
    command.reset_mock()
    monkeypatch.setattr(ci, 'gh', Mock(return_value='[{"url":"existing-owner-edited-pr"}]'))
    assert ci.candidate_pr(ci_environment, proposal, 'main')['status'] == 'already_open'
    command.assert_not_called()


def test_bot_pr_dispatch_uses_supported_workflow_exception(ci_environment, monkeypatch):
    api = Mock()
    monkeypatch.setattr(ci, 'gh', api)
    ci.dispatch_pr_check(ci_environment, 9, 'main')
    args = api.call_args.args[0]
    assert args[:3] == ['workflow', 'run', 'feed-review.yml']
    assert 'mode=check' in args and 'pr_number=9' in args


@pytest.mark.parametrize('changed', [False, True])
def test_health_commit_deploys_pages_only_when_state_changed(ci_environment, monkeypatch, changed):
    import sys
    monkeypatch.setattr(sys, 'argv', ['ci', '--root', str(ci_environment), 'commit', '--message', 'Health', '--deploy-pages'])
    monkeypatch.setattr(ci, 'commit_paths', Mock(return_value=changed))
    monkeypatch.setattr(ci, 'default_branch', Mock(return_value='main'))
    deploy = Mock()
    monkeypatch.setattr(ci, 'dispatch_pages', deploy)
    ci.main()
    if changed:
        deploy.assert_called_once_with(ci_environment, 'main')
    else:
        deploy.assert_not_called()


def test_weekly_release_reuses_tag_and_propagates_lookup_failure(ci_environment, monkeypatch):
    notes = ci_environment / 'digests/2026-W44.md'
    card = ci_environment / 'site/cards/digest-2026-W44.png'
    notes.parent.mkdir(parents=True)
    card.parent.mkdir(parents=True)
    notes.write_text('Owner-approved weekly digest')
    card.write_bytes(b'png-test')
    missing = SimpleNamespace(returncode=1, stdout='', stderr='gh: Not Found (HTTP 404)')
    existing = SimpleNamespace(returncode=0, stdout='{"html_url":"https://github.com/owner/follow-rsi/releases/tag/follow-rsi-2026-W44"}', stderr='')
    denied = SimpleNamespace(returncode=1, stdout='', stderr='gh: Forbidden (HTTP 403)')
    monkeypatch.setattr(ci, 'run', Mock(side_effect=[missing, existing, denied]))
    api = Mock(return_value='release-url')
    monkeypatch.setattr(ci, 'gh', api)
    assert ci.weekly_release(ci_environment, '2026-W44', 'published-sha')['status'] == 'created'
    assert ci.weekly_release(ci_environment, '2026-W44', 'published-sha')['status'] == 'updated'
    calls = [call.args[0] for call in api.call_args_list]
    assert [call[:3] for call in calls] == [
        ['release', 'create', 'follow-rsi-2026-W44'], ['release', 'edit', 'follow-rsi-2026-W44'],
        ['release', 'upload', 'follow-rsi-2026-W44']]
    assert '--notes-file' in calls[0] and '--target' in calls[0] and '--clobber' in calls[2]
    with pytest.raises(RuntimeError, match='403'):
        ci.weekly_release(ci_environment, '2026-W44', 'published-sha')
    assert api.call_count == 3


@pytest.mark.parametrize('kind', ['daily', 'weekly'])
def test_daily_and_weekly_publications_have_distinct_outputs(ci_environment, monkeypatch, kind):
    from scripts.feed import review, digest, promote
    selector = {'date': '2026-10-27'} if kind == 'daily' else {'week': '2026-W44'}
    path = 'review/daily/2026-10-27.yaml' if kind == 'daily' else 'review/2026-W44.yaml'
    request = {'kind': kind, **selector, 'path': path}
    monkeypatch.setattr(ci, 'publication_pr', Mock(return_value=(merged_pr(), [request], 'owner')))
    validate = Mock()
    monkeypatch.setattr(ci, 'validate_request', validate)
    monkeypatch.setattr(ci, 'configure_model', Mock())
    monkeypatch.delenv('LLM_API_KEY', raising=False)
    apply = Mock()
    monkeypatch.setattr(review, 'apply_daily_review', apply)
    daily, weekly = Mock(return_value={'daily': True}), Mock(return_value={'weekly': True})
    monkeypatch.setattr(digest, 'publish_day', daily)
    monkeypatch.setattr(digest, 'publish_week', weekly)
    promotion = Mock(return_value={'count': 0})
    monkeypatch.setattr(promote, 'promote_candidates', promotion)
    candidate = Mock(return_value={'candidate': True})
    monkeypatch.setattr(ci, 'candidate_pr', candidate)
    release = Mock(return_value={'release': True})
    monkeypatch.setattr(ci, 'weekly_release', release)
    monkeypatch.setattr(ci, 'default_branch', lambda root: 'main')
    events = []
    monkeypatch.setattr(ci, 'commit_paths', lambda *args: events.append('commit') or True)
    monkeypatch.setattr(ci, 'dispatch_pages', lambda *args: events.append('pages'))
    monkeypatch.setattr(ci, 'run', Mock(return_value=SimpleNamespace(stdout='published-sha')))
    ci.publish(ci_environment, pr_number=8)
    assert events == ['commit', 'pages']
    receipt = read_yaml(ci_environment / 'data/feed/review-provenance' / f'{next(iter(selector.values()))}.json')
    assert receipt['owner_login'] == 'owner' and receipt['github_pr'] == 8
    if kind == 'daily':
        daily.assert_called_once_with(ci_environment, '2026-10-27')
        apply.assert_called_once_with(ci_environment, '2026-10-27', provenance={
            'github_pr': 8, 'owner_login': 'owner', 'merge_commit': 'merge-sha'})
        promotion.assert_called_once_with(ci_environment, date='2026-10-27')
        candidate.assert_called_once()
        weekly.assert_not_called()
        release.assert_not_called()
    else:
        weekly.assert_called_once_with(ci_environment, '2026-W44', client=None, render_card=True)
        release.assert_called_once_with(ci_environment, '2026-W44', 'published-sha')
        apply.assert_not_called()
        daily.assert_not_called()
        promotion.assert_not_called()
        candidate.assert_not_called()
    validate.side_effect = ValueError('invalid decision')
    events.clear()
    with pytest.raises(ValueError, match='invalid decision'):
        ci.publish(ci_environment, pr_number=8)
    assert events == []


def test_pr_prompt_inputs_allow_variables_but_no_jinja_execution():
    ci.safe_prompt_template('Title: {{ title }}\nAbstract: {{ abstract }}\n{"answer": "text"}')
    for source in ['{{ cycler.__init__.__globals__ }}', '{{ range(10) }}', '{% include "secrets" %}',
                   '{% for x in authors %}{{ x }}{% endfor %}']:
        with pytest.raises(ValueError, match='Jinja'):
            ci.safe_prompt_template(source)
    for prompt in (ROOT / 'feed/prompts').glob('*.md'):
        ci.safe_prompt_template(prompt.read_text())


def test_pr_model_cannot_redirect_api_key(tmp_path, monkeypatch):
    (tmp_path / 'feed').mkdir()
    (tmp_path / 'feed/model.yaml').write_text('provider: deepseek\nmodel: deepseek-flash\nbase_url: https://api.deepseek.com/v1\n')
    malicious = 'provider: deepseek\nmodel: deepseek-flash\nbase_url: https://untrusted.example/v1\n'
    replies = ['feed/model.yaml', json.dumps({'content': base64.b64encode(malicious.encode()).decode()})]
    monkeypatch.setenv('GITHUB_REPOSITORY', 'owner/repo')
    monkeypatch.setattr(ci, 'gh', Mock(side_effect=replies))
    with pytest.raises(ValueError, match='provider/base URL'):
        ci.stage_eval_inputs(tmp_path, 7, 'abc123')
    assert 'untrusted' not in (tmp_path / 'feed/model.yaml').read_text()


def test_scheduled_workflows_share_write_lock_and_manual_dispatch():
    workflows = {name: read_yaml(ROOT / '.github/workflows' / f'feed-{name}.yml')
                 for name in ['daily', 'weekly', 'review', 'picks', 'publish', 'eval']}
    assert {value['concurrency']['group'] for value in workflows.values()} == {'follow-rsi-state-${{ github.repository }}'}
    assert all('workflow_dispatch' in value['on'] for value in workflows.values())
    assert workflows['daily']['on']['schedule'][0]['cron'] == '23 2 * * *'
    assert workflows['weekly']['on']['schedule'][0]['cron'] == '7 21 * * 0'
    assert workflows['review']['on']['schedule'][0]['cron'] == '17 3 * * *'
    assert workflows['picks']['on']['schedule'][0]['cron'] == '41 23 * * 0'
    assert workflows['publish']['name'] == 'Follow RSI publish'
    assert workflows['publish']['permissions']['actions'] == 'write'
    assert workflows['review']['jobs']['queue']['permissions']['actions'] == 'write'
    assert workflows['review']['jobs']['validate-owner-decisions']['permissions']['statuses'] == 'write'
    for name in ['review', 'picks', 'publish', 'eval']:
        for job in workflows[name]['jobs'].values():
            checkout = next(step for step in job['steps'] if step.get('uses') == 'actions/checkout@v4')
            assert checkout['with']['ref'] == '${{ github.event.repository.default_branch }}'
    for name in ['daily', 'weekly']:
        commit = workflows[name]['jobs']['discover']['steps'][-1]['run']
        assert 'site/badges/feed-updated.json' in commit and '--deploy-pages' in commit
        assert workflows[name]['permissions']['actions'] == 'write'
