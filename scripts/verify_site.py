"""Local browser acceptance: public views, withdrawals, desktop/mobile and srcdoc."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from threading import Thread

from playwright.sync_api import sync_playwright, expect
from common import ROOT


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def header_shape(page):
    return page.locator('#site-header').evaluate('''node => {
      const copy = node.cloneNode(true);
      for (const el of [copy, ...copy.querySelectorAll('*')]) {
        for (const attribute of [...el.attributes]) {
          if (['href','data-page','data-site-index','aria-current','aria-label'].includes(attribute.name)) el.removeAttribute(attribute.name);
        }
      }
      return copy.outerHTML.replace(/\\s+/g, ' ');
    }''')


def verify(output=None):
    output = output or ROOT / 'docs/internal/screenshots/redesign'
    output.mkdir(parents=True, exist_ok=True)
    for path in [*ROOT.glob('README*.md'), *(ROOT/'site').rglob('*.html')]:
        text = path.read_text()
        assert not re.search(r'TODO|<AUTHOR_NAME>|incomplete|Social preview', text), path
    for name in ('README.md', 'README_en.md'):
        assert len((ROOT/name).read_text().splitlines()) <= 200
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    errors, checks, shots = [], [], []
    first_blocks = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for width, height in ((1440,1000),(390,844)):
                for theme in ('light','dark'):
                    ctx = browser.new_context(viewport={'width':width,'height':height}, color_scheme=theme)
                    ctx.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
                    ctx.add_init_script("try { localStorage.setItem('harness.lang','zh'); } catch(error) { if(error.name !== 'SecurityError') throw error; }")
                    page=ctx.new_page(); page.on('pageerror', lambda error: errors.append(str(error)))
                    paths={**{view:'/site/index.html#'+view for view in ('home','papers','map','routes','gaps')},
                           'daily':'/site/daily/index.html','weekly':'/site/weekly/index.html',
                           'guide':'/site/guide.html','drawer':'/site/index.html#p-hda',
                           'withdrawn':'/site/daily/2026-10-27.html'}
                    shapes=[]
                    for view,path in paths.items():
                        page.goto(base+path); page.evaluate('document.fonts.ready')
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (view,width,theme)
                        shapes.append(header_shape(page))
                        if view in ('papers','map','routes','gaps'):
                            expect(page.locator('#home-hero')).not_to_be_visible()
                            target={'papers':'#bar','map':'.map-section','routes':'.routes','gaps':'.gaps'}[view]
                            top=page.locator(target).first.bounding_box()['y']
                            first_blocks[f'{view}-{width}-{theme}']=round(top,2)
                            if width==1440: assert top <=260,(view,top)
                        if view=='papers':
                            expect(page.locator('#sort')).to_have_value('must')
                            expect(page.locator('#result-count')).to_contain_text('98 / 98')
                            expected=page.evaluate('Object.keys(HARNESS_DATA.meta.sections)')
                            for sort in ('newest','oldest','must','evidence'):
                                page.select_option('#sort',sort)
                                assert page.locator('.group[data-section-id]').evaluate_all('(groups)=>groups.map(g=>g.dataset.sectionId)') == expected
                            page.select_option('#sort','must')
                            assert page.locator('.row .ev').evaluate_all('(els)=>els.every(e=>e.hasAttribute("aria-label"))')
                            if width==390:
                                expect(page.locator('#filter-panel')).not_to_be_visible()
                                page.locator('#filter-open').click();expect(page.locator('#filter-panel')).to_be_visible()
                                page.locator('#filter-open').click()
                        if view=='map':
                            stats=page.evaluate('HARNESS_DATA.stats')
                            expect(page.locator('[data-map-total]')).to_have_text(str(stats['scopes']['core']+stats['scopes']['harness_eval']))
                            for section,count in stats['sections'].items():
                                control=page.locator(f'[data-map-section="{section}"] b')
                                if control.count():expect(control).to_have_text(str(count))
                        if view=='routes':expect(page.locator('.route')).to_have_count(9)
                        if view=='gaps':expect(page.locator('.gap')).to_have_count(7)
                        if view=='drawer':
                            expect(page.locator('#drawer')).to_be_visible()
                            expect(page.locator('#dtitle')).to_contain_text('Harness-Delta')
                        if view=='withdrawn':
                            expect(page.locator('h1')).to_contain_text('已撤下')
                            expect(page.locator('.weekly-paper')).to_have_count(0)
                        filename=f'{view}-{width}-{theme}.png'; page.screenshot(path=str(output/filename),animations='disabled')
                        shots.append({'view':view,'width':width,'theme':theme,'file':filename})
                        if view in ('home', 'daily') and width==1440:
                            page.locator('#lang').click()
                            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                            filename=f'{view}-en-{width}-{theme}.png'
                            page.screenshot(path=str(output/filename),animations='disabled')
                            shots.append({'view':view+'-en','width':width,'theme':theme,'file':filename})
                            page.locator('#lang').click()
                    assert len(set(shapes))==1, 'Shared header DOM diverged'
                    # Retrospective is separate from the empty daily page; capture both languages.
                    recaps=sorted((ROOT/'site/recaps').glob('*.json'))
                    if recaps:
                        page.goto(base+'/site/recaps/'+recaps[-1].stem+'.html')
                        if width==1440:
                            assert page.locator('.weekly-paper').first.bounding_box()['y'] <=400
                        for lang in ('zh','en'):
                            if lang=='en':page.locator('#lang').click()
                            filename=f'retrospective-{lang}-{width}-{theme}.png'
                            page.screenshot(path=str(output/filename),animations='disabled')
                            shots.append({'view':'retrospective-'+lang,'width':width,'theme':theme,'file':filename})
                    ctx.close()
            ctx=browser.new_context(viewport={'width':1440,'height':1000})
            ctx.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
            page=ctx.new_page();page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base+'/site/index.html#papers')
            page.locator('#q').fill('HDA');expect(page.locator('.row')).to_have_count(1)
            page.locator('.row').click();expect(page.locator('#dclose')).to_be_focused()
            page.keyboard.press('Shift+Tab');assert page.evaluate('!!document.activeElement.closest("#drawer")')
            page.keyboard.press('Escape');expect(page.locator('.row')).to_be_focused()
            page.locator('#clear').click();page.locator('#advanced-title').click()
            page.locator('[data-field="held_out"][data-value="yes"]').click()
            yes=set(page.locator('.row').evaluate_all('(els)=>els.map(e=>e.dataset.open)'))
            page.locator('[data-field="held_out"][data-value="unknown"]').click()
            union=set(page.locator('.row').evaluate_all('(els)=>els.map(e=>e.dataset.open)'));assert yes<union
            page.locator('[data-field="cross_model_transfer"][data-value="yes"]').click()
            assert all(page.evaluate('(id)=>HARNESS_DATA.papers.find(p=>p.id===id).evidence.cross_model_transfer',pid)=='yes' for pid in page.locator('.row').evaluate_all('(els)=>els.map(e=>e.dataset.open)'))
            page.set_content('<iframe id="preview" sandbox="allow-scripts" style="width:100%;height:900px"></iframe>')
            source=(ROOT/'site/index.html').read_text().replace('<head>',f'<head><base href="{base}/site/">',1)
            page.locator('#preview').evaluate('(frame,source)=>frame.srcdoc=source',source)
            frame=page.frame_locator('#preview')
            for view,content in [('papers','.row:visible'),('map','.map-focus'),('routes','.route'),('gaps','.gap')]:
                frame.locator(f'[data-header-view="{view}"]').click();expect(frame.locator(content).first).to_be_visible()
            frame.locator('[data-header-view="papers"]').click()
            frame.locator('#q').fill('HDA');frame.locator('.row').click();expect(frame.locator('#drawer')).to_be_visible()
            sandbox=page.locator('#preview').element_handle().content_frame()
            sandbox.evaluate("HARNESS_DATA.config.base_url='about:srcdoc'")
            frame.locator('#copy').click();expect(frame.locator('#copymsg')).to_contain_text('请从已发布的网站复制分享链接')
            frame.locator('#dclose').click();expect(frame.locator('#drawer')).not_to_be_visible()
            frame.locator('#lang').click();expect(frame.locator('#result-count')).to_contain_text('Showing')
            frame.locator('#theme').click()
            ctx.close();browser.close()
        assert not errors, errors
        checks=['Ten views × light/dark × 1440/390 without horizontal overflow','Identical shared header DOM',
                'Non-home first content top ≤260px on desktop','Fixed taxonomy order under all four sorts',
                'Scope-derived map counts, all catalog results and accessible evidence labels',
                'Search, OR/AND facets, drawer focus and Escape return','Opaque srcdoc view switching, drawer, copy, language and theme',
                'No public placeholder strings; README ≤200 lines']
        report={'status':'passed','checks':checks,'first_content_top':first_blocks,'screenshots':shots,'console_errors':errors}
        (output/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        (output/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Follow RSI acceptance</title><style>body{font:16px system-ui;margin:24px}main{display:grid;grid-template-columns:1fr 1fr;gap:20px}img{max-width:100%;border:1px solid #ccc}</style><h1>Follow RSI · 页面验收</h1><main>'+''.join(f'<figure><figcaption>{s["view"]} · {s["width"]} · {s["theme"]}</figcaption><img src="{s["file"]}"></figure>' for s in shots)+'</main>')
        print(f'Passed {len(checks)} acceptance groups; {len(shots)} screenshots in {output}')
    finally:
        server.shutdown();server.server_close()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    verify(parser.parse_args().output)
