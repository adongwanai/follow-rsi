"""Run the current 45-case gate in an isolated, recorded input snapshot."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
from threading import Lock

OUTPUT = Path(__file__).resolve().parent
RUN_ROOT = OUTPUT / 'run-root'
SOURCE_ROOT = OUTPUT.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RUN_ROOT))

from scripts.feed.cli import configure
from scripts.feed import eval as evaluator

manifest = json.loads((OUTPUT / 'input-manifest.json').read_text())
for relative, digest in manifest['sha256'].items():
    assert hashlib.sha256((RUN_ROOT / relative).read_bytes()).hexdigest() == digest, relative
assert Path(evaluator.__file__).resolve().is_relative_to(RUN_ROOT)
configure(RUN_ROOT, SOURCE_ROOT / '.env.local')

results_dir = OUTPUT / 'case-results'
results_dir.mkdir(exist_ok=True)
original_judge = evaluator.judge_item
lock = Lock()
completed = 0


def recorded_judge(item, client, root, **kwargs):
    global completed
    result = original_judge(item, client, root, **kwargs)
    (results_dir / (item['arxiv_id'] + '.json')).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with lock:
        completed += 1
        print(json.dumps({'completed': completed, 'total': 45, 'arxiv': item['arxiv_id'],
                          'label': result.get('label'), 'primary': result.get('primary'),
                          'gate': result.get('gate', {}).get('verdict'),
                          'error': result.get('llm', {}).get('error'),
                          'at': datetime.now(timezone.utc).isoformat()}, ensure_ascii=False), flush=True)
    return result


evaluator.judge_item = recorded_judge
print('Starting isolated 45-case gate evaluation; no credential values are logged.', flush=True)
report = evaluator.run_evaluation(RUN_ROOT, workers=2,
                                  label_file='harness-gate-cases.yaml', report_prefix='gate-report')
for extension in ('json', 'md'):
    shutil.copyfile(RUN_ROOT / 'feed/eval' / ('gate-report.' + extension),
                    OUTPUT / ('gate-report.' + extension))
print(evaluator.report_markdown(report), flush=True)
if report['status'] != 'complete' or not report['thresholds_passed']:
    raise SystemExit(1)
