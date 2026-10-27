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


def readme_metrics(root, lang):
    """Publish weekly metrics only from a reviewed, published edition."""
    zh = lang == 'zh'
    header = ('| 本周发现 | 本周收录 | 自动判断准确率 | 漏检（对照公开清单） | 中位时效 |'
              if zh else '| Found this week | Accepted | Auto-judgment precision | Misses vs. public lists | Median latency |')
    lines = [header, '| :---: | :---: | :---: | :---: | :---: |']
    editions = [json.loads(path.read_text()) for path in (root / 'site/weekly').glob('????-W??.json')]
    published = [edition for edition in editions if edition.get('reviewed_only') and not edition.get('demo')]
    if published:
        latest = max(published, key=lambda edition: edition['week'])
        metrics = latest['metrics']
        precision = '—' if metrics['precision'] is None else f"{metrics['precision']:.1%}"
        latency = '—' if metrics['latency_days'] is None else f"{metrics['latency_days']:g} {'天' if zh else 'days'}"
        misses = metrics.get('recall_vs_reference', {}).get('missed', '—')
        lines += [f"| {metrics['found']} | {metrics['accepted']} | {precision} | {misses} | {latency} |", '',
                  f"[{'最近发布' if zh else 'Latest edition'}: {latest['week']}](digests/{latest['week']}{'' if zh else '.en'}.md)"]
    else:
        lines.append('| — | — | — | — | — |')
    evaluation = root / 'feed/eval/report.json'
    if evaluation.exists():
        report = json.loads(evaluation.read_text())
        status = 'passed' if report.get('thresholds_passed') else report['status'] if report['status'] != 'complete' else 'failed'
        lines += ['', f"{'提示词回归评测' if zh else 'Prompt regression evaluation'}: **{status}** · [" + ('报告' if zh else 'report') + '](feed/eval/report.md).']
    return '\n'.join(lines)


