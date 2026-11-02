from scripts.feed.recall_check import compare, suggest_keywords, run, harness_reference_ids
from scripts.common import ROOT
import shutil
import pytest
from scripts.feed.normalize import normalize_record
from scripts.feed.storage import save_items

NOW = '2026-10-27T12:00:00+00:00'


def test_recall_distinguishes_misses_from_pending():
    refs = [{'arxiv_id': f'2610.1000{i}', 'title': 'Recursive memory improvement', 'published': '2026-10-20'} for i in range(4)]
    items = [normalize_record(ref, now=NOW) for ref in refs[1:]]
    items[0]['llm'] = {'label': 'exclude'}
    items[1].update(llm={'label': 'borderline'}, review={'decision': 'reject'})
    items[2]['llm'] = {'label': 'include'}
    misses, pending = compare(refs, items, '2026-08-28')
    assert [m['reason'] for m in misses] == ['never_fetched', 'excluded', 'borderline_rejected']
    assert pending == ['2610.10003']
    assert 'memory' in suggest_keywords(misses)


def test_offline_reference_report_keeps_metadata_gaps_visible(tmp_path):
    (tmp_path / 'feed').mkdir()
    shutil.copyfile(ROOT / 'feed/sources.yaml', tmp_path / 'feed/sources.yaml')
    shutil.copyfile(ROOT / 'feed/taxonomy.yaml', tmp_path / 'feed/taxonomy.yaml')
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/papers.yaml').write_text('papers: []\n')
    record = {'arxiv_id': '2610.10001', 'title': 'Retained recursive experience', 'published': '2026-10-20'}
    report = run(tmp_path, now=NOW, reference_texts={'Harness-RSI': 'https://arxiv.org/abs/2610.10001v3 and 2610.10002'}, metadata=[record])
    assert report['metadata_unavailable'] == ['2610.10002']
    assert report['misses'][0]['reason'] == 'never_fetched'
    assert (tmp_path / 'review/2026-W44.misses.yaml').exists()
    assert report['reference_status']['Harness-RSI']['ok']


METHODS = r"""
export const methods = [
  {id: "2610.10001", title: "Harness code", arxiv: "https://arxiv.org/abs/2610.10001v2"},
  {id: "2610.10002", title: "A harness mention in the title is not a taxonomy label"},
  {id: "2610.10003", title: "Retained memory {without code changes}", summary: "ref https://arxiv.org/abs/2610.19999"},
  {id: "no-paper", arxiv: null, title: "Harness system without arXiv"},
].map((method) => ({...method, arxiv: `https://arxiv.org/abs/${method.id}`}));
"""
TAXONOMY = r"""
export const methodTaxonomy = {
  // No inferred tags from comments or titles.
  "2610.10001": {artifact: ["Non-parametric", "Harness code"]},
  "2610.10002": {artifact: ["Parametric"]},
  "2610.10003": {artifact: ["Memory"]},
  "2610.19998": {artifact: ["Harness code"]},
  "no-paper": {artifact: ["Harness code"]},
};
"""


def test_prism_reference_requires_explicit_harness_taxonomy_and_real_metadata_id():
    assert harness_reference_ids(METHODS, TAXONOMY, 'methods') == ['2610.10001']
    papers = METHODS.replace('export const methods', 'export const papers')
    taxonomy = TAXONOMY.replace('methodTaxonomy', 'paperTaxonomy')
    assert harness_reference_ids(papers, taxonomy, 'papers') == ['2610.10001']
    with pytest.raises(ValueError, match='explicitly labelled'):
        harness_reference_ids(METHODS, TAXONOMY.replace('Harness code', 'Memory'), 'methods')


def test_missing_prism_taxonomy_never_falls_back_to_whole_reference(tmp_path):
    (tmp_path / 'feed').mkdir()
    shutil.copyfile(ROOT / 'feed/sources.yaml', tmp_path / 'feed/sources.yaml')
    shutil.copyfile(ROOT / 'feed/taxonomy.yaml', tmp_path / 'feed/taxonomy.yaml')
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/papers.yaml').write_text('papers: []\n')
    report = run(tmp_path, now=NOW, reference_texts={'awesome-rsi-methods': METHODS}, metadata=[])
    assert report['scope'] == 'harness'
    assert report['misses'] == [] and report['metadata_unavailable'] == []
    assert report['reference_status']['awesome-rsi-methods']['ok'] is False
    assert 'full-table extraction' in report['reference_status']['awesome-rsi-methods']['error']
    report = run(tmp_path, now=NOW, reference_texts={'awesome-rsi-methods': METHODS},
                 taxonomy_texts={'awesome-rsi-methods': TAXONOMY}, metadata=[])
    assert report['metadata_unavailable'] == ['2610.10001']
    assert report['reference_status']['awesome-rsi-methods']['ids'] == 1



def test_harness_reference_outside_classification_is_a_scope_miss_not_pending():
    from scripts.feed.scope import load_scope
    ref = {'arxiv_id': '2610.10001', 'title': 'Harness-code reference', 'published': '2026-10-20'}
    item = normalize_record(ref, now=NOW)
    item['llm'] = {'label': 'include', 'primary': 'model_weights', 'secondary': ['harness']}
    misses, pending = compare([ref], [item], '2026-08-28', scope=load_scope(ROOT))
    assert not pending and misses[0]['reason'] == 'outside_publish_scope'


def test_recorded_arxiv_query_recalls_eight_previously_missed_catalog_entries(monkeypatch):
    from datetime import datetime, timezone
    from pathlib import Path
    from unittest.mock import Mock
    from scripts.common import read_yaml
    from scripts.feed import fetch_arxiv
    from scripts.feed.dedupe import dedupe_items
    expected = {'2610.28380', '2610.30042', '2610.28201', '2610.28815',
                '2610.21791', '2610.31401', '2610.22466', '2610.30499'}
    # Public Atom entries recorded from the successful 2026-10-27 query run;
    # no live network or generated abstracts are used in this regression.
    body = (Path(__file__).parent / 'fixtures/arxiv-harness-recall.xml').read_text()
    monkeypatch.setattr(fetch_arxiv, 'request', Mock(return_value=body))
    source = next(s for s in read_yaml(ROOT / 'feed/sources.yaml')['sources'] if s['id'] == 'arxiv-harness')
    records, _ = fetch_arxiv.fetch(source, days=14, now=datetime(2026, 10, 27, tzinfo=timezone.utc))
    papers = read_yaml(ROOT / 'data/papers.yaml')['papers']
    result = dedupe_items(records, repo_papers=papers)
    assert {r['arxiv_id'] for r in result} == expected
    assert all(r['in_repo'] and r['source_hits'] == ['arxiv-harness'] for r in result)
