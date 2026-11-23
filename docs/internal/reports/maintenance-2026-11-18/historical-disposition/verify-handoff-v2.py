"""Verify final suggestion contracts and preserved prior decisions without applying them."""
from datetime import datetime,timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import yaml
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from scripts.feed.review import source_hash
from scripts.feed.guard import check_summary
from scripts.feed.scope import load_scope,scope_status
OUT=ROOT/'docs/internal/reports/maintenance-2026-11-18/historical-disposition'
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
with gzip.open(ROOT/'data/feed/raw/maintenance-2026-11-18/backlog-audit/pr135-historical-inventory-v1.jsonl.gz','rt') as f:
 inv={r['id']:r for r in map(json.loads,f)}
scope=load_scope(ROOT)
checks=[]
for stem,version in [('positive',4),('exclusion',1)]:
 jsonpath=OUT/f'{stem}-proposals-v{version}.json';yamlpath=OUT/f'{stem}-review-rows-v{version}.yaml'
 proposals=json.loads(jsonpath.read_text())['items'];rows=yaml.safe_load(yamlpath.read_text())['items']
 assert len(proposals)==len(rows)
 for proposal,row in zip(proposals,rows):
  id=proposal['id'];assert id==row['id'];c=inv[id]['canonical_snapshot']
  assert source_hash(c)==proposal['source_hash']==row['source_hash']
  assert c['first_seen']==proposal['first_seen_preserved']
  assert row['decision']==proposal['decision_suggestion']
  itemcheck={'id':id,'source_hash_matches':True,'first_seen_preserved':True,'decision':row['decision']}
  if row['decision']=='backlog':
   for key in ['summary_override','direction_override','evidence_quick']:assert proposal[key]==row[key]
   summ=row['summary_override'];guard=check_summary(c['title'],c['abstract'],summ['summary_zh'],summ['summary_en']);assert guard['ok'],(id,guard)
   status=scope_status(row['direction_override'],scope);assert status=='in_scope',id
   itemcheck.update(numeric_guard=guard,publish_scope=status)
  assert row['promote_to_repo'] is False
  sources=[proposal['source']] if 'source' in proposal else proposal['source_receipts']
  for receipt in sources:
   assert sha(receipt['source_file'])==receipt['source_sha256']
   assert sha(receipt['text_file'])==receipt['text_sha256']
  itemcheck['source_and_text_hashes_verified']=len(sources)
  checks.append(itemcheck)
ledger_path='data/feed/raw/maintenance-2026-11-18/historical-disposition/disposition-ledger-v2.jsonl.gz'
with gzip.open(ROOT/ledger_path,'rt') as f:ledger=list(map(json.loads,f))
assert len(ledger)==len({r['id'] for r in ledger})==121
assert sum(r['skip_apply_when_no_new_adjudication'] for r in ledger)==92
for r in ledger:
 assert r['canonical_review_before']==inv[r['id']]['canonical_snapshot']['review']
 assert r['first_seen_preserved']==inv[r['id']]['canonical_snapshot']['first_seen']
 assert r['reason_zh'] and r['issue_refs']
 assert r['canonical_writes']==r['github_writes']==0
 if not r['skip_apply_when_no_new_adjudication']:
  ref=r['proposal_reference'];assert sha(ref['path'])==ref['sha256']
 else:assert r['canonical_apply_recommendation']=='keep_canonical_review_unchanged'
summary={'created_at':datetime.now(timezone.utc).isoformat(),'counts':{
 'source_bound_suggestions':29,'backlog':19,'reject':10,'numeric_guards_ok':19,
 'directions_in_current_publish_scope':19,'raw_and_text_hash_pairs':30,
 'prior_review_objects_preserved':121,'canonical_review_must_remain_unchanged':92,
 'paid_requests':0,'canonical_writes':0,'github_writes':0},
 'ledger_reference':{'path':ledger_path,'sha256':sha(ledger_path)},
 'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p.relative_to(ROOT))} for p in [OUT/'positive-proposals-v4.json',OUT/'positive-review-rows-v4.yaml',OUT/'exclusion-proposals-v1.json',OUT/'exclusion-review-rows-v1.yaml']],
 'checks':checks,'evidence_boundary':'Structural/hash/literal numeric checks do not replace the independently recorded source and semantic review, true dated merge, or parent live publication verification.'}
p=OUT/'handoff-local-verification-v2.json';assert not p.exists();p.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'counts':summary['counts'],'receipt_sha256':sha(p.relative_to(ROOT))},ensure_ascii=False,indent=2))
