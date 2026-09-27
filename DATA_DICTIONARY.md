# Data dictionary

## Table_S1_v14_nonstreaming_energy.csv
- `organization`: submitting organization
- `config`: short configuration identifier used in the manuscript
- `status`: MLPerf availability category used in the final results sheet
- `task`: AD, IC, IC2, KWS, or VWW
- `latency_ms`: final-sheet latency in milliseconds
- `metric_value`: final-sheet measured energy per inference
- `metric_unit`: uJ/inference
- `result_id`: final-sheet result identifier
- `sheet_row`: source spreadsheet row number
- `source_commit`: immutable MLCommons repository commit
- `energy_source_path`, `performance_source_path`, `system_source_path`: source artifact paths in the pinned repository

## Table_S2_v14_streaming_power.csv
- `avg_power_mW`: average system power for the continuous SWW service
- `period_ms`: processing period derived from reported throughput and aligned to the final-sheet interpretation
- `duty_cycle_pct`: reported active duty cycle in percent
- `service_energy_uJ`: total energy accumulated over the full streaming service interval; this is not treated as per-inference energy

## Table_S10_nonstreaming_trial_repeatability.csv
- `cv_pct`: sample coefficient of variation across repeated Energy/Inf trials
- `max_abs_dev_from_median_pct`: largest absolute trial deviation from the within-log median
