"""Independently regenerate the frozen audit and compare outputs byte-for-byte."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
from validate_audit import analyze
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'generated'
FILENAMES=['audit_summary.json','type_and_eligibility_audit.csv','hash_lineage_audit.csv','status_filter_winners.csv','deduplication_ablation.csv','matched_release_recomputed.csv','software_configuration_stress.csv']
with TemporaryDirectory() as td:
    analyze(ROOT,td)
    for name in FILENAMES:
        before=(BASE/name).read_bytes();after=(Path(td)/name).read_bytes()
        if before!=after:
            raise SystemExit(f'MISMATCH: {name}: expected sha256={hashlib.sha256(before).hexdigest()}, got sha256={hashlib.sha256(after).hexdigest()}')
print(f'PASS: all {len(FILENAMES)} archived analytical outputs reproduced byte-for-byte.')
