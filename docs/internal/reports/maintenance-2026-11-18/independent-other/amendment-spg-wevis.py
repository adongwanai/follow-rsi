"""Append two narrow source-bound corrections without rewriting the frozen review."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys

from bs4 import BeautifulSoup

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from scripts.feed.guard import check_summary

OUT = ROOT / 'docs/internal/reports/maintenance-2026-11-18/independent-other'
sha = lambda b: hashlib.sha256(b).hexdigest()
norm = lambda s: ' '.join(s.split())
now = datetime.now(timezone.utc).isoformat()
frozen_path = OUT / 'review-findings.json'
frozen_sha = 'c0ea23c585f394e1ebf3e25f4c87a7578e8309c9af52497d934106e8c125b8e3'
assert sha(frozen_path.read_bytes()) == frozen_sha
frozen = json.loads(frozen_path.read_text())
rows = {r['id']: r for r in frozen['items']}
inputs = {r['id']: r for r in json.loads((OUT / 'input-records.json').read_text())['records']}


def extract(aid, selector, needle=None, limit=2400):
    row = rows['arxiv:' + aid]
    src = row['source_receipt']
    assert sha((ROOT / src['body_path']).read_bytes()) == src['body_sha256']
    assert sha((ROOT / src['text_path']).read_bytes()) == src['text_sha256']
    soup = BeautifulSoup((ROOT / src['body_path']).read_text(), 'html.parser')
    el = soup.find(id=selector)
    assert el is not None, selector
    section = norm(el.get_text(' ', strip=True))
    start = section.index(needle) if needle else 0
    selected = section[start:start + limit]
    text = norm((ROOT / src['text_path']).read_text())
    offset = text.index(selected)
    return {'selector': selector, 'quote': selected,
            'text_start': offset, 'text_end': offset + len(selected),
            'quote_sha256': sha(selected.encode()), 'body_sha256': src['body_sha256'],
            'text_sha256': src['text_sha256'], 'source_url': src['official_url']}


spg = {
    'id': 'arxiv:2611.18818', 'version': 1, 'reviewed_on': '2026-11-18',
    'supersedes': {'suggestion': 'reject', 'frozen_reason_zh': rows['arxiv:2611.18818']['reason_zh']},
    'suggestion': 'defer',
    'scope_status': 'unresolved boundary between retained experience and feedback-revised operational skill instructions',
    'possible_classification_if_evidence_resolved': {'primary': 'harness', 'harness_sub': 'evidence_selection'},
    'reason_zh': '撤回仅以经验 schema/adapter 固定及自然语言形式作排除的理由。failure-driven SkillBank expansion、insight Edit/Add 及冻结后跨任务复用是正证据；principle/when_to_apply 可以承载可执行于 LLM 的操作指令。当前可具体阅读的生成示例未绑定报告实验，尚不足确认实际采用的修改对象与持久部署链。',
    'positive_evidence_zh': [
        'C.2.2 明确保留 failure-driven SkillBank expansion、ExpeL 的 Agree/Remove/Edit/Add，以及跨任务 Shared Reflexion。',
        '§4.1 的 practice trajectory 更新 backend state，随后冻结，并对 held-out tasks 单次评测，明确支持持久经验/技能跨任务使用。',
        'C.3 的 principle/when_to_apply 描述操作条件与动作规则；不能因文本格式或管理器固定就排除。',
        'C.4 的真实持久日志列出 retrieved skill guidance 和 held-out 成功轨迹，支持确有后续使用。'],
    'counterevidence_and_gap_zh': [
        'Verify Object Location First 是 Prompt B.1 内的 JSON 格式例，不是已核实实验工件。',
        'Require Observable State Change 是附录新生成例，正文明确 illustrative output、separate from reported experimental runs。',
        'C.4 给技能标题、避免事项和执行轨迹，未给与具体失败反馈、技能原文修改/插入记录绑定的版本链；不能据此断言所有条目只是原始经验，也不能把 illustrative 示例当正式采用修改。'],
    'missing_evidence_zh': '补报告实验实际采用的 skill/insight 原文或版本差异，绑定产生它的失败反馈、写入/接受记录和后续任务调用。无需以可执行代码作为唯一形式；条件化、跨任务保留的操作指令也可成立。',
    'resume_action_zh': '获取实验日志/已部署 skillbank 或 insight 文件后复核对象；若确为反馈生成且持久调用的操作规则，可纳入 Harness 专项任务/证据选择。否则归经验或数据选择范围。',
    'original_quotes': [extract('2611.18818', 'A3.SS2.SSS2'),
                        extract('2611.18818', 'S4.SS1', 'Practice and evaluation.', 1950),
                        extract('2611.18818', 'A3.SS3', 'Prompt B.1:', 3100),
                        extract('2611.18818', 'A3.SS4', limit=2400)],
    'formal_acceptance': False,
}

zh = ('WeVisForensics 同时更新视觉检查器权重和可复用的报告规则；规则修订须在近期留出调用上改善判断并保留既有正确判断，再发布到后续轮次。'
      '视觉 OCR 一致性检查器也参与训练；音频工具和 PaddleOCR 检测器保持固定。')
en = ('WeVisForensics updates both visual-inspector weights and reusable reporting rules. Rule revisions must improve judgments on held-out recent calls '
      'without losing previously correct judgments before publication to subsequent rounds. The visual OCR consistency inspector also trains, while audio tools '
      'and the PaddleOCR detector remain fixed.')
inp = inputs['arxiv:2611.21373']
guard = check_summary(inp['title'], inp['abstract'], zh, en)
assert guard['ok'], guard
wevis = {
    'id': 'arxiv:2611.21373', 'version': 1, 'reviewed_on': '2026-11-18',
    'suggestion': 'include', 'primary': 'harness', 'harness_sub': 'coevolution',
    'supersedes': {'summary_zh': rows['arxiv:2611.21373']['summary_zh'],
                   'summary_en': rows['arxiv:2611.21373']['summary_en']},
    'correction_zh': '旧摘要笼统写 OCR 保持固定会误导。固定的是用于定位/识别候选文本的 PaddleOCR detector；OCR consistency inspector 是参与 LoRA 和 skill-card 更新的视觉成员。',
    'summary_zh': zh, 'summary_en': en, 'summary_number_guard': guard,
    'original_quotes': [extract('2611.21373', 'S2.SS2', 'Table 1:', 1250),
                        extract('2611.21373', 'S2.SS2.SSS0.Px4', limit=2000),
                        extract('2611.21373', 'A4', 'OCR 6 rules', 1500)],
    'limitations_zh': ['近期留出 calls 的验收不保证所有视频表现单调；分类建议保持 coevolution。']}

doc = {'generated_at': now, 'reviewer': 'independent sub-agent /root/nov18_independent_recovery',
       'amendment_type': 'post-freeze narrow crossreview correction',
       'frozen_review_path': str(frozen_path.relative_to(ROOT)), 'frozen_review_sha256': frozen_sha,
       'frozen_review_unchanged': True, 'paid_model_requests': 0, 'network_requests': 0,
       'amendments': [spg, wevis],
       'effective_counts_after_amendment': {'include': 11, 'reject': 35, 'defer': 5},
       'effective_groups_after_amendment': {'new_non_hf_intake': {'include': 9, 'reject': 32, 'defer': 3},
                                          'existing_open_issue': {'include': 2, 'reject': 3, 'defer': 2}},
       'boundary': 'Append-only advisory corrections; no canonical/formal-review/git/publication mutation.'}
out = OUT / 'amendment-spg-wevis.json'
out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
(OUT / 'amendment-spg-wevis.md').write_text('''# 独立第三轮补充纠正：SPG-Select 与 WeVisForensics

原冻结 `review-findings.json` 保持不变。本补充优先于其中这两个条目的相关字段。

- **SPG-Select（2611.18818）：reject → defer。** 固定 schema、管理器或自然语言形式不足以排除 Harness。正文确有失败驱动的技能/insight 更新及冻结后跨任务使用正证据。需要补报告实验实际采用的技能原文、反馈与写入/修改及后续调用链，辨别它是操作规则还是普通经验条目。
- `Verify Object Location First` 是生成提示内的 JSON 格式例；明确被称为与报告实验分离的 illustrative output 是 `Require Observable State Change`。两者都不能冒充已部署的实验修改。
- **WeVisForensics（2611.21373）：仍纳入 harness/coevolution，修正摘要。** 固定的是 PaddleOCR detector 与音频工具；视觉 OCR consistency inspector 参与 LoRA 和 skill-card 训练。新中英摘要在 JSON 中，数字守卫通过。
- 生效总数变为 **11 纳入建议、35 排除、5 待补**；其中新增非 HF 是 9/32/3，历史 issue 仍 2/3/2。

本次只复用已保存正文，网络与付费请求均为零。原冻结摘要不被覆盖，变更及原文引句以本补充逐项回溯。
''')
assert sha(frozen_path.read_bytes()) == frozen_sha
receipt = {'checked_at': now, 'frozen_review_sha256_unchanged': frozen_sha,
           'amendment_sha256': sha(out.read_bytes()), 'exact_quotes_verified': 7,
           'source_body_and_text_hashes_verified': True, 'corrected_summary_number_guard': guard,
           'network_requests': 0, 'paid_requests': 0, 'canonical_writes': 0, 'formal_review_writes': 0}
(OUT / 'amendment-validation.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
files = [OUT / name for name in ['amendment-spg-wevis.py', 'amendment-spg-wevis.json', 'amendment-spg-wevis.md', 'amendment-validation.json']]
manifest = {'generated_at': now,
            'base_manifest_sha256': sha((OUT / 'file-manifest.json').read_bytes()),
            'base_manifest_unchanged': True,
            'files': [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                       'sha256': sha(p.read_bytes())} for p in files]}
(OUT / 'amendment-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
