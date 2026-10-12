# New-release adaptation protocol

**Status:** schema and smoke tests implemented; **not** prospective validation on an unseen MLPerf Tiny release.

1. **Obtain evidence.** Identify the official release sheet and repository; pin the exact source commit for reproducibility. Document task definitions and result divison/quality status.
2. **Classify metrics.** For each task, check whether the reported quantity is an inference energy or continuous service power. Never infer this from a generic `Power` column name alone. Do not combine incompatible measurement windows.
3. **Normalize.** Copy or map task-level source fields into the canonical schema in `docs/data_dictionary.md`. Each input row must represent one reported task/configuration/metric, not a vendor average.
4. **Dry-run validator.** `python src/import_release.py --input NEW.csv --release vNEXT --output normalized/vNEXT.csv` checks units, task compatibility, positive values, statuses and key uniqueness. `--map adapter.json` renames source CSV columns. It does **not** verify source content.
5. **Verify source records.** Inspect the pinned energy and performance logs, implement an adapter for any changed field, and check raw artifact hashes. Retain conflicts as labelled alternatives. Never presume two distinct files mean two independent test campaigns.
6. **Declare selection cohort.** Preview/available is a policy choice, not a measurement error. Use a configuration's actual status in the relevant source release.
7. **Compare against frozen evidence.** Re-run the baseline analysis on the new release in isolation; only then attempt explicit matching with older hardware/software conditions.
8. **Test and version.** Add representative verified regression fixtures, document source commit and analysis change log, obtain peer review. Archive immutable tag via Zenodo.

**Important:** The frozen 88-row corpus is never implicitly modified by the future-release importer. A new scientifically reviewed analysis version must deliberately update dataset selection, source ledger, test invariants and study limitations.
