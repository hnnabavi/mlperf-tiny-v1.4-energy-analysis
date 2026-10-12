# Verification and integrity scope

## Completed

- Deterministic archival audit on curated MLPerf Tiny releases v1.2–v1.4 and targeted v1.0/v1.1 source lineage.
- Separate handling for inference energy (`uJ/inference`) and SWW streaming power (`mW`).
- Explicit task boundary (IC distinct from IC2).
- Release-record reuse flagged through previously recorded official source blob identities.
- Trial and release selection statistics summarized without pseudo-independent p-values.
- Core `test_audit.py` tests and future importer `tests/test_release_import.py` smoke tests.
- Deterministic comparison of archived numerical outputs by `reproduce_check.py`.

## Not established

- No new physical experiments or calibration of electrical instrumentation.
- No independent confirmation of every published measurement or live source URL in this package build.
- Not all file-hash-unique records correspond to independent measurement campaigns.
- No validated future-release predictions or improvement over published adaptive real-time governors.
- The example future importer validates syntax and declared semantics only. It does not verify physical boundary compatibility, measurement provenance or model quality.
- Researcher and journal must decide if public authorship metadata is compatible with double-blind review.

## Reproduction criteria

1. `python -m unittest -v test_audit.py` passes four core tests.
2. `python -m unittest discover -s tests -v` passes importer tests.
3. `python reproduce_check.py` reports matching all ordered CSV cells and JSON content across seven frozen analytical outputs.
4. Scripts and source files pass a local corruption/immutability check in the release manifest.
