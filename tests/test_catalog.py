"""Source fidelity, generated receipts and deterministic rebuild acceptance."""
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest
import yaml
from jsonschema import ValidationError

from common import ROOT, CHECKS, FIELDS, KEYS, evidence, number_tokens, read_yaml
from build import build, cell, compute_stats, replace_block
from validate import validate


@pytest.fixture
def project(tmp_path):
    for directory in ('data', 'scripts/templates', 'directions'):
        shutil.copytree(ROOT / directory, tmp_path / directory, ignore=shutil.ignore_patterns('feed'))
    for name in ('README.md', 'README_zh.md', 'README_en.md', 'site.config.yaml'):
        shutil.copy(ROOT / name, tmp_path / name)
    return tmp_path


def save_data(root, data):
    (root / 'data/papers.yaml').write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))


def test_valid_source_and_routes():
    data, routes = validate()
    assert data['papers'] and routes
    assert all(isinstance(p.get('en_machine_translated'), bool) for p in data['papers'] if p.get('summary_en'))


@pytest.mark.parametrize('mutation', ['duplicate_id', 'duplicate_arxiv', 'section', 'candidate', 'evidence', 'number'])
def test_invalid_source_rejected(project, mutation):
    data = read_yaml(project / 'data/papers.yaml')
    a, b = data['papers'][:2]
    if mutation == 'duplicate_id':
        b['id'] = a['id']
    elif mutation == 'duplicate_arxiv':
        b['arxiv'] = a['arxiv']
    elif mutation == 'section':
        a['section'] = 'invented'
    elif mutation == 'candidate':
        a['status'] = 'candidate'
    elif mutation == 'evidence':
        a['evidence'] = {'held_out': True}
    else:
        a['summary_en'] += ' 123456789%'
    save_data(project, data)
    with pytest.raises((ValueError, ValidationError)):
        validate(project)


def test_route_reference_rejected(project):
    routes = read_yaml(project / 'data/routes.yaml')
    routes['routes'][0]['papers'].append('missing-paper')
    (project / 'data/routes.yaml').write_text(yaml.safe_dump(routes, allow_unicode=True))
    with pytest.raises(ValueError, match='missing paper IDs'):
        validate(project)


def test_translations_and_chinese_outputs_are_faithful():
    data, _ = validate()
    zh = (ROOT / 'README.md').read_text()
    assert (ROOT / 'README_zh.md').read_text() == '[中文首页 → README.md](README.md)\n'
    catalog = (ROOT / 'PAPERS.md').read_text()
    for paper in data['papers']:
        receipt = (ROOT / 'papers' / (paper['id'] + '.md')).read_text()
        row = next(line for line in catalog.splitlines() if line.startswith('| ' + paper['date'] + ' |') and f"papers/{paper['id']}.md" in line)
        for field in ('summary', 'result'):
            original = paper.get(field + '_zh', '')
            assert original in receipt
            assert cell(original) in row
            assert Counter(number_tokens(original)) == Counter(number_tokens(paper.get(field + '_en', '')))


def test_coverage_marks_and_social_pages():
    data, _ = validate()
    core = [p for p in data['papers'] if p.get('status') != 'candidate']
    stats = compute_stats(data)
    for name, fields in [('evidence_coverage', FIELDS), ('check_coverage', list(CHECKS))]:
        count = sum(evidence(p)[k] != 'unknown' for p in core for k in fields)
        assert stats[name]['ratio'] == count / (len(core) * len(fields))
    site = json.loads((ROOT / 'site/papers.json').read_text())
    by_id = {p['id']: p for p in site['papers']}
    for paper in data['papers']:
        badge = json.loads((ROOT / 'badges' / (paper['id'] + '.json')).read_text())
        values = evidence(paper)
        expected = '1E7F48' if all(values[k] == 'yes' for k in KEYS) else '8B909B' if any(values[k] == 'unknown' for k in KEYS) else '2A33D4'
        assert badge['color'] == expected
        if paper.get('needs_reading'):
            assert by_id[paper['id']]['verification_label'] == '待细读 / Needs verification'
            assert 'Needs verification' in badge['message']
            for name in ('PAPERS.md',):
                row = next(line for line in (ROOT/name).read_text().splitlines() if line.startswith('| ' + paper['date'] + ' |') and f"papers/{paper['id']}.md" in line)
                assert '待细读 / Needs verification' in row
        receipt = (ROOT / 'papers' / (paper['id'] + '.md')).read_text()
        if paper.get('arxiv', '').startswith('cs/'):
            assert 'huggingface.co/papers/' not in receipt
        social = (ROOT / 'site/p' / (paper['id'] + '.html')).read_text()
        assert 'og:title' in social and 'og:description' in social and 'summary_large_image' in social
        assert (ROOT / 'site/cards' / (paper['id'] + '.png')).is_file()


