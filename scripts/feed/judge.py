"""Abstract-only classification and guarded bilingual summaries."""
from copy import deepcopy
import json
from pathlib import Path

from scripts.common import ROOT, read_yaml
from scripts.feed.guard import (EVIDENCE_NOTICE, check_summary, enforce_evidence,
                                normalized_whitespace, unknown_evidence)
from scripts.feed.llm import LLMError, stage_settings

HARNESS_OBJECTS = {'system_prompt', 'tool_code', 'skill_files', 'context_memory_policy',
                   'control_flow', 'in_loop_verifier', 'improver'}
OTHER_OBJECTS = {'model_weights': 'model_weights', 'training_env_reward': 'data_task',
                 'external_artifact': 'ai4ai', 'memory_entries': 'experience_world_model'}


def taxonomy_definitions(root=ROOT):
    return json.dumps(read_yaml(Path(root) / 'feed/taxonomy.yaml'), ensure_ascii=False, indent=2)


def _error(result, stage, error):
    result['label'] = 'error'
    result['review_required'] = True
    result['llm']['label'] = 'error'
    result['llm']['error'] = {'stage': stage, 'message': str(error)}
    return result


def _provenance(response):
    # Cache-hit status is per invocation, not a change to the paper's judgment.
    return {key: value for key, value in response.items() if key != 'cached'}


def guard_scope(abstract, relevance, classification=None):
    """Require source quotes for a decision; missing evidence stays unknown.

    Matching confirms provenance, not the semantic truth of the model's reading.
    Raw responses remain in llm provenance for the owner's review.
    """
    source = normalized_whitespace(abstract)

    def supported(quote):
        return (quote is not None and bool(normalized_whitespace(quote))
                and normalized_whitespace(quote) in source)

    support = {field: quote if supported(quote) else None
               for field, quote in relevance['scope_support'].items()}
    kind = relevance['scope_kind']
    issues = []
    if relevance['label'] == 'exclude':
        required = ('exclusion_quote',)
    elif kind == 'method':
        required = ('object_quote', 'feedback_quote', 'persistence_quote')
    elif kind in ('evaluation', 'theory'):
        required = ('study_quote',)
    else:
        required = ()
        issues.append('scope_kind')
    issues.extend('scope_support.' + field for field in required if support[field] is None)

    result = {'scope_support': support}
    if classification is not None:
        primary = classification['primary']
        study_kinds = {'evaluation_benchmark': 'evaluation', 'theory_survey': 'theory'}
        if ((primary in study_kinds and kind != study_kinds[primary])
                or (kind in study_kinds.values() and study_kinds.get(primary) != kind)):
            issues.append('scope_kind_classification')

    result['label'] = 'borderline' if issues else relevance['label']
    result['exclude_reason'] = relevance['exclude_reason'] if result['label'] == 'exclude' else None
    result['scope_guard'] = {'supported': not issues, 'issues': issues,
                             'model_label': relevance['label']}
    return result


def guard_harness(abstract, gate):
    result = deepcopy(gate)
    source = normalized_whitespace(abstract)
    study = result.get('study_quote')
    study_supported = (isinstance(study, str) and bool(normalized_whitespace(study))
                       and normalized_whitespace(study) in source)
    if 'study_quote' in result and not study_supported:
        result['study_quote'] = None
    for field in ('feedback_driven', 'persists_across_tasks'):
        quote = result[field]['quote']
        if quote is None or not normalized_whitespace(quote) or normalized_whitespace(quote) not in source:
            result[field] = {'value': 'unclear', 'quote': None}
    obj = result['improved_object']
    if obj in OTHER_OBJECTS and result['verdict'] != 'exclude':
        primary = result['suggested_primary']
        if primary not in ('evaluation_benchmark', 'theory_survey'):
            primary = OTHER_OBJECTS[obj]
        result.update(verdict='other_direction', suggested_primary=primary, harness_specific='no')
    elif result['verdict'] == 'harness':
        if result['suggested_primary'] in ('evaluation_benchmark', 'theory_survey'):
            if not study_supported or result['harness_specific'] != 'yes':
                result['verdict'] = 'borderline'
        elif (obj not in HARNESS_OBJECTS or result['feedback_driven']['value'] != 'yes'
                or result['persists_across_tasks']['value'] != 'yes' or result['harness_specific'] != 'yes'):
            result['verdict'] = 'borderline'
    return result


def run_harness_gate(item, client, root=ROOT):
    settings = stage_settings('harness_gate', root, getattr(client, 'model', None))
    samples, provenance = [], []
    for index in range(settings['samples']):
        response = client.run('harness_gate', item,
                              variables={'taxonomy_definitions': taxonomy_definitions(root)},
                              retry_token=f'independent-sample-{index + 1}')
        provenance.append(_provenance(response))
        samples.append(guard_harness(item['abstract'], response['data']))
    gate = samples[0]
    signatures = {(sample['verdict'], sample['improved_object'], sample['suggested_primary'],
                   sample['harness_specific'], sample['feedback_driven']['value'],
                   sample['persists_across_tasks']['value']) for sample in samples}
    agreed = len(signatures) == 1
    if not agreed:
        gate = {**gate, 'verdict': 'borderline', 'why_zh': '独立闸门判断不一致，需人工复核'}
    return gate, {'samples': provenance, 'sample_count': len(samples), 'agreement': agreed}


