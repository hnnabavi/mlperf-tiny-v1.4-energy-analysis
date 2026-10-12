# Provenance-Aware TinyML Benchmarking

**An executable framework for reproducible energy–performance comparisons.**

[![Python verification](https://github.com/hnnabavi/mlperf-tiny-v1.4-energy-analysis/actions/workflows/validation.yml/badge.svg)](https://github.com/hnnabavi/mlperf-tiny-v1.4-energy-analysis/actions/workflows/validation.yml)

This repository contains the deterministic, archival validation package associated with the manuscript **“Provenance-Aware TinyML Benchmarking: An Executable Framework for Reproducible Energy–Performance Comparisons.”** The earlier v1.4-only study remains part of this repository's history, and its earlier files (`src/reproduce_core.py`, etc.) may remain accessible as legacy analyses.

## What this software does

- Separates **energy per inference** (`uJ/inference`) from **continuous streaming average power** (`mW`).
- Maintains task boundaries (AD, IC, IC2, KWS, VWW versus SWW).
- Records availability categories independently of measured performance.
- Identifies **documented identical archived source files** across benchmark releases.
- Reproduces descriptive shifts and policy-dependent minimum-energy selections.
- Keeps conflicting official-sheet versus repository evidence explicitly labelled.

It **does not** establish new experimental energy measurements, metrological calibration, independence of different archived files, or physical-deployment reliability.

## Verified input cohort and findings

| Source cohort | Reported entries | Interpretation |
|:---|---:|:---|
| MLPerf Tiny v1.2–v1.4 | 88 | 73 non-streaming inference energy + 15 SWW service power |
| v1.4 | 43 | 37 inference energy + six streaming average power |
| Historical v1.0–v1.3 artifact checks | Targeted | Six repeated Syntiant energy source files identified in four release archives |

The v1.2–v1.3 deduplication example changes three task medians by **31.3–31.7%**; v1.4 available-only filtering changes the task-wise minimum-energy option for **5/5 non-streaming tasks**. Across eight matched ST task/board comparisons, the median absolute release energy change is **3.38%**. These are **archival descriptive results**, not prospective experimental predictions. See `generated/audit_summary.json`.

## Installation and reproduction

**Requirements:** Python **3.9 or newer**. The core audit uses only the Python standard library.

```bash
# Run after cloning or downloading and extracting the repository:
python validate_audit.py --input . --output generated
python -m unittest -v test_audit.py
python -m unittest discover -s tests -v
python reproduce_check.py
```

Windows users may use `py -3` in place of `python`. Run the commands from the repository root. `reproduce_check.py` independently reruns the frozen audit in a temporary folder and compares its seven outputs byte-for-byte with `generated/`.

**Optional figure generation:** install `matplotlib` and `numpy` then run `python generate_figures.py`; figure scripts are not needed to reproduce the numerical audit.

## Reuse on a new dataset

1. Consult [`docs/data_dictionary.md`](docs/data_dictionary.md) and [`docs/future_releases.md`](docs/future_releases.md).
2. Supply a task-level input CSV such as [`examples/new_release_input.csv`](examples/new_release_input.csv).
3. Run: `python src/import_release.py --input examples/new_release_input.csv --release example --output /tmp/example_normalized.csv`.
4. Inspect the normalized record output and audit flags **before** using the values in cross-release comparisons. The importer **does not** automatically append unverified files to the 88-record analysis.

The sample contains fabricated illustrative values marked `example`, solely to demonstrate validation; **do not** cite it as measured MLPerf data. Future schema changes require a release-specific adapter and new tests.

## Research materials

- `reported_88_cells.csv`: curated source-aligned, release-labelled metric records.
- `historical_source_ledger.csv`: source-path and Git blob SHA-1 lineage for selected v1.0–v1.3 artifacts.
- `v14_nonstreaming_energy.csv`, `v14_streaming_power.csv`: separately typed v1.4 records.
- `matched_release_v13_v14.csv`: eight retrospective matched comparisons.
- `deadline_selection_stress.csv`: 164 **dependent budget scenarios**; not 164 experiments.
- `software_configuration_holdout.csv`: eight software-path contrasts; not independent device replicates.
- `generated/`: reproducibly derived outputs.
- `docs/source_provenance.md`: original source citations, review status and documented exceptions.
- `docs/data_dictionary.md`: column definitions and physical units.
- `docs/future_releases.md`: validation rules for newly published MLPerf releases.
- `docs/verification_scope.md`: evidence quality, known limits and reproducibility checks.

## Sources, licensing, citation

The original MLPerf Tiny results were published by **MLCommons and benchmark submitters**. This repository attributes and links upstream evidence; it is **not** an original measurement campaign. See [`docs/source_provenance.md`](docs/source_provenance.md).

The newly authored validation software and repository documentation are made available under **Apache-2.0** (`LICENSE`). Original upstream artifacts remain subject to their respective upstream licences and attributions; see `NOTICE`. GitHub's citation interface reads `CITATION.cff`.

For scientifically exact reuse, cite the **specific version DOI** after a Zenodo archive is published. **No DOI has been assigned yet**; do not replace this statement with an invented identifier.

**Research anonymity:** The repository is public and contains identifiable author information. Confirm double-blind policy before citing this author-identifiable URL inside an anonymized review manuscript.