def test_idempotence_and_authored_blocks(project):
    build(project)
    path = project / 'notes/hda.md'
    path.parent.mkdir(exist_ok=True)
    path.write_text('## 精读笔记\n\nHandwritten audit notes: keep this.\n')
    names = ('README.md', 'README_en.md')
    for name in names:
        path = project/name
        path.write_text(path.read_text() + f'\nAuthored footer in {name}: <SITE_URL> / <GITHUB_USER>.\n')
    def handwritten(path):
        return re.sub(r'(<!-- AUTO:([A-Z_]+):START -->).*?(<!-- AUTO:\2:END -->)',
                      r'\1\3', path.read_text(), flags=re.S)
    before = {name: handwritten(project/name) for name in names}
    build(project)
    assert 'Handwritten audit notes: keep this.' in (project/'papers/hda.md').read_text()
    assert {name: handwritten(project/name) for name in names} == before
    def git(*args):
        return subprocess.run(['git', *args], cwd=project, check=True, capture_output=True, text=True)
    git('init', '-q')
    git('add', '.')
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture')
    build(project)
    build(project)
    git('diff', '--exit-code')
    assert git('status', '--porcelain').stdout == ''


def test_auto_markers_fail_closed():
    for text in ('nothing', '<!-- AUTO:X:END --><!-- AUTO:X:START -->', '<!-- AUTO:X:START --><!-- AUTO:X:START --><!-- AUTO:X:END -->'):
        with pytest.raises(ValueError):
            replace_block(text, 'X', 'replacement')


def test_retired_repository_name_is_absent():
    retired = ('awesome-' + 'harness-evolution').encode()
    paths = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT
    ).decode().strip('\0').split('\0')
    matches = [name for name in paths if (ROOT/name).is_file() and retired in (ROOT/name).read_bytes()]
    assert not matches, matches


def test_readme_scope_counts_and_no_empty_sections():
    data, _ = validate()
    stats = compute_stats(data)
    assert stats['scopes'] == {'core': 61, 'harness_eval': 16, 'background': 16, 'general_rsi': 8}
    assert sum(stats['scopes'].values()) == stats['included']
    assert stats['must_read_fully_reviewed'] == 0
    for name in ('README.md', 'README_en.md'):
        text = (ROOT / name).read_text()
        assert len(text.splitlines()) <= 200
        assert not any(word in text for word in ('TODO', '<AUTHOR_NAME>', 'incomplete', 'Social preview'))
    assert not (ROOT / 'stats.json').exists()
    for path in (ROOT / 'papers').glob('*.md'):
        assert '<!-- TODO' not in path.read_text()


def test_reviewed_series_scope_and_evidence_boundaries():
    data, routes = validate()
    by_id = {paper['id']: paper for paper in data['papers']}
    for paper_id, arxiv_id, scope in (
        ('rsihub', '2610.32253', 'harness_eval'),
        ('harnessdev', '2609.01437', 'harness_eval'),
        ('aspire', '2608.31111', 'general_rsi'),
        ('s3gym', '2608.31100', 'general_rsi'),
    ):
        paper = by_id[paper_id]
        assert paper['arxiv'] == arxiv_id
        assert paper['scope'] == scope
        assert paper['section'] == 'evaluation'
        assert not paper.get('needs_reading')
        assert (ROOT / 'notes' / f'{paper_id}.md').is_file()

    # Two execution harnesses using GPT-5.4 do not establish cross-model transfer.
    assert evidence(by_id['rsihub'])['cross_model_transfer'] == 'no'
    assert evidence(by_id['rsihub'])['matched_budget_baseline'] == 'unknown'
    # RQ1 directly re-executes frozen artifacts; RQ2 is not a matched-search control.
    assert evidence(by_id['harnessdev'])['cross_model_transfer'] == 'yes'
    assert evidence(by_id['harnessdev'])['matched_budget_baseline'] == 'no'
    assert evidence(by_id['harnessdev'])['cost_reported'] == 'partial'
    # Equal interaction budgets in S3Gym are not equal total inference/training costs.
    assert evidence(by_id['s3gym'])['matched_budget_baseline'] == 'unknown'
    assert evidence(by_id['s3gym'])['cost_reported'] == 'unknown'

    route = next(r for r in routes if r['name_en'] == 'Experimental design (everyone)')
    assert route['papers'][route['papers'].index('hda') + 1] == 'harnessdev'
    assert route['papers'][:4] == ['rethinking-evaluation', 'hda', 'harnessdev', 'rsihub']
    assert by_id['harnessdev']['must_read']
    assert {'aspire', 's3gym'}.isdisjoint(route['papers'])
    assert compute_stats(data)['scopes']['core'] == 61
