# Evidence for external skills and open source

Read only relevant candidates when selecting, evaluating or auditing tool use. Product owns the problem/evidence, Engineering compatibility/execution, Quality verification, Security authority/rights, and Lead cost/selection. Add no permanent tool-evaluation role.

## Selection

1. State the problem and AC; check available tools, project dependencies and standard libraries first.
2. When external comparison is needed, compare at most three relevant candidates on the same criteria. Research more only if existing candidates fail the AC. Record research N/A for unrelated work.
3. Check official sources for maintenance, date, revision/version, license/file-specific terms, host/OS compatibility, permissions/data transfer, dependencies and expected cost. SNS, stars and downloads are discovery signals, not active-use, quality or safety evidence. A single snapshot cannot establish growth.
4. Read the exact selected package ID/path and apply it to a small actual task. Record the part used, artifact, execution result and quality. Distinguish applying a documented method from executing a script/CLI. Installation, permission and external transfer remain within user authority and host rules.
5. Compare with the existing method against identical AC, then adopt/defer/reject. Savings cannot offset functional, independent-security or applicable-compliance failure. Fall back to existing methods if an optional tool is unavailable/unreadable, recording gaps; a user-required unavailable tool blocks its dependent step.

## Evidence states

States describe claims, not automatic promotions. Record the highest supported scope and missing evidence separately. Applying a documented method does not require claiming installable availability.

| State | Evidence required | Does not establish |
| --- | --- | --- |
| DISCOVERED | Original URL, check date, relevant problem | Inspection, installation, use |
| INSPECTED | Actually read file/document, revision or check date, rights/constraints, applicability | Execution |
| AVAILABLE | Exact current package/path/version and confirmed readability or executability | Passing AC |
| APPLIED | Actual method/command, target, resulting artifact/log | Validated effect |
| VERIFIED | APPLIED evidence plus AC results, quality review and comparison scope for this revision/environment | Universal efficiency or security |

`result: PASS / FAIL / NOT_RUN` is separate. Failed use stays APPLIED + FAIL; unrun stays NOT_RUN, never VERIFIED + PASS. Missing evidence retains the last supported state. VERIFIED identifies passed AC and limits; security approval remains governed separately.

## When comparing task outcomes

- Before execution, fix model/effort, host/OS, package versions/hashes, common tasks, hidden acceptance checks, failure criteria, repeats and time/usage limits. Verify actual model records and provide the same tool authority and initial guidance. A skill-layer comparison does not measure a full product with hooks, MCP or child agents. Check policy-read encoding and loading errors in every arm.
- Retain started failures, timeouts and aborts in the denominator. Record retries, extra hints, order and cache differences. Define file preparation, successful installation commands, unique skill discovery, actual use and task completion separately. An untested host stays NOT_RUN; another host's success is not a substitute.
- Where practical, blind independent artifact reviewers to conditions. Apply newly discovered edge cases uniformly as posthoc exploratory checks, separate from frozen scores. Never overwrite earlier artifacts, scores or policy hashes as results for a new version.
- Separate input, cached input and output; do not add cached or reasoning subsets twice. Distinguish actor-only tokens from the full workflow including preparation, retries, children and independent review. Missing usage is UNMEASURED. Fewer cache-inclusive tokens alone do not establish monetary savings.
- Differences observed in a small sample do not establish general superiority, equivalence or noninferiority (not worse than a predefined margin). Such claims require effect targets, margins, sample sizes and analysis fixed before execution. Unproven superiority does not mean not inferior. Check existing execution authority and budget before additional experiments.

## One task record

Add one row/block to the existing PR/task record instead of another evaluation document.

```text
problem/AC | owner | candidate/source/file/revision-or-checked-at
license/maintenance/host/OS/permissions/data/cost/unknowns
state | actual_method_or_command | artifact_or_log | result/AC/reviewer
baseline_or_existing_option | decision(adopt/defer/reject)/reason | scope/limits
recheck_trigger | next_owner
```

Example: a CLI absent from installed tools with only its README read is INSPECTED, result NOT_RUN. Suggesting a command is not APPLIED. Writing and validating an acceptance test using a documented method supports that artifact's use claim; it does not establish execution of the external CLI.

Recheck relevant evidence before adoption and after version, permission, data-boundary, advisory or AC changes. Reuse current same-scope evidence; never copy a previous project's PASS into a new environment. For tokens use the [usage evaluation](../../../evals/token-efficiency.md), matching conditions and capturing all calls/retries/reviews plus quality gates. Without logs, report UNMEASURED.
