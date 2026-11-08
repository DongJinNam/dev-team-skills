# Apply measured skill feedback

> Implementer: Tech Lead, using the existing approved workflow and inline execution; independent reviewers own semantic and security verdicts.

**Goal:** Apply the observed installation, encoding and evidence-reporting lessons to the active bilingual skills, then commit, push and open a PR.

**Design:** Keep the measured 12-run sources/results frozen. Add concise operational guidance to Engineering Squad and its tool-adoption reference; correct Harness Engineering's unsupported compatibility promises and distinguish package, discovery and behavior evidence. Reuse existing validation tools and preserve historical decision captures.

**Authority:** User requested skill updates plus commit/push/PR on 2026-11-08, paused, then explicitly resumed. Earlier expected-benefit and stop/report agreements remain in scope. No additional CLI performance experiment, separate API billing, merge or release is authorized.

**Owners:** Lead implements and checks; `/root/eval_review` supplies independent design objections; a fresh native actor answers the regression prompts; a different reviewer checks their meaning; `/root/security_review` checks the final diff and committed head/base. Mode COMBINED, with previously read skill-creator and Superpowers planning/writing-skills guidance.

## Accepted design objection

The existing 19 cases establish preservation of previous decision contracts, not the new encoding or comparison guidance. Keep this distinction and separately inspect the new instructions against observed failure modes. A new actor's decision answers are not performance improvement evidence. Removing temporary credentials and spawning a subprocess does not create an OS sandbox; record remaining filesystem/network exposure.

## Steps and acceptance

- [x] Update `skills/engineering-squad/SKILL*.md` and `references/tool-adoption*.md`: explicit UTF-8 reads, separate setup/discovery/use evidence, frozen comparisons, failed denominators, posthoc checks and cached/full-workflow usage.
- [x] Update `skills/harness-engineering/SKILL*.md`: BOM-free skills, native discovery, package-check limitations, reviewed generated-code execution and publishable evidence.
- [x] Collect fresh answers to the existing 19 public prompts, with no expected answers or prior responses given to the actor; obtain separate semantic review and point CI to the matching new capture. Preserve prior captures unchanged.
- [x] Review three new pressure scenarios (partial discovery/encoding, small cached-token comparison, generated-code execution with credentials) separately from the 19-case regression.
- [x] Run the 79 unit tests, PowerShell/Bash package checks, current decision replay and diff checks; record unrun environments and test scope.
- [ ] Independent security review; commit the authorized changes, verify final head/base, push the requested branch and create a PR using the repository template.

## Evidence and stop conditions

Prior observed failures are recorded in the [12-run report](../../decisions/2026-11-07-four-arm-results.md): unsupported install command, BOM load failure, policy-read encoding errors and incomplete cost attribution. These motivate the changes; their original measurements are not post-change results. Current behavior evidence requires a new capture, never old responses with rewritten policy hashes. Failed required checks, credentials/rights issues or work outside authorization stop the affected step and are reported to the user. No invented approval, blanket compatibility, general superiority or noninferiority claim.
