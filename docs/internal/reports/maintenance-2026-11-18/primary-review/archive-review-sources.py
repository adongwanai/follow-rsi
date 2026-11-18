from pathlib import Path
import gzip,hashlib,json
R=Path.cwd();base=R/'data/feed/raw/maintenance-2026-11-18';rows=[]
for group in ['independent-hf16','independent-hf17','independent-other','independent-recovery']:
 for p in sorted((base/group).rglob('*')):
  if not p.is_file() or p.suffix=='.gz':continue
  b=p.read_bytes();out=p.with_name(p.name+'.gz');compressed=gzip.compress(b,mtime=0)
  if out.exists():assert out.read_bytes()==compressed
  else:out.write_bytes(compressed)
  assert gzip.decompress(out.read_bytes())==b
  rows.append({'original_path':str(p.relative_to(R)),'stored_path':str(out.relative_to(R)),'sha256_uncompressed':hashlib.sha256(b).hexdigest(),'sha256_stored':hashlib.sha256(compressed).hexdigest(),'bytes_uncompressed':len(b),'bytes_stored':len(compressed)})
p=R/'docs/internal/reports/maintenance-2026-11-18/primary-review/source-storage-index.json'
p.write_text(json.dumps({'encoding':'gzip','hash_semantics':'Original review hashes bind decompressed bytes. Original paths can be restored with gzip.decompress. No source bytes were normalized or edited.','files':rows},ensure_ascii=False,indent=2)+'\n')
# Preserve expanded copies locally for inspection without staging duplicate source bytes.
exclude=R/'.git/info/exclude';text=exclude.read_text() if exclude.exists() else ''
for row in rows:
 rule='/'+row['original_path']+'\n'
 if rule not in text:text+=rule
exclude.write_text(text)
print({'files':len(rows),'uncompressed_bytes':sum(x['bytes_uncompressed'] for x in rows),'stored_bytes':sum(x['bytes_stored'] for x in rows)})
