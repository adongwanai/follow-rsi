"""Save newly observed official posts for independent reading, without scope labels."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import time
import requests
from bs4 import BeautifulSoup

R = Path.cwd()
W = R / 'build/maintenance-2026-11-16/source-intake'
D = W / 'post-fulltexts'
D.mkdir(exist_ok=True)
proposal = json.loads((W / 'integration-proposal.json').read_text())
records = [x['record'] for x in proposal['new_items'] if x['record']['kind'] == 'post']
records.sort(key=lambda x: (not any(term in x['id'] for term in ['control-room','coderabbit']), x['id']))
for record in records:
    url = record['links']['url']
    slug = url.rstrip('/').rsplit('/', 1)[-1]
    dest = D / (slug + '.html')
    receipt = D / (slug + '.receipt.json')
    if receipt.exists():
        continue
    row = {'id': record['id'], 'title_from_official_feed': record['title'],
           'request_url': url, 'requested_at': datetime.now(timezone.utc).isoformat()}
    try:
        response = requests.get(url, headers={'User-Agent':'FollowRSI/0.1 (official source verification)'}, timeout=30)
        dest.write_bytes(response.content)
        row.update(http_status=response.status_code, final_url=response.url,
                   body_path=str(dest.relative_to(R)), body_sha256=hashlib.sha256(response.content).hexdigest(),
                   bytes=len(response.content), content_type=response.headers.get('Content-Type'))
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for tag in soup(['script','style','nav','footer']):
                tag.decompose()
            main = soup.find('main') or soup
            text = main.get_text(' ', strip=True)
            path = D / (slug + '.txt')
            path.write_text(text)
            row.update(text_path=str(path.relative_to(R)), text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                       text_characters=len(text), title=soup.title.get_text(' ',strip=True) if soup.title else None)
        else:
            row['error'] = f'HTTP {response.status_code}; no fulltext derived'
    except requests.RequestException as error:
        row['error'] = f'{type(error).__name__}: {error}'
    row['finished_at'] = datetime.now(timezone.utc).isoformat()
    receipt.write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(row,ensure_ascii=False),flush=True)
    time.sleep(1.1)
