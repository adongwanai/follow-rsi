"""Owner corrections are auditable, repeatable and cannot resurrect a withdrawn day."""
import json
from pathlib import Path
import shutil
import pytest
from scripts.common import ROOT, read_yaml
from scripts.feed.corrections import publish_corrected_recap
from scripts.feed.digest import publish_day
from scripts.feed.storage import load_items, save_items


def correction_repo(tmp_path):
    for file in ('data/feed/items.jsonl', 'data/feed/withdrawn-editions.json', 'data/feed/state.json',
                 'data/papers.yaml', 'feed/taxonomy.yaml', 'feed/sources.yaml', 'site.config.yaml',
                 'site/feed/status.json', 'review/daily/2026-10-27.yaml',
                 'review/corrections/2026-10-27.yaml', 'review/corrections/2026-10-27.en.yaml'):
        path=tmp_path/file;path.parent.mkdir(parents=True,exist_ok=True);shutil.copy(ROOT/file,path)
    return tmp_path


def test_correction_restores_only_owner_list_and_preserves_original_review(tmp_path):
    root=correction_repo(tmp_path)
    original=(root/'review/daily/2026-10-27.yaml').read_bytes()
    result=publish_corrected_recap(root,'2026-10-27','2026-10-14','2026-10-27')
    owner=read_yaml(root/'review/corrections/2026-10-27.yaml')
    expected={'arxiv:'+row['arxiv'] for row in owner['keep_harness']+owner['missed_should_appear']['skipped_because_in_repo']}
    assert len(expected)==16
    assert {item['id'] for item in result['items']}==expected
    assert result['counts']['harness']==15 and result['counts']['theory_survey']==1
    assert (root/'review/daily/2026-10-27.yaml').read_bytes()==original
    assert not (root/'site/daily/2026-10-27.json').exists()
    feed=json.loads((root/'site/feed/latest.json').read_text())
    assert {item['id'] for item in feed['items']}==expected
    assert all(item['edition_kind']=='retrospective' for item in feed['items'])
    before=(root/'data/feed/items.jsonl').read_bytes()
    public=(root/'site/recaps/2026-10-14--2026-10-27.json').read_bytes()
    publish_corrected_recap(root,'2026-10-27','2026-10-14','2026-10-27')
    assert (root/'data/feed/items.jsonl').read_bytes()==before
    assert (root/'site/recaps/2026-10-14--2026-10-27.json').read_bytes()==public
    with pytest.raises(ValueError,match='withdrawn'):
        publish_day(root,'2026-10-27')


def test_bad_recap_window_fails_before_changing_source_reviews(tmp_path):
    root=correction_repo(tmp_path)
    before=(root/'data/feed/items.jsonl').read_bytes()
    with pytest.raises(ValueError,match='no observed HF recommendation'):
        publish_corrected_recap(root,'2026-10-27','2026-10-26','2026-10-27')
    assert (root/'data/feed/items.jsonl').read_bytes()==before


@pytest.mark.parametrize('arxiv_id', ['2610.35434', '2610.27435'])
@pytest.mark.parametrize('already_published', [False, True])
def test_retracted_keep_or_restored_item_blocks_correction_without_writes(tmp_path, arxiv_id, already_published):
    root = correction_repo(tmp_path)
    if already_published:
        publish_corrected_recap(root, '2026-10-27', '2026-10-14', '2026-10-27')
    item = next(item for item in load_items(root) if item['arxiv_id'] == arxiv_id)
    item['retracted'] = True
    save_items(root, [item])
    before = {str(path.relative_to(root)): path.read_bytes()
              for path in root.rglob('*') if path.is_file()}
    with pytest.raises(ValueError, match=f'{item["id"]}: retracted items cannot be restored'):
        publish_corrected_recap(root, '2026-10-27', '2026-10-14', '2026-10-27')
    after = {str(path.relative_to(root)): path.read_bytes()
             for path in root.rglob('*') if path.is_file()}
    assert after == before
