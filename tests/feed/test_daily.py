"""Offline tests for daily review, deferral, and the human publication boundary."""
from copy import deepcopy

import pytest
import yaml
import jsonschema

from scripts.common import read_yaml
from scripts.feed.review import (apply_daily_review, approved_daily_items, interactive_daily_review,
                                 queue_daily_review, validate_daily_review)
from scripts.feed.storage import load_items, save_items
from test_review import WEEK, make_repo

DAY = "2026-10-27"
NEXT = "2026-10-28"


def make_daily_repo(root):
    make_repo(root)
    (root / "review" / f"{WEEK}.yaml").unlink()
    queue_daily_review(root, DAY)
    return root


def write_daily(root, update, date=DAY):
    path = root / "review/daily" / f"{date}.yaml"
    review = read_yaml(path)
    update(review)
    path.write_text(yaml.safe_dump(review, allow_unicode=True, sort_keys=False))
    return review


def accept_daily(root):
    def decide(review):
        for row in review["items"]:
            row["decision"] = "accept" if row["arxiv_id"] == "2610.99991" else "reject"
        for row in review["lab_updates"]:
            row["decision"] = "reject"
    return write_daily(root, decide)


def test_pending_blocks_and_defer_is_not_an_approval(tmp_path):
    root = make_daily_repo(tmp_path)
    assert approved_daily_items(root, DAY) == []
    write_daily(root, lambda review: review["items"][0].update(decision="pending"))
    with pytest.raises(ValueError, match="pending"):
        validate_daily_review(root, DAY)
    accept_daily(root)
    write_daily(root, lambda review: review["items"][1].update(decision="defer"))
    validate_daily_review(root, DAY)
    assert approved_daily_items(root, DAY) == []


def test_partial_code_evidence_survives_queue_without_approval(tmp_path):
    root = make_daily_repo(tmp_path)
    items = load_items(root)
    item = next(value for value in items if value.get("arxiv_id") == "2610.99991")
    item["evidence_quick"]["code_released"] = {
        "value": "partial", "quote": "https://github.com/fixture/readme-only"}
    save_items(root, [item])
    review = queue_daily_review(root, DAY)
    row = next(value for value in review["items"] if value["id"] == item["id"])
    assert row["evidence_quick"]["code_released"] == item["evidence_quick"]["code_released"]
    assert row["decision"] == "defer"
    validate_daily_review(root, DAY)
    assert approved_daily_items(root, DAY) == []
    write_daily(root, lambda value: value["items"][0]["evidence_quick"]["held_out"].update(value="partial"))
    with pytest.raises(jsonschema.ValidationError):
        validate_daily_review(root, DAY)


def test_rollover_preserves_unmerged_decisions_and_resets_deferral(tmp_path):
    root = make_daily_repo(tmp_path)
    review = accept_daily(root)
    review["items"][0].update(decision="defer", note="Read full text tomorrow")
    review["items"][1].update(note="Recovered owner edit")
    # Carried PR edits override the stale queue committed on main.
    result = queue_daily_review(root, NEXT, carried_reviews=[review])
    assert result["items"][0]["decision"] == "defer"
    assert result["items"][0]["note"] == "Read full text tomorrow"
    assert result["items"][1]["decision"] == "accept"
    assert result["items"][1]["note"] == "Recovered owner edit"
    assert result["lab_updates"][0]["decision"] == "reject"
    path = root / "review/daily" / f"{NEXT}.yaml"
    before = path.read_bytes()
    queue_daily_review(root, NEXT)
    assert path.read_bytes() == before


def test_applied_decisions_dont_recur_but_changed_versions_need_review(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    provenance = {"github_pr": 7, "owner_login": "fixture-owner", "merge_commit": "abc123"}
    assert apply_daily_review(root, DAY, now=DAY + "T12:00:00Z", provenance=provenance) == 3
    path = root / "data/feed/items.jsonl"
    before = path.read_bytes()
    assert apply_daily_review(root, DAY, now=DAY + "T14:00:00Z") == 0
    assert path.read_bytes() == before
    applied = next(item for item in load_items(root) if item["id"] == "arxiv:2610.99991")
    assert applied["review"]["github_pr"] == 7
    result = queue_daily_review(root, NEXT)
    assert result["items"] == result["lab_updates"] == []
    applied["version"] = 2
    save_items(root, [applied])
    result = queue_daily_review(root, NEXT)
    assert len(result["items"]) == 1 and result["items"][0]["decision"] == "defer"


def test_deferred_apply_does_not_add_eval_labels_and_returns_next_day(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    write_daily(root, lambda review: review["items"][0].update(decision="defer"))
    apply_daily_review(root, DAY)
    assert read_yaml(root / "feed/eval/labeled.yaml") == []
    result = queue_daily_review(root, NEXT)
    assert len(result["items"]) == 1 and result["items"][0]["decision"] == "defer"


def test_deferred_error_row_overrides_guard_numbers_without_requiring_classification(tmp_path):
    root = make_daily_repo(tmp_path)
    items = load_items(root)
    item = next(value for value in items if value["arxiv_id"] == "2610.99992")
    item["llm"] = {"label": "error", "confidence": 0}
    save_items(root, [item])
    queue_daily_review(root, DAY)
    accept_daily(root)
    write_daily(root, lambda review: review["items"][0].update(decision="defer", summary_override="人工摘要 99%。"))
    with pytest.raises(ValueError, match="number guard"):
        validate_daily_review(root, DAY)
    write_daily(root, lambda review: review["items"][0].update(summary_override="人工摘要 20%。"))
    validate_daily_review(root, DAY)


def test_daily_cli_skip_means_defer(tmp_path):
    root = make_daily_repo(tmp_path)
    answers = iter(["s", "m", "harness/improver", "r"])
    result = interactive_daily_review(root, DAY, input_fn=lambda _: next(answers), output_fn=lambda _: None)
    assert result["items"][0]["decision"] == "defer"
    assert result["items"][1]["decision"] == "move"
    validate_daily_review(root, DAY)
