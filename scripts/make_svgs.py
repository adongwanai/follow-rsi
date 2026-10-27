"""Generate README visuals for Follow RSI: direction map + banner, zh/en x light/dark.
Usage: python make_svgs.py <out_dir>
"""
import sys, os
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "light": dict(bg="#F1F2F4", surface="#FFFFFF", ink="#14161C", ink2="#585D69", rule="#D6D9E0",
                  dot="#D6D9E0", accent="#2A33D4", accent_soft="#E4E6FF", on_accent="#FFFFFF"),
    "dark": dict(bg="#0E1015", surface="#161920", ink="#E8EAF0", ink2="#9BA1AD", rule="#2A2F3A",
                 dot="#262B35", accent="#8D93FF", accent_soft="#22264A", on_accent="#0E1015"),
}
SERIF = "'Noto Serif SC','Source Han Serif SC','Songti SC','STSong',Georgia,serif"
SANS = "-apple-system,BlinkMacSystemFont,'PingFang SC','Noto Sans CJK SC','Noto Sans SC','Microsoft YaHei','Segoe UI',sans-serif"
MONO = "'SFMono-Regular','JetBrains Mono',Menlo,Consolas,monospace"

def t(x, y, s, size, fill, family=SANS, weight=400, anchor="start", ls=None, cls=None):
    extra = f' letter-spacing="{ls}"' if ls is not None else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}{c}>{esc(s)}</text>')

def dots(w, h, c):
    return (f'<defs><pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse">'
            f'<circle cx="9" cy="9" r="1" fill="{c["dot"]}"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" fill="{c["bg"]}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#dots)"/>')

# ------------------------------------------------------------------ direction map
MAP = {
 "zh": dict(
   title="RSI 研究版图",
   sub="按「每一轮被改进、并带入下一轮的是什么」划分 · 代表工作取自 Follow RSI 收录论文",
   foot="Follow RSI · 方向图 2026.10",
   sections=[
     ("改进对象", "主轴：每一轮被改进、并带入下一轮的对象"),
     ("协同方式", "一次改一类对象，还是多类一起改"),
     ("应用场景", "在哪里自我改进"),
     ("支撑方向", "怎么衡量、怎么解释、怎么管住"),
     ("横切维度", "给自己的论文定位"),
   ],
   main_a=[
     ("Harness / 脚手架 RSI", "提示 · 工具 · 记忆 · 技能 · 控制流 · 改进器本身", "AHE · Self-Harness · DarwinX · RRSI · AIDE²", "证据库重点 · 98 篇"),
     ("模型 / 权重 RSI", "模型用自己产生的数据训练自己", "RSIPO · Terminal-RSI · RISE", None),
     ("数据与任务 RSI", "数据配比 · 任务与课程 · 环境", "NeoHorse-1 · ClawLoop", None),
   ],
   main_b=[
     ("训练算法 / AI 研发", "训练算法 · 模型研发 · 研究流程", "Frontis-MA1 · SwarmRSI"),
     ("经验与世界模型", "记忆 · 规则手册 · 世界模型 · 探索", "Memento 3 · RSIAgent"),
     ("元 RSI", "改进「负责改进的机制」本身", "Hyperagents · Meta^n · HSI"),
     ("具身与物理 RSI", "机器人在仿真或真机中递归改进", "EMHO · Physical RSI"),
   ],
   coop=[("单层改进", "只改一类对象", "大多数工作"),
         ("模型与 Harness 协同", "Harness 与权重交替或联合更新", "HarnessX · Self-HPO · CoEvo-RSI"),
         ("多层统一框架", "模型、数据、Harness 统一调度", "MetaRSI / RSI²")],
   apps=[("编码与终端", "DGM · Ouroboros"), ("AI 研究与 MLE", "AIDE² · RHI"),
         ("科学发现", "SwarmRSI · ScienceBuddy"), ("企业流程", "StarHarness · OO-Harness"),
         ("电脑操作", "Agent S4 · PILOT")],
   support=[("评测与基准", "Evo-Bench · RSIGym"), ("归因与可信度", "HDA · Auditing"),
            ("理论与综述", "Self-Evolving Agent Harness"), ("安全与治理", "Trusting Trust")],
   cross=[("谁来改", "自改 · 他改 · 训练出的改进者"), ("反馈来源", "真值 · 代理信号 · 自评"),
          ("递归深度", "L1–L5"), ("改进时机", "离线 · 在线 · 测试时"),
          ("证据强度", "留出集 · 同预算 · 跨模型")],
 ),
 "en": dict(
   title="The RSI Research Map",
   sub="Organized by what gets improved and carried into the next round · examples from papers tracked by Follow RSI",
   foot="Follow RSI · research map 2026.10",
   sections=[
     ("WHAT IMPROVES", "Main axis: the object improved and carried into the next round"),
     ("HOW THEY COMBINE", "One kind of object, or several at once"),
     ("WHERE", "Where self-improvement happens"),
     ("SUPPORT", "How it is measured, explained and governed"),
     ("CROSS-CUTTING", "Dimensions for positioning your own paper"),
   ],
   main_a=[
     ("Harness / scaffold RSI", "Prompts · tools · memory · skills · control flow · the improver", "AHE · Self-Harness · DarwinX · RRSI · AIDE²", "Evidence base · 98 papers"),
     ("Model-weight RSI", "Models train on their own data", "RSIPO · Terminal-RSI · RISE", None),
     ("Data & task RSI", "Data mixtures · curricula · environments", "NeoHorse-1 · ClawLoop", None),
   ],
   main_b=[
     ("AI-for-AI RSI", "Training algorithms · R&D · research", "Frontis-MA1 · SwarmRSI"),
     ("Experience & world models", "Memory · rulebooks · world models", "Memento 3 · RSIAgent"),
     ("Meta-level RSI", "Improving the improver itself", "Hyperagents · Meta^n · HSI"),
     ("Embodied RSI", "Robots improving in sim or reality", "EMHO · Physical RSI"),
   ],
   coop=[("Single-layer", "One kind of object", "Most work"),
         ("Model–harness co-evolution", "Harness and weights updated together", "HarnessX · Self-HPO · CoEvo-RSI"),
         ("Unified multi-layer", "Model, data and harness scheduled jointly", "MetaRSI / RSI²")],
   apps=[("Coding & terminal", "DGM · Ouroboros"), ("AI research & MLE", "AIDE² · RHI"),
         ("Scientific discovery", "SwarmRSI · ScienceBuddy"), ("Enterprise workflows", "StarHarness · OO-Harness"),
         ("Computer use", "Agent S4 · PILOT")],
   support=[("Benchmarks", "Evo-Bench · RSIGym"), ("Attribution & trust", "HDA · Auditing"),
            ("Theory & surveys", "Self-Evolving Agent Harness"), ("Safety & governance", "Trusting Trust")],
   cross=[("Who edits", "self · external · trained"), ("Feedback", "ground truth · proxy · self"),
          ("Recursion depth", "L1–L5"), ("Timing", "offline · online · test time"),
          ("Evidence", "held-out · budget · transfer")],
 ),
}