def apply_gate(result, gate):
    """The verified gate, never a classifier label alone, admits Harness papers."""
    result['gate'] = gate
    if gate['verdict'] == 'borderline':
        result['label'] = 'borderline'
        result['exclude_reason'] = None
    elif gate['verdict'] == 'exclude':
        result['label'] = 'exclude'
    elif gate['verdict'] == 'other_direction':
        study = {'evaluation_benchmark': 'evaluation', 'theory_survey': 'theory'}
        if (result['primary'] in study and result.get('scope_kind') == study[result['primary']]):
            result['gate'] = {**gate, 'suggested_primary': result['primary']}
        else:
            result['primary'] = gate['suggested_primary']
        result['harness_sub'] = None
        result['secondary'] = [value for value in result['secondary']
                               if value not in ('harness', result['primary'])]
    elif (gate['verdict'] == 'harness' and result['primary'] not in
          ('harness', 'evaluation_benchmark', 'theory_survey')):
        result['gate'] = {**gate, 'verdict': 'borderline', 'why_zh': '主方向与闸门不一致，需人工确定分类'}
        result['label'] = 'borderline'
    result['improved_object_zh'] = gate['improved_object_zh']
    return result


def judge_item(item, client, root=ROOT, *, include_evidence=True):
    result = deepcopy(item)
    if result.get('in_repo'):
        from scripts.feed.library import curated_item
        return curated_item(result, root)
    if result.get('kind', 'paper') != 'paper':
        return result
    result['llm'] = {}
    result['evidence_quick'] = unknown_evidence()
    result['evidence_notice'] = EVIDENCE_NOTICE.copy()
    result['review_required'] = True
    if result.get('metadata_pending') or not result.get('abstract', '').strip():
        return _error(result, 'metadata', LLMError('Original paper abstract is unavailable; metadata hydration is required'))
    stage = 'relevance'
    try:
        response = client.run(stage, result)
        result['llm'][stage] = _provenance(response)
        relevance = response['data']
        result.update(relevance)
        guarded = guard_scope(result['abstract'], relevance)
        result.update(guarded)
        result['llm'].update({**relevance, **guarded})
        if result['label'] == 'exclude':
            return result
        stage = 'classify'
        response = client.run(stage, result, variables={'taxonomy_definitions': taxonomy_definitions(root)})
        result['llm'][stage] = _provenance(response)
        classification = response['data']
        confidence = min(result['confidence'], classification['confidence'])
        result.update(classification)
        guarded = guard_scope(result['abstract'], relevance, classification)
        result.update(guarded)
        result['confidence'] = confidence
        result['llm'].update({**classification, **guarded})
        result['llm']['confidence'] = confidence
        if (result['primary'] in ('harness', 'evaluation_benchmark', 'theory_survey')
                or 'harness' in result['secondary']):
            stage = 'harness_gate'
            gate, provenance = run_harness_gate(result, client, root)
            result['llm'][stage] = provenance
            if result['label'] == 'borderline' and gate['verdict'] == 'harness':
                gate = {**gate, 'verdict': 'borderline', 'why_zh': '相关性依据仍不足，保留待审'}
            apply_gate(result, gate)
            result['llm'].update({key: result[key] for key in
                                  ('label', 'primary', 'harness_sub', 'secondary', 'improved_object_zh')})
        if result['label'] == 'include' and include_evidence:
            stage = 'evidence'
            response = client.run(stage, result, variables={'comments': result.get('comments', '')})
            result['llm'][stage] = _provenance(response)
            from scripts.feed.fetch_github import verify_code_links
            code = verify_code_links(result.get('code_links', []))
            result['code_link_checks'] = code['checks']
            result['evidence_quick'] = enforce_evidence(result['abstract'], response['data'], code['evidence'])
        return result
    except LLMError as error:
        return _error(result, stage, error)


def summarize_item(item, client, root=ROOT):
    result = deepcopy(item)
    if result.get('in_repo'):
        from scripts.feed.library import curated_item
        return curated_item(result, root)
    if result.get('label') not in ('include', 'borderline'):
        return result
    result.setdefault('llm', {})
    result['summary_zh'] = ''
    result['summary_en'] = ''
    result['guard_failed'] = False
    result['initial_guard_failed'] = False
    if result.get('metadata_pending') or not result.get('abstract', '').strip():
        return _error(result, 'metadata', LLMError('Original paper abstract is unavailable; metadata hydration is required'))
    feedback = None
    stage = 'summarize'
    for attempt in range(2):
        try:
            stage = 'summarize'
            response = client.run(stage, result, feedback=feedback)
            result['llm'][stage] = _provenance(response)
            zh = response['data']['summary_zh']
            checked = check_summary(result['title'], result['abstract'], zh)
            if checked['ok']:
                stage = 'translate'
                response = client.run(stage, result, variables={'summary_zh': zh}, feedback=feedback)
                result['llm'][stage] = _provenance(response)
                en = response['data']['summary_en']
                checked = check_summary(result['title'], result['abstract'], zh, en)
                if checked['ok']:
                    result['summary_zh'], result['summary_en'] = zh, en
                    result['llm']['number_guard'] = {'ok': True, 'attempts': attempt + 1}
                    return result
        except LLMError as error:
            return _error(result, stage, error)
        result['initial_guard_failed'] = True
        feedback = ('以下数字不在原文中：' + ', '.join(checked['invalid_zh'])
                    + '；英文数字必须与中文作为多重集合完全相同：'
                    + json.dumps(checked['translation_mismatch'], ensure_ascii=False))
        result['llm']['number_guard'] = {**checked, 'attempts': attempt + 1}
    result['guard_failed'] = True
    result['review_required'] = True
    # Neither language can retain a failed generation.
    result['summary_zh'] = result['summary_en'] = ''
    return result
