"""Optional offline browser acceptance and reference comparison screenshots."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from threading import Thread

from playwright.sync_api import sync_playwright, expect
from common import ROOT


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def verify():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    output = ROOT / 'docs/screenshots'
    output.mkdir(parents=True, exist_ok=True)
    errors = []
    checks = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={'width':1280, 'height':960}, color_scheme='light')
            context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base + '/site/index.html')
            expect(page.locator('#result-count')).to_contain_text('20 / 98')
            assert not page.locator('.foundations').get_attribute('open')
            first = page.locator('.row:visible').first
            pid = first.get_attribute('data-open')
            first.click()
            expect(page.locator('#drawer')).to_be_visible()
            expect(page.locator('#dclose')).to_be_focused()
            page.keyboard.press('Shift+Tab')
            assert page.evaluate('document.activeElement.closest("#drawer") !== null')
            page.keyboard.press('Escape')
            expect(page.locator(f'.row[data-open="{pid}"]')).to_be_focused()
            checks.append('drawer keyboard focus, trap and Escape return')
            page.keyboard.press('/')
            expect(page.locator('#q')).to_be_focused()
            page.locator('#clear').click()
            page.locator('#q').fill('HDA')
            expect(page.locator('.row')).to_have_count(1)
            page.locator('.row').click()
            assert page.locator('#drawer .kv').count() == 1
            assert page.locator('#drawer a[download]').get_attribute('href') == 'cards/hda.png'
            page.keyboard.press('Escape')
            page.locator('#clear').click()
            page.locator('#advanced-title').click()
            page.locator('[data-field="held_out"][data-value="yes"]').click()
            yes_ids = set(page.locator('.row').evaluate_all('(els)=>els.map(e=>e.dataset.open)'))
            page.locator('[data-field="held_out"][data-value="unknown"]').click()
            union_ids = set(page.locator('.row').evaluate_all('(els)=>els.map(e=>e.dataset.open)'))
            assert yes_ids < union_ids
            page.locator('[data-field="cross_model_transfer"][data-value="yes"]').click()
            and_ids = set(page.locator('.row').evaluate_all('(els)=>els.map(e=>e.dataset.open)'))
            assert and_ids <= union_ids
            assert all(page.evaluate('(id)=>HARNESS_DATA.papers.find(p=>p.id===id).evidence.cross_model_transfer', pid) == 'yes' for pid in and_ids)
            page.locator('[data-help="held_out"]').click()
            expect(page.locator('#help-held_out')).to_be_visible()
            before = page.locator('[data-section="all"] .n').inner_text()
            page.locator('#theme').click()
            assert page.locator('[data-section="all"] .n').inner_text() == before
            checks.append('search, OR/AND evidence filters, definitions and counts')
            page.locator('#advanced-title').click()
            page.locator('#clear').click()
            for sort in ('newest','oldest','must','evidence'):
                page.locator('#sort').select_option(sort)
                expect(page.locator('#result-count')).to_contain_text('98 / 98')
            page.locator('#lang').click()
            expect(page.locator('#result-count')).to_contain_text('Showing')
            page.reload()
            expect(page.locator('#result-count')).to_contain_text('Showing')
            checks.append('sort modes and language/theme persistence')
            page.goto(base+'/site/index.html#p-hda')
            expect(page.locator('#dtitle')).to_contain_text('Harness-Delta Attribution')
            page.keyboard.press('ArrowRight')
            expect(page.locator('#dtitle')).not_to_contain_text('Harness-Delta Attribution')
            page.keyboard.press('ArrowLeft')
            expect(page.locator('#dtitle')).to_contain_text('Harness-Delta Attribution')
            page.keyboard.press('Escape')
            page.goto(base+'/site/index.html#routes')
            expect(page.locator('.route')).to_have_count(9)
            assert page.locator('.route .step').count() == page.locator('.route time').count()
            page.goto(base+'/site/index.html#gaps')
            expect(page.locator('.gap')).to_have_count(7)
            checks.append('deep links, next/previous and numbered dated reading routes')
            assert page.locator('#weekly-link').get_attribute('href') == 'weekly/index.html'
            context.close()
            comparisons = []
            for width, height in ((1280,960),(400,900)):
                for theme in ('light','dark'):
                    for variant, path in (('reference','design/reference.html'),('site','site/index.html')):
                        ctx=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme)
                        ctx.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
                        shot=ctx.new_page()
                        shot.on('pageerror',lambda error:errors.append(str(error)))
                        shot.goto(base+'/'+path)
                        shot.evaluate('(theme)=>document.documentElement.dataset.theme=theme',theme)
                        shot.evaluate('document.fonts.ready')
                        if variant=='site':
                            assert shot.evaluate('document.documentElement.scrollWidth<=innerWidth'), (width,theme)
                            if width==400:
                                expect(shot.locator('#filter-panel')).not_to_be_visible()
                                shot.locator('#filter-open').click()
                                expect(shot.locator('#filter-panel')).to_be_visible()
                                shot.locator('#filter-open').click()
                            assert all(shot.locator('.row .ev').evaluate_all('(es)=>es.map(e=>Boolean(e.getAttribute("aria-label")))'))
                        filename=f'{variant}-{width}-{theme}.png'
                        shot.screenshot(path=str(output/filename),full_page=False,animations='disabled')
                        comparisons.append((variant,width,theme,filename))
                        ctx.close()
            browser.close()
        assert not errors, errors
        checks.append('1280/400 light/dark, no horizontal overflow, accessible evidence labels')
        html='<!doctype html><meta charset="utf-8"><title>Reference and implementation</title><style>body{font:14px system-ui;margin:30px;background:#eceef2}main{display:grid;grid-template-columns:1fr 1fr;gap:24px}img{width:100%;border:1px solid #bbc}h1{font-size:24px}</style><h1>Reference → implementation · 1280 / 400 · light / dark</h1><p>The site retains the ledger palette and receipt design. New filters, bilingual navigation and publication activity intentionally extend the reference.</p><main>'
        html+=''.join(f'<figure><figcaption>{variant} · {width}px · {theme}</figcaption><img src="{filename}"></figure>' for variant,width,theme,filename in comparisons)+'</main>'
        (output/'index.html').write_text(html)
        (output/'verification.json').write_text(json.dumps({'status':'passed','checks':checks,'console_errors':errors},ensure_ascii=False,indent=2)+'\n')
        print(f'Browser acceptance passed: {len(checks)} groups; eight screenshots in docs/screenshots/.')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    verify()
