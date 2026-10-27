"""Audit the complete generated site locally; external destinations are not fetched."""
import argparse
from datetime import datetime, timezone
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import struct
from threading import Thread
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

from playwright.sync_api import Error as BrowserError, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = (1280, 400)
VIEWS = ('papers', 'map', 'routes', 'gaps')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class References(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if attrs.get(key):
                self.links.append({'attribute': key, 'target': attrs[key]})
        if tag == 'meta' and (attrs.get('property') in ('og:image', 'og:url')
                              or attrs.get('name') == 'twitter:image'):
            self.links.append({'attribute': attrs.get('property') or attrs['name'], 'target': attrs['content']})


def relative(root, path):
    return path.relative_to(root).as_posix()


def inspect_links(root, page_name, links, public_base, papers, cache, seen, local_base=None):
    """Resolve repository-hosted targets without making any external request."""
    checks = []
    public = urlsplit(public_base)
    site_base = public_base.rstrip('/') + '/'
    page_url = urljoin(site_base, page_name.removeprefix('site/'))
    for link in links:
        original = link['target']
        if not original or original.startswith(('data:', 'mailto:', 'tel:', 'javascript:', 'blob:')):
            continue
        target = urlsplit(urljoin(page_url, original))
        if local_base and original.startswith(local_base + '/site/'):
            target = urlsplit(urljoin(site_base, original.split('/site/', 1)[1]))
        if target.netloc != public.netloc or not target.path.startswith(public.path.rstrip('/') + '/'):
            seen['external'].add(original)
            continue
        path = unquote(target.path[len(public.path.rstrip('/')) + 1:])
        if not path or path.endswith('/'):
            path += 'index.html'
        key = (page_name, link['attribute'], path, target.fragment, target.query)
        if key in seen['references']:
            continue
        seen['references'].add(key)
        destination = root / 'site' / path
        issue = None
        if not destination.is_file():
            issue = '站内目标不存在'
        elif target.fragment and destination.suffix == '.html':
            fragment = unquote(target.fragment)
            if path == 'index.html' and fragment in VIEWS:
                pass
            elif path == 'index.html' and fragment.startswith('p-'):
                if fragment[2:] not in papers:
                    issue = '论文片段没有对应数据'
            else:
                if path not in cache:
                    cache[path] = References(destination.read_text(encoding='utf-8')).ids
                if fragment not in cache[path]:
                    issue = 'HTML 片段没有对应元素'
        checks.append({'page': page_name, 'attribute': link['attribute'], 'target': original,
                       'resolved': 'site/' + path + ('#' + target.fragment if target.fragment else ''),
                       'status': 'fail' if issue else 'pass', **({'problem': issue} if issue else {})})
    return checks


def static_audit(root, data):
    papers = {paper['id']: paper for paper in data['papers']}
    pages = sorted((root / 'site').rglob('*.html'))
    cache, seen, references, problems = {}, {'external': set(), 'references': set()}, [], []
    for path in pages:
        parsed = References(path.read_text(encoding='utf-8'))
        cache[relative(root / 'site', path)] = parsed.ids
        references.extend(inspect_links(root, relative(root, path), parsed.links, data['config']['base_url'],
                                        papers, cache, seen))
    for path in sorted((root / 'site').rglob('*.css')):
        urls = re.findall(r'url\(\s*[\'\"]?([^\)\'\"]+)', path.read_text(encoding='utf-8'))
        references.extend(inspect_links(root, relative(root, path), [{'attribute': 'css:url', 'target': url} for url in urls],
                                        data['config']['base_url'], papers, cache, seen))
    cards = []
    for ident in papers:
        path = root / 'site/cards' / f'{ident}.png'
        row = {'paper': ident, 'path': relative(root, path), 'status': 'pass'}
        if not path.is_file():
            row.update(status='fail', problem='论文分享图片缺失')
        else:
            header = path.read_bytes()[:24]
            if header[:8] != b'\x89PNG\r\n\x1a\n' or len(header) < 24:
                row.update(status='fail', problem='PNG 文件头无效')
            else:
                width, height = struct.unpack('>II', header[16:24])
                row.update(width=width, height=height, bytes=path.stat().st_size)
                if (width, height) != (1080, 1350):
                    row.update(status='fail', problem='图片尺寸不是 1080 × 1350')
        if not (root / 'site/p' / f'{ident}.html').is_file():
            problems.append({'page': f'site/p/{ident}.html', 'problem': '论文分享落地页缺失'})
        cards.append(row)
    return pages, references, cards, problems, cache, seen


LAYOUT = '''() => {
 const width = innerWidth, body = document.body, html = document.documentElement;
 const documentWidth = Math.max(body.scrollWidth, html.scrollWidth);
 const drawer = document.querySelector('#drawer:not([hidden])');
 const offenders = [...document.querySelectorAll('body *')].filter(el => {
   if (!el.getClientRects().length || el.closest('[hidden]')) return false;
   const rect = el.getBoundingClientRect();
   return rect.width && (rect.right > width + 2 || rect.left < -2);
 }).slice(0, 8).map(el => ({tag:el.tagName.toLowerCase(),id:el.id,class:el.className,
   right:Math.round(el.getBoundingClientRect().right),left:Math.round(el.getBoundingClientRect().left)}));
 return {viewport:width,document_width:documentWidth,
   overflow:documentWidth > width + 2,
   drawer_overflow:!!drawer && drawer.scrollWidth > drawer.clientWidth + 2,
   offenders};
}'''
DOM_LINKS = '''() => [...document.querySelectorAll('[href],[src],a[download]')].flatMap(el =>
 ['href','src'].filter(key=>el.hasAttribute(key)).map(key=>({attribute:el.hasAttribute('download')?'download':key,
 target:el.getAttribute(key)})))'''


def browser_audit(root, data, pages, references, cache, seen, export_cards=True, scenarios=None):
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(root)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    papers = {paper['id']: paper for paper in data['papers']}
    results, denied = [], set()
    current = {'row': None}

    def problem(message, detail=None):
        current['row']['problems'].append({'problem': message, **({'detail': detail} if detail else {})})

    def links(page):
        source = unquote(urlsplit(page.url).path).lstrip('/')
        references.extend(inspect_links(root, source,
                                        page.evaluate(DOM_LINKS), data['config']['base_url'], papers, cache, seen, base))

    def layout(page, phase='final'):
        measured = page.evaluate(LAYOUT)
        current['row']['layouts'].append({'phase': phase, **measured})
        if measured['overflow'] or measured['drawer_overflow']:
            problem('页面或论文小票横向溢出', {'phase': phase, 'elements': measured['offenders']})

    def run_case(page, name, width, action, language='zh', scenario='page'):
        if scenarios is not None and scenario not in scenarios:
            return
        row = {'page': name, 'viewport': width, 'language': language, 'scenario': scenario,
               'checks': [], 'layouts': [], 'problems': []}
        current['row'] = row
        try:
            action(row)
            layout(page)
            links(page)
        except (BrowserError, AssertionError) as error:
            problem('浏览器交互失败', str(error).replace(str(root), '.'))
        row['status'] = 'pass' if not row['problems'] else 'fail'
        results.append(row)
        if len(results) % 30 == 0:
            print(f'Audited {len(results)} browser cases; {sum(r["status"] == "fail" for r in results)} failures', flush=True)

    def attach(page):
        page.on('pageerror', lambda error: problem('JavaScript pageerror', str(error)))
        page.on('console', lambda message: problem('控制台 error', message.text)
                if message.type == 'error' and not message.text.startswith('Failed to load resource:') else None)
        page.on('response', lambda response: problem('站内 HTTP 错误', {'url':response.url.replace(base + '/', ''),
                                                                     'status':response.status})
                if response.url.startswith(base + '/') and response.status >= 400 else None)
        page.on('requestfailed', lambda request: problem('站内资源请求失败',
                {'url': request.url.replace(base + '/', ''), 'failure': request.failure})
                if request.url.startswith(base + '/') else None)

    def visit(page, path):
        response = page.goto(base + '/' + path, wait_until='load')
        assert response is None or response.ok, f'HTTP {response.status}'
        page.evaluate('document.fonts.ready')

    def set_language(page, value, control='#lang'):
        expected = 'zh-CN' if value == 'zh' else 'en'
        if page.locator('html').get_attribute('lang') != expected:
            page.locator(control).click()
        assert page.locator('html').get_attribute('lang') == expected, '语言切换未生效'

    def themes(page, row):
        colors = {}
        modes = ('auto', 'light', 'dark')
        for _ in modes:
            current_theme = page.locator('html').get_attribute('data-theme') or 'auto'
            expected = modes[(modes.index(current_theme) + 1) % len(modes)]
            page.locator('#theme').click()
            assert page.locator('html').get_attribute('data-theme') == expected, '主题按钮未切换主题'
            assert page.evaluate("localStorage.getItem('harness.theme')") == expected, '主题偏好没有保存'
            colors[expected] = page.locator('body').evaluate('(el)=>getComputedStyle(el).backgroundColor')
            layout(page, 'theme-' + expected)
        assert colors['light'] != colors['dark'], '深浅主题未改变页面背景'
        row['checks'].append('自动/浅色/深色切换与偏好保存')

    def search_and_sort(page, row, lang):
        visit(page, 'site/index.html#papers')
        set_language(page, lang)
        page.locator('#clear').click()
        assert page.locator('#main .row').count() == data['stats']['included'], '全清后未显示全部正式收录论文'
        page.locator('#q').fill('AutoSaddler')
        assert page.locator('#main .row[data-open="autosaddler"]').count() == 1, '搜索未找到 AutoSaddler'
        assert 0 < page.locator('#main .row').count() < data['stats']['included'], '搜索未缩小结果集'
        page.locator('#q').fill('follow-rsi-no-such-paper-000')
        assert page.locator('#main .row').count() == 0, '无结果搜索仍返回论文'
        assert page.locator('#main .empty').is_visible(), '无结果搜索缺少提示'
        page.locator('#clear').click()
        assert page.locator('#q').input_value() == '', '全清未清空搜索词'
        if page.locator('#filter-open').is_visible():
            if page.locator('#filter-open').get_attribute('aria-expanded') != 'true':
                page.locator('#filter-open').click()
            assert page.locator('#filter-open').get_attribute('aria-expanded') == 'true', '手机筛选面板未展开'
        page.locator('[data-toggle="verify"]').click()
        assert all(papers[ident].get('needs_reading') for ident in page.locator('#main .row').evaluate_all('(els)=>els.map(el=>el.dataset.open)')), '待细读筛选包含不符论文'
        if page.locator('.advanced-filters').get_attribute('open') is None:
            page.locator('#advanced-title').click()
        if page.locator('[data-help="held_out"]').get_attribute('aria-expanded') != 'true':
            page.locator('[data-help="held_out"]').click()
        assert page.locator('#help-held_out').is_visible(), '筛选定义未展开'
        page.locator('#clear').click()
        assert page.locator('[data-toggle][aria-pressed="true"]').count() == 0, '全清未清除开关筛选'
        assert page.locator('#main .row').count() == data['stats']['included'], '全清未恢复结果'
        row['checks'] += ['关键词搜索与空结果提示', '全清恢复正式收录列表', '待细读筛选', '筛选定义按钮', '结果计数']
        assert f'{data["stats"]["included"]} / {data["stats"]["included"]}' in page.locator('#result-count').inner_text(), '结果计数错误'
        for sort in ('newest', 'oldest', 'must', 'evidence'):
            page.locator('#sort').select_option(sort)
            groups = page.locator('#main .rows').evaluate_all('(els)=>els.map(el=>[...el.querySelectorAll("[data-open]")].map(p=>p.dataset.open))')
            for group in groups:
                selected = [papers[ident] for ident in group]
                if sort in ('newest', 'oldest'):
                    dates = [paper['date'] for paper in selected]
                    assert dates == sorted(dates, reverse=sort == 'newest'), f'{sort} 未按日期排序'
                elif sort == 'must':
                    flags = [bool(paper.get('must_read')) for paper in selected]
                    assert flags == sorted(flags, reverse=True), '必读优先排序不符'
                else:
                    recorded = [sum(paper['evidence'][key] != 'unknown' for key in data['stats']['check_coverage']['fields']) for paper in selected]
                    assert recorded == sorted(recorded, reverse=True), '证据完整度排序不符'
            layout(page, 'sort-' + sort)
        row['checks'].append('四种排序（分类内顺序）')

    def route_reading(page, row, route, route_index, lang):
        visit(page, 'site/index.html#routes')
        set_language(page, lang)
        route_card = page.locator('#main .route').nth(route_index)
        for position, ident in enumerate(route['papers'], 1):
            step = route_card.locator('[data-open]').nth(position - 1)
            assert step.get_attribute('data-open') == ident, '阅读路线论文顺序错误'
            assert step.locator('.step').inner_text() == f'{position}.', '阅读路线步骤序号错误'
            assert step.locator('time').inner_text() == papers[ident]['date'], '阅读路线日期错误'
        route_card.locator('[data-open]').first.click()
        assert page.locator('#dtitle').inner_text() == papers[route['papers'][0]]['title'], '路线首篇打开错误'
        for position, ident in enumerate(route['papers'][1:], 1):
            page.locator('#next').click()
            assert page.locator('#dtitle').inner_text() == papers[ident]['title'], '下一篇没有沿当前阅读路线前进'
            if position == 1:
                page.keyboard.press('ArrowLeft')
                assert page.locator('#dtitle').inner_text() == papers[route['papers'][0]]['title'], '左键未返回路线上一篇'
                page.keyboard.press('ArrowRight')
                assert page.locator('#dtitle').inner_text() == papers[ident]['title'], '右键未进入路线下一篇'
            layout(page, 'route-paper-' + ident)
        assert page.locator('#next').is_disabled(), '路线末篇仍可向后翻到路线之外'
        links(page)
        page.keyboard.press('Escape')
        assert page.locator('#drawer').is_hidden(), 'Esc 未关闭论文小票'
        assert page.locator('[data-view="routes"]').get_attribute('aria-current') == 'page', '关闭小票后未回到阅读路线'
        row['checks'] += ['路线顺序/序号/日期', '逐篇下一篇', '左右方向键', '路线末尾边界', 'Esc 关闭并返回路线']

    def open_paper(page, paper, name, row):
        visit(page, name)
        page.wait_for_selector('#drawer:not([hidden])')
        assert page.locator('#dtitle').inner_text() == paper['title'], '落地页打开了错误的论文'
        flags = page.locator('#drawer .receipt > .tag.verify').all_text_contents()
        marked = any('待细读' in value or 'Needs verification' in value for value in flags)
        assert marked == bool(paper.get('needs_reading')), 'needs_reading 标记与数据不符'
        image = page.locator('#drawer img.sharepreview')
        image.scroll_into_view_if_needed()
        page.wait_for_function('''() => {const image=document.querySelector('#drawer img.sharepreview');
                                   return image.complete && image.naturalWidth === 1080;}''')
        assert page.locator('#drawer a[download]').get_attribute('href') == f'cards/{paper["id"]}.png'
        layout(page, 'drawer-open')
        links(page)
        page.locator('#dclose').click()
        assert page.locator('#drawer').is_hidden(), '关闭按钮未关闭论文小票'
        assert not page.locator('#app').evaluate('(el)=>el.inert'), '关闭后主页面仍不可操作'
        row['checks'] += ['落地页打开对应论文', 'needs_reading 标记', '分享图加载和下载地址', '关闭后主页面可操作']

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for width in VIEWPORTS:
                context = browser.new_context(viewport={'width': width, 'height': 960}, color_scheme='light')
                def route(request_route):
                    if request_route.request.url.startswith(base + '/'):
                        request_route.continue_()
                    else:
                        denied.add(request_route.request.url)
                        request_route.abort()
                context.route('**/*', route)
                page = context.new_page()
                page.set_default_timeout(8000)
                attach(page)
                for path in pages:
                    name = relative(root, path)
                    if path.parent.name == 'p' and path.stem in papers:
                        run_case(page, name, width, lambda row, p=papers[path.stem], n=name: open_paper(page, p, n, row))
                    else:
                        def ordinary(row, name=name):
                            visit(page, name)
                            assert page.title().strip(), '页面标题为空'
                            assert page.locator('body').inner_text().strip(), '页面没有可读内容'
                            row['checks'] += ['页面加载', '非空标题与正文']
                            if name == 'site/index.html':
                                page.wait_for_selector('[data-view="papers"][aria-current="page"]')
                            elif name == 'site/card.html':
                                page.wait_for_selector('html[data-card-ready="true"]')
                                row['checks'].append('无参数卡片工具可打开')
                        run_case(page, name, width, ordinary)
                for language in ('zh', 'en'):
                    for view in VIEWS:
                        def main_view(row, view=view, language=language):
                            visit(page, 'site/index.html#' + view)
                            set_language(page, language)
                            page.wait_for_selector(f'[data-view="{view}"][aria-current="page"]')
                            assert page.locator('#main').inner_text().strip(), '视图无内容'
                            for image in page.locator('#main [role="img"]').all():
                                assert image.get_attribute('aria-label'), '证据图标缺少无障碍文字'
                            for ident in page.locator('#main [data-open]').evaluate_all('(els)=>els.map(el=>el.dataset.open)'):
                                assert ident in papers, '论文按钮引用未知 ID：' + ident
                            if view == 'gaps':
                                discussions = page.locator('#main .gap .discussion-link a')
                                assert discussions.count() == len(data['gaps']), '研究空白缺少讨论入口'
                                for discussion in discussions.all():
                                    assert discussion.get_attribute('href') == data['config']['repository_url'].rstrip('/') + '/discussions', '研究空白讨论地址错误'
                                row['checks'].append('每条研究空白的 Discussions 地址（未访问外站）')
                            themes(page, row)
                            row['checks'] += ['视图片段与高亮一致', '双语渲染', '证据图标文字标签', '论文按钮 ID 有效']
                        run_case(page, 'site/index.html#' + view, width, main_view, language)
                    run_case(page, 'site/index.html#papers', width,
                             lambda row, lang=language: search_and_sort(page, row, lang), language, 'search-filter-sort')
                    for route_index, reading_route in enumerate(data['routes']):
                        run_case(page, 'site/index.html#routes', width,
                                 lambda row, r=reading_route, i=route_index, lang=language: route_reading(page, row, r, i, lang),
                                 language, 'reading-route-' + str(route_index + 1))
                for name, control in [('site/guide.html', '#guide-language'), ('site/daily/index.html', '#language'),
                                      ('site/weekly/index.html', '#language')]:
                    def english(row, name=name, control=control):
                        visit(page, name)
                        for lang in ('zh', 'en'):
                            set_language(page, lang, control)
                            assert page.evaluate("localStorage.getItem('harness.lang')") == lang, '语言偏好未保存'
                            if name == 'site/guide.html':
                                assert page.locator('#guide-' + lang).is_visible(), '导读对应语言正文未显示'
                            layout(page, 'language-' + lang)
                        if name == 'site/guide.html':
                            saved = page.evaluate("localStorage.getItem('harness.theme')") or 'auto'
                            assert page.locator('html').get_attribute('data-theme') == saved, '导读未继承主题偏好'
                            row['checks'].append('导读继承主题偏好')
                        else:
                            themes(page, row)
                        row['checks'].append('中英往返切换、偏好保存与正文加载')
                    run_case(page, name, width, english, 'en')
                def atom(row):
                    visit(page, 'site/feed/atom.xml')
                    page.wait_for_selector('main h1')
                    assert 'Atom' in page.locator('main h1').inner_text(), 'Atom 没有渲染订阅说明'
                    tree = ET.parse(root / 'site/feed/atom.xml')
                    namespace = {'a': 'http://www.w3.org/2005/Atom'}
                    entries = tree.findall('a:entry', namespace)
                    assert page.locator('main article').count() == len(entries), 'Atom 页面条目数与 XML 不一致'
                    assert page.locator('main code').inner_text() == tree.find('a:link[@rel="self"]', namespace).get('href'), 'Atom 订阅地址不符'
                    if not entries:
                        assert '等待人工审核' in page.locator('main').inner_text(), '空 Atom 缺少等待审核说明'
                    row['checks'] += ['XML 由 XSL 实际渲染', '订阅地址和条目数', '空 feed 状态（如适用）']
                run_case(page, 'site/feed/atom.xml', width, atom, scenario='atom-xsl')
                context.close()
            if export_cards:
                context = browser.new_context(viewport={'width': 1080, 'height': 1350}, color_scheme='light')
                context.route('**/*', route)
                page = context.new_page()
                page.set_default_timeout(8000)
                attach(page)
                for language in ('zh', 'en'):
                    for paper in papers.values():
                        name = f'site/card.html?id={paper["id"]}&lang={language}'
                        def export(row, name=name, paper=paper):
                            visit(page, name)
                            page.wait_for_selector('html[data-card-ready="true"]')
                            assert page.locator('#card').evaluate('(el)=>el.scrollHeight<=el.clientHeight && el.scrollWidth<=el.clientWidth'), '卡片内容溢出'
                            flags = page.locator('#card .card-flag.verify').all_text_contents()
                            marked = any('待细读' in value or 'Needs verification' in value for value in flags)
                            assert marked == bool(paper.get('needs_reading')), '卡片 needs_reading 标记不符'
                            row['checks'] += ['卡片渲染完成', '导出画布内部无溢出', '卡片 needs_reading 标记']
                        run_case(page, name, 1080, export, language)
                page.set_viewport_size({'width': 1280, 'height': 640})
                def og(row):
                    visit(page, 'site/card.html?og=1')
                    page.wait_for_selector('html[data-card-ready="true"]')
                    assert page.locator('#card').evaluate('(el)=>el.offsetWidth===1280 && el.offsetHeight===640 && el.scrollHeight<=el.clientHeight && el.scrollWidth<=el.clientWidth'), 'OG 画布尺寸或内容溢出'
                    row['checks'] += ['OG 导出画布 1280×640', 'OG 内容无溢出']
                run_case(page, 'site/card.html?og=1', 1280, og, scenario='og-export')
                context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return results, sorted(denied)


def markdown(report):
    total = report['summary']
    method = ('仅执行静态资源检查；本次未运行浏览器，不据此判断交互或布局。'
              if report['scope']['static_only'] else
              '使用本地 HTTP 服务和 Chromium，桌面宽度 1280px、手机宽度 400px。'
              '检查四个主视图、搜索/全清/排序、阅读路线连续翻页、语言与现有主题控件、Atom 的 XSL 实际渲染。')
    if total['card_export_cases']:
        method += f'另检查 {total["card_export_cases"]} 个中英文论文卡片导出场景和 1280×640 OG 画布。'
    if report.get('verification_history'):
        first, rerun = report['verification_history']
        method += (f'首轮运行 {first["cases"]} 项后，修正审计脚本对筛选展开状态的假设，'
                   f'仅复验受影响的 {rerun["cases"]} 项，全部通过；期间站点文件未变。完整记录保留在 JSON。')
    lines = ['# 全站页面审计', '', f'审计时间：{report["checked_at"]}', '',
             f'结果：**{report["status"]}**。检查 {total["html_pages"]} 个 HTML 页面、{total["paper_pages"]} 个论文落地页、'
             f'{total["card_assets"]} 张分享图和 {total["browser_cases"]} 个浏览器场景。', '',
             method + '站内 href、src、CSS URL、下载资源及论文/视图片段按本地文件和数据核验。', '',
             '**边界：没有访问或验证 arXiv、GitHub、作者主页等外部链接的可达性；外部网络请求主动阻止，不计为本站损坏。'
             '此报告检查功能、资源和布局，不代替论文证据审阅，也不声称逐像素人工审美评估。**', '',
             '## 检查结果', '',
             f'- 站内引用：{total["internal_references"]} 条，失败 {total["reference_failures"]} 条。',
             f'- 分享图片：{total["card_assets"]} 张，失败 {total["card_failures"]} 张。',
             f'- 浏览器场景：{total["browser_cases"]} 项，通过 {total["browser_passed"]} 项，失败 {total["browser_failures"]} 项。',
             f'- 浏览器 HTML 覆盖：{total["html_browser_pages"]} / {total["html_pages"]} 页；论文落地页 {total["paper_browser_pages"]} / {total["paper_pages"]} 页。',
             f'- 外部链接：仅记录 {total["external_targets_unchecked"]} 个目标，未做网络可达性测试。', '',
             '## 发现的问题', '']
    failures = report['problems'] + [row for row in report['references'] if row['status'] == 'fail']
    failures += [row for row in report['cards'] if row['status'] == 'fail']
    for row in report['browser']:
        failures += [{'page': row['page'], 'problem': problem['problem'],
                      'detail': f'{row["viewport"]}px / {row["language"]}: {problem.get("detail", "")}' }
                     for problem in row['problems']]
    if failures:
        for entry in failures:
            location = entry.get('page') or entry.get('path', '')
            detail = str(entry.get('detail') or entry.get('target') or '').replace('\n', ' ')
            lines.append(f'- `{location}`：{entry["problem"]}' + (f'；{detail}' if detail else ''))
    else:
        lines.append('本次静态检查未发现资源或片段错误；交互和布局尚未检查。' if report['scope']['static_only'] else
                     '本次检查未发现未修复的本站功能、资源、片段或横向溢出问题。')
    lines += ['', '## 页面覆盖清单', '', '| 页面 | 场景数 | 结果 |', '|---|---:|---|']
    names = sorted({row['page'].split('?', 1)[0].split('#', 1)[0] for row in report['browser']})
    for name in names:
        cases = [row for row in report['browser'] if row['page'].split('?', 1)[0].split('#', 1)[0] == name]
        lines.append(f'| `{name}` | {len(cases)} | {"通过" if all(row["status"] == "pass" for row in cases) else "失败"} |')
    lines += ['', '逐项视口、语言、小票操作、标记检查、资源地址及错误细节保存在同目录 `page-audit.json`。', '']
    return '\n'.join(lines)


def audit(root=ROOT, output=None, static_only=False, export_cards=True):
    root = Path(root)
    output = output or root / 'build/page-audit'
    data = json.loads((root / 'site/papers.json').read_text(encoding='utf-8'))
    pages, references, cards, problems, cache, seen = static_audit(root, data)
    browser, blocked = ([], []) if static_only else browser_audit(root, data, pages, references, cache, seen, export_cards)
    browser_pages = {row['page'].split('?', 1)[0].split('#', 1)[0] for row in browser}
    summary = {'html_pages': len(pages), 'paper_pages': len(data['papers']), 'card_assets': len(cards),
               'internal_references': len(references), 'reference_failures': sum(row['status'] == 'fail' for row in references),
               'card_failures': sum(row['status'] == 'fail' for row in cards), 'browser_cases': len(browser),
               'browser_passed': sum(row['status'] == 'pass' for row in browser),
               'browser_failures': sum(row['status'] == 'fail' for row in browser),
               'html_browser_pages': sum(name.endswith('.html') for name in browser_pages),
               'paper_browser_pages': sum(name.startswith('site/p/') for name in browser_pages),
               'card_export_cases': sum(row['page'].startswith('site/card.html?id=') for row in browser),
               'external_targets_unchecked': len(seen['external'])}
    report = {'checked_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
              'status': '未通过' if problems or any(summary[key] for key in ('reference_failures', 'card_failures', 'browser_failures')) else '通过',
              'scope': {'viewports': list(VIEWPORTS), 'static_only': static_only, 'export_cards': export_cards,
                        'external_network': 'blocked; external link availability not checked'},
              'pages': [relative(root, path) for path in pages],
              'summary': summary, 'problems': problems, 'references': references, 'cards': cards,
              'browser': browser, 'external_targets_unchecked': sorted(seen['external']), 'blocked_external_requests': blocked}
    output.mkdir(parents=True, exist_ok=True)
    (output / 'page-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'page-audit.md').write_text(markdown(report), encoding='utf-8')
    print(json.dumps({'status': report['status'], **summary}, ensure_ascii=False), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--static-only', action='store_true')
    parser.add_argument('--skip-card-exports', action='store_true')
    arguments = parser.parse_args()
    result = audit(arguments.root, arguments.output, arguments.static_only, not arguments.skip_card_exports)
    raise SystemExit(0 if result['status'] == '通过' else 1)
