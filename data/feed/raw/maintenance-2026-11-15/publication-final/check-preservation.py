from pathlib import Path
import hashlib,json,re,subprocess,sys
from scripts.feed.storage import load_items,write_json
from scripts.feed.review import source_hash
R=Path.cwd();B=R/'build/maintenance-2026-11-15';D=R/'docs/internal/reports/maintenance-2026-11-15'
baseline=json.loads((B/'preservation-baseline.json').read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
    names=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],text=True).split('\0')
    return {n:digest(R/n) for n in names if n and (R/n).is_file()}
before=snapshot();subprocess.run(['.venv/bin/python','scripts/build.py'],check=True)
assert snapshot()==before,'Build is not idempotent'
for name,authored in baseline['readme'].items():
    assert re.sub(r'(<!-- AUTO:[A-Z_]+:START -->).*?(<!-- AUTO:[A-Z_]+:END -->)',r'\1\2',(R/name).read_text(),flags=re.S)==authored,name
for group in ['daily_manifests','daily_markdown','daily_reviews','daily_provenance']:
    for name,sha in baseline[group].items():
        if Path(name).name.split('.')[0] in {'2026-11-11','2026-11-12'}:
            assert digest(D/'prior-editions'/name)==sha,name
        else:
            assert digest(R/name)==sha,name
for group in ['weekly','cards']:
    for name,sha in baseline[group].items():assert digest(R/name)==sha,name
manifest=json.loads((D/'raw-file-manifest.json').read_text());assert len(manifest['files'])==manifest['count']
for row in manifest['files']:
    p=R/row['path'];assert digest(p)==row['sha256'] and p.stat().st_size==row['bytes'],row['path']
secrets=[]
for line in (R/'.env.local').read_text().splitlines():
    key,sep,value=line.strip().removeprefix('export ').partition('=');value=value.strip().strip('\"\'')
    if sep and any(s in key.upper() for s in ['KEY','TOKEN','SECRET']) and len(value)>=20:secrets.append(value.encode())
changed=subprocess.check_output(['git','diff','--name-only','-z',baseline['base_commit']],text=True).split('\0')
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],text=True).split('\0')
scan=sorted({n for n in changed+untracked if n and (R/n).is_file()})
for name in scan:
    data=(R/name).read_bytes();assert not any(s in data for s in secrets),'Private value found in '+name
    assert 'balance-private' not in name and not Path(name).name.startswith('.env'),name
old={x['id']:x for x in map(json.loads,(B/'source-intake/canonical-baseline.jsonl').read_text().splitlines())}
current={x['id']:x for x in load_items(R)};assert len(old)==2074 and len(current)==2090
source_only={'arxiv:2611.16009','arxiv:2611.16409'}
formal={x['id'] for x in json.loads((B/'review-preflight.json').read_text())['new_or_changed_decisions'] if x['apply_to_canonical']}
for ident,prior in old.items():
    allowed={'source_hits'} if ident in source_only else set()
    if ident in formal:allowed|={'review','review_history'}
    delta={k for k in prior.keys()|current[ident].keys() if prior.get(k)!=current[ident].get(k)}
    assert delta<=allowed,(ident,delta-allowed)
    assert current[ident]['first_seen']==prior['first_seen'] and current[ident]['version']==prior['version'],ident
    assert source_hash(current[ident])==source_hash(prior),ident
old_item=json.loads((B/'prior-public-item-preservation.json').read_text());assert old_item['old_public_item_restored_exactly']
original_manifest=json.loads((D/'prior-editions/site/daily/2026-11-11.json').read_text())
original=next(x for x in original_manifest['items'] if x['id']==old_item['id'])
now=next(x for x in json.loads((R/'site/daily/2026-11-11.json').read_text())['items'] if x['id']==old_item['id'])
assert original==now
navigation=json.loads((B/'navigation-update-receipt.json').read_text());assert navigation['passed']
for row in navigation['files']:
    name=row['path'];original=subprocess.check_output(['git','show',baseline['base_commit']+':'+name])
    assert hashlib.sha256(original).hexdigest()==row['before_sha256']
    text=original.decode()
    for replacement in row.get('exact_replacements',navigation['exact_replacements']):
        assert text.count(replacement['before'])==1,(name,replacement['before'])
        text=text.replace(replacement['before'],replacement['after'],1)
    assert text.encode()==(R/name).read_bytes(),name
    assert digest(R/name)==row['after_sha256']
report={'checked_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
    'build_idempotent':True,'authored_readme_unchanged':True,'weekly_and_cards_unchanged':True,
    'prior_daily_manifests_and_markdown_preserved_except_archived_Nov11_Nov12_supplements':True,
    'prior_reviews_and_provenance_archived':True,'old_WICL_public_item_preserved_exactly':True,
    'old_14256_canonical_review_not_reapplied':current['arxiv:2611.14256']==old['arxiv:2611.14256'],
    'raw_sha256_verified':manifest['count'],'private_value_scan_passed':True,'scanned_changed_files':len(scan),
    'canonical_count':len(current),'all_old_first_seen_versions_and_scientific_fields_preserved':True,
    'old_html_shared_navigation_only':{'files':len(navigation['files']),'proof':'navigation-update-receipt.json','whole_html_bytes_unchanged':False,'publication_body_preserved':True},
    'scope':'Engineering, source binding and publication preservation, not model quality evaluation or experimental reproduction.'}
write_json(B/'preservation-post-review.json',report);write_json(D/'preservation-post-review.json',report)
print(json.dumps(report,ensure_ascii=False))
