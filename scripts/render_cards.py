"""Optional media step: pip install playwright; playwright install chromium.

All page requests are local. No fonts, paper data, or QR images are fetched.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
from threading import Thread

from playwright.sync_api import sync_playwright

from common import ROOT, read_yaml


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress routine HTTP access logs; browser failures still fail the run.


def render(root, ids=None):
    papers = read_yaml(root / 'data/papers.yaml')['papers']
    chosen = [p for p in papers if ids is None or p['id'] in ids]
    if ids and set(ids) - {p['id'] for p in chosen}:
        raise ValueError('Unknown paper ID requested')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(root / 'site')))
    Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}'
    output = root / 'site/cards'
    output.mkdir(exist_ok=True)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={'width':1080,'height':1350}, device_scale_factor=1, color_scheme='light')
            page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(url + '/') else route.abort())
            for p in chosen:
                page.goto(url + '/card.html?id=' + p['id'])
                page.wait_for_selector('html[data-card-ready="true"]')
                assert page.locator('#card').evaluate('(el) => el.scrollHeight <= el.clientHeight && el.scrollWidth <= el.clientWidth'), p['id']
                page.locator('#card').screenshot(path=str(output / (p['id'] + '.png')), animations='disabled')
            page.set_viewport_size({'width':1280,'height':640})
            page.goto(url + '/card.html?og=1')
            page.wait_for_selector('html[data-card-ready="true"]')
            page.locator('#card').screenshot(path=str(root / 'site/og.png'), animations='disabled')
            browser.close()
        shutil.copyfile(root / 'site/og.png', root / 'assets/social-preview.png')
    finally:
        server.shutdown()
        server.server_close()
    print(f'Rendered {len(chosen)} cards and the 1280×640 social preview.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--ids', nargs='+')
    args = parser.parse_args()
    render(args.root, args.ids)
