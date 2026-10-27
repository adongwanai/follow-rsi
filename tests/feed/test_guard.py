import pytest

from scripts.feed.guard import check_intro, check_summary, enforce_evidence, numbers, unknown_evidence


@pytest.mark.parametrize(('text', 'expected'), [
    ('Improved by +12.5% with -3.8 points', ['+12.5%', '-3.8']),
    ('全角＋１２．５％，−３．８；１，２３４，５６７', ['+12.5%', '-3.8', '1234567']),
    ('4–30 steps; 4-30 trials; 2.42M samples; 3.8x / 1.84× speed',
     ['4', '30', '4', '30', '2.42', '3.8', '1.84']),
    ('wins 4/26 and 12.5% versus 12.50%', ['4/26', '12.5%', '12.50%']),
    ('1,000.25 or 1,200 vs 4,30', ['1000.25', '1200', '4', '30']),
])
def test_literal_numeric_forms(text, expected):
    assert numbers(text) == expected


def test_summary_subset_and_translation_multiset():
    assert check_summary('4 benchmarks', '+12.5% with 2.42M samples',
                         '在4个基准上提升+12.5%，使用2.42M样本',
                         'Improves +12.5% across 4 benchmarks using 2.42M samples')['ok']
    changed = check_summary('', 'score 12.5%', '达到12.6%', 'Reaches 12.6%')
    assert changed['invalid_zh'] == ['12.6%']
    assert not changed['ok']
    missing = check_summary('4 tasks', '', '4个任务，每组4个', '4 tasks')
    assert missing['translation_mismatch']['missing'] == ['4']
    assert not missing['ok']
    assert not check_summary('score 12.5%', '', '得分12.5', 'Score 12.5')['ok']
    assert not check_summary('change -3.8', '', '变化+3.8', 'Change +3.8')['ok']


def test_intro_numbers_come_only_from_counts():
    assert check_intro('本周共4篇，Harness有3篇。',
                       '4 papers this week, 3 in Harness.', {'total': 4, 'harness': 3})['ok']
    assert not check_intro('共有5篇。', '5 papers.', {'total': 4})['ok']


def test_evidence_requires_literal_abstract_quote_and_length():
    evidence = unknown_evidence()
    evidence['held_out'] = {'value': 'yes', 'quote': 'held-out\n benchmarks'}
    evidence['matched_budget'] = {'value': 'yes', 'quote': 'same budget baseline'}
    evidence['cross_model'] = {'value': 'yes', 'quote': 'other models'}
    evidence['code_released'] = {'value': 'yes', 'quote': 'https://github.com/example/project'}
    checked = enforce_evidence('We evaluate held-out benchmarks and transfer to other models.', evidence)
    assert checked['held_out']['value'] == checked['cross_model']['value'] == 'yes'
    assert checked['matched_budget'] == checked['code_released'] == {'value': 'unknown', 'quote': None}
    evidence['held_out']['quote'] = 'We'
    evidence['cross_model']['quote'] = ' ' * 10
    assert all(entry['value'] == 'unknown' for entry in enforce_evidence('We', evidence).values())
