"""Shared data loading and evidence definitions. No network access."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    'held_out': ('留出集', 'Held-out evaluation'),
    'matched_budget_baseline': ('同预算对照', 'Matched-budget baseline'),
    'cross_model_transfer': ('跨模型迁移', 'Cross-model transfer'),
    'cost_reported': ('报告成本', 'Cost reported'),
    'disjoint_evolution_set': ('不相交演化集', 'Disjoint evolution set'),
    'reliability_metric': ('可靠性指标', 'Reliability metric'),
    'code_released': ('开源代码', 'Code released'),
    'evolved_harness_released': ('公开演化出的 Harness', 'Evolved harness released'),
}
CLASSES = {
    'who_edits': ['self', 'external', 'trained', 'self_human_reviewed', 'unknown'],
    'feedback': ['ground_truth', 'proxy', 'self_generated_tests', 'demonstrations', 'self_judgment', 'unknown'],
    'timing': ['offline', 'online', 'test_time', 'during_run', 'unknown'],
    'topology': ['chain', 'tree', 'graph', 'unknown'],
}
FIELDS = [*CHECKS, *CLASSES]
KEYS = list(CHECKS)[:4]
ICONS = {'yes': '✅', 'partial': '◐', 'no': '❌', 'unknown': '❔', 'na': '—'}
SYMBOLS = {'yes': '✓', 'partial': '◐', 'no': '✕', 'unknown': '?', 'na': '–'}
# Preserve signs, decimal spelling, percentages, ranges, and literal units.
NUMBERS = re.compile(r'[+−–-]?\d+(?:\.\d+)*(?:[%％]|pp|[KMB](?![a-z])|×)?')


class DataLoader(yaml.SafeLoader):
    """Keep dates and yes/no as strings; true/false remain booleans."""


DataLoader.yaml_implicit_resolvers = {
    key: [(tag, pattern) for tag, pattern in values
          if tag not in ('tag:yaml.org,2002:bool', 'tag:yaml.org,2002:timestamp')]
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
DataLoader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false)$', re.I), list('tTfF'))


def read_yaml(path):
    return yaml.load(Path(path).read_text(encoding='utf-8'), Loader=DataLoader)


def evidence(paper):
    return {key: paper.get('evidence', {}).get(key, 'unknown') for key in FIELDS}


def paper_url(paper):
    return 'https://arxiv.org/abs/' + paper['arxiv'] if 'arxiv' in paper else paper['url']


def number_tokens(value):
    return NUMBERS.findall(value)
