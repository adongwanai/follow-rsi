"""Deterministic checks on generated numbers and abstract-only quick evidence."""
from collections import Counter
import json
import re
import unicodedata

EVIDENCE_FIELDS = ('held_out', 'matched_budget', 'cross_model', 'code_released')
EVIDENCE_NOTICE = {'zh': '自动判断，未核实', 'en': 'Automatic, unverified'}
_NUMBER = re.compile(r'[-+]?\d+/\d+|[-+]?\d+(?:\.\d+)?%?')
_THOUSANDS = re.compile(r'(?<!\d)[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?')


def numbers(text):
    """Return literal numeric tokens; magnitude/multiplier suffixes are not tokens.

    Normalize full-width characters, thousands separators and Unicode minus.
    Dashes between two numbers denote a range, rather than a negative endpoint.
    Fractions remain a single token and percentages retain their percent sign.
    """
    normalized = unicodedata.normalize('NFKC', str(text)).replace('−', '-')
    normalized = _THOUSANDS.sub(lambda match: match.group().replace(',', ''), normalized)
    normalized = re.sub(r'(?<=\d)\s*[-–—]\s*(?=\d)', ' ', normalized)
    return _NUMBER.findall(normalized)


def check_summary(title, abstract, summary_zh, summary_en=None):
    allowed = set(numbers(title + ' ' + abstract))
    zh = Counter(numbers(summary_zh))
    invalid = sorted(set(zh) - allowed)
    mismatch = {}
    if summary_en is not None:
        en = Counter(numbers(summary_en))
        if en != zh:
            mismatch = {'missing': list((zh - en).elements()),
                        'extra': list((en - zh).elements())}
    return {'ok': not invalid and not mismatch, 'invalid_zh': invalid,
            'translation_mismatch': mismatch}


def check_intro(intro_zh, intro_en, counts):
    """Direction counts are the only source of automatically generated numbers."""
    source = counts if isinstance(counts, str) else json.dumps(counts, ensure_ascii=False)
    checked = check_summary('', source, intro_zh, intro_en)
    checked['invalid_en'] = sorted(set(numbers(intro_en)) - set(numbers(source)))
    checked['ok'] = checked['ok'] and not checked['invalid_en']
    return checked


def normalized_whitespace(text):
    return ' '.join(text.split())


def enforce_evidence(abstract, evidence, code_evidence=None):
    """A yes needs 5–60 characters quoted from the abstract, never just comments."""
    normalized_abstract = normalized_whitespace(abstract)
    result = {}
    for field in EVIDENCE_FIELDS:
        if field == 'code_released':
            result[field] = code_evidence or {'value': 'unknown', 'quote': None}
            continue
        entry = evidence[field]
        quote = entry['quote']
        supported = (entry['value'] == 'yes' and isinstance(quote, str)
                     and 5 <= len(quote) <= 60
                     and normalized_whitespace(quote) in normalized_abstract
                     and bool(normalized_whitespace(quote)))
        result[field] = {'value': 'yes', 'quote': quote} if supported else {
            'value': 'unknown', 'quote': None}
    return result


def unknown_evidence():
    return {field: {'value': 'unknown', 'quote': None} for field in EVIDENCE_FIELDS}
