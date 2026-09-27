# MLPerf Tiny v1.4 energy and streaming-power analysis

Reproducibility repository for the manuscript:

**Measured Energy and Streaming Power in TinyML: A Source-Pinned, Boundary-Aware Analysis of MLPerf Tiny v1.4**

Authors: Seyed Mohammad Hossein Nabavi; Somayeh Hajforoosh; Seyed Mohammad Amin Nabavi

## What this repository reproduces

This repository preserves the central datasets and deterministic analysis used in the manuscript while keeping the original MLCommons benchmark sources authoritative.

- AD, IC, IC2, KWS and VWW are treated as measured **energy per inference** (uJ/inference).
- SWW is treated separately as **average system power** (mW) for a continuous streaming service.
- Pareto comparisons are task-specific.
- Available-only and overall frontiers are reported separately.
- Composition sensitivity and exact deterministic robustness radii are reproduced.
- Five-trial energy repeatability is summarized separately from metrological uncertainty.
- A documented Syntiant final-sheet/repository discrepancy is retained rather than silently reconciled.

## Primary sources

- MLPerf Tiny v1.4 final results sheet: https://docs.google.com/spreadsheets/d/18Wwe_AIKSjjbfThMqkji5hRoG6T4BfXd/edit
- MLCommons v1.4 results repository pinned at commit: `467349483deb933f9259775b47d6c534a0d25da5`
- Repository snapshot date used by the manuscript: 27 September 2026
- Historical corroboration: MLPerf Tiny v1.2 public results repository

## Quick reproduction

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r src/requirements.txt
python src/reproduce_core.py
```

Outputs are written to `outputs/` and include task dispersion, Pareto frontiers, exact robustness radii, leave-one-configuration-out and leave-one-organization-out analyses, and the streaming-power frontier.

## Core data

- `data/v14_nonstreaming_core.csv`: 37 non-streaming energy-per-inference cells.
- `data/v14_streaming_core.csv`: six streaming-wake-word average-power cells.
- `data/repeatability_summary.csv`: configuration-level summary of the five-trial energy repeatability analysis.
- `data/v12_syntiant_operating_points.csv`: historical Syntiant operating-point pair used for cross-release corroboration.
- `data/syntiant_source_discrepancy.csv`: final-sheet versus pinned-repository discrepancy retained as a provenance sensitivity check.

The journal supplementary package contains the expanded row-level provenance tables and trial-level diagnostics.

## Interpretation constraints

Short-run repeatability is **not** a complete measurement-uncertainty budget. Likewise, the final-sheet and pinned-repository values are treated as distinct evidence layers when they disagree.

## Citation

Please cite the accompanying manuscript after publication. `CITATION.cff` describes this repository release.
