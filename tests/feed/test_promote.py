from scripts.common import FIELDS, read_yaml
from scripts.feed.promote import promote_candidates
from scripts.feed.storage import load_items, save_items
from test_daily import DAY, accept_daily as accept_one, make_daily_repo as make_repo, write_daily as write_review


def test_candidate_proposal_preserves_canonical_yaml_and_all_unknown_evidence(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    before = (root / "data/papers.yaml").read_bytes()
    result = promote_candidates(root, date=DAY)
    assert result["count"] == 1
    assert result["branch"] == "feed/candidates-" + DAY
    assert (root / "data/papers.yaml").read_bytes() == before
    proposal = read_yaml(result["papers_path"])
    candidate = proposal["papers"][0]
    assert candidate["status"] == candidate["section"][:-1] == "candidate"
    assert candidate["needs_reading"] is True
    assert candidate["evidence"] == {field: "unknown" for field in FIELDS}
    assert "held_out: yes" in open(result["body_path"]).read()


def test_explicit_false_and_non_harness_papers_do_not_promote(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    write_review(root, lambda review: review["items"][1].update(promote_to_repo=False))
    assert promote_candidates(root, date=DAY)["count"] == 0
    write_review(root, lambda review: review["items"][1].update(promote_to_repo=True, direction_override={"primary": "evaluation_benchmark", "secondary": ["harness"]}))
    assert promote_candidates(root, date=DAY)["count"] == 0


def test_existing_arxiv_is_not_duplicated(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    result = promote_candidates(root, date=DAY)
    proposed = open(result["papers_path"]).read()
    (root / "data/papers.yaml").write_text(proposed)
    assert promote_candidates(root, date=DAY)["count"] == 0


def test_owner_authored_english_has_honest_provenance_in_staged_catalog(tmp_path):
    root = make_repo(tmp_path)
    accept_one(root)
    write_review(root, lambda review: review["items"][1].update(summary_override={
        "summary_zh": "人工核查：留出任务达到 20%。", "summary_en": "Owner review: held-out tasks reach 20%."}))
    result = promote_candidates(root, date=DAY)
    candidate = read_yaml(result["papers_path"])["papers"][0]
    assert candidate["en_machine_translated"] is False
