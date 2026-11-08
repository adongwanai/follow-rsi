"""Independently account for the frozen gate run; never call a model or relabel."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def normalize(text):
    return ' '.join(text.split())


def score(cases):
    counts = Counter()
    for case in cases:
        target = case['expected']['verdict'] == 'harness'
        output = case['predicted']
        admitted = output.get('label') == 'include' and output.get('gate', {}).get('verdict') == 'harness'
        counts['tp' if target and admitted else 'fn' if target else 'fp' if admitted else 'tn'] += 1
    tp, fp, fn, tn = (counts[k] for k in ('tp', 'fp', 'fn', 'tn'))
    return {'evaluated': len(cases), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
            'precision': tp / (tp + fp) if tp + fp else None,
            'recall': tp / (tp + fn) if tp + fn else None}


report = load(BASE / 'gate-report.json')
manifest = load(BASE / 'input-manifest.json')
hash_checks = {path: sha(BASE / 'run-root' / path) == expected
               for path, expected in manifest['sha256'].items()}
assert len(hash_checks) == 60 and all(hash_checks.values())
labels = yaml.safe_load((BASE / 'run-root/feed/eval/harness-gate-cases.yaml').read_text())
assert len(labels) == 45 and len({item['arxiv'] for item in labels}) == 45
cases = report['cases']
assert [case['expected'] for case in cases] == labels
assert report['status'] == 'complete' and report['evaluated'] == report['total'] == 45
assert not any(report[key] for key in ('missing_metadata', 'invalid_metadata', 'conflicting_labels'))
raw = {}
for case in cases:
    item = load(BASE / 'case-results' / (case['arxiv'] + '.json'))
    assert not item['llm'].get('error')
    assert all(item[key] == value for key, value in case['predicted'].items())
    assert item['llm'] == case['provenance']
    raw[case['arxiv']] = item

subsets = {
    'full_45': cases,
    'owner_25': [case for case in cases if case['expected']['labeled_by'] == 'owner'],
    'library_20': [case for case in cases if case['expected']['labeled_by'] != 'owner'],
    'without_prompt_examples_35': [case for case in cases if not case['expected']['in_prompt_example']],
    'owner_without_prompt_examples_15': [case for case in cases if case['expected']['labeled_by'] == 'owner'
                                        and not case['expected']['in_prompt_example']],
    'prompt_examples_10': [case for case in cases if case['expected']['in_prompt_example']],
}
scores = {name: score(rows) for name, rows in subsets.items()}
for independent, official in (('full_45', 'harness'), ('owner_25', 'harness_owner_review'),
                             ('without_prompt_examples_35', 'harness_without_prompt_examples')):
    assert all(scores[independent][key] == report['metrics'][official][key]
               for key in ('precision', 'recall', 'evaluated'))

notes = {
    '2610.22732': 'TokenEconomizer：原 owner 为 Harness；相关性模型 include，但 gate 认为摘要未充分明确反馈驱动修改，降为 borderline。固定标签记 FN，不据此改写 owner 判断。',
    '2610.21453': 'CarryOn：原 owner 为 borderline；模型把“when refined skills are reused”解读为跨任务持久性而准入。逐字引用存在，但不能单靠逐字匹配消除语义边界。固定标签记 FP。',
    '2610.34238': 'Δτ-Bench：原 owner 为其他方向 evaluation_benchmark；gate 通过 Harness 专项评测支路准入。原摘要提到技能维护，模型将此扩大为 Harness 演化专项证据。固定标签记 FP，保留 owner 标签。',
    '2604.20938': 'HARBOR：预选 library 正例；相关性阶段缺少持久性引句，保持 borderline，即使后续 gate 样本原始输出 harness。原有 owner scope 歧义仍存在，保留预选标签计 FN。',
    '2609.18366': 'Bad Genius：原 gate 样本为 harness，但反馈引句把源文公式 $B_{\\mathrm{rel}}$ 改为 B_rel，逐字 guard 无法匹配，最终反馈字段 unclear、gate borderline。记 FN；不削弱 guard 或重跑改善分数。',
    '2609.09134': 'Co-Evolving Harnesses and Models：预选 library 协同演化正例；相关性 include，gate 认为摘要未明确 Harness 的反馈修改而给 borderline。协同演化例外未稳定被识别；不是仅因 model_frozen=no 自动排除。固定标签记 FN。',
}
mistakes = []
for case in report['metrics']['harness_mistakes']:
    ident = case['arxiv']
    item = raw[ident]
    mistakes.append({'arxiv': ident, 'title': item['title'],
                     'type': 'FN' if case['expected']['verdict'] == 'harness' else 'FP',
                     'expected': case['expected'], 'predicted': case['predicted'],
                     'raw_gate_samples': [sample['data'] for sample in item['llm'].get('harness_gate', {}).get('samples', [])],
                     'finding_zh': notes[ident]})
assert len(mistakes) == 6 and set(notes) == {row['arxiv'] for row in mistakes}

quote_issues = []
sample_counts = Counter()
for ident, item in raw.items():
    gate = item['llm'].get('harness_gate', {})
    if gate:
        sample_counts[gate['sample_count']] += 1
    for index, sample in enumerate(gate.get('samples', [])):
        data = sample['data']
        for field in ('feedback_driven', 'persists_across_tasks'):
            quote = data[field]['quote']
            if quote and normalize(quote) not in normalize(item['abstract']):
                quote_issues.append({'arxiv': ident, 'sample': index, 'field': field,
                                     'quote': quote, 'exact_whitespace_normalized_match': False})

result = {
    'created_at': datetime.now(timezone.utc).isoformat(),
    'reviewer': '/root/today_pipeline_audit',
    'run_status': 'complete', 'quality_status': 'failed_recall_threshold',
    'exit_code': 1, 'exit_reason': 'completed evaluation; recall below unchanged 0.90 threshold',
    'input_files_verified_unchanged': 60, 'fixed_labels_unchanged': True,
    'fixed_cases': 45, 'case_result_provenance_matches_official_report': True,
    'metadata_errors': 0, 'api_schema_errors': 0,
    'stage_models': report['stage_models'], 'gate_sample_counts': dict(sample_counts),
    'subsets': scores, 'thresholds': report['thresholds'],
    'metrics_independently_recomputed_match': True,
    'prompt_example_overlap': 10, 'blind_holdout_claimed': False,
    'labels_changed_after_observing_results': False, 'reruns_to_improve_score': 0,
    'raw_gate_quote_mismatches': quote_issues,
    'mistakes': mistakes,
    'files': {name: sha(BASE / name) for name in ('input-manifest.json', 'gate-report.json', 'gate-report.md', 'run.log')},
    'canonical_writes': False, 'publication_authorized': False,
}
(BASE / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')

text = [
    '# 2026-10-30 Harness gate 固定样本复核', '',
    '45/45 评估完整；0 metadata、身份、API 或 schema 错误。质量门槛未通过：召回率 24/28 = 85.71%，低于 90%。退出码 1 表示质量失败，不是运行中断。', '',
    '| 子集 | 样本 | TP | FP | FN | TN | Precision | Recall |',
    '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |',
]
for name, values in scores.items():
    text.append('| ' + ' | '.join([name] + [str(values[key]) for key in ('evaluated', 'tp', 'fp', 'fn', 'tn')]
                                 + [f"{values[key]:.4f}" if values[key] is not None else '—' for key in ('precision', 'recall')]) + ' |')
text += ['', '全体 precision 虽超过 0.85，owner 子集 precision 仅 0.7778、recall 仅 0.8750。20 个预选 library 样本全为正例，不能用其精确率证明负例排除能力，也不能让它们掩盖 owner 子集问题。', '',
         '10 个案例已经出现在 gate prompt 中，因此不是盲测。去掉它们后仍只是排除已知 prompt 校准案例的子集，不声称严格独立留出集。library 标签是预选评估目标，未替代全文审查；HARBOR 的已知 scope 歧义继续保留。', '',
         'relevance/classify 使用 deepseek-flash；gate 使用 deepseek-v4-pro，每项 1 个 gate 样本。此评估不等同三轮来源复核。60 个输入和代码文件的 SHA-256 在结束后全部一致；45 个固定标签未变，报告逐项输出与独立保存的 case-results 一致，指标另行复算一致。', '',
         '六个固定标签误判：', '']
text += ['- ' + row['finding_zh'] for row in mistakes]
text += ['', '这次只跑当前 45-case gate；未运行旧 105/107 evaluator，未修改 labels、prompts、canonical 数据或发布文件，也未为提升分数重复调用模型。逐字引用匹配只能核验文本存在，不能证明语义充分。', '',
         '详细证据见 `gate-report.json`、`verification.json` 和 `input-manifest.json`。所有结论为审核建议，不是 owner accept 或发布授权。', '']
(BASE / 'review.md').write_text('\n'.join(text))
print(json.dumps({'quality_status': result['quality_status'], 'subsets': scores,
                  'mistake_ids': [row['arxiv'] for row in mistakes],
                  'raw_gate_quote_mismatches': quote_issues}, ensure_ascii=False, indent=2))
