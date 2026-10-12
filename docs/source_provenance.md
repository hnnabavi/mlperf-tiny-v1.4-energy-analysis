# Upstream benchmark provenance

The research analyses published MLPerf Tiny records. The authors did not collect new hardware measurements. The original energy/power data were produced and reported by MLCommons benchmark submitters.

| Release | Official repository | Pinned revision |
|:--|:--|:--|
| v1.0 | https://github.com/mlcommons/tiny_results_v1.0 | `c7761cf84076d601c4a0ed2ecc51e77d40696ed2` |
| v1.1 | https://github.com/mlcommons/tiny_results_v1.1 | `c32ef94d19429ef1d318e9c7a60002a4bd70e11b` |
| v1.2 | https://github.com/mlcommons/tiny_results_v1.2 | `cadb362343f559d459e7cdb8748685ba76b9eb23` |
| v1.3 | https://github.com/mlcommons/tiny_results_v1.3 | `cd605ea0981306693c9e19765a15801c776988dc` |
| v1.4 | https://github.com/mlcommons/tiny_results_v1.4 | `467349483deb933f9259775b47d6c534a0d25da5` |

The MLCommons repository root `LICENSE.md` carries the Apache License 2.0 in the inspected v1.2 and v1.4 results repositories. Each source record retains its original URL and provenance fields in the CSV ledgers.

**Verification scope:** Source URL and documented Git blob identifiers are in the ledgers. Two representative Syntiant blobs were cross-checked across v1.0–v1.3. Other source URLs have not all been independently downloaded afresh in this packaging run. Sheet/repository Syntiant metadata and some recorded results conflict; the source hierarchy preserves these as alternative values, not silently reconciled truth.

**Source/corpus distinctions:** 88 = release-reported power-related rows from v1.2–v1.4; not 88 physically independent hardware configurations. The six Syntiant source files duplicated between v1.2 and v1.3 are counted once for deduplicated medians only. 164 task-budget choices are related scenarios, not experiments.
