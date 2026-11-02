"""Deterministic, offline build. Only AUTO blocks replace authored Markdown."""
import argparse
from collections import Counter
from datetime import date, timedelta
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jinja2 import Environment, FileSystemLoader, select_autoescape

from scripts.common import ROOT, CHECKS, CLASSES, FIELDS, KEYS, ICONS, SYMBOLS, evidence, paper_url, read_yaml
from scripts.validate import validate


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8') != content:
        path.write_text(content, encoding='utf-8')


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def replace_block(text, name, content):
    start, end = f'<!-- AUTO:{name}:START -->', f'<!-- AUTO:{name}:END -->'
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) > text.index(end):
        raise ValueError(f'Expected one ordered AUTO:{name} marker pair')
    before, rest = text.split(start)
    _, after = rest.split(end)
    return before + start + '\n\n' + content.strip() + '\n\n' + end + after


def cell(value):
    return str(value).replace('|', '&#124;').replace('\n', '<br>')


def flag(p):
    return ' **待细读 / Needs verification**' if p.get('needs_reading') else ''


def label(p):
    return p['title'] + flag(p)


def short(p):
    match = re.search(r'\(([^)]+)\)\s*$', p['title'])
    return match[1] if match else re.split(r'[:：]', p['title'])[0]


def compute_stats(data):
    core = [p for p in data['papers'] if p.get('status') != 'candidate']
    def coverage(fields):
        reviewed = sum(evidence(p)[k] != 'unknown' for p in core for k in fields)
        total = len(core) * len(fields)
        return {'reviewed': reviewed, 'total': total, 'ratio': reviewed / total if total else 0, 'fields': list(fields)}
    as_of = date.fromisoformat(data['meta']['as_of'])
    recent = [p['id'] for p in core if len(p['date']) == 10 and as_of - timedelta(days=13) <= date.fromisoformat(p['date']) <= as_of]
    return {
        'as_of': data['meta']['as_of'], 'total': len(data['papers']), 'included': len(core),
        'candidates': len(data['papers']) - len(core), 'must_read': sum(p.get('must_read', False) for p in core),
        'needs_reading': sum(p.get('needs_reading', False) for p in core),
        'sections': {s: sum(p['section'] == s for p in data['papers']) for s in data['meta']['sections']},
        'evidence_coverage': coverage(FIELDS), 'check_coverage': coverage(CHECKS),
        'with_recorded_checks': sum(any(evidence(p)[k] != 'unknown' for k in CHECKS) for p in core),
        'months': {f'2026-{m:02}': sum(p['date'].startswith(f'2026-{m:02}') for p in core) for m in range(3, 11)},
        'recent_ids': sorted(recent, key=lambda pid: next(p['date'] for p in core if p['id'] == pid), reverse=True),
        'scopes': dict(Counter(p['scope'] for p in core)),
        # No full-text completion receipts have been recorded; partial fields are not completion.
        'must_read_fully_reviewed': 0,
    }


def must_reads(papers, routes):
    by_id = {p['id']: p for p in papers}
    ordered = list(dict.fromkeys(pid for r in routes for pid in r['papers']))
    # Some source-marked must-reads are not on a route. Keep them after route entries.
    ordered += [p['id'] for p in papers if p['id'] not in ordered]
    return [by_id[pid] for pid in ordered if by_id[pid].get('must_read')]


def read_gaps(root):
    content = (root / 'directions/open-problems.md').read_text()
    zh, en = content.split('## English\n', 1)
    def parse(text):
        return re.findall(r'^\d+\. \*\*(.+?)\*\*：?\s*(.+)$', text, re.M)
    zh_items, en_items = parse(zh), parse(en)
    if len(zh_items) != 7 or len(en_items) != 7:
        raise ValueError('Expected seven bilingual open problems')
    return [{'title_zh': a, 'text_zh': b, 'title_en': c, 'text_en': d,
             'refs': list(dict.fromkeys(re.findall(r'\.\./papers/([a-z0-9-]+)\.md', b)))}
            for (a, b), (c, d) in zip(zh_items, en_items)]


SCOPE_NAMES = {
    'core': ('Harness 自进化方法', 'Harness evolution methods'),
    'harness_eval': ('Harness 专项评测与理论', 'Harness evaluation and theory'),
    'background': ('奠基、前史与基线', 'Foundations and baselines'),
    'general_rsi': ('通用 RSI', 'General RSI'),
    'candidates': ('延伸候选', 'Candidates'),
}
CLASS_NAMES = {'who_edits': ('谁来改', 'Who edits'), 'feedback': ('反馈来源', 'Feedback'),
               'timing': ('改进时机', 'Timing'), 'topology': ('演化结构', 'Topology')}
