"""Re-run the frozen audit and verify stable analytical content on every platform.

CSV line-ending conventions vary between Windows and Linux; comparing parsed rows,
including column order, avoids misleading binary mismatches with identical analysis.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import csv
import json
from validate_audit import analyze

ROOT = Path(__file__).resolve().parent
BASE = ROOT/'generated'
FILENAMES = [
  'audit_summary.json', 'type_and_eligibility_audit.csv',
  'hash_lineage_audit.csv', 'status_filter_winners.csv',
  'deduplication_ablation.csv', 'matched_release_recomputed.csv',
  'software_configuration_stress.csv'
]

def content(path):
    if path.suffix == '.json':
        return json.loads(path.read_text(encoding='utf-8'))
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader=csv.reader(handle)
        return list(reader)

with TemporaryDirectory() as tmp:
    analyze(ROOT,tmp)
    for name in FILENAMES:
        expected=content(BASE/name)
        actual=content(Path(tmp)/name)
        if expected != actual:
            raise SystemExit('MISMATCH in reproduced analysis: ' + name)
print(f'PASS: all {len(FILENAMES)} analytical outputs match by exact ordered CSV cells or JSON structure.')