def readme_blocks(data, routes, stats, lang, config, root):
    papers, sections = data['papers'], data['meta']['sections']
    zh = lang == 'zh'
    cov, checks = stats['evidence_coverage'], stats['check_coverage']
    base = (config['base_url'] or '<SITE_URL>').rstrip('/')
    badge_values = [('证据库' if zh else 'evidence_base', f"{stats['included']}_{'篇' if zh else 'papers'}", '2A33D4'),
                    ('必读' if zh else 'must-read', f"{stats['must_read']}", '14161C'),
                    ('更新' if zh else 'updated', stats['as_of'], '14161C'),
                    ('内容' if zh else 'content', 'CC_BY_4.0', '14161C')]
    badges = ' '.join(f'![{name}](https://img.shields.io/badge/{quote(name.replace("-", "--"))}-{quote(value.replace("-", "--"))}-{color})'
                      for name, value, color in badge_values)
    badges += f' ![feed](https://img.shields.io/endpoint?url={quote(base + "/badges/feed-updated.json", safe="")})'
    if zh:
        overview = f"{stats['included']} 篇正式收录 · {stats['candidates']} 篇候选 · {stats['must_read']} 篇必读 · {stats['needs_reading']} 篇待细读。"
        coverage = f"证据字段已审 **{cov['ratio']:.1%}**（{cov['reviewed']}/{cov['total']}，每篇 8 项核查 + {len(CLASSES)} 项分类）；其中 8 项核查已审 **{checks['ratio']:.1%}**（{checks['reviewed']}/{checks['total']}）。统计仅含正式收录；已审指值非 `unknown`，包含 `no`、`partial`、`na`，不表示达标。"
    else:
        overview = f"{stats['included']} included · {stats['candidates']} candidates · {stats['must_read']} must-reads · {stats['needs_reading']} need verification."
        coverage = f"Evidence fields **{cov['ratio']:.1%} reviewed so far** ({cov['reviewed']}/{cov['total']}; 8 checks + {len(CLASSES)} classifications per paper). The 8 audit checks alone are **{checks['ratio']:.1%} reviewed so far** ({checks['reviewed']}/{checks['total']}). Included papers only; reviewed means non-`unknown`, including `no`, `partial`, and `na`, not a pass rate."
    stat_lines = [overview, '', coverage, '', '<details><summary>' + ('各方向篇数' if zh else 'Paper counts by direction') + '</summary>', '', '| 方向 / Section | 篇数 / Papers |', '| --- | ---: |']
    stat_lines += [f"| {sections[s][lang]} | {count} |" for s, count in stats['sections'].items()]
    stat_lines += ['', '</details>']
    must = '\n'.join(f"{i}. [{p['title']}](papers/{p['id']}.md){flag(p)}" for i, p in enumerate(must_reads(papers, routes), 1))
    by_id = {p['id']: p for p in papers}
    rt = ['| 路线 | 顺序 | 问题 |' if zh else '| Route | Order | Question |', '| --- | --- | --- |']
    for r in routes:
        chain = ' → '.join(f"[{short(by_id[pid])}](papers/{pid}.md){flag(by_id[pid])}" for pid in r['papers'])
        rt.append(f"| {cell(r['name_'+lang])} | {chain} | {cell(r['question_'+lang])} |")
    tables = ['✅ yes / 有 · ◐ partial / 部分 · ❌ no / 没有 · ❔ unknown / 未审 · — na / 不适用', '',
              '图标顺序：留出集 · 同预算对照 · 跨模型迁移 · 报告成本。缺失证据不作推断。' if zh else 'Icon order: held-out · matched budget · cross-model transfer · cost. Missing evidence is never inferred.', '']
    for section in sections:
        group = sorted([p for p in papers if p['section'] == section], key=lambda p: p['date'])
        tables += [f"### {sections[section][lang]}", '', f'<details><summary>{len(group)} '+('篇论文' if zh else 'papers')+'</summary>', '',
                   '| 日期 | 论文 | 机构 | 核心机制 | 关键结果 | 证据 | 页面 |' if zh else '| Date | Paper | Organizations | Mechanism | Key result | Evidence | Page |',
                   '| --- | --- | --- | --- | --- | --- | --- |']
        for p in group:
            e = evidence(p)
            tables.append('| ' + ' | '.join([p['date'], f"[{cell(p['title'])}]({paper_url(p)}){flag(p)}", cell(' · '.join(p.get('orgs', []))), cell(p.get('summary_'+lang, '')), cell(p.get('result_'+lang, '')), ' '.join(ICONS[e[k]] for k in KEYS), f"[{'证据卡' if zh else 'Receipt'}](papers/{p['id']}.md)"]) + ' |')
        tables += ['', '</details>', '']
    repository = quote(config['repository'], safe='/')
    history = f'[![Star History](https://api.star-history.com/svg?repos={repository}&type=Date)](https://star-history.com/#{repository}&Date)'
    return {'BADGES': badges, 'STATS': '\n'.join(stat_lines), 'MUST_READ': must, 'ROUTES': '\n'.join(rt),
            'TABLES': '\n'.join(tables), 'METRICS': readme_metrics(root, lang), 'STAR_HISTORY': history}


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
    lines += ['', '| 证据字段 / Evidence field | 值 / Value |', '| --- | --- |']
    e = evidence(p)
    lines += [f'| `{k}` | {e[k]} |' for k in FIELDS]
    for field, title in [('summary', '一句话'), ('result', '关键结果')]:
        if field + '_zh' in p:
            lines += ['', f"**{title}**：{p[field+'_zh']}"]
    translation = 'machine translation' if p.get('en_machine_translated') else 'owner translation' if 'en_machine_translated' in p else 'translation planned'
    lines += ['', f'<details><summary>English · {translation}</summary>', '', flag(p).strip()]
    for field, title in [('summary', 'Summary'), ('result', 'Key result')]:
        if field + '_zh' in p:
            lines += ['', f"**{title}**: {p.get(field+'_en', '<!-- TODO: English translation -->')}"]
    lines += ['', '</details>']
    return '\n'.join(lines)


