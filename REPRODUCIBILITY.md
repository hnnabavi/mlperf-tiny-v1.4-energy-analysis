# Reproducibility notes

## Software environment

The public core reproduction requires Python 3.10+ with pandas and NumPy. The manuscript analyses were additionally checked with Matplotlib/Jupyter in the journal supplementary package.

## Reproduction

Run:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r src/requirements.txt
python src/reproduce_core.py
```

The script writes deterministic outputs to `outputs/`:
- task-wise energy/latency dispersion;
- overall and available-only Pareto frontiers;
- exact deterministic Pareto robustness radii;
- leave-one-configuration-out sensitivity;
- leave-one-organization-out sensitivity;
- streaming-power frontier.

The repository also provides the historical v1.2 Syntiant operating-point data and the source discrepancy table used for the provenance sensitivity discussion.

## Source pin

All v1.4 source checks in the paper use MLCommons `tiny_results_v1.4` commit:

`467349483deb933f9259775b47d6c534a0d25da5`

The final published v1.4 results sheet remains the primary quantitative source used for manuscript tables. Where the final sheet and pinned repository disagree, the discrepancy is documented rather than silently reconciled.

## Interpretation constraints

- Non-streaming metrics are energy per inference.
- Streaming wake-word metrics are average system power.
- Repeated trials characterize short-run repeatability, not a complete uncertainty budget.
- Derived tables are deterministic transformations of public benchmark values.