VALUE_ZH = {'yes': '有', 'no': '没有', 'partial': '部分', 'unknown': '未审', 'na': '不适用',
            'self': '自身', 'external': '外部改进器', 'trained': '训练出的改进器',
            'self_human_reviewed': '自身修改、人工审核', 'ground_truth': '标准答案',
            'proxy': '代理信号', 'self_generated_tests': '自生成测试', 'demonstrations': '示范',
            'self_judgment': '自我判断', 'offline': '离线', 'online': '在线',
            'test_time': '测试时', 'during_run': '运行中', 'chain': '链', 'tree': '树', 'graph': '图'}


def latest_edition(root):
    daily = [json.loads(path.read_text()) for path in (root / 'site/daily').glob('????-??-??.json')]
    recaps = [json.loads(path.read_text()) for path in (root / 'site/recaps').glob('*.json')]
    reviewed = [edition for edition in daily + recaps if edition.get('reviewed_only') and not edition.get('demo')]
    if not reviewed:
        return None
    latest = max(reviewed, key=lambda e: e.get('end', e.get('date', '')))
    retrospective = latest.get('kind') == 'retrospective'
    return {**latest, 'url': f"recaps/{latest['start']}--{latest['end']}.html" if retrospective else f"daily/{latest['date']}.html"}


def readme_metrics(root, lang):
    editions = [json.loads(path.read_text()) for path in (root / 'site/weekly').glob('????-W??.json')]
    published = [e for e in editions if e.get('reviewed_only') and not e.get('demo')]
    if not published:
        return ''
    latest = max(published, key=lambda e: e['week'])
    return f"[{'本周质量指标' if lang == 'zh' else 'Weekly metrics'}](digests/{latest['week']}{'' if lang == 'zh' else '.en'}.md)"


def source_summary(root, lang, config):
    path = root / 'site/feed/status.json'
    if not path.exists():
        return '尚无成功运行的信源记录。' if lang == 'zh' else 'No successful source run has been recorded.'
    state = json.loads(path.read_text())
    successful = [key for key, value in state.get('sources', {}).items() if value.get('enabled') and value.get('last_success')]
    failed = [key for key, value in state.get('sources', {}).items() if value.get('enabled') and value.get('last_ok') is False]
    zh = lang == 'zh'
    text = ('已实际运行成功：' if zh else 'Sources with recorded successful runs: ') + ' · '.join(successful) + '。'
    if failed:
        text += (' 本次失败：' if zh else ' Failed in the latest run: ') + ' · '.join(failed) + '。'
    return text + f" [{'信源状态' if zh else 'Source status'}]({config['base_url'].rstrip('/')}/feed/status.json)."


