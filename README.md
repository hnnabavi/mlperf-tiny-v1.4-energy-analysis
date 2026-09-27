# MLPerf Tiny v1.4 energy and streaming-power analysis

Reproducibility package for the manuscript:

**Measured Energy and Streaming Power in TinyML: A Source-Pinned, Boundary-Aware Analysis of MLPerf Tiny v1.4**

Authors: Seyed Mohammad Hossein Nabavi; Somayeh Hajforoosh; Seyed Mohammad Amin Nabavi

## Scope

This repository reproduces the source-pinned secondary analysis of the final MLPerf Tiny v1.4 power-related results. The analysis preserves metric semantics:

- AD, IC, IC2, KWS and VWW: measured **energy per inference** (uJ/inference).
- SWW: **average system power** (mW) for the continuous streaming service, with duty cycle and estimated processing period.

SWW is deliberately not pooled with non-streaming energy-per-inference values.

## Primary sources

- MLPerf Tiny v1.4 final results sheet: https://docs.google.com/spreadsheets/d/18Wwe_AIKSjjbfThMqkji5hRoG6T4BfXd/edit
- Pinned MLCommons results repository commit: `467349483deb933f9259775b47d6c534a0d25da5`
- Repository snapshot date used in the manuscript: 27 September 2026

## Quick reproduction

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r src/requirements.txt
python src/reproduce_analysis.py
```

For a fresh source-level audit (internet required):

```bash
python src/extract_from_mlcommons.py
```

The Jupyter notebook in `notebooks/reproduce_results.ipynb` provides an interactive reproduction of the main descriptive analyses and figures.

## Data files

The `data/` directory contains derived analysis tables and source manifests. The public MLCommons source data remain authoritative. The derived files preserve result IDs, source paths, and the pinned commit so every row can be traced back to the public benchmark artifacts.

## Known provenance issue

The final v1.4 results sheet places Syntiant result `1.4-0011` in the Closed-results block, while the pinned system JSON reports `Division = Open`. The final sheet also contains IC/VWW values that do not round to the pinned result artifacts. The manuscript treats the final sheet as the primary published quantitative source and reports the pinned-repository alternative as a source-choice sensitivity analysis. No silent reconciliation is performed.

## Repeatability vs uncertainty

The non-streaming repository logs contain five repeated energy trials per cell. These support short-run repeatability diagnostics but do **not** constitute a complete uncertainty budget; systematic measurement-boundary and synchronization effects may remain.

## License note

Original analysis code in this package may be released under a code license selected by the authors. Source benchmark data remain subject to the upstream MLCommons terms. Do not imply that an analysis-code license relicenses MLCommons source material.

## Citation

Use the manuscript citation after publication. A `CITATION.cff` file is included for the repository itself.
