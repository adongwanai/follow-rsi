"""Use the curated library for existing papers without asking an LLM to relabel them."""
from copy import deepcopy
from pathlib import Path

from scripts.common import evidence, read_yaml


def curated_item(item, root):
    result = deepcopy(item)
    data = read_yaml(Path(root) / 'data/papers.yaml')
    paper = next(p for p in data['papers']
                 if p.get('arxiv') == item.get('arxiv_id') or p['id'] == item.get('repo_id'))
    section = paper['section']
    scope = paper.get('scope', 'core' if section in {
        'evolve_main', 'generalize', 'evidence_selection', 'improver', 'component', 'coevolution'} else 'background')
    primary = 'harness' if scope == 'core' else 'evaluation_benchmark' if section == 'evaluation' else 'theory_survey'
    included = scope in ('core', 'harness_eval') and paper.get('status') != 'candidate'
    sub = section if primary == 'harness' and section != 'candidates' else None
    result.update(in_repo=True, repo_id=paper['id'], label='include' if included else 'borderline',
                  primary=primary, harness_sub=sub, secondary=['harness'] if scope == 'harness_eval' else [],
                  summary_zh=paper.get('summary_zh', ''), summary_en=paper.get('summary_en', ''),
                  review_required=True, needs_review=paper.get('needs_review', False), guard_failed=False,
                  initial_guard_failed=False)
    result['llm'] = {'label': result['label'], 'primary': primary, 'harness_sub': sub,
                     'secondary': result['secondary'], 'confidence': 1, 'origin': 'evidence_library',
                     'reason_zh': '沿用人工证据库分类；待核条目仍需正文复核。'}
    fields = {'held_out': 'held_out', 'matched_budget': 'matched_budget_baseline',
              'cross_model': 'cross_model_transfer', 'code_released': 'code_released'}
    values = evidence(paper)
    result['evidence_quick'] = {
        key: {'value': 'yes' if values[source] == 'yes' else 'unknown',
              'quote': f'papers/{paper["id"]}.md' if values[source] == 'yes' else None}
        for key, source in fields.items()}
    targets = {'prompt': 'system_prompt', 'tools': 'tool_code', 'skills': 'skill_files',
               'memory': 'context_memory_policy', 'context': 'context_memory_policy',
               'control_flow': 'control_flow', 'workflow': 'control_flow', 'improver': 'improver',
               'verifier': 'in_loop_verifier'}
    target = next((targets[key] for key in paper.get('edit_targets', []) if key in targets), 'none')
    result['gate'] = {'verdict': 'harness' if included else 'other_direction',
                      'harness_specific': 'yes' if included else 'no',
                      'improved_object': target if primary == 'harness' else 'none',
                      'improved_object_zh': {'system_prompt': '系统提示', 'tool_code': '工具代码',
                          'skill_files': '技能文件', 'context_memory_policy': '上下文与记忆管理策略',
                          'control_flow': '控制流', 'improver': '改进器', 'in_loop_verifier': '环内验证器',
                          'none': '详见证据卡'}[target],
                      'model_frozen': 'unclear', 'origin': 'evidence_library',
                      'feedback_driven': {'value': 'unclear', 'quote': None},
                      'persists_across_tasks': {'value': 'unclear', 'quote': None},
                      'suggested_primary': primary, 'why_zh': result['llm']['reason_zh']}
    return result