def readme_blocks(data, routes, stats, lang, config, root):
    papers, sections = data['papers'], data['meta']['sections']
    zh = lang == 'zh'
    base = config['base_url'].rstrip('/')
    badge_values = [('方法论文' if zh else 'methods', str(stats['scopes']['core']), '2A33D4'),
                    ('必读' if zh else 'must-read', str(stats['must_read']), '14161C'),
                    ('更新' if zh else 'updated', stats['as_of'], '14161C'),
                    ('内容' if zh else 'content', 'CC_BY_4.0', '14161C')]
    badges = ' '.join(f'![{name}](https://img.shields.io/badge/{quote(name.replace("-", "--"))}-{quote(value.replace("-", "--"))}-{color})'
                      for name, value, color in badge_values)
    if (root / 'articles/why-ai-self-improvement.md').exists():
        title = '深度解读：为什么 AI 还不会自我进化' if zh else 'Deep dive (Chinese): Why AI still struggles with self-improvement'
        badges += f'\n\n[**{title} →**]({base}/articles/why-ai-self-improvement.html)'
    scopes = stats['scopes']
    counts = (f"{scopes['core']} 篇方法 · {scopes['harness_eval']} 篇 Harness 评测与理论 · {scopes['background'] + scopes['general_rsi']} 篇奠基与通用 RSI。"
              if zh else f"{scopes['core']} methods · {scopes['harness_eval']} Harness evaluation and theory · {scopes['background'] + scopes['general_rsi']} foundations and general RSI papers.")
    latest = latest_edition(root)
    today = []
    if latest:
        title = latest.get('title_zh' if zh else 'title_en') or latest['date']
        today = [f"**[{title}]({base}/{latest['url']})** · {len(latest['items'])} " + ('篇，经人工审核。' if zh else 'papers, human reviewed.'), '']
        for item in latest['items'][:5]:
            sub = item['direction'].get('harness_sub')
            section = sections[sub][lang] if sub else ('评测与理论' if zh else 'Evaluation and theory')
            today.append(f"- [{item.get('short_title', item['title'])}]({item['links'].get('arxiv') or item['links'].get('url')}) · {section} · {item.get('summary_'+lang, '')}")
        today += ['', f"[{'阅读本期全部内容' if zh else 'Read this edition'} →]({base}/{latest['url']})"]
    else:
        today = ['今天没有新的 Harness 自进化论文。审核通过后发布，旧论文不冒充今日新作。' if zh else 'No new reviewed Harness evolution edition today. Historical discoveries are kept separate.']
    must = ['| 日期 | 论文 | 一句话 | 证据 |' if zh else '| Date | Paper | In one line | Evidence |', '| --- | --- | --- | --- |']
    for p in must_reads(papers, routes):
        marks = ' '.join(ICONS[evidence(p)[key]] for key in KEYS)
        must.append(f"| {p['date']} | [{cell(short(p))}](papers/{p['id']}.md) | {cell(p.get('summary_'+lang,''))} | {marks} |")
    must += ['', '图标：留出集 · 同预算 · 跨模型 · 成本；❔ 表示未审。' if zh else 'Icons: held-out · matched budget · cross-model · cost; ❔ means not yet reviewed.', '', counts,
             f"[{'完整清单' if zh else 'Full catalog'}: {stats['included']} + {stats['candidates']} {'候选' if zh else 'candidates'}](PAPERS.md) · [{'在网站筛选' if zh else 'Filter on the site'}]({base}/#papers)"]
    by_id = {p['id']: p for p in papers}
    rt = ['| 路线 | 顺序 | 读完能回答 |' if zh else '| Route | Order | What you can answer |', '| --- | --- | --- |']
    for r in routes:
        if not (r['name_zh'] in ('打基础','方法主线') or r['name_zh'].startswith('实验设计')):
            continue
        chain = ' → '.join(f"[{short(by_id[pid])}](papers/{pid}.md)" for pid in r['papers'])
        rt.append(f"| {cell(r['name_'+lang])} | {chain} | {cell(r['question_'+lang])} |")
    rt += ['', f"[{'全部阅读路线' if zh else 'All reading routes'} →]({base}/#routes)"]
    repository = quote(config['repository'], safe='/')
    history = f'[![Star History](https://api.star-history.com/svg?repos={repository}&type=Date)](https://star-history.com/#{repository}&Date)'
    return {'BADGES': badges, 'TODAY': '\n'.join(today), 'MUST_READ': '\n'.join(must), 'ROUTES': '\n'.join(rt),
            'SOURCES': source_summary(root, lang, config), 'METRICS': readme_metrics(root, lang), 'STAR_HISTORY': history}


def catalog(data, stats, config):
    lines = ['# Follow RSI · 论文全集', '', f"{stats['included']} 篇正式收录，{stats['candidates']} 篇候选。scope 是阅读范围，不等于全文证据已核验。", '',
             f"[网站筛选]({config['base_url'].rstrip('/')}/#papers) · [返回首页](README.md)", '',
             '证据顺序：留出集 · 同预算 · 跨模型 · 成本；❔ 未审，不推断缺失证据。']
    for scope, names in SCOPE_NAMES.items():
        group = [p for p in data['papers'] if ('candidates' if p.get('status') == 'candidate' else p['scope']) == scope]
        lines += ['', f'## {names[0]} · {len(group)} 篇', '', '| 日期 | 论文 | 核心机制 | 关键结果 | 证据 |', '| --- | --- | --- | --- | --- |']
        for p in sorted(group, key=lambda p: p['date'], reverse=True):
            marks = ' '.join(ICONS[evidence(p)[key]] for key in KEYS)
            lines.append(f"| {p['date']} | [{cell(p['title'])}](papers/{p['id']}.md){flag(p)} | {cell(p.get('summary_zh',''))} | {cell(p.get('result_zh',''))} | {marks} |")
    return '\n'.join(lines) + '\n'


