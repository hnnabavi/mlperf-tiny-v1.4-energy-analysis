"""Smoke tests for release-agnostic input normalization."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('future_importer',ROOT/'src/import_release.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FutureReleaseTests(unittest.TestCase):
    def setUp(self):
        self.path = ROOT/'examples/new_release_input.csv'
    def test_valid_typed_example(self):
        rows = module.normalize(self.path,'example')
        self.assertEqual(len(rows),2)
        self.assertEqual({r['unit'] for r in rows},{'mW','uJ/inference'})
        self.assertTrue(all(r['source_hash_verified']=='no' for r in rows))
    def test_bad_metric_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv'
            text=self.path.read_text(encoding='utf-8')
            p.write_text(text.replace('uJ/inference','mW',1),encoding='utf-8')
            with self.assertRaises(ValueError): module.normalize(p,'example')
    def test_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'duplicate.csv'
            text=self.path.read_text(encoding='utf-8')
            p.write_text(text+text.splitlines()[1]+'\n',encoding='utf-8')
            with self.assertRaises(ValueError): module.normalize(p,'example')
    def test_wrong_release_rejected(self):
        with self.assertRaises(ValueError): module.normalize(self.path,'v1.5')

if __name__=='__main__':unittest.main()
