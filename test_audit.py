"""Independent invariants and mutation tests for validate_audit.py."""
import tempfile,pathlib,csv,unittest,json
from validate_audit import analyze,metric_errors
ROOT=pathlib.Path(__file__).resolve().parent
class AuditTests(unittest.TestCase):
 def test_metric_unit_enforced(self):
  r={'metric_class':'energy_per_inference','unit':'mW','metric_value':'10','task':'AD'}
  self.assertIn('INVALID_ENERGY_UNIT',metric_errors(r))
  r.update(metric_class='streaming_average_system_power',unit='mW')
  self.assertIn('POWER_TASK_MISMATCH',metric_errors(r))
 def test_nonpositive(self):
  r={'metric_class':'energy_per_inference','unit':'uJ/inference','metric_value':'-1','task':'AD'}
  self.assertIn('NONPOSITIVE_OR_NONFINITE',metric_errors(r))
 def test_original_inputs(self):
  with tempfile.TemporaryDirectory() as td:
   d=analyze(ROOT,td)
   self.assertEqual(d['total_source_rows'],88)
   self.assertEqual((d['nonstream_energy_rows'],d['stream_average_power_rows']),(73,15))
   self.assertEqual(d['v14_ungated_vs_available_winner_changes'],5)
   self.assertEqual(d['historical_reused_four_release_groups'],6)
   self.assertEqual(d['release_selection_changes'],2)
   self.assertEqual(d['software_pairs_inside_joint_fixed10pct'],1)
   with open(pathlib.Path(td)/'deduplication_ablation.csv', newline='') as fh:
    ded=list(csv.DictReader(fh))
   dmap={x['task']:float(x['naive_relative_difference_pct']) for x in ded}
   for task in ('IC','KWS','VWW'):self.assertLess(dmap[task],-31)
   self.assertEqual(dmap['AD'],0)
 def test_detect_mutated_source_input(self):
  with tempfile.TemporaryDirectory() as td:
   td=pathlib.Path(td)
   for name in ['reported_88_cells.csv','v14_nonstreaming_energy.csv','v14_streaming_power.csv','historical_source_ledger.csv','matched_release_v13_v14.csv','deadline_selection_stress.csv','software_configuration_holdout.csv']:
    (td/name).write_bytes((ROOT/name).read_bytes())
   p=td/'reported_88_cells.csv'; src=p.read_text();self.assertIn('uJ/inference',src)
   p.write_text(src.replace('uJ/inference','mW',1))
   with self.assertRaises(AssertionError):analyze(td,td/'out')
if __name__=='__main__':unittest.main(verbosity=2)
