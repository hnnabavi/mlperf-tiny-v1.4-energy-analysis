# Release and DOI checklist (not yet published)

## Version reviewed

The staged software metadata is `2.0.0-rc1`, subject to author approval and GitHub QA. Do not tag a final release until all source documents, authorship metadata and journal anonymization decisions have been checked.

1. Commit or merge the tested contents of this directory into https://github.com/hnnabavi/mlperf-tiny-v1.4-energy-analysis.
2. Confirm the GitHub Actions workflow passes on the exact commit intended for release.
3. Log in to https://zenodo.org and link the same GitHub account, then use the GitHub integration page, Sync now and enable the repository.
4. Update the version from release-candidate to `2.0.0` and create the matching GitHub tagged Release **after** Zenodo integration is enabled.
5. Confirm Zenodo has automatically archived the GitHub release and generated a DOI.
6. Cite the **version DOI** in the manuscript rather than guessing a DOI or using an unverified concept DOI.
7. Retain `CITATION.cff` and `.zenodo.json`, and verify names and licenses with all co-authors.

**Double-blind caveat:** This public GitHub repository identifies the authors. Follow your journal's anonymous-review policy; do not link to identifiable public author resources from the blinded manuscript if doing so reveals author identity.

Official instructions:
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/
- https://zenodo.org/help/versioning
