"""Publication boundary tests use synthetic, explicitly offline metadata."""
from copy import deepcopy
import json
from pathlib import Path
import shutil

import pytest
import yaml

from scripts.common import ROOT, read_yaml
from scripts.feed.guard import unknown_evidence
from scripts.feed.review import (apply_review, approved_items, interactive_review,
                                 queue_review, validate_review)
from scripts.feed.storage import load_items, save_items

WEEK = "2026-W44"


def make_repo(root):
    for path in ("feed/taxonomy.yaml", "feed/sources.yaml", "site.config.yaml", "data/schema.json"):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / path, target)
    collection = read_yaml(ROOT / "data/papers.yaml")
    collection["papers"] = []
    (root / "data/papers.yaml").write_text(yaml.safe_dump(collection, allow_unicode=True, sort_keys=False))
    (root / "data/routes.yaml").write_text("routes: []\n")
    (root / "feed/eval").mkdir()
    (root / "feed/eval/labeled.yaml").write_text("[]\n")
    evidence = unknown_evidence()
    evidence["held_out"] = {"value": "yes", "quote": "held-out tasks"}
    item = {
        "id": "arxiv:2610.99991", "kind": "paper", "arxiv_id": "2610.99991", "version": 1,
        "title": "Offline Fixture: Persistent Skill Evolution", "authors": ["Synthetic fixture author"],
        "abstract": "This offline fixture describes persistent skill evolution across held-out tasks at 20%.",
        "comments": "", "categories": ["cs.AI"], "published": "2026-10-26T10:00:00Z",
        "updated": "2026-10-26T10:00:00Z", "first_seen": "2026-10-27T10:00:00Z",
        "links": {"arxiv": "https://arxiv.org/abs/2610.99991", "hf": "https://huggingface.co/papers/2610.99991"},
        "code_links": [], "source_hits": ["arxiv-harness", "hf-daily"], "seed_hits": ["seed"],
        "hf_upvotes": 12, "in_repo": False,
        "llm": {"label": "include", "primary": "harness", "harness_sub": "component", "secondary": [], "confidence": .95},
        "summary_zh": "跨任务保留技能，在留出任务上达到 20%。",
        "summary_en": "Skills persist across tasks, reaching 20% on held-out tasks.",
        "evidence_quick": evidence, "guard_failed": False, "initial_guard_failed": False,
    }
    borderline = deepcopy(item)
    borderline.update(id="arxiv:2610.99992", arxiv_id="2610.99992", title="Offline Borderline Fixture")
    borderline["llm"].update(label="borderline", confidence=.5)
    excluded = deepcopy(item)
    excluded.update(id="arxiv:2610.99993", arxiv_id="2610.99993", title="Offline Excluded Fixture")
    excluded["llm"].update(label="exclude", exclude_reason="static_framework")
    release = {"id": "release:https://example.org/release/1", "kind": "release", "title": "Fixture v1",
               "release_version": "v1", "published": "2026-10-26T10:00:00Z", "first_seen": "2026-10-27T10:00:00Z",
               "links": {"url": "https://example.org/release/1"}, "source_hits": ["github-releases"]}
    save_items(root, [item, borderline, excluded, release])
    queue_review(root, WEEK)
    return root


def write_review(root, update):
    path = root / "review" / f"{WEEK}.yaml"
    review = read_yaml(path)
    update(review)
    path.write_text(yaml.safe_dump(review, allow_unicode=True, sort_keys=False))
    return review


def accept_one(root):
    def decide(review):
        for row in review["items"]:
            row["decision"] = "accept" if row["arxiv_id"] == "2610.99991" else "reject"
        for row in review["lab_updates"]:
            row["decision"] = "reject"
    return write_review(root, decide)


