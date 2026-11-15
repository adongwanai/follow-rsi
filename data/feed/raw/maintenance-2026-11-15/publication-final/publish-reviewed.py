from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import base64
import hashlib
import json
import subprocess
import sys
import yaml
from scripts.feed.ci import merged_review_requests, human_owner_review
from scripts.feed.review import validate_daily_review, apply_daily_review, source_hash
from scripts.feed.digest import publish_day, initialize_public
from scripts.feed.storage import write_json, load_items, save_items

R=Path.cwd(); B=R/'build/maintenance-2026-11-15'; REPO='adongwanai/follow-rsi'
def gh(endpoint):
    return json.loads(subprocess.check_output(['gh','api',endpoint],text=True))
def merged_bytes(path,commit):
    obj=gh(f'repos/{REPO}/contents/{path}?ref={commit}')
    blob=gh(f'repos/{REPO}/git/blobs/{obj["sha"]}')
    return base64.b64decode(blob['content'])
def digest(data):
    return hashlib.sha256(data).hexdigest()

preflight=json.loads((B/'review-preflight.json').read_text())
expected={x['date']:x for x in preflight['reviews']}
verified=[]
for arg in sys.argv[1:]:
    number,head=arg.split(':'); number=int(number); pr=gh(f'repos/{REPO}/pulls/{number}')
    assert pr['merged'] and pr['base']['ref']=='main' and pr['head']['repo']['full_name']==REPO
    assert pr['head']['sha']==head
    pages=json.loads(subprocess.check_output(['gh','api','--paginate','--slurp',f'repos/{REPO}/pulls/{number}/files?per_page=100'],text=True))
    files=[x for page in pages for x in page]; assert len(files)==pr['changed_files']
    requests=merged_review_requests({'pull_request':pr},[x['filename'] for x in files],REPO); assert len(requests)==1
    request=requests[0]; day=request['date']; assert day in expected
    owner=human_owner_review(pr,gh(f'repos/{REPO}/pulls/{number}/reviews?per_page=100'),REPO)
    checks=gh(f'repos/{REPO}/commits/{head}/check-runs?per_page=100')['check_runs']
    for name in ['build','validate']:
        selected=[x for x in checks if x['name']==name]
        assert selected and max(selected,key=lambda x:x['id'])['conclusion']=='success',(number,name)
    statuses=gh(f'repos/{REPO}/commits/{head}/status')['statuses']
    selected=[x for x in statuses if x['context']=='Follow RSI owner decisions']
    assert selected and selected[0]['state']=='success'
    content=merged_bytes(request['path'],pr['merge_commit_sha'])
    assert content==(R/request['path']).read_bytes() and digest(content)==expected[day]['draft_sha256']
    validate_daily_review(R,day)
    verified.append({'request':request,'provenance':{'github_pr':number,'owner_login':owner,'merge_commit':pr['merge_commit_sha']},
                     'head':head,'review_sha256':digest(content),'content':content,'pr':pr})
assert {x['request']['date'] for x in verified}=={'2026-11-11','2026-11-12','2026-11-15'}

summaries=json.loads((B/'summary-draft-v3.json').read_text())
summary_review=json.loads((B/'independent/summary-review-v3.json').read_text())
assert summary_review['input']['sha256']==digest((B/'summary-draft-v3.json').read_bytes())
assert summary_review['summary_content_review_complete'] and summary_review['counts']['pass']==9
before_all={x['id']:deepcopy(x) for x in load_items(R)}
for item in summaries['items']:
    assert source_hash(before_all[item['id']])==item['source_hash_before_summary']
old_manifest=json.loads((R/'docs/internal/reports/maintenance-2026-11-15/prior-editions/site/daily/2026-11-11.json').read_text())
old_public=next(x for x in old_manifest['items'] if x['id']=='arxiv:2611.12885')
assert old_public['review_date']=='2026-11-12'