def bibtex(p):
    fields = [('title', p['title']), ('year', p['date'][:4]), ('url', paper_url(p))]
    if p.get('arxiv'):
        fields += [('eprint', p['arxiv']), ('archivePrefix', 'arXiv')]
    return '@misc{' + p['id'] + ',\n' + ',\n'.join('  ' + k + ' = {' + v + '}' for k, v in fields) + '\n}'


def paper_card(p, sections):
    links = [f"[arXiv]({paper_url(p)})"] if 'arxiv' in p else [f"[Website]({p['url']})"]
    if p.get('arxiv') and not p['arxiv'].startswith('cs/'):
        links += [f"[HF](https://huggingface.co/papers/{p['arxiv']})"]
    if p.get('code'):
        links += [f"[Code]({p['code']})"]
    lines = [' · '.join(links), '', f"{p['date']} · {' · '.join(p.get('orgs', []))} · {sections[p['section']]['zh']}", '',
             ('**必读 / MUST READ**' if p.get('must_read') else '') + flag(p)]
    if p.get('status') == 'candidate':
        lines += ['', '**候选 / Candidate**']
    if p.get('needs_review'):
        lines += ['', '**分类待复核**：' + p['review_suggestion_zh']]
    lines += ['', '| 证据字段 | 记录 |', '| --- | --- |']
    e = evidence(p)
    for key, names in {**CHECKS, **CLASS_NAMES}.items():
        lines.append(f"| {names[0]} | {ICONS.get(e[key], '')} {VALUE_ZH[e[key]]} |")
    for field, title in [('summary', '一句话'), ('result', '关键结果')]:
        if p.get(field + '_zh'):
            lines += ['', f"**{title}**：{p[field+'_zh']}"]
    lines += ['', '<details><summary>English</summary>', '', '| Evidence field | Record |', '| --- | --- |']
    for key, names in {**CHECKS, **CLASS_NAMES}.items():
        value = 'not yet reviewed' if e[key] == 'unknown' else e[key]
        lines.append(f'| {names[1]} | {ICONS.get(e[key], "")} {value} |')
    for field, title in [('summary', 'Summary'), ('result', 'Key result')]:
        if p.get(field + '_en'):
            lines += ['', f"**{title}**: {p[field+'_en']}"]
    lines += ['', '</details>']
    return '\n'.join(lines)


def authored_notes(root, p, previous):
    """Move actual authored sections once; discard only empty TODO scaffolding."""
    after = previous.split('<!-- AUTO:CARD:END -->', 1)[-1] if previous else ''
    after = re.sub(r'<!-- AUTO:RELATED:START -->.*?<!-- AUTO:RELATED:END -->', '', after, flags=re.S)
    # The generated include is refreshed from the notes file, never re-imported.
    after = re.sub(r'<!-- AUTO:NOTES:START -->.*?<!-- AUTO:NOTES:END -->', '', after, flags=re.S)
    after = re.sub(r'<!--.*?-->', '', after, flags=re.S)
    pieces = re.split(r'(?m)(?=^## )', after)
    authored = '\n\n'.join(piece.strip() for piece in pieces if re.sub(r'(?m)^## .*$', '', piece).strip())
    path = root / 'notes' / (p['id'] + '.md')
    if authored:
        if path.exists() and authored not in path.read_text():
            raise ValueError(f'Conflicting authored notes for {p["id"]}; merge them manually')
        if not path.exists():
            write(path, authored + '\n')
    return path.read_text().strip() if path.exists() else ''


def related_papers(p, papers, routes):
    def ordinal(value):
        return date.fromisoformat((value + '-01-01')[:10]).toordinal()
    same = [other for other in papers if other['id'] != p['id'] and other['section'] == p['section']]
    adjacent = sorted(same, key=lambda other: (abs(ordinal(other['date']) - ordinal(p['date'])), other['id']))[:4]
    ids = [other['id'] for other in adjacent]
    ids += [pid for route in routes if p['id'] in route['papers'] for pid in route['papers'] if pid != p['id']]
    by_id = {other['id']: other for other in papers}
    return '\n'.join(f"- [{by_id[pid]['title']}]({pid}.md)" for pid in dict.fromkeys(ids))