def test_queue_priorities_exclusions_and_owner_decisions_survive_rerun(tmp_path):
    root = make_repo(tmp_path)
    review = read_yaml(root / "review" / f"{WEEK}.yaml")
    assert review["items"][0]["llm"]["label"] == "borderline"
    assert len(review["items"]) == 2
    assert len(read_yaml(root / "review" / f"{WEEK}.excluded.yaml")["items"]) == 1
    accept_one(root)
    before = (root / "review" / f"{WEEK}.yaml").read_bytes()
    queue_review(root, WEEK)
    assert (root / "review" / f"{WEEK}.yaml").read_bytes() == before


def test_pending_paper_and_lab_update_block_publication(tmp_path):
    root = make_repo(tmp_path)
    with pytest.raises(ValueError, match="pending"):
        validate_review(root, WEEK)
    accept_one(root)
    write_review(root, lambda review: review["lab_updates"][0].update(decision="pending"))
    with pytest.raises(ValueError, match="pending lab"):
        validate_review(root, WEEK)


def test_summary_overrides_must_use_source_numbers_and_matching_translation(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    def override(review):
        review["items"][1]["summary_override"] = {"summary_zh": "达到 99%。", "summary_en": "Reached 99%."}
    write_review(root, override)
    with pytest.raises(ValueError, match="number guard"):
        validate_review(root, WEEK)
    write_review(root, lambda review: review["items"][1].update(summary_override={"summary_zh": "达到 20%。", "summary_en": "Reached 21%."}))
    with pytest.raises(ValueError, match="number guard"):
        validate_review(root, WEEK)
    write_review(root, lambda review: review["items"][1].update(summary_override="达到 20%。"))
    assert approved_items(root, WEEK)[0]["summary_en"] == ""


def test_picks_must_be_accepted_and_owner_authored(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    write_review(root, lambda review: review.update(picks=[{"arxiv_id": "2610.99992", "why_zh": "人工填写", "why_en": "Owner text"}]))
    with pytest.raises(ValueError, match="Picks"):
        validate_review(root, WEEK)


def test_move_requires_valid_direction_and_cannot_be_an_accept_pick(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    write_review(root, lambda review: review["items"][1].update(decision="move"))
    with pytest.raises(ValueError, match="requires direction"):
        validate_review(root, WEEK)
    write_review(root, lambda review: review["items"][1].update(direction_override="harness/improver"))
    assert approved_items(root, WEEK)[0]["llm"]["harness_sub"] == "improver"
    write_review(root, lambda review: review["items"][1].update(direction_override="invented-category"))
    with pytest.raises(ValueError, match="invalid primary"):
        validate_review(root, WEEK)


def test_source_change_requires_new_approval_but_retains_notes(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    write_review(root, lambda review: review["items"][1].update(note="Owner's note"))
    item = load_items(root)[0]
    item["version"] = 2
    save_items(root, [item])
    with pytest.raises(ValueError, match="source changed"):
        validate_review(root, WEEK)
    review = queue_review(root, WEEK)
    changed = next(row for row in review["items"] if row["arxiv_id"] == "2610.99991")
    assert changed["decision"] == "pending" and changed["note"] == "Owner's note"


def test_apply_review_append_only_idempotence_and_eval_increment(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    before = (root / "data/feed/items.jsonl").read_text()
    assert apply_review(root, WEEK, now="2026-11-01T23:55:00Z") == 3
    after = (root / "data/feed/items.jsonl").read_text()
    assert after.startswith(before)
    assert apply_review(root, WEEK, now="2026-11-02T00:00:00Z") == 0
    assert (root / "data/feed/items.jsonl").read_text() == after
    labels = read_yaml(root / "feed/eval/labeled.yaml")
    assert len(labels) == 1 and labels[0]["label"] == "exclude" and labels[0]["labeled_by"] == "owner"


def test_cli_review_leaves_skips_pending(tmp_path):
    root = make_repo(tmp_path)
    answers = iter(["r", "m", "harness/improver", "s"])
    result = interactive_review(root, WEEK, input_fn=lambda _: next(answers), output_fn=lambda _: None)
    assert result["items"][1]["decision"] == "move"
    assert result["lab_updates"][0]["decision"] == "pending"
