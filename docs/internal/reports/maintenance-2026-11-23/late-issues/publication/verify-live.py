from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import json,hashlib,urllib.request,urllib.error,xml.etree.ElementTree as ET,subprocess
R=Path.cwd();D=R/'docs/internal/reports/maintenance-2026-11-23/publication-final';B=R/'build/maintenance-2026-11-23';BASE='https://adongwanai.github.io/follow-rsi/'
paths=[f'daily/2026-11-{day}.{suffix}' for day in ('18','19','20','21','22','23') for suffix in ('json','html')]
paths+=['daily/index.html','weekly/2026-W47.json','weekly/2026-W47.html','weekly/index.html','recaps/2026-11-23--2026-11-23.json','recaps/2026-11-23--2026-11-23.html','feed/latest.json','feed/atom.xml','feed/status.json','index.html','data.js','papers.json','daily/2026-10-27.html','daily/2026-11-12.json','daily/2026-11-11.json','daily/2026-11-16.json','daily/2026-11-17.json','weekly/2026-W46.json','recaps/2026-11-16--2026-11-18.json','p/self-evolving-multi-task.html','p/audit-the-scaffold.html']
card=json.loads((D/'v2-card-check.json').read_text())
paths += [p['path'].removeprefix('site/') for p in card['files'] if p['path'].startswith('site/') and p['path'].endswith('.png')]
paths=list(dict.fromkeys(paths));targets=[(BASE+p,R/'site'/p) for p in paths]
targets += [(BASE+p,R/'site'/local) for p,local in [('', 'index.html'),('daily/','daily/index.html'),('weekly/','weekly/index.html')]]
targets += [('https://raw.githubusercontent.com/adongwanai/follow-rsi/main/'+p,R/p) for p in ('README.md','README_en.md')]
assert all(p.is_file() for _,p in targets)
sha=lambda b:hashlib.sha256(b).hexdigest()
def fetch(target):
 url,p=target;r={'url':url,'local_path':str(p.relative_to(R)),'observed_at':datetime.now(timezone.utc).isoformat(),'expected_sha256':sha(p.read_bytes())}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache'}),timeout=35) as response:
   b=response.read();r.update(http_status=response.status,final_url=response.url,bytes=len(b),sha256=sha(b))
 except (urllib.error.URLError,TimeoutError) as e:
  r.update(error_type=type(e).__name__,error=str(e),bytes_match=False);return r,None
 r['bytes_match']=r['sha256']==r['expected_sha256'];return r,b