def build(root=ROOT):
    from scripts.articles import build_articles

    build_articles(root)
    data, routes = validate(root)
    config = read_yaml(root / 'site.config.yaml')
    stats = compute_stats(data)
    env = Environment(loader=FileSystemLoader(root / 'scripts/templates'), autoescape=select_autoescape(['html', 'svg']), keep_trailing_newline=True)
    for lang, filename in [('zh', 'README.md'), ('en', 'README_en.md')]:
        text = (root / filename).read_text()
        for name, content in readme_blocks(data, routes, stats, lang, config, root).items():
            text = replace_block(text, name, content)
        write(root / filename, text)
    write(root / 'PAPERS.md', catalog(data, stats, config))
    for p in data['papers']:
        path = root / 'papers' / (p['id'] + '.md')
        previous = path.read_text() if path.exists() else ''
        notes = authored_notes(root, p, previous)
        text = f"# {p['title']}\n\n<!-- AUTO:CARD:START -->\n<!-- AUTO:CARD:END -->\n"
        text = replace_block(text, 'CARD', paper_card(p, data['meta']['sections']))
        if notes:
            text += '\n<!-- AUTO:NOTES:START -->\n\n' + notes + '\n\n<!-- AUTO:NOTES:END -->\n'
        related = related_papers(p, data['papers'], routes)
        if related:
            text += '\n<!-- AUTO:RELATED:START -->\n\n## 相关论文\n\n' + related + '\n\n<!-- AUTO:RELATED:END -->\n'
        write(path, text)
        e = evidence(p)
        color = '1E7F48' if all(e[k] == 'yes' for k in KEYS) else '8B909B' if any(e[k] == 'unknown' for k in KEYS) else '2A33D4'
        badge = {'schemaVersion': 1, 'label': 'evidence', 'message': ' · '.join(f'{name} {SYMBOLS[e[k]]}' for k, name in zip(KEYS, ['held-out', 'budget', 'transfer', 'cost'])), 'color': color}
        if p.get('needs_reading'):
            badge['message'] += ' · 待细读 / Needs verification'
        for folder in ['badges', 'site/badges']:
            write(root / folder / (p['id'] + '.json'), dump(badge))
        base = (config['base_url'] or '').rstrip('/')
        write(root / 'site/p' / (p['id'] + '.html'), env.get_template('paper.html').render(p=p, description=p.get('summary_zh','')+flag(p).replace('**',''), image=(base+'/cards/'+p['id']+'.png') if base else '../cards/'+p['id']+'.png', canonical=base+'/p/'+p['id']+'.html' if base else None))
    enriched = [{**p, 'evidence': evidence(p), 'short_title': short(p), 'bibtex': bibtex(p),
                 'note_url': config['repository_url'] + '/blob/main/notes/' + p['id'] + '.md' if (root / 'notes' / (p['id'] + '.md')).exists() else None, 'verification_label': '待细读 / Needs verification' if p.get('needs_reading') else ''} for p in data['papers']]
    gaps = read_gaps(root)
    payload = {'meta': data['meta'], 'papers': enriched, 'routes': routes, 'gaps': gaps, 'stats': stats, 'config': config, 'latest_edition': latest_edition(root)}
    write(root / 'site/papers.json', dump(payload))
    # A generated script also works over file://, where fetch(JSON) is restricted.
    write(root / 'site/data.js', 'window.HARNESS_DATA = ' + json.dumps(payload, ensure_ascii=False).replace('</', '<\\/') + ';\n')
    write(root / 'site/stats.json', dump(stats))
    # Owner artwork is static. Regenerate it explicitly with scripts/make_svgs.py.
    write(root / 'assets/taxonomy.svg', env.get_template('taxonomy.svg').render(sections=data['meta']['sections'], stats=stats))
    from scripts.site_header import render_header
    for filename, active, marker in [('index.html', 'home', 'SHARED_HEADER'), ('guide.html', 'guide', 'AUTO:HEADER')]:
        path = root / 'site' / filename
        if path.exists():
            text = path.read_text()
            start, end = f'<!-- {marker}:START -->', f'<!-- {marker}:END -->'
            if start not in text or end not in text:
                raise ValueError(f'{filename}: missing shared-header markers')
            before, rest = text.split(start, 1)
            _, after = rest.split(end, 1)
            write(path, before + start + '\n' + render_header(config, active) + '\n' + end + after)
    if not config.get('discussions_enabled'):
        print('Discussions are not enabled in site.config.yaml; discussion links are hidden.')
    citation = root / 'CITATION.cff'
    if citation.exists():
        value = citation.read_text()
        value = re.sub(r'(?m)^  - name: .*$', '  - name: ' + json.dumps(config['author_name'], ensure_ascii=False), value)
        write(citation, value)
    print(f"Built {stats['included']} included papers, {stats['candidates']} candidates, and {stats['must_read']} must-reads.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    build(parser.parse_args().root)
