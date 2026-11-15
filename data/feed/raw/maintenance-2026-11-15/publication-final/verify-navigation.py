from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,subprocess
from scripts.feed.storage import write_json
r=Path.cwd();b=r/'build/maintenance-2026-11-15';base=json.loads((b/'preservation-baseline.json').read_text())
names=[n for n in base['daily_pages'] if Path(n).stem not in ['2026-11-11','2026-11-12']]
names.extend(str(p.relative_to(r)) for p in (r/'site/recaps').glob('*.html'))
rows=[];shared=None
for name in names:
 old=subprocess.check_output(['git','show',base['base_commit']+':'+name]);current=(r/name).read_bytes();text=old.decode()
 def line(tag,day):
  values=re.findall(r'^<'+tag+r'[^\n]*\.\./daily/'+day+r'\.html[^\n]*$',text,re.M)
  assert len(values)==1,(name,tag,day)
  return values[0]
 opt=line('option','2026-11-14');a11=line('a','2026-11-11');a12=line('a','2026-11-12');a14=line('a','2026-11-14')
 new12='<a href="../daily/2026-11-12.html">2026-11-12 <small>3 <span class="zh">篇</span><span class="en">papers</span></small></a>'
 replacements=[{'before':opt,'after':opt+'\n\n\n'+opt.replace(' selected','').replace('2026-11-14','2026-11-15')},
  {'before':a11,'after':a11.replace('<small>1 ','<small>5 ')},
  {'before':a12,'after':new12},
  {'before':a14,'after':a14+'\n\n\n'+a14.replace(' aria-current="page"','').replace('2026-11-14','2026-11-15')}]
 for rep in replacements:
  assert text.count(rep['before'])==1 and rep['after']!=rep['before'];text=text.replace(rep['before'],rep['after'],1)
 assert current==text.encode(),name
 assert old.split(b'<main id="publication-main">',1)[1]==current.split(b'<main id="publication-main">',1)[1],name
 row={'path':name,'before_sha256':hashlib.sha256(old).hexdigest(),'after_sha256':hashlib.sha256(current).hexdigest(),'publication_main_bytes_preserved':True}
 if shared is None:shared=replacements
 elif replacements!=shared:row['exact_replacements']=replacements
 rows.append(row)
write_json(b/'navigation-update-receipt.json',{'verified_at':datetime.now(timezone.utc).isoformat(),'base_commit':base['base_commit'],'passed':True,'exact_replacements':shared,'files':rows,'validation_refinement':'Uniform-option/link assumptions failed on the old Nov14 page because its current-day option is selected and its anchor has aria-current. Final per-file exact replacements preserve both attributes. Publication data was not changed to satisfy the check.','boundary':'Only shared navigation changes on these prior pages: the new Nov15 option/link and Nov11/Nov12 supplement counts. All original publication-main bytes, including the Oct27 withdrawal notice, are preserved; complete HTML bytes have changed.'})
print({'navigation_only_pages':len(rows),'replacements_per_page':4,'old_publication_bodies_preserved':True})
