import pytest
from arxiv_watch import normalize_id, parse_feed, issue_ids, select_candidates, issue_body, watch


def test_atom_preserves_original_abstract_and_deduplicates():
    xml = '''<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/abs/2610.12345v2</id><title>Exact title</title><summary>Exactly 4/26 and 54%.</summary></entry></feed>'''
    entries = parse_feed(xml)
    assert entries[0]['id'] == '2610.12345'
    assert issue_body(entries[0]) == 'Exact title\n\nhttps://arxiv.org/abs/2610.12345\n\nExactly 4/26 and 54%.\n'
    known = issue_ids([{'body': 'https://arxiv.org/pdf/2610.12345v1.pdf'}])
    assert select_candidates(entries, known) == []
    assert normalize_id('https://arxiv.org/abs/cs/0309048v1') == 'cs/0309048'
    items = [{'id': str(i)} for i in range(30)]
    assert len(select_candidates(items + items, set())) == 15


def test_invalid_metadata_and_local_network_are_rejected(monkeypatch):
    with pytest.raises(ValueError):
        normalize_id('bad')
    with pytest.raises(ValueError):
        parse_feed('<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>2610.12345</id></entry></feed>')
    monkeypatch.delenv('GITHUB_ACTIONS', raising=False)
    with pytest.raises(RuntimeError, match='only in GitHub Actions'):
        watch()
