# Data dictionary

## data/v14_nonstreaming_core.csv
One row per non-streaming MLPerf Tiny v1.4 task-configuration result used in the manuscript.

- `organization`: submitting organization.
- `config`: short configuration identifier.
- `status`: MLPerf availability category used by the final results sheet.
- `task`: AD, IC, IC2, KWS, or VWW.
- `latency_ms`: final-sheet latency in milliseconds.
- `metric_value`: measured energy per inference.
- `result_id`: final-sheet result identifier.
- `sheet_row`: source spreadsheet row.

Energy unit: microjoules per inference.

## data/v14_streaming_core.csv
Streaming wake-word results. These are intentionally not pooled with energy-per-inference data.

- `period_ms`: processing period in milliseconds.
- `avg_power_mW`: average system power in milliwatts.
- `duty_cycle_pct`: reported active duty cycle, percent.
- `result_id`, `sheet_row`: source identifiers.

## data/repeatability_summary.csv
Configuration-level summary of the repeated non-streaming energy trials.

- `n_cells`: number of task cells represented.
- `max_trial_cv_pct`: largest within-log coefficient of variation.
- `median_trial_cv_pct`: median within-log coefficient of variation.
- `max_abs_trial_deviation_pct`: largest trial deviation from the within-log median.

## data/v12_syntiant_operating_points.csv
Historical Syntiant operating-point pair used only for cross-release corroboration.

## data/syntiant_source_discrepancy.csv
Documented differences between the final v1.4 results sheet and the pinned Syntiant repository artifacts. These differences are preserved as provenance evidence and are not silently overwritten.
