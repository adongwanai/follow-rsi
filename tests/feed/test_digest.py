from copy import deepcopy
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import jsonschema
import pytest
import yaml

from scripts.common import read_yaml
from scripts.feed.digest import (_write_feed, initialize_public, publish_day, publish_demo,
                                 publish_week, remove_retracted)
from scripts.feed.review import (apply_daily_review, queue_daily_review, queue_weekly_picks,
                                 validate_weekly_picks)
from scripts.feed.storage import load_items, save_items
from test_daily import DAY, NEXT, accept_daily, make_daily_repo, write_daily
from test_review import WEEK, make_repo


def ready_week(root):
    accept_daily(root)
    apply_daily_review(root, DAY)
    publish_day(root, DAY, now=DAY + "T12:00:00Z")
    queue_weekly_picks(root, WEEK)


def write_picks(root, **values):
    path = root / "review" / f"{WEEK}.yaml"
    review = read_yaml(path)
    review.update(values)
    path.write_text(yaml.safe_dump(review, allow_unicode=True, sort_keys=False))


def test_pending_daily_review_writes_no_public_outputs(tmp_path):
    root = make_daily_repo(tmp_path)
    with pytest.raises(ValueError, match="pending"):
        publish_day(root, DAY)
    assert not (root / "site/feed/latest.json").exists()
    assert not (root / "daily").exists()


