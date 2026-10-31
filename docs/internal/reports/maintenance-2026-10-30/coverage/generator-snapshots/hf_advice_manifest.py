"""Adapt the completed HF 16 source reports; never read or write canonical data."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from coverage_ledger import input_fingerprint

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def check_file(path, expected):
    actual = sha(ROOT / path)
    if actual != expected:
        raise ValueError(f'Source hash mismatch: {path}')


def quoted(quote, source):
    if ' '.join(quote.split()) not in ' '.join(source.split()):
        raise ValueError(f'Quote does not match recorded source: {quote}')


primary_path = BASE / 'hf-today-review/manifest.json'
third_path = BASE / 'independent-round3/hf-today-report.json'
primary, third = read(primary_path), read(third_path)
snapshot = {row['id']: row for row in read(BASE / 'hf-today-normalized.json')}
assert len(snapshot) == len(primary['items']) == len(third['items']) == 16
assert primary['review_rounds_completed'] == [1, 2] and third['round'] == 3
for record in primary['input_snapshots']:
    check_file(record['path'], record['sha256'])
for record in primary['source_hash_checks']:
    check_file(record['path'], record['sha256'])

namespaces = {'a': 'http://www.w3.org/2005/Atom'}
atom = ET.fromstring((BASE / 'hf-today-official.atom').read_bytes())
official_abstracts = {}
for entry in atom.findall('a:entry', namespaces):
    url = entry.findtext('a:id', namespaces=namespaces)
    arxiv = url.rsplit('/', 1)[-1].split('v')[0]
    official_abstracts['arxiv:' + arxiv] = entry.findtext('a:summary', namespaces=namespaces)

body_sources = {row['arxiv_id']: row for row in primary['full_text_sources']}
advice = []
primary_quotes = 0
third_quotes = 0
for row in primary['items']:
    ident = row['id']
    current_input = snapshot[ident]
    assert current_input['title'] == row['title']
    assert ' '.join(current_input['abstract'].split()) == ' '.join(official_abstracts[ident].split())
    assert row['owner_decision'] == 'defer' and not row['publication_authorized']
    for evidence in row['evidence']:
        check_file(evidence['source_file'], evidence['source_sha256'])
        evidence_path = ROOT / evidence['source_file']
        if evidence_path.suffix == '.json':
            paragraphs = {entry['id']: entry['text'] for entry in read(evidence_path)}
            source_text = paragraphs[evidence['paragraph_id']]
        else:
            source_text = evidence_path.read_text()
        quoted(evidence['quote'], source_text)
        primary_quotes += 1
    for number, phase in ((1, 'official_identity_dates_and_abstract_read'),
                          (2, 'source_scope_boundary_and_counterevidence_review')):
        record = {'id': ident, 'round': number, 'phase': phase,
                  'report_file': str(primary_path.relative_to(ROOT)),
                  'report_sha256': sha(primary_path), 'reviewer': primary['reviewer'],
                  'reviewer_type': 'codex_source_reader_not_owner',
                  'verdict': row['harness_scope_recommendation'],
                  'input_fingerprint_sha256': input_fingerprint(current_input),
                  'input_snapshot': 'build/backlog-all-2026-10-30/hf-today-normalized.json',
                  'review_level': row[f'round_{number}'], 'independence': primary['independence'],
                  'formal_decision': 'defer', 'publication_authorized': False}
        if number == 2 and row['arxiv_id'] in body_sources:
            source = body_sources[row['arxiv_id']]
            record.update(body_file=source['text_file'], body_sha256=source['text_sha256'])
        advice.append(record)

for row in third['items']:
    ident = row['id']
    assert row['formal_decision'] == 'defer'
    source = row['abstract_source']
    check_file(source['file'], source['sha256'])
    assert hashlib.sha256(' '.join(official_abstracts[ident].split()).encode()).hexdigest() == row['official_abstract_sha256']
    assert snapshot[ident]['title'] == row['title']
    assert ' '.join(snapshot[ident]['abstract'].split()) == ' '.join(official_abstracts[ident].split())
    quoted(row['abstract_quote'], official_abstracts[ident])
    third_quotes += 1
    record = {'id': ident, 'round': 3, 'phase': 'separate_agent_source_scope_review',
              'report_file': str(third_path.relative_to(ROOT)), 'report_sha256': sha(third_path),
              'reviewer': third['reviewer_agent'], 'reported_reviewer_role': row['reviewer'],
              'reviewer_type': 'codex_source_reader_not_owner',
              'verdict': row['harness_recommendation'],
              'input_fingerprint_sha256': input_fingerprint(snapshot[ident]),
              'input_snapshot': 'build/backlog-all-2026-10-30/hf-today-normalized.json',
              'abstract_hash_normalization': 'whitespace_only',
              'review_level': row['review_level'], 'independence': third['independence'],
              'formal_decision': 'defer', 'publication_authorized': False}
    if row.get('body_receipt'):
        receipt = read(ROOT / row['body_receipt'])
        check_file(receipt['text_file'], receipt['text_sha256'])
        check_file(receipt['excerpt_file'], receipt['excerpt_sha256'])
        for attempt in receipt['attempts']:
            if attempt.get('sha256'):
                check_file(attempt['raw_file'], attempt['sha256'])
        text = (ROOT / receipt['text_file']).read_text()
        for quote in row['body_quotes']:
            quoted(quote, text)
            third_quotes += 1
        record.update(body_file=receipt['text_file'], body_sha256=receipt['text_sha256'],
                      body_receipt=row['body_receipt'],
                      body_receipt_sha256=sha(ROOT / row['body_receipt']))
    advice.append(record)

assert len(advice) == 48
output = BASE / 'hf-today-advice-manifest.json'
output.write_text(json.dumps(advice, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'output': str(output.relative_to(ROOT)), 'records': len(advice),
                  'ids': len(snapshot), 'primary_phases': 2, 'primary_artifacts': 1,
                  'total_report_artifacts': 2,
                  'recorded_reviewers': sorted({row['reviewer'] for row in advice}),
                  'primary_quotes_verified': primary_quotes, 'third_quotes_verified': third_quotes,
                  'fully_blind': False, 'all_formal_decisions_defer': True}, ensure_ascii=False, indent=2))
