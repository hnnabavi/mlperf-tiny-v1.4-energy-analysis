# Reproducibility notes

## Software environment

The package was prepared and tested with Python 3.13.5, pandas 2.2.3, NumPy 2.3.5, and Matplotlib 3.10.8. The scripts are written for Python 3.10+ and use only common scientific-Python packages.

## Two reproduction modes

1. **Offline deterministic reproduction**: `src/reproduce_analysis.py` starts from the bundled CSV tables and regenerates the Pareto, exact robustness, composition, streaming, repeatability-summary, and source-choice outputs.
2. **Source-level check**: `src/extract_from_mlcommons.py` downloads the final public sheet and fetches artifacts from immutable MLCommons commit `467349483deb933f9259775b47d6c534a0d25da5`. It rebuilds primary-source checks and trial-repeatability files.

## Interpretation constraints

- Non-streaming metrics are energy per inference.
- Streaming wake-word metrics are average system power; do not convert them to uJ/inference unless a defensible work-unit definition is explicitly introduced.
- Repeated trials measure short-run repeatability only.
- The final sheet is the primary published result source; repository mismatches are preserved as provenance sensitivity rather than overwritten.