def test_daily_feed_schema_latest_index_and_idempotence(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    report = publish_day(root, DAY, now=DAY + "T12:00:00Z")
    assert report["published"] and report["accepted"] == 1
    zh = (root / "daily" / f"{DAY}.md").read_text()
    en = (root / "daily" / f"{DAY}.en.md").read_text()
    assert "自动判断，未核实" in zh and "Automated, unverified" in en
    assert en.index("[hf]") < en.index("[arxiv]")
    feed = json.loads((root / "site/feed/latest.json").read_text())
    schema = json.loads((root / "site/feed/schema.json").read_text())
    jsonschema.validate(feed, schema)
    assert feed["dates"] == [DAY]
    assert feed["items"][0]["review_date"] == DAY
    assert feed["items"][0]["hf_upvotes"] == 12
    assert DAY in (root / "site/daily/index.html").read_text()
    assert "urn:follow-rsi:daily:" + DAY in (root / "site/feed/atom.xml").read_text()
    before = {str(path.relative_to(root)): path.read_bytes() for path in (root / "site").rglob("*") if path.is_file()}
    publish_day(root, DAY)
    after = {str(path.relative_to(root)): path.read_bytes() for path in (root / "site").rglob("*") if path.is_file()}
    assert before == after


def test_no_daily_acceptance_preserves_latest_index(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    queue_daily_review(root, NEXT)
    before = (root / "site/daily/index.html").read_bytes()
    report = publish_day(root, NEXT)
    assert report["published"] is False
    assert not (root / "site/daily" / f"{NEXT}.html").exists()
    assert (root / "site/daily/index.html").read_bytes() == before


def test_weekly_requires_daily_publication_and_cannot_use_old_full_review(tmp_path):
    root = make_repo(tmp_path)
    with pytest.raises(jsonschema.ValidationError):
        publish_week(root, WEEK)
    queue_weekly_picks(root, WEEK)
    write_picks(root, picks=[{"arxiv_id": "2610.99991", "why_zh": "人工理由", "why_en": "Owner reason"}])
    with pytest.raises(ValueError, match="daily-approved"):
        validate_weekly_picks(root, WEEK)


def test_weekly_uses_only_daily_snapshots_and_preserves_owner_picks(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    write_picks(root, picks=[{"arxiv_id": "2610.99991", "why_zh": "我想仔细核查技能迁移。", "why_en": "I want to examine skill transfer."}],
                editor_note_zh="本周收录 1 篇。", editor_note_en="This week includes 1 paper.")
    report = publish_week(root, WEEK, now="2026-11-01T23:55:00Z")
    assert report["accepted"] == 1
    en = (root / "digests" / f"{WEEK}.en.md").read_text()
    assert "I want to examine skill transfer." in en and "This week includes 1 paper." in en
    html = (root / "site/weekly" / f"{WEEK}.html").read_text()
    assert "og:image" in html and "This week includes 1 paper." in html
    before = {str(path.relative_to(root)): path.read_bytes() for path in (root / "site").rglob("*") if path.is_file()}
    publish_week(root, WEEK)
    assert before == {str(path.relative_to(root)): path.read_bytes() for path in (root / "site").rglob("*") if path.is_file()}
    write_picks(root, editor_note_zh="本周收录 99 篇。", editor_note_en="This week includes 99 papers.")
    with pytest.raises(ValueError, match="number guard"):
        publish_week(root, WEEK)


def test_empty_weekly_picks_section_is_absent_and_intro_guard_retries(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    class FakeLLM:
        def __init__(self):
            self.calls = []
        def run(self, name, item, **kwargs):
            self.calls.append(kwargs)
            return {"data": {"intro_zh": "本周 999 篇。", "intro_en": "999 papers this week."}}
    client = FakeLLM()
    publish_week(root, WEEK, client=client)
    assert len(client.calls) == 2 and client.calls[1]["feedback"]
    manifest = json.loads((root / "site/weekly" / f"{WEEK}.json").read_text())
    assert manifest["intro"]["source"] == "count-template" and "999" not in manifest["intro"]["zh"]
    assert "本周精选" not in (root / "digests" / f"{WEEK}.md").read_text()
    assert "Owner's picks" not in (root / "digests" / f"{WEEK}.en.md").read_text()


def test_daily_and_weekly_body_order_is_chronological_without_reordering_picks(tmp_path):
    root = make_daily_repo(tmp_path)
    sources = load_items(root)
    earlier = next(item for item in sources if item["arxiv_id"] == "2610.99992")
    earlier.update(published="2026-10-25T10:00:00Z", seed_hits=[], hf_upvotes=0)
    earlier_lab = deepcopy(next(item for item in sources if item["kind"] == "release"))
    earlier_lab.update(id="release:https://example.org/release/0", title="Earlier lab update",
                       release_version="v0", published="2026-10-25T10:00:00Z",
                       links={"url": "https://example.org/release/0"})
    save_items(root, [earlier, earlier_lab])
    queue_daily_review(root, DAY)
    def approve(review):
        for row in review["items"]:
            row["decision"] = "accept"
        for row in review["lab_updates"]:
            row.update(decision="accept", direction_override="harness/component")
    write_daily(root, approve)
    publish_day(root, DAY, now=DAY + "T12:00:00Z")
    queue_weekly_picks(root, WEEK)
    picks = [{"arxiv_id": ident, "why_zh": "人工精选。", "why_en": "Owner selection."}
             for ident in ("2610.99991", "2610.99992")]
    write_picks(root, picks=picks)
    publish_week(root, WEEK)
    for kind, period in (("daily", DAY), ("weekly", WEEK)):
        manifest = json.loads((root / "site" / kind / f"{period}.json").read_text())
        assert [item["arxiv_id"] for item in manifest["items"]] == ["2610.99992", "2610.99991"]
        assert [item["release_version"] for item in manifest["lab_updates"]] == ["v0", "v1"]
        html = (root / "site" / kind / f"{period}.html").read_text()
        assert re.findall(r'<article class="weekly-paper">.*?<h3>(.*?)</h3>', html, re.S) == [
            "Offline Borderline Fixture", "Offline Fixture"]
        assert html.index("https://example.org/release/0") < html.index("https://example.org/release/1")
    assert manifest["picks"] == picks
    assert re.findall(r'<article class="weekly-pick">.*?<h3>(.*?)</h3>', html, re.S) == [
        "Offline Fixture: Persistent Skill Evolution", "Offline Borderline Fixture"]
    feed = json.loads((root / "site/feed/latest.json").read_text())
    assert [item["arxiv_id"] for item in feed["items"]] == ["2610.99992", "2610.99991"]


def test_weekly_archive_uses_chronological_order_after_backfill_and_initialization(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    publish_week(root, WEEK)
    earlier_week = "2026-W43"
    queue_weekly_picks(root, earlier_week)
    publish_week(root, earlier_week)
    path = root / "site/weekly/index.html"
    html = path.read_text()
    assert html.index(f'href="{earlier_week}.html"') < html.index(f'href="{WEEK}.html"')
    path.unlink()
    initialize_public(root)
    assert path.read_text() == html


def test_atom_publishes_daily_editions_once_and_ignores_weekly_updates(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    publish_week(root, WEEK, now="2026-11-01T23:55:00Z")
    atom = ET.parse(root / "site/feed/atom.xml").getroot()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    assert [entry.findtext("a:id", namespaces=ns) for entry in atom.findall("a:entry", ns)] == [
        "urn:follow-rsi:daily:" + DAY]
    assert atom.findtext("a:updated", namespaces=ns) == DAY + "T12:00:00Z"
    config = read_yaml(root / "site.config.yaml")
    assert atom.find("a:link[@rel='alternate']", ns).get("href") == config["base_url"].rstrip("/") + "/daily/"
    assert (root / "site/weekly" / f"{WEEK}.html").exists()
    assert json.loads((root / "site/weekly" / f"{WEEK}.json").read_text())["week"] == WEEK
    feed = json.loads((root / "site/feed/latest.json").read_text())
    assert feed["weeks"] == [WEEK] and feed["dates"] == [DAY]
    assert feed["updated_at"] == "2026-11-01T23:55:00Z"


def test_false_quick_evidence_downgraded_before_publishing(tmp_path):
    root = make_daily_repo(tmp_path)
    accept_daily(root)
    write_daily(root, lambda review: review["items"][1]["evidence_quick"].update(matched_budget={"value": "yes", "quote": "invented equal budgets"}))
    publish_day(root, DAY)
    item = json.loads((root / "site/feed/latest.json").read_text())["items"][0]
    assert item["evidence_quick"]["matched_budget"] == {"value": "unknown", "quote": None}


def test_empty_archive_is_honest_and_does_not_replace_existing_feed(tmp_path):
    root = make_daily_repo(tmp_path)
    initialize_public(root)
    feed = root / "site/feed/latest.json"
    assert json.loads(feed.read_text())["items"] == []
    assert "awaiting owner review" in (root / "site/daily/index.html").read_text()
    atom = (root / "site/feed/atom.xml").read_text()
    assert '<?xml-stylesheet type="text/xsl" href="atom.xsl"?>' in atom
    assert 'rel="related"' in atom and "/pulls" in atom
    assert "<entry>" not in atom and (root / "site/feed/atom.xsl").exists()
    before = feed.read_bytes()
    initialize_public(root)
    assert before == feed.read_bytes()
    ready_week(root)
    before = feed.read_bytes()
    initialize_public(root)
    assert before == feed.read_bytes()


def test_feed_uses_four_calendar_weeks_and_removes_retracted_items(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    publish_week(root, WEEK)
    manifest = json.loads((root / "site/weekly" / f"{WEEK}.json").read_text())
    older = {**manifest, "week": "2026-W40"}
    boundary = {**manifest, "week": "2026-W41"}
    middle = {**manifest, "week": "2026-W42"}
    result = _write_feed(root, [manifest, older, middle, boundary],
                         {"base_url": None, "author_name": "Owner"}, {"arxiv:2610.99991"})
    assert result["weeks"] == ["2026-W41", "2026-W42", WEEK] and result["items"] == []


def test_private_demo_cannot_mutate_owner_queue_or_public_feed(tmp_path):
    root = make_daily_repo(tmp_path)
    initialize_public(root)
    watched = [root / "review/daily" / f"{DAY}.yaml", root / "data/feed/items.jsonl", root / "site/feed/latest.json"]
    before = [path.read_bytes() for path in watched]
    report = publish_demo(root, WEEK, render_card=False)
    assert report["demo"] and report["accepted"] == 2
    assert before == [path.read_bytes() for path in watched]
    output = Path(report["output_dir"])
    feed = json.loads((output / "site/feed/latest.json").read_text())
    assert feed["demo"] is True and feed["reviewed_only"] is False
    assert all(item["review_decision"] == "demo_autoaccept" for item in feed["items"])
    assert "演示用，自动通过" in (output / "digests" / f"{WEEK}.md").read_text()
    assert "演示用，自动通过" in (output / "daily" / f"{DAY}.md").read_text()
    assert "DEMO / 自动通过" in (output / "site/weekly" / f"digest-{WEEK}.card.html").read_text()
    assert "演示用，自动通过" in (output / "site/daily/index.html").read_text()
    with pytest.raises(ValueError, match="ignored build"):
        publish_demo(root, WEEK, output_dir=root / "site/demo", render_card=False)
    with pytest.raises(ValueError, match="demo"):
        _write_feed(root, [json.loads((output / "site/weekly" / f"{WEEK}.json").read_text())], {}, set())
    assert publish_demo(root, WEEK, render_card=False)["accepted"] == 2


def test_retractions_remove_daily_weekly_text_picks_and_cards_without_owner_changes(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    write_picks(root, picks=[{"arxiv_id": "2610.99991", "why_zh": "人工原因", "why_en": "Owner reason"}])
    publish_week(root, WEEK)
    paths = [root / "review" / f"{WEEK}.yaml", root / "review/daily" / f"{DAY}.yaml"]
    before = [path.read_bytes() for path in paths]
    card = root / "site/cards" / f"digest-{WEEK}.png"
    card.parent.mkdir()
    card.write_bytes(b"old card fixture")
    item = next(item for item in load_items(root) if item["id"] == "arxiv:2610.99991")
    item["retracted"] = True
    save_items(root, [item])
    result = remove_retracted(root, now="2026-11-02T10:00:00Z")
    assert result["removed"] == 1 and result["weeks"] == [WEEK] and result["dates"] == [DAY]
    assert not card.exists() and before == [path.read_bytes() for path in paths]
    assert json.loads((root / "site/feed/latest.json").read_text())["items"] == []
    assert item["title"] not in (root / "site/weekly" / f"{WEEK}.html").read_text()
    assert item["title"] not in (root / "site/daily/index.html").read_text()
    assert item["title"] not in (root / "daily" / f"{DAY}.en.md").read_text()
    assert "Owner's picks" not in (root / "digests" / f"{WEEK}.en.md").read_text()
    assert remove_retracted(root)["removed"] == 0


def test_new_daily_version_updates_feed_and_latest_page_without_rewriting_previous_day(tmp_path):
    root = make_daily_repo(tmp_path)
    ready_week(root)
    # A backfilled earlier edition may be published after the next edition.
    publish_day(root, DAY, now=NEXT + "T18:00:00Z")
    first_page = (root / "site/daily" / f"{DAY}.html").read_bytes()
    item = next(item for item in load_items(root) if item["id"] == "arxiv:2610.99991")
    item.update(version=2, title="Revised Fixture: Persistent Skill Evolution")
    save_items(root, [item])
    queue_daily_review(root, NEXT)
    write_daily(root, lambda review: review["items"][0].update(decision="accept"), date=NEXT)
    apply_daily_review(root, NEXT)
    publish_day(root, NEXT, now=NEXT + "T12:00:00Z")
    feed = json.loads((root / "site/feed/latest.json").read_text())
    assert len(feed["items"]) == 1 and feed["items"][0]["version"] == 2
    assert feed["items"][0]["review_date"] == NEXT and feed["dates"] == [DAY, NEXT]
    latest = (root / "site/daily/index.html").read_text()
    assert "<h3>Revised Fixture</h3>" in latest
    assert latest.index(f'href="{DAY}.html"') < latest.index(f'href="{NEXT}.html"')
    assert (root / "site/daily" / f"{DAY}.html").read_bytes() == first_page
    publish_week(root, WEEK)
    manifest = json.loads((root / "site/weekly" / f"{WEEK}.json").read_text())
    assert len(manifest["items"]) == 1 and manifest["items"][0]["version"] == 2
    atom = ET.parse(root / "site/feed/atom.xml").getroot()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    assert [entry.findtext("a:id", namespaces=ns) for entry in atom.findall("a:entry", ns)] == [
        "urn:follow-rsi:daily:" + DAY, "urn:follow-rsi:daily:" + NEXT]
    assert atom.findtext("a:updated", namespaces=ns) == NEXT + "T18:00:00Z"


def test_metrics_exclude_deferred_include_and_use_first_daily_publication(tmp_path):
    root = make_daily_repo(tmp_path)
    item = next(item for item in load_items(root) if item["id"] == "arxiv:2610.99992")
    item["llm"]["label"] = "include"
    save_items(root, [item])
    queue_daily_review(root, DAY)
    accept_daily(root)
    write_daily(root, lambda review: next(row for row in review["items"] if row["arxiv_id"] == "2610.99992").update(decision="defer"))
    apply_daily_review(root, DAY, now=DAY + "T10:00:00Z")
    publish_day(root, DAY, now=DAY + "T12:00:00Z")
    queue_weekly_picks(root, WEEK)
    publish_week(root, WEEK, now="2026-11-01T23:55:00Z")
    metrics = json.loads((root / "data/feed/metrics.json").read_text())["weeks"][WEEK]
    assert metrics["precision"] == 1
    assert metrics["latency_days"] == pytest.approx(26 / 24)
