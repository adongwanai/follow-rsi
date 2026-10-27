from scripts.feed.recall_check import compare, suggest_keywords, run
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
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data/papers.yaml').write_text('papers: []\n')
    record = {'arxiv_id': '2610.10001', 'title': 'Retained recursive experience', 'published': '2026-10-20'}
    report = run(tmp_path, now=NOW, reference_texts={'reference': 'https://arxiv.org/abs/2610.10001v3 and 2610.10002'}, metadata=[record])
    assert report['metadata_unavailable'] == ['2610.10002']
    assert report['misses'][0]['reason'] == 'never_fetched'
    assert (tmp_path / 'review/2026-W44.misses.yaml').exists()
    assert report['reference_status']['reference']['ok']
