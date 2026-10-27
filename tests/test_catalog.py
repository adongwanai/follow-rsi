"""Source fidelity, generated receipts and deterministic rebuild acceptance."""
from collections import Counter
import json
from pathlib import Path
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
    for name in ('README.md', 'README_en.md'):
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
    assert (ROOT / 'README_zh.md').read_text() == zh
    for paper in data['papers']:
        receipt = (ROOT / 'papers' / (paper['id'] + '.md')).read_text()
        row = next(line for line in zh.splitlines() if line.startswith('| ' + paper['date'] + ' |') and f"papers/{paper['id']}.md" in line)
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
            for name in ('README.md', 'README_en.md', 'README_zh.md'):
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
    path = project / 'papers/hda.md'
    path.write_text(path.read_text().replace('<!-- TODO -->', 'Handwritten audit notes: keep this.', 1))
    for name in ('README.md', 'README_en.md'):
        path = project/name
        path.write_text(path.read_text() + '\nAuthored footer: keep verbatim.\n')
    build(project)
    assert 'Handwritten audit notes: keep this.' in (project/'papers/hda.md').read_text()
    for name in ('README.md', 'README_en.md'):
        assert (project/name).read_text().endswith('Authored footer: keep verbatim.\n')
    assert (project/'README_zh.md').read_bytes() == (project/'README.md').read_bytes()
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