def box(x, y, w, h, c, title, line1=None, line2=None, hi=False, dashed=False, tsize=16, badge=None):
    fill = c["accent_soft"] if hi else c["surface"]
    stroke = c["accent"] if hi else c["rule"]
    sw = 1.5 if hi else 1
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>']
    ty = y + 28
    out.append(t(x + 16, ty, title, tsize, c["accent"] if hi else c["ink"], SERIF, 700, cls="fit"))
    if badge:
        out.append(f'<g class="badge">')
        bw = 14 + 7.2 * len(badge) if badge.isascii() else 16 + 12 * sum(1 if ord(ch) > 127 else 0.55 for ch in badge)
        out.append(f'<rect x="{x + w - 16 - bw:.1f}" y="{y + 12:.1f}" width="{bw:.1f}" height="22" rx="3" fill="{c["accent"]}"/>')
        out.append(t(x + w - 16 - bw / 2, y + 27.5, badge, 12, c["on_accent"], MONO if badge.isascii() else SANS, 600, "middle"))
        out.append('</g>')
    if line1:
        out.append(t(x + 16, ty + 22, line1, 13, c["ink2"], SANS, cls="fit"))
    if line2:
        out.append(t(x + 16, ty + (44 if line1 else 22), line2, 12, c["accent"], MONO, cls="fit"))
    return "".join(out)

def direction_map(lang, theme):
    d, c = MAP[lang], THEMES[theme]
    W, M, G = 1200, 40, 16
    CW = W - 2 * M
    parts = []
    y = 56
    parts.append(t(M, y, d["title"], 30, c["ink"], SERIF, 900))
    parts.append(t(M, y + 28, d["sub"], 14, c["ink2"]))
    y += 64

    def section(idx, y):
        name, desc = d["sections"][idx]
        parts.append(f'<line x1="{M}" y1="{y:.1f}" x2="{W - M}" y2="{y:.1f}" stroke="{c["ink"]}" stroke-width="1"/>')
        parts.append(t(M, y + 22, name, 13, c["accent"], MONO if lang == "en" else SANS, 600, ls=(1.2 if lang == "en" else 1)))
        off = 118 if lang == "zh" else (len(name) * 9 + 30)
        parts.append(t(M + off, y + 22, desc, 13, c["ink2"]))
        return y + 38

    # 1. main axis
    y = section(0, y)
    u = (CW - 3 * G) / 4
    xs = [M, M + 2 * u + 2 * G, M + 3 * u + 3 * G]
    ws = [2 * u + G, u, u]
    for (title, l1, l2, badge), x, w in zip(d["main_a"], xs, ws):
        parts.append(box(x, y, w, 100, c, title, l1, l2, hi=badge is not None, badge=badge, tsize=18 if badge else 16))
    y += 100 + G
    for i, (title, l1, l2) in enumerate(d["main_b"]):
        parts.append(box(M + i * (u + G), y, u, 100, c, title, l1, l2))
    y += 100 + 26

    # 2. cooperation
    y = section(1, y)
    w3 = (CW - 2 * G) / 3
    for i, (title, l1, l2) in enumerate(d["coop"]):
        parts.append(box(M + i * (w3 + G), y, w3, 100, c, title, l1, l2))
    y += 100 + 26

    # 3. applications
    y = section(2, y)
    w5 = (CW - 4 * G) / 5
    for i, (title, l2) in enumerate(d["apps"]):
        parts.append(box(M + i * (w5 + G), y, w5, 76, c, title, None, l2, tsize=15))
    y += 76 + 26

    # 4. support
    y = section(3, y)
    w4 = (CW - 3 * G) / 4
    for i, (title, l2) in enumerate(d["support"]):
        parts.append(box(M + i * (w4 + G), y, w4, 76, c, title, None, l2, tsize=15))
    y += 76 + 26

    # 5. cross-cutting
    y = section(4, y)
    for i, (title, l1) in enumerate(d["cross"]):
        parts.append(box(M + i * (w5 + G), y, w5, 76, c, title, l1, None, dashed=True, tsize=15))
    y += 76 + 30
    parts.append(t(W - M, y, d["foot"], 12, c["ink2"], MONO, anchor="end"))
    H = y + 28
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}" '
            f'role="img" aria-label="{esc(d["title"])}"><title>{esc(d["title"])}</title>')
    return head + dots(W, H, c) + "".join(parts) + "</svg>"

