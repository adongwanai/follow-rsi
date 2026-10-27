"""Optional offline browser acceptance and reference comparison screenshots."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright, expect
from common import ROOT


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def verify_map(page, stats):
    page.locator('[data-view="map"]').click()
    expect(page.locator('[data-map-total]')).to_have_text(str(stats['included']))
    assert page.locator('[data-map-row]').evaluate_all('(rows)=>rows.map(row=>row.dataset.mapRow)') == [
        'objects', 'cooperation', 'applications', 'support', 'cross']
    for row, count in [('objects', 7), ('cooperation', 3), ('applications', 5), ('support', 4), ('cross', 5)]:
        expect(page.locator(f'[data-map-row="{row}"] .map-tile')).to_have_count(count)
    sections = ['evolve_main', 'generalize', 'evidence_selection', 'improver', 'component', 'coevolution']
    expect(page.locator('.map-subdirections button')).to_have_count(len(sections))
    for section in sections:
        control = page.locator(f'.map-subdirections [data-map-section="{section}"]')
        expect(control.locator('b')).to_have_text(str(stats['sections'][section]))
        control.click()
        expect(page.locator('[data-view="papers"]')).to_have_attribute('aria-current', 'page')
        expect(page.locator('.row')).to_have_count(stats['sections'][section])
        assert page.locator('.row').evaluate_all(
            '(rows, section)=>rows.every(row=>HARNESS_DATA.papers.find(p=>p.id===row.dataset.open).section===section)', section)
        page.locator('[data-view="map"]').click()
    expect(page.locator('.map-planned')).to_have_count(6)
    page.locator('.map-planned .map-title-button').first.click()
    expect(page.locator('#map-vote')).to_be_visible()
    expected_discussions = page.evaluate('HARNESS_DATA.config.repository_url.replace(/\\/$/, "") + "/discussions"')
    expect(page.locator('#map-vote a')).to_have_attribute('href', expected_discussions)
    page.locator('.map-examples [data-open="hsi"]').click()
    expect(page.locator('#dtitle')).to_contain_text('Hierarchical Self-Improvement')
    page.locator('#dclose').click()
    expect(page.locator('[data-view="map"]')).to_have_attribute('aria-current', 'page')
    page.locator('.map-count').click()
    expect(page.locator('.row')).to_have_count(stats['included'])


def verify(output=None):
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    output = output or ROOT / 'docs/screenshots'
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
            stats = page.evaluate('HARNESS_DATA.stats')
            expect(page.locator('#result-count')).to_contain_text(f"{stats['must_read']} / {stats['included']}")
            assert page.locator('[data-view]').evaluate_all('(buttons)=>buttons.map(b=>b.dataset.view)') == ['papers', 'map', 'routes', 'gaps']
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
                expect(page.locator('#result-count')).to_contain_text(f"{stats['included']} / {stats['included']}")
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
            verify_map(page, stats)
            page.locator('[data-view="map"]').click()
            page.locator('[data-view="routes"]').click()
            page.go_back()
            expect(page.locator('[data-view="map"]')).to_have_attribute('aria-current', 'page')
            page.go_forward()
            expect(page.locator('[data-view="routes"]')).to_have_attribute('aria-current', 'page')
            checks.append('map layout, live counts, six direction filters, representative papers and browser history')
            context.close()
            sandbox_context = browser.new_context(viewport={'width':1280, 'height':960})
            sandbox_context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
            sandbox_page = sandbox_context.new_page()
            sandbox_page.on('pageerror', lambda error: errors.append(str(error)))
            sandbox_page.set_content('<iframe id="preview" sandbox="allow-scripts" style="width:100%;height:900px;border:0"></iframe>')
            source = (ROOT / 'site/index.html').read_text().replace('<head>', f'<head><base href="{base}/site/">', 1)
            sandbox_page.locator('#preview').evaluate('(frame, source)=>frame.srcdoc=source', source)
            frame = sandbox_page.frame_locator('#preview')
            expect(frame.locator('#result-count')).to_contain_text(f"{stats['must_read']} / {stats['included']}")
            sandbox = sandbox_page.locator('#preview').element_handle().content_frame()
            assert sandbox.evaluate('''() => {
                try { localStorage.getItem('harness.lang'); return false; }
                catch (error) { return error.name === 'SecurityError'; }
            }''')
            assert sandbox.evaluate('''() => {
                try { history.replaceState(null, '', '#blocked'); return false; }
                catch (error) { return error.name === 'SecurityError'; }
            }''')
            for target, content in [('map', '.map-focus'), ('routes', '.route'), ('gaps', '.gap'), ('papers', '.row')]:
                frame.locator(f'[data-view="{target}"]').click()
                expect(frame.locator(content).first).to_be_visible()
                expect(frame.locator(f'[data-view="{target}"]')).to_have_attribute('aria-current', 'page')
            frame.locator('[data-open="hda"]').first.click()
            expect(frame.locator('#drawer')).to_be_visible()
            frame.locator('#copy').click()
            public_base = sandbox.evaluate('HARNESS_DATA.config.base_url')
            expect(frame.locator('#copymsg')).to_contain_text(public_base.rstrip('/') + '/p/hda.html')
            for unavailable in ('', 'about:srcdoc'):
                sandbox.evaluate('(value)=>HARNESS_DATA.config.base_url=value', unavailable)
                frame.locator('#copy').click()
                expect(frame.locator('#copymsg')).to_contain_text('请从已发布的网站复制分享链接')
            sandbox.evaluate('(value)=>HARNESS_DATA.config.base_url=value', public_base)
            frame.locator('#next').click()
            expect(frame.locator('#dtitle')).not_to_contain_text('Harness-Delta Attribution')
            frame.locator('#prev').click()
            expect(frame.locator('#dtitle')).to_contain_text('Harness-Delta Attribution')
            frame.locator('#dclose').click()
            expect(frame.locator('#drawer')).not_to_be_visible()
            frame.locator('#lang').click()
            expect(frame.locator('#result-count')).to_contain_text('Showing')
            frame.locator('#theme').click()
            verify_map(sandbox, stats)
            sandbox_context.close()
            checks.append('opaque sandbox srcdoc: all views, drawer navigation/close/copy, unavailable URL, language and theme')
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
                        if variant=='site':
                            for language in ('zh', 'en'):
                                if shot.locator('html').get_attribute('lang') != ('zh-CN' if language=='zh' else 'en'):
                                    shot.locator('#lang').click()
                                shot.locator('[data-view="map"]').click()
                                expect(shot.locator('[data-map-total]')).to_have_text(str(stats['included']))
                                assert shot.evaluate('document.documentElement.scrollWidth<=innerWidth'), ('map',width,theme,language)
                                assert shot.locator('.map-tile').evaluate_all('(tiles)=>tiles.every(tile=>tile.scrollWidth<=tile.clientWidth)'), ('map tile',width,theme,language)
                                map_filename=f'map-{width}-{theme}-{language}.png'
                                shot.screenshot(path=str(output/map_filename),full_page=True,animations='disabled')
                                comparisons.append(('map '+language,width,theme,map_filename))
                        ctx.close()
            browser.close()
        assert not errors, errors
        checks.append('1280/400 light/dark, bilingual map without overflow, accessible evidence labels')
        html='<!doctype html><meta charset="utf-8"><title>Reference and implementation</title><style>body{font:14px system-ui;margin:30px;background:#eceef2}main{display:grid;grid-template-columns:1fr 1fr;gap:24px}img{width:100%;border:1px solid #bbc}h1{font-size:24px}</style><h1>Reference → implementation · 1280 / 400 · light / dark</h1><p>The site retains the ledger palette and receipt design. New filters, bilingual navigation and publication activity intentionally extend the reference.</p><main>'
        html+=''.join(f'<figure><figcaption>{variant} · {width}px · {theme}</figcaption><img src="{filename}"></figure>' for variant,width,theme,filename in comparisons)+'</main>'
        (output/'index.html').write_text(html)
        (output/'verification.json').write_text(json.dumps({'status':'passed','checks':checks,'console_errors':errors},ensure_ascii=False,indent=2)+'\n')
        print(f'Browser acceptance passed: {len(checks)} groups; {len(comparisons)} screenshots in {output}.')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional screenshot/report directory')
    verify(parser.parse_args().output)
