# External contributions: evidence and handoff

Read only when preparing a code contribution to another repository. Connect existing ownership, authorization and verification contracts through these fields; add no role or standing meeting. For consuming an external tool, use the [adoption contract](./tool-adoption_en.md).

## 1. Target and scope

Lead assigns relevant Product/Engineering/Quality capabilities and maintains this record.

| Record | Evidence |
| --- | --- |
| User fit | Domain, requested contribution type and exclusions. For core work, prioritize reproducible bugs, boundary behavior and regressions. Obtain a user decision before substituting translation. |
| Repository state | Upstream URL, base branch/SHA, check date, recent releases/maintenance, relevant issues and overlapping PRs. Stars aid discovery, not acceptance predictions. |
| Contribution conditions | Check LICENSE plus CONTRIBUTING, PR templates and contributor checks for CLA/DCO, extra accounts, certification, fees and prior issue agreement, separately. Unknown stays UNKNOWN. |
| Selection | Reproducer, expected/actual behavior, user impact, change size, verification cost, compatibility and required maintainer agreement. Suggest another candidate if required conditions are unmet. |

A permissive license does not guarantee unrestricted contribution. Distinguish GitHub login from additional project signing/certification. With no explicit prior-agreement requirement, an authorized local bug fix restoring an existing contract may proceed. Check upstream agreement procedures for new APIs, intentional behavior changes or large designs. Neither path guarantees acceptance or merge.

## 2. Verification record

Quality uses existing tools and one `AC | revision | command/environment | executed scope | expected/actual | result | log/limits` table.

- For a bug regression, record the intended failure on unchanged code and success after the fix, including how new tests were applied to the old code. An unrun baseline is not a reproduced failure.
- For lazy reads, caches or pooled state, inspect relevant boundaries: actual driver results (normalization/null), repeated changes/invalidation, retry after failure, restoration on return without a read, and absent defaults. This is not a mandatory all-cases suite for every change.
- Inspect default test selection and CI commands first. Distinguish default, focused, additional stress and external-service runs, skips and exclusions. Retain observed failures; compare under matching base conditions to classify introduced, existing, environment-related or unverified causes. Existing failures do not waive required gates.
- If Docker or another environment is unavailable, retain NOT_RUN for the original suite. Record actual methods, driver/DB versions, adapter and lifecycle differences for alternatives such as a real local DB. Alternative evidence is not a full original-suite PASS.
- Compare performance with matching inputs, iterations, environment and warmup. Query counts, latency and throughput are different metrics. Unmeasured elapsed time, production performance and token savings remain UNMEASURED.

## 3. Publication handoff

After final editing, Lead fills these fields. Reuse existing authorization and stop contracts; reconfirm only affected changes.

```text
Target: upstream/fork, base branch/SHA, head branch/SHA
Scope: user goal, issue, file list/count, commit count, additions/deletions
Title/body: exact strings to publish
Verification: commands/results, skips/exclusions, failures, alternative-test limits, measured metric
Authority: local edits/publication/merge scope, final-approval condition and evidence
Outstanding: gaps/blockers and next actions
```

Calculate statistics from the complete intended change, including new files. Inspect `git status --short` plus staged/unstaged diffs and stage only relevant paths. After committing, use the merge-base diff/stat and commit list against the target base. Do not omit untracked files by relying on `git diff --stat` alone or include unrelated files with `git add .`. Remove sensitive logs from public text.

If the user requires final approval, present the packet before creating the PR. Reuse approval for unchanged content, target and scope rather than asking again. If changes exceed that approval, show the delta and hold affected publication. PR creation authority is not merge/deployment authority.

## 4. Publish and verify

1. Check actual write capabilities and permissions; successful reads do not establish write access. Use connector/CLI/browser routes only when the host permits them and account, repository and data authorization covers them. Record integration 403 failures and available paths rather than hiding or repeatedly retrying them. Never bypass policy/approval denials or independently expand tokens/permissions.
2. After upload, compare the remote head's complete diff/files with the tested local change; equal-base Git tree comparison is an option. Commit metadata may change the SHA without changing content, but never copy head-bound security PASS to a new SHA. Hold PR creation on mismatch or unverified equivalence and investigate.
3. Read back the created PR URL, Open/Draft state, base/head, exact title/body and file statistics. Report only observed CI state. Creation, successful checks, review approval and merge are distinct outcomes. Merge still follows existing independent security, compliance, QA and authorization contracts.

Write natural English starting with the problem and resulting behavior, followed by verification and limitations. Do not attribute unperformed work to a human or omit upstream-required AI contribution disclosure.
