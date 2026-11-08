# Skill comparison protocol

Installation, actual invocation, task correctness and efficiency are separate measurements. The existing nineteen decision scenarios test this repository's policy; they are not a fair leaderboard for unrelated skills. `compare_usage.py` remains the detailed full-call token accountant. `compare_outcomes.py` adds paired outcome and elapsed-time summaries without claiming statistical significance or causality.

## Before running models

Register the task inputs, hidden common acceptance tests, sample IDs, repeat count, candidate revisions and success criteria before inspecting results. Compare no skill, a pinned external skill (for example Superpowers), and dev-team-skills in separate pairs. Use the same model/settings, OS/client version, repository snapshot, clean installation state, permissions, time budget and initial user instructions; record these in `config`. Do not load the candidate's policy into the baseline session. Randomize or counterbalance arm order and use a fresh session for each task/repeat. A comparison against Superpowers must run dev-team-skills standalone; a combined workflow is a separate treatment.

Include at least a bug fix, a small feature and a documentation-only change, with executable acceptance tests appropriate to each. Shared tests assess correct output and scope, not dev-team-specific role names or report wording. Have a separate reviewer check the final diff without knowing the arm. Freeze scoring before the runs; retain both original and corrected scores if a scorer defect is discovered. Choose repeat count, minimum useful difference and uncertainty analysis before any claim of superiority. Three repetitions of one CLI command are only a local smoke test.

The user subsequently approved a bounded 12-run ChatGPT-account pilot, completed on 2026-11-07; see the [results](../docs/decisions/2026-11-07-four-arm-results.md). This does not authorize further model runs or separate API billing. Authentication issues stop affected execution; insufficient evidence stops unsupported conclusions. Record blocked/unattempted experiments as NOT_RUN, not failed completed trials. Once a preregistered trial starts, installation failure, timeout or cancellation must remain in the denominator. Persist partial usage and failure logs rather than dropping the trial. An incomplete planned experiment cannot establish superiority.

## Outcome input contract (schema_version 1)

Use UTF-8 JSON. Required top-level fields:

- `schema_version`: integer `1`; `origin`: `measured` or `fixture`.
- `sample_ids`: nonempty unique IDs fixed before execution (task + repeat).
- `config`: exactly `model`, `settings`, `environment`, `tasks_sha256`, `rubric_sha256`; first three are nonblank strings, hashes are lowercase SHA-256. Environment records OS, client/version, clean state and fixed permissions. Settings include time budget and order protocol.
- `baseline` and `candidate`: each has `revision` (immutable package ID/commit; record no-skill explicitly), a copy of the same `config`, and `samples` matching every planned ID exactly once.
- Each sample: `id`, `installed`, `activated`, `passed` (booleans), `interventions` (nonnegative integer), `elapsed_seconds` (nonnegative finite number or null), `total_tokens` (nonnegative integer or null), `evidence` (nonblank artifact/log reference).

`installed` means host installation succeeded (for no-skill control: clean environment prepared). `activated` requires observed use of the intended policy, not just a file copy or enabled flag (for no-skill: verified absence of candidate policies). `passed` means common task acceptance tests and independent diff review passed. Impossible transitions are rejected. An intervention is additional human guidance after the frozen prompt, including setup corrections; a required initial authorization is supplied equally to all arms.

Time covers setup start to completion/failure, including retries and review. Tokens include all parent, child, retry, review and editing calls; do not count cached/reasoning subtotals twice. Supply `null` when unavailable, never zero. A missing measurement makes the full-arm mean null; the measured count remains visible. Different success rates can make raw time/token means misleading: retain failure rates and budgets next to cost figures. `compare_usage.py` supplies the stricter equal-quality full-call cost comparison.

Metrics report numerator/denominator/percent for installation, activation, completion, and `first_pass` (completion with zero interventions). Delta is candidate minus baseline in **percentage points**, not relative percent. Input metadata and evidence references are operator assertions: `evidence_authenticated=false` always. `superiority=NOT_ESTABLISHED` always; the reporter summarizes observations and does not infer broad quality from them. Exit 0 means valid report, not successful tasks. Invalid input exits 2.

## Reproduce

Python 3.10+ standard library; these commands are the same in PowerShell and Bash:

```text
python evals/compare_outcomes.py path/to/paired-outcomes.json
python evals/compare_usage.py --help
python -m unittest discover -s tests -p test_outcomes.py
```

`tests/test_outcomes.py::record` is a synthetic two-sample example: 1/2 (50%) first-pass, 7.5 seconds mean, token mean unknown. It tests accounting, not skill performance. For a CLI report smoke test using that fixture:

```text
python -c "import sys,json,pathlib; sys.path.insert(0,'tests'); from test_outcomes import record; pathlib.Path('paired-fixture.json').write_text(json.dumps(record()),encoding='utf-8')"
python evals/compare_outcomes.py paired-fixture.json
```

The command writes UTF-8 explicitly on both shells. Delete the local fixture after inspection. Do not publish it as measured evidence.

The opt-in install check uses temporary `CODEX_HOME`, local package commands and no model calls:

```text
python evals/check_codex_install.py --output install-report.json --runs 3
```

It changes only disposable Codex settings/cache and the explicitly named output file, which it overwrites. Current user's configuration is not changed. It checks legacy command rejection, corrected registration/install/list, enabled state and exact copies of eight skill files. It does not measure automatic discovery, actual policy invocation, remote marketplace access, macOS/Linux installation or Claude. See the committed [Windows report](runs/2026-11-07-codex-install.json).

Current cross-skill pilot: **12 attempts, 3 per arm**. All frozen checks passed; blinded review and separately labelled posthoc probes found one default-arm task incomplete. dev-team matched the other skill arms' reviewed task count with lower observed actor tokens/time, but used more uncached input. These observations do not establish general superiority, noninferiority or monetary savings. Full workflow tokens including external evaluation remain UNMEASURED. See [pilot execution and reproduction](pilot/README.md).