status_path=R/'data/feed/daily-status.json'; status=json.loads(status_path.read_text())
assert not any(x['date']=='2026-11-15' for x in status['days'])
status['days'].append(json.loads((B/'status-bulletin-draft.json').read_text()))
status['updated_at']=datetime.now(timezone.utc).isoformat(); write_json(status_path,status)
receipts=[]
for value in sorted(verified,key=lambda x:x['request']['date']):
    request=value['request']; day=request['date']; provenance=value['provenance']; content=value['content']
    write_json(R/'data/feed/review-provenance'/f'{day}.json',{**request,**provenance})
    full=validate_daily_review(R,day); selected=set(expected[day]['changed_ids_only_to_apply']); subset=deepcopy(full)
    for group in ['items','lab_updates']:
        subset[group]=[x for x in full[group] if x['id'] in selected]
    assert {x['id'] for x in subset['items']+subset['lab_updates']}==selected
    before={x['id']:deepcopy(x) for x in load_items(R)}; histories=[]
    for key in selected:
        old=before[key]
        if old.get('review'):
            row=deepcopy(old); history=row.setdefault('review_history',[])
            if old['review'] not in history:
                history.append(deepcopy(old['review']))
            histories.append(row)
    save_items(R,histories)
    try:
        (R/request['path']).write_text(yaml.safe_dump(subset,allow_unicode=True,sort_keys=False,width=110))
        count=apply_daily_review(R,day,provenance=provenance)
    finally:
        (R/request['path']).write_bytes(content)
    after={x['id']:x for x in load_items(R)}
    assert all(after[key]==old for key,old in before.items() if key not in selected)
    assert all(after[key]['review']['source_hash']==source_hash(after[key]) for key in selected)
    result=publish_day(R,day,allow_status=True)
    if result.get('manifest'):
        result['manifest']=str(Path(result['manifest']).relative_to(R))
    if day=='2026-11-11':
        path=R/'site/daily/2026-11-11.json'; edition=json.loads(path.read_text())
        rebuilt=next(x for x in edition['items'] if x['id']==old_public['id'])
        changed=[k for k in old_public.keys()|rebuilt.keys() if old_public.get(k)!=rebuilt.get(k)]
        assert changed==['review_date'],changed
        edition['items']=[deepcopy(old_public) if x['id']==old_public['id'] else x for x in edition['items']]
        write_json(path,edition)
        assert after[old_public['id']]==before_all[old_public['id']]
        write_json(B/'prior-public-item-preservation.json',{'id':old_public['id'],'edition':'2026-11-11',
            'old_item_sha256':digest(json.dumps(old_public,sort_keys=True,ensure_ascii=False).encode()),
            'render_function_proposed_changes':changed,'old_public_item_restored_exactly':True,
            'canonical_record_preserved':True,'old_review_date':old_public['review_date'],
            'supplement_reviewed_on':'2026-11-15','not_a_new_review_of_old_item':True})
    receipt={**request,**provenance,'head':value['head'],'review_sha256':value['review_sha256'],
             'verified_at':datetime.now(timezone.utc).isoformat(),'applied_records':count,
             'applied_ids':sorted(selected),'local_generation':result,
             'application_boundary':'Exact merged review bytes and exact-head CI verified; only selected changed rows applied. Existing formal decisions and original public review dates preserved.',
             'authorization':'Owner standing automatic review/merge/publication authorization; account merge does not imply manual per-paper reading.',
             'boundary':'Locally generated from real merged review; Pages deployment and public HTTP verification remain separate.'}
    receipts.append(receipt); write_json(B/'publication-generation.json',receipts)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)
assert sum(x['applied_records'] for x in receipts)==18
initialize_public(R)
write_json(B/'publication-prerequisites.json',{
    'dated_reviews':[{'date':x['request']['date'],**x['provenance'],'head':x['head'],'review_sha256':x['review_sha256']} for x in verified],
    'source_and_summary_hashes_verified':True,'unchanged_public_item_preserved':True,
    'paid_generation_requests':0,'global_quality_warning_preserved':{'date':'2026-11-05','complete':False,'recall':0.892857,'threshold':0.90},
    'not_a_new_model_evaluation':True,'online_verified':False})
