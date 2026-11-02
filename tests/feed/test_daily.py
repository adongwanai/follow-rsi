"""Offline tests for daily review, deferral, and the human publication boundary."""
from copy import deepcopy
import json

import pytest
import yaml
import jsonschema

from scripts.common import read_yaml
from scripts.feed.digest import initialize_public, publish_day
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


@pytest.mark.parametrize("source", ["saved_queue", "unmerged_pr"])
@pytest.mark.parametrize("owner_decision", ["accept", "reject", "move"])
def test_legacy_pending_rolls_to_defer_without_changing_owner_edits(tmp_path, source, owner_decision):
    root = make_daily_repo(tmp_path)
    items = load_items(root)
    for item in items:
        if item["kind"] == "paper":
            # This test preserves edits for papers observed on both boards.
            item["hf_daily_dates"] = [DAY, NEXT]
    save_items(root, items)
    queue_daily_review(root, DAY)

    def legacy_decisions(review):
        review["items"][0].update(decision="pending", note="Still needs the full text")
        review["items"][1].update(
            decision=owner_decision, note="Owner checked the changed object",
            direction_override="harness/improver", promote_to_repo=False,
            summary_override={"summary_zh": "留出任务达到 20%。", "summary_en": "Held-out tasks reach 20%."})
        review["lab_updates"][0].update(decision="pending", note="Check the official announcement")

    review = read_yaml(root / "review/daily" / f"{DAY}.yaml")
    legacy_decisions(review)
    if source == "saved_queue":
        write_daily(root, legacy_decisions)
    original = root / "review/daily" / f"{DAY}.yaml"
    original.write_text("# Retain the owner's original review file.\n" + original.read_text())
    original_bytes = original.read_bytes()
    carried = [review] if source == "unmerged_pr" else None
    carried_snapshot = deepcopy(carried)

    result = queue_daily_review(root, NEXT, carried_reviews=carried)

    assert result["items"][0]["decision"] == "defer"
    assert result["items"][0]["note"] == "Still needs the full text"
    assert result["items"][0]["carried_from"] == DAY
    for field in ("decision", "note", "direction_override", "summary_override", "promote_to_repo"):
        assert result["items"][1][field] == review["items"][1][field]
    assert result["lab_updates"][0]["decision"] == "defer"
    assert result["lab_updates"][0]["note"] == "Check the official announcement"
    assert original.read_bytes() == original_bytes
    assert carried == carried_snapshot
    validate_daily_review(root, NEXT)
    approved = approved_daily_items(root, NEXT)
    assert {item["id"] for item in approved} == (
        {review["items"][1]["id"]} if owner_decision in ("accept", "move") else set())

    write_daily(root, lambda value: value["items"][0].update(decision="pending"), date=NEXT)
    with pytest.raises(ValueError, match="pending review blocks publication"):
        validate_daily_review(root, NEXT)
    write_daily(root, lambda value: value["items"][0].update(decision="defer"), date=NEXT)
    write_daily(root, lambda value: value["lab_updates"][0].update(decision="pending"), date=NEXT)
    with pytest.raises(ValueError, match="pending review blocks publication"):
        validate_daily_review(root, NEXT)


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


def test_late_discovery_requires_explicit_actual_review_date(tmp_path):
    root = make_daily_repo(tmp_path)
    item = next(value for value in load_items(root) if value.get("arxiv_id") == "2610.99991")
    item.update(first_seen=NEXT + "T10:00:00Z", hf_daily_dates=[DAY])
    save_items(root, [item])
    assert item["id"] not in {row["id"] for row in queue_daily_review(root, DAY)["items"]}

    queued = queue_daily_review(root, DAY, reviewed_on=NEXT)
    assert queued["date"] == DAY and queued["reviewed_on"] == NEXT
    assert item["id"] in {row["id"] for row in queued["items"]}
    accept_daily(root)
    path = root / "review/daily" / f"{DAY}.yaml"
    before = path.read_bytes()
    queue_daily_review(root, DAY)
    assert path.read_bytes() == before

    write_daily(root, lambda review: review.pop("reviewed_on"))
    with pytest.raises(ValueError, match="discovered after this review date"):
        validate_daily_review(root, DAY)
    write_daily(root, lambda review: review.update(reviewed_on=NEXT))
    assert {row["id"] for row in approved_daily_items(root, DAY)} == {item["id"]}
    assert apply_daily_review(root, DAY, now=NEXT + "T12:00:00Z") == 3
    applied = next(value for value in load_items(root) if value["id"] == item["id"])
    assert applied["review"]["date"] == DAY
    assert applied["review"]["reviewed_on"] == NEXT
    assert apply_daily_review(root, DAY, now=NEXT + "T14:00:00Z") == 0


