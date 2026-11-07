"""Regenerate the article figures with matplotlib and a CJK font installed.

Input: the verbatim Table 6 transcription next to the generated SVG/CSV.
This is a manual authoring step; the offline website build uses committed SVGs.
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'site/articles/assets'
plt.rcParams.update({'font.family': 'Arial Unicode MS', 'svg.hashsalt': 'follow-rsi-article',
                     'font.size': 11, 'axes.unicode_minus': False})
BLUE, ORANGE, INK = '#2936ce', '#ac472f', '#20222a'


def save(fig, name, title, description):
    target = ASSETS / (name + '.svg')
    fig.savefig(target, metadata={'Date': None, 'Title': title, 'Description': description},
                facecolor='#faf9f6', bbox_inches='tight')
    target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines()) + '\n')
    plt.close(fig)


def table6():
    data = json.loads((ASSETS / 'harnessdev-table6.json').read_text())
    with (ASSETS / 'harnessdev-table6.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(data['rows'][0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(data['rows'])
    fig, axes = plt.subplots(2, 1, figsize=(10.6, 9.4), gridspec_kw={'height_ratios': [5, 4]})
    fig.subplots_adjust(left=.22, right=.94, top=.80, bottom=.16, hspace=.48)
    for ax, setting, heading in zip(axes, ('self', 'fixed_gemini'),
            ('自己搭、自己跑 · 5 条独立轨迹', '从头固定由 Gemini 执行 · 4 条独立轨迹')):
        rows = [r for r in data['rows'] if r['setting'] == setting]
        ax.set_facecolor('#faf9f6')
        for pos, row in enumerate(rows):
            for offset, field, color in ((-.17, 'feedback_delta_reported', BLUE),
                                         (.17, 'heldout_delta_reported', ORANGE)):
                value = float(row[field])
                ax.barh(pos + offset, value, height=.28, color=color, zorder=3)
                ax.text(value + (.25 if value >= 0 else -.25), pos + offset,
                        f'{value:+.2f}', ha='left' if value >= 0 else 'right',
                        va='center', fontsize=10, color=INK)
        ax.set_yticks(range(len(rows)), [r['creator'] for r in rows])
        ax.invert_yaxis()
        ax.set_xlim(-13, 16)
        ax.axvline(0, color='#888b95', linewidth=.8)
        ax.grid(axis='x', color='#e0e0e5', zorder=0)
        ax.set_title(heading, loc='left', fontsize=13, fontweight='bold', pad=14)
        ax.tick_params(axis='both', length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
    axes[1].set_xlabel('论文报告的 Δ（百分点）', labelpad=12)
    fig.text(.05, .96, '反馈上的进步，能留到新任务上吗？', fontsize=23, fontweight='bold', color=INK)
    fig.text(.05, .915, 'HarnessDev · 表 6 · 初始 H₀ 到作者声明末版的变化', fontsize=12, color='#626674')
    fig.text(.05, .875, '■ 反馈：SWE-Pro 100 题与 Terminal-Bench 89 题的均值', color=BLUE, fontsize=11)
    fig.text(.59, .875, '■ 留出：SWE-Pro 630 题', color=ORANGE, fontsize=11)
    fig.text(.05, .085, '两组分别展示；反馈列与留出列题集不同。每个组合仅一条演化轨迹，无独立重复演化误差条。',
             fontsize=10, color='#626674')
    fig.text(.05, .055, '保留原表 Δ，未用四舍五入端点重新相减。来源：arXiv 2609.01437，Table 6。',
             fontsize=10, color='#626674')
    fig.text(.05, .025, 'Follow RSI · adongwanai.github.io/follow-rsi', fontsize=10, color=BLUE)
    save(fig, 'harnessdev-table6', 'HarnessDev 表 6：九条演化轨迹',
         '分组横向柱状图。五条 self-runtime 轨迹留出增益全正；四条 fixed-Gemini 轨迹中三条留出下降。数值见同目录 CSV。')


def loop():
    fig, ax = plt.subplots(figsize=(10.6, 4.7))
    ax.set_xlim(0, 10.6); ax.set_ylim(0, 4.7); ax.axis('off')
    ax.text(.3, 4.22, '三个问题，贯穿同一道验证关', fontsize=22, fontweight='bold', color=INK)
    columns = [(.3, '01', '决定改什么', 'Aspire', '目标、数据与训练选择'),
               (3.85, '02', '从经历中学习', 'S³Gym', '自评、上下文与记忆'),
               (7.4, '03', '沉淀进 Harness', 'HarnessDev', '可复用的程序与流程')]
    for x, number, title, paper, caption in columns:
        ax.add_patch(FancyBboxPatch((x, 1.55), 2.9, 2.12, boxstyle='round,pad=.06,rounding_size=.08',
                                   facecolor='white', edgecolor='#dddedf'))
        ax.text(x+.17, 3.24, number, fontsize=13, color=BLUE)
        ax.text(x+.17, 2.78, title, fontsize=17, fontweight='bold', color=INK)
        ax.text(x+.17, 2.27, paper, fontsize=13, color=BLUE)
        ax.text(x+.17, 1.86, caption, fontsize=10.5, color='#626674')
    for x in (3.36, 6.91):
        ax.text(x, 2.55, '→', fontsize=22, color='#888b95', ha='center')
    ax.add_patch(FancyBboxPatch((.3, .52), 10, .64, boxstyle='round,pad=.06,rounding_size=.06',
                               facecolor='#e9eafa', edgecolor='none'))
    ax.text(5.3, .83, '独立验证：新任务上是否有效？同预算下是否更好？能否区分收益与噪声？',
            ha='center', va='center', color=BLUE, fontsize=12)
    ax.text(.3, .15, '本文的阅读顺序，不是三个基准共同执行的实验流水线。   Follow RSI', fontsize=10, color='#626674')
    save(fig, 'self-improvement-loop', '自我进化的三个阅读问题',
         'Aspire：决定改什么。S³Gym：从经历中学习。HarnessDev：沉淀进 Harness。独立验证贯穿所有问题。')


if __name__ == '__main__':
    table6()
    loop()
