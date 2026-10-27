"""Validate the single source of truth and reading-route references."""
import argparse
from collections import Counter
from pathlib import Path
import json
import sys

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jsonschema import Draft202012Validator, FormatChecker

from scripts.common import ROOT, number_tokens, read_yaml


def validate(root=ROOT):
    data = read_yaml(root / 'data/papers.yaml')
    schema = json.loads((root / 'data/schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)
    papers = data['papers']
    for key in ('id', 'arxiv'):
        duplicates = [value for value, count in Counter(p[key] for p in papers if key in p).items() if count > 1]
        if duplicates:
            raise ValueError(f'Duplicate {key}: {duplicates}')
    sections = data['meta']['sections']
    ids = {p['id'] for p in papers}
    for p in papers:
        if p['section'] not in sections:
            raise ValueError(f"{p['id']}: unknown section {p['section']}")
        if (p['section'] == 'candidates') != (p.get('status') == 'candidate'):
            raise ValueError(f"{p['id']}: candidate section/status must agree")
        for field in ('summary', 'result'):
            if field + '_en' in p:
                if field + '_zh' not in p or 'en_machine_translated' not in p:
                    raise ValueError(f"{p['id']}: English translation requires Chinese source and translation flag")
                if Counter(number_tokens(p[field + '_zh'])) != Counter(number_tokens(p[field + '_en'])):
                    raise ValueError(f"{p['id']}: {field} translation changes numeric tokens")
    routes = read_yaml(root / 'data/routes.yaml')['routes']
    for route in routes:
        unknown = set(route['papers']) - ids
        if unknown:
            raise ValueError(f"{route['name_en']}: missing paper IDs {sorted(unknown)}")
    return data, routes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    data, routes = validate(args.root)
    print(f"Validated {len(data['papers'])} papers and {len(routes)} routes.")
