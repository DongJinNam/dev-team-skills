### Fixed

- Release promotion now rewrites the CHANGELOG preamble's "current packaged version" sentence to the new version, so it no longer lags one release behind.
- `scripts/release.py` docstring now matches `bump_manifests`: the marketplace version is bumped for every entry in `plugins`, not just `plugins[0]`.
- CHANGELOG `[1.2.0]` entry states the tag and GitHub Release were published when the change merged.
- The security-packet workflow runs only for same-repository pull requests; fork PRs no longer trigger the `pull-requests: write` job.
- `scripts/capture_plan.py` and `scripts/security_packet.py` reject `--base`/`--head` values that are not hex commit SHAs (4-40 chars).
- The capture runbook now states who records per-model call counts (the renewal Lead), in what format (one table row per model), and when (per batch, totalled at the end).
