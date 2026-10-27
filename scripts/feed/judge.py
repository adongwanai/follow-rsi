"""Abstract-only classification and guarded bilingual summaries."""
from copy import deepcopy
import json
from pathlib import Path

from scripts.common import ROOT, read_yaml
from scripts.feed.guard import (EVIDENCE_NOTICE, check_summary, enforce_evidence,
                                unknown_evidence)
from scripts.feed.llm import LLMError


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


def judge_item(item, client, root=ROOT):
    result = deepcopy(item)
    if result.get('in_repo') or result.get('kind', 'paper') != 'paper':
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
        result.update(response['data'])
        result['llm'].update(response['data'])
        if result['label'] == 'exclude':
            return result
        stage = 'classify'
        response = client.run(stage, result, variables={'taxonomy_definitions': taxonomy_definitions(root)})
        result['llm'][stage] = _provenance(response)
        classification = response['data']
        confidence = min(result['confidence'], classification['confidence'])
        result.update(classification)
        result['confidence'] = confidence
        result['llm'].update(classification)
        result['llm']['confidence'] = confidence
        if result['label'] == 'include':
            stage = 'evidence'
            response = client.run(stage, result, variables={'comments': result.get('comments', '')})
            result['llm'][stage] = _provenance(response)
            result['evidence_quick'] = enforce_evidence(result['abstract'], response['data'])
        return result
    except LLMError as error:
        return _error(result, stage, error)


def summarize_item(item, client, root=ROOT):
    result = deepcopy(item)
    if result.get('in_repo') or result.get('label') not in ('include', 'borderline'):
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