@pytest.mark.parametrize("reviewed_on,message", [
    ("2026-10-26", "cannot precede the edition date"),
    ("2026-02-30", "day is out of range"),
])
def test_actual_review_date_must_be_valid_and_not_before_edition(tmp_path, reviewed_on, message):
    root = make_daily_repo(tmp_path)
    with pytest.raises(ValueError, match=message):
        queue_daily_review(root, DAY, reviewed_on=reviewed_on)
    write_daily(root, lambda review: review.update(reviewed_on=reviewed_on))
    with pytest.raises(ValueError, match=message):
        validate_daily_review(root, DAY)


def test_later_review_does_not_change_hf_edition_eligibility(tmp_path):
    root = make_daily_repo(tmp_path)
    item = next(value for value in load_items(root) if value.get("arxiv_id") == "2610.99991")
    item.update(first_seen=NEXT + "T10:00:00Z", hf_daily_dates=[NEXT])
    save_items(root, [item])
    queued = queue_daily_review(root, DAY, reviewed_on=NEXT)
    row = next(value for value in queued["items"] if value["id"] == item["id"])
    assert row["window_status"] == "backlog"
    accept_daily(root)
    # A claimed window in the review file cannot override the observed HF day.
    write_daily(root, lambda review: next(value for value in review["items"]
                                         if value["id"] == item["id"]).update(window_status="in_window"))
    with pytest.raises(ValueError, match="requires window_status=in_window"):
        validate_daily_review(root, DAY)


@pytest.mark.parametrize("reviewed_on", [None, DAY, NEXT])
def test_daily_outputs_separate_edition_and_actual_review_dates(tmp_path, reviewed_on):
    root = make_daily_repo(tmp_path)
    queue_daily_review(root, DAY, reviewed_on=reviewed_on)
    accept_daily(root)
    actual_day = reviewed_on or DAY
    apply_daily_review(root, DAY, now=actual_day + "T12:00:00Z")
    publish_day(root, DAY, now=actual_day + "T12:05:00Z")

    edition = json.loads((root / "site/daily" / f"{DAY}.json").read_text())
    assert edition["date"] == DAY and edition["reviewed_on"] == actual_day
    feed = json.loads((root / "site/feed/latest.json").read_text())
    assert feed["dates"] == [DAY]
    assert feed["items"][0]["review_date"] == actual_day
    zh = (root / "daily" / f"{DAY}.md").read_text()
    en = (root / "daily" / f"{DAY}.en.md").read_text()
    html = (root / "site/daily" / f"{DAY}.html").read_text()
    assert f"刊期日期：{DAY}" in zh and f"审核日期：{actual_day}" in zh
    assert f"Edition date: {DAY}" in en and f"Review date: {actual_day}" in en
    assert f"刊期日期：{DAY}" in html and f"审核日期：{actual_day}" in html
    assert f"Edition date: {DAY}" in html and f"Review date: {actual_day}" in html
    assert ("**补刊**" in zh) == (actual_day > DAY)
    assert ("**Published later**" in en) == (actual_day > DAY)
    assert ('<span class="zh">补刊</span>' in html) == (actual_day > DAY)
    assert ('<span class="en">Published later</span>' in html) == (actual_day > DAY)
    before = {path: path.read_bytes() for path in (root / "site").rglob("*") if path.is_file()}
    publish_day(root, DAY)
    assert all(path.read_bytes() == content for path, content in before.items())


def test_daily_status_explains_empty_days_without_creating_editions(tmp_path):
    root = make_daily_repo(tmp_path)
    status = {"updated_at": NEXT + "T12:00:00Z", "days": [
        {"date": NEXT, "status": "empty_board", "reason_zh": "当日 HF 榜为空。", "reason_en": "The HF board was empty."},
        {"date": DAY, "status": "no_eligible_papers", "reason_zh": "没有合格的 Harness 论文。", "reason_en": "No eligible Harness papers."},
    ]}
    (root / "data/feed/daily-status.json").write_text(json.dumps(status, ensure_ascii=False))
    initialize_public(root)
    html = (root / "site/daily/index.html").read_text()
    assert "更新记录" in html and "Update log" in html
    assert "当日 HF 榜为空。" in html and "No eligible Harness papers." in html
    assert html.index(f'datetime="{DAY}"') < html.index(f'datetime="{NEXT}"')
    assert list((root / "site/daily").glob("????-??-??.*")) == []
    assert "<entry>" not in (root / "site/feed/atom.xml").read_text()
    assert json.loads((root / "site/feed/latest.json").read_text())["items"] == []