# ------------------------------------------------------------------ banner
BANNER = {
 "zh": dict(eyebrow="FOLLOW RSI · 递归自我改进", title="Follow RSI",
            tagline="每天 5 分钟，跟上 RSI 前沿。",
            sub="AI 正在学会改进自己。我们为它的每一步留下记录。",
            s1=("HDA · arXiv 2610.22466", "54%", ["搜索集上的演化收益，平均 54%", "来自过拟合，14% 来自多花的算力"]),
            s2=("Auditing · arXiv 2610.27610", "4/26", ["声称改进了「改进流程」的论文里，", "只有 4 篇做了同起点、同预算对比"]),
            tsize=26, ssize=16, stub_size=15),
 "en": dict(eyebrow="FOLLOW RSI · RECURSIVE SELF-IMPROVEMENT", title="Follow RSI",
            tagline="Five minutes a day to keep up with recursive self-improvement.",
            sub="AI is learning to improve itself. We keep the record.",
            s1=("HDA · arXiv 2610.22466", "54%", ["of harness-evolution gains on the", "search set come from overfitting"]),
            s2=("Auditing · arXiv 2610.27610", "4/26", ["papers claiming a better improver", "ran a matched-budget comparison"]),
            tsize=19, ssize=15, stub_size=13.5),
}

def banner(lang, theme):
    b, c = BANNER[lang], THEMES[theme]
    W, H, M = 1280, 340, 48
    p = [dots(W, H, c)]
    p.append(t(M, 92, b["eyebrow"], 13, c["accent"], MONO, 600, ls=1.6))
    p.append(t(M - 3, 170, b["title"], 78, c["ink"], SERIF, 900, ls=-1))
    p.append(t(M, 220, b["tagline"], b["tsize"], c["ink"], SERIF if lang == "zh" else SANS, 700))
    p.append(t(M, 256, b["sub"], b["ssize"], c["ink2"]))
    p.append(f'<line x1="{M}" y1="290" x2="{M + 64}" y2="290" stroke="{c["accent"]}" stroke-width="3"/>')
    sx, sw, sh = 800, 432, 104
    for i, (src, big, lines) in enumerate([b["s1"], b["s2"]]):
        y = 70 + i * (sh + 16)
        p.append(f'<rect x="{sx}" y="{y}" width="{sw}" height="{sh}" rx="6" fill="{c["surface"]}" stroke="{c["rule"]}"/>')
        p.append(f'<line x1="{sx}" y1="{y + 12}" x2="{sx}" y2="{y + sh - 12}" stroke="{c["bg"]}" stroke-width="3"/>')
        p.append(f'<line x1="{sx}" y1="{y + 12}" x2="{sx}" y2="{y + sh - 12}" stroke="{c["rule"]}" stroke-width="2" stroke-dasharray="4 4"/>')
        p.append(t(sx + 20, y + 26, src, 12, c["ink2"], MONO))
        p.append(t(sx + 20, y + 80, big, 46, c["ink"], MONO, 700, ls=-1, cls="big"))
        tx = sx + (138 if len(big) <= 3 else 156)
        p.append(t(tx, y + 62, lines[0], b["stub_size"], c["ink2"], cls="fit"))
        p.append(t(tx, y + 84, lines[1], b["stub_size"], c["ink2"], cls="fit"))
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Follow RSI"><title>Follow RSI</title>')
    return head + "".join(p) + "</svg>"

for lang in ("zh", "en"):
    for theme in ("light", "dark"):
        sfx = "" if lang == "en" else "-zh"
        open(os.path.join(OUT, f"rsi-map{sfx}-{theme}.svg"), "w", encoding="utf-8").write(direction_map(lang, theme))
        open(os.path.join(OUT, f"banner{sfx}-{theme}.svg"), "w", encoding="utf-8").write(banner(lang, theme))
print("ok", sorted(os.listdir(OUT)))
