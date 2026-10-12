# Input schema and data dictionary

The frozen corpus uses two related schemas. Original columns are not overwritten or inferred unless documented.

## `reported_88_cells.csv` (frozen manuscript cohort)

| Column | Meaning |
|:--|:--|
| `release` | MLPerf Tiny release label: `1.2`, `1.3`, or `1.4` |
| `organization`, `hardware_key` | Submitter and hardware identity as curated from source |
| `task` | AD / IC / IC2 / KWS / VWW / SWW |
| `metric_class` | `energy_per_inference` or `streaming_average_system_power` |
| `metric_value`, `unit` | Positive numeric measurement; `uJ/inference` for non-streaming, `mW` for SWW |
| `latency_ms`, `throughput_ips` | Reported task performance, if available; do not assume identical acquisition boundaries with energy |
| `average_period_ms`, `duty_cycle_fraction` | Streaming service metrics when provided |
| `status` | MLPerf reported eligibility: available, preview, or status unchecked; **not** live merchant availability |
| `division` | Repository or result-sheet division, with explicit conflicts kept |
| `duplicate_of` | Prior release-labelled identical file, when source blob identity supports this |
| `source_url`, `source_commit` | Upstream artifact location and pinned Git revision |
| `notes` | Manual evidence qualifiers and source issues |

## `v14_nonstreaming_energy.csv`

37 task/configuration rows. `latency_ms` and `metric_value` (µJ/inference) refer to published report fields. Includes provenance paths and status. `metric_type` and `metric_unit` preserve physical semantics.

## `v14_streaming_power.csv`

Six rows. `avg_power_mW` and `power_raw_mW` represent streaming average system power; `period_ms`, duty cycle and `elapsed_s` are service-level metrics. These are **not** equivalent to inference energy.

## `historical_source_ledger.csv`

Contains targeted release/file/task paths and Git blob identifiers. Equality of documented blob SHA-1 values proves identity of archived file contents, **not** hardware measurement independence.

## Future importer `src/import_release.py`

| Canonical field | Requirement |
|:--|:--|
| `release` | Supplied by `--release`; source column, if present, must agree |
| `task`, `configuration` | Mandatory; one key per task/config/metric |
| `metric_class`, `unit` | Mandatory and validated together |
| `value` | Finite positive measurement in declared physical units |
| `status` | `available`, `preview`, `unchecked`, or `unknown` |
| `source_url` | Mandatory citation or evidence URI (format not independently authenticated) |
| `source_hash` | Optional upstream hash. Copied as unverified; no source bytes downloaded |

Future importer output includes `source_hash_verified=no` and `manual_measurement_boundary_review=required`. Source identity, electrical boundaries, runtime versions, and publication eligibility must be independently reviewed.