def build(root=ROOT):
    data, routes = validate(root)
    config = read_yaml(root / 'site.config.yaml')
    stats = compute_stats(data)
    env = Environment(loader=FileSystemLoader(root / 'scripts/templates'), autoescape=select_autoescape(['html', 'svg']), keep_trailing_newline=True)
    for lang, filename in [('zh', 'README.md'), ('zh', 'README_zh.md'), ('en', 'README_en.md')]:
        text = (root / filename).read_text()
        for name, content in readme_blocks(data, routes, stats, lang, config, root).items():
            text = replace_block(text, name, content)
        write(root / filename, text)
    for p in data['papers']:
        path = root / 'papers' / (p['id'] + '.md')
        text = path.read_text() if path.exists() else f"# {p['title']}\n\n<!-- AUTO:CARD:START -->\n<!-- AUTO:CARD:END -->\n\n## 精读笔记\n\n<!-- TODO -->\n\n## 视频\n\n<!-- TODO -->\n\n## 可延伸的 idea\n\n<!-- TODO -->\n\n## 相关论文\n\n<!-- TODO -->\n"
        write(path, replace_block(text, 'CARD', paper_card(p, data['meta']['sections'])))
        e = evidence(p)
        color = '1E7F48' if all(e[k] == 'yes' for k in KEYS) else '8B909B' if any(e[k] == 'unknown' for k in KEYS) else '2A33D4'
        badge = {'schemaVersion': 1, 'label': 'evidence', 'message': ' · '.join(f'{name} {SYMBOLS[e[k]]}' for k, name in zip(KEYS, ['held-out', 'budget', 'transfer', 'cost'])), 'color': color}
        if p.get('needs_reading'):
            badge['message'] += ' · 待细读 / Needs verification'
        for folder in ['badges', 'site/badges']:
            write(root / folder / (p['id'] + '.json'), dump(badge))
        base = (config['base_url'] or '').rstrip('/')
        write(root / 'site/p' / (p['id'] + '.html'), env.get_template('paper.html').render(p=p, description=p.get('summary_zh','')+flag(p).replace('**',''), image=(base+'/cards/'+p['id']+'.png') if base else '../cards/'+p['id']+'.png', canonical=base+'/p/'+p['id']+'.html' if base else None))
    enriched = [{**p, 'evidence': evidence(p), 'short_title': short(p), 'verification_label': '待细读 / Needs verification' if p.get('needs_reading') else ''} for p in data['papers']]
    gaps = read_gaps(root)
    payload = {'meta': data['meta'], 'papers': enriched, 'routes': routes, 'gaps': gaps, 'stats': stats, 'config': config}
    write(root / 'site/papers.json', dump(payload))
    # A generated script also works over file://, where fetch(JSON) is restricted.
    write(root / 'site/data.js', 'window.HARNESS_DATA = ' + json.dumps(payload, ensure_ascii=False).replace('</', '<\\/') + ';\n')
    for path in ['stats.json', 'site/stats.json']:
        write(root / path, dump(stats))
    # Owner artwork is static. Regenerate it explicitly with scripts/make_svgs.py.
    write(root / 'assets/taxonomy.svg', env.get_template('taxonomy.svg').render(sections=data['meta']['sections'], stats=stats))
    for section in data['meta']['sections']:
        if section == 'candidates':
            continue
        path = root / 'directions' / (section + '.md')
        if not path.exists():
            write(path, f"# {data['meta']['sections'][section]['zh']}\n\n## 整体解读 / Overview\n\n<!-- TODO -->\n")
    print(f"Built {stats['included']} included papers, {stats['candidates']} candidates, and {stats['must_read']} must-reads.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    build(parser.parse_args().root)