with ThreadPoolExecutor(max_workers=6) as pool:fetched=list(pool.map(fetch,targets))
receipts=[r for r,_ in fetched];bodies={r['local_path']:b for r,b in fetched if b is not None};checks={'all_public_bytes_match':all(r['bytes_match'] for r in receipts)}
if checks['all_public_bytes_match']:
 feed=json.loads(bodies['site/feed/latest.json']);days={r['date']:r for r in feed['daily_editions']};wanted={f'2026-11-{d}':n for d,n in [('18',7),('19',10),('20',10),('21',0),('22',0),('23',0)]}
 checks['all_six_daily_counts_and_review_dates']=all(days[d]['paper_count']==n and days[d]['reviewed_on']=='2026-11-23' for d,n in wanted.items())
 checks['three_status_bulletins']=all(days[f'2026-11-{d}']['kind']=='daily_status' for d in ('21','22','23'))
 checks['three_delayed_paper_editions']=all(len(json.loads(bodies[f'site/daily/{d}.json'])['items'])==n for d,n in wanted.items() if n)
 checks['prior_nov18_timestamp_preserved']=json.loads(bodies['site/daily/2026-11-18.json'])['published_at']==json.loads((D/'prior-nov18-observed-status.json').read_text())['published_at']
 recap=json.loads(bodies['site/recaps/2026-11-23--2026-11-23.json']);checks['four_historical_additions']=recap['kind']=='retrospective' and len(recap['items'])==4 and all(r['news_date']<'2026-11-23' and r['review_date']=='2026-11-23' for r in recap['items'])
 w=json.loads(bodies['site/weekly/2026-W47.json']);checks['w47_34_daily_33_prior_historical']=len(w['items'])==34 and len(w['backlog'])==33 and not ({r['id'] for r in w['items']}&{r['id'] for r in w['backlog']})
 status=json.loads(bodies['site/feed/status.json']);checks['status_is_current_12_source_snapshot']=status['checked_at'].startswith('2026-11-23') and sum(r['enabled'] for r in status['sources'].values())==12 and status['sources']['hf-daily']['today_board_count']==13
 checks['s2_partial_and_failure_retained']=status['sources']['s2-citations']['availability']=='partial' and not status['sources']['s2-authors']['last_ok']
 ns={'a':'http://www.w3.org/2005/Atom'};atom=ET.fromstring(bodies['site/feed/atom.xml']);entries={e.findtext('a:id',namespaces=ns):e for e in atom.findall('a:entry',ns)}
 checks['atom_has_all_six_dates']=all('urn:follow-rsi:daily:'+d in entries for d in wanted)
 checks['atom_status_summaries_are_substantive']=all(len(entries['urn:follow-rsi:daily:2026-11-'+d].findtext('a:summary',namespaces=ns))>150 for d in ('21','22','23'))
 checks['readmes_link_latest']=all('daily/2026-11-23.html' in bodies[p].decode() and '2026-W47' in bodies[p].decode() for p in ('README.md','README_en.md'))
 checks['withdrawal_preserved']='已撤下' in bodies['site/daily/2026-10-27.html'].decode() and '2026-10-27' not in feed['dates'] and not (R/'site/daily/2026-10-27.json').exists()
 home=json.loads(bodies['site/data.js'].decode().removeprefix('window.HARNESS_DATA = ').rstrip().removesuffix(';'));checks['homepage_latest_nov23']=home['latest_edition']['date']=='2026-11-23'
 by={r['id']:r for r in json.loads((R/'docs/internal/reports/maintenance-2026-11-23/primary-review/final-adjudication.json').read_text())['items']}
 by.update({r['id']:r for r in json.loads((R/'docs/internal/reports/maintenance-2026-11-23/late-issues/primary-review.json').read_text())['items']})
 pub=[x for d,n in wanted.items() if n for x in json.loads(bodies[f'site/daily/{d}.json'])['items']]+recap['items']
 checks['all_31_summaries_match_independent_review']=len(pub)==31 and all(x['summary_zh']==by[x['id']]['summary_override']['summary_zh'] and x['summary_en']==by[x['id']]['summary_override']['summary_en'] for x in pub)
 checks['v2_card_public_hashes_match_review']=all(sha(bodies[f['path']])==f['sha256'] for f in card['files'] if f['path'] in bodies and (f['path'].endswith('.png') or f['path'] in ('site/p/self-evolving-multi-task.html','site/p/audit-the-scaffold.html')))
 checks['v2_card_objects_match_independent_review']=all(sha(json.dumps(next(x for x in payload['papers'] if x['id']==item['paper_id']),ensure_ascii=False,sort_keys=True).encode())==item['generated_record_sha256'] for payload in (home,json.loads(bodies['site/papers.json'])) for item in card['items'])
 checks['w47_supplement_latency_is_unknown']=w['metrics']['latency_days'] is None and '时效中位数标为待核' in w['editor_note_zh']
result={'observed_at':datetime.now(timezone.utc).isoformat(),'local_git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'requests':receipts,'checks':checks,'online_verified':all(checks.values()),'paid_generation_requests':0,'scope':'Live byte and publication-content verification; not experimental replication.'}
name='late-live-verification-'+datetime.now(timezone.utc).strftime('%H%M%S')+'.json';(B/name).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'online_verified':result['online_verified'],'checked_urls':len(receipts),'failed_checks':[k for k,v in checks.items() if not v],'mismatched_urls':[r['url'] for r in receipts if not r['bytes_match']],'receipt':str(B/name)},ensure_ascii=False))
assert result['online_verified'],'Inspect actual receipts before claiming online publication.'
(B/'late-live-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
