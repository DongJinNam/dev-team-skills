# Four-arm skill-layer pilot

[Results and limitations](../../docs/decisions/2026-11-07-four-arm-results.md) · [Machine-readable evidence](../runs/2026-11-07-four-arm/results.json)

The approved run used Windows, Codex CLI 0.167.0, ChatGPT login and `gpt-6-astra / high`: four arms × three tasks, one attempt each, at most 300 seconds per attempt. Actual model and effort are recorded for every trial. Superpowers 7.0.1, ECC 2.2.3 at `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`, and the pre-BOM-fix dev-team skill tree were used. Native bundled skills remain available to all arms; candidate hooks, MCP, AGENTS files and child models were excluded. This is not a full product benchmark.

## Files

- `tasks.py`: public task specifications and initial files, copied into fresh trial workspaces.
- `score.py`: frozen hidden acceptance tests, never copied to candidates. It imports generated code in a subprocess, **not a security sandbox**. Execute only after independent code inspection and removal of authentication copies, using a credential-free environment.
- `run_pilot.py`: Windows experiment orchestrator. `--execute` launches model work and consumes account usage. Without it, preparation only. Existing experiment roots cannot be overwritten. Its timeout process-tree cleanup uses Windows `taskkill`; orchestration on macOS/Linux is not validated. The task/scoring and reporting modules use standard Python.
- `../check_skill_discovery.py`: credential-free native `app-server` skill-list probe. It sends initialize/skills-list requests only, not a model turn. The target should be an isolated local test workspace with no unreviewed project configuration.

## Offline verification

Python 3.10+; these commands are the same in PowerShell and Bash:

```text
python -B -m unittest discover -s tests -p test_pilot_scoring.py
python -B evals/compare_outcomes.py evals/runs/2026-11-07-four-arm/vs-superpowers-input.json
```

The test suite checks bad fixtures and known reference implementations. The archived candidate code has also been independently inspected; its reported functional results can be reproduced with `score(task_id, workspace)` against the corresponding evidence directory. Original tests remain 32 + 21 + 5; `posthoc_probe.py` in the evidence directory contains the five JSON checks introduced after blinded review and must remain labelled separately.

## Another model experiment requires a new execution decision

Example preparation command (replace placeholders; no model calls without `--execute`):

```text
python -B -m evals.pilot.run_pilot --root NEW_EXPERIMENT_DIR --superpowers PINNED_SUPERPOWERS_DIR --ecc PINNED_ECC_CHECKOUT --auth-home CURRENT_CODEX_HOME
```

The original 12-run approval does not authorize another batch. Agree on repeats, tasks, acceptance criteria and account-use limits before further execution. Keep model/effort, source hashes, timing boundaries and cached/uncached token accounting comparable. `--root` must be a dedicated experiment directory, never an existing user workspace.

Generated artifacts are not automatically executed by the collector. The actual sequence was: collect → remove all temporary auth copies → condition-blinded static review and hash confirmation → credential-free scoring → publish sanitized evidence. Primary test scores, review verdicts and later exploratory probes are distinct. Reported actor tokens exclude offline experiment preparation and the independent evaluator; full-workflow tokens/currency costs remain unknown.

Before publishing logs, remove auth/session reasoning files and mask local user paths. The evidence directory retains prompt, final message, code/tests, command/file-change audit, stderr, usage and source/artifact hashes. It intentionally excludes the copied third-party packages and private credential material.

Policy-reading command outputs are omitted from the public audit to avoid redistributing third-party skill source text. Each omission retains the path-masked output's UTF-8 byte count and SHA-256; commands, status and exit codes remain. Mixed task output in those commands is omitted as well. Some native PowerShell reads displayed corrupted non-ASCII characters because no encoding was specified; this uncontrolled difference limits attribution to the skills themselves. A future experiment must verify consistent UTF-8 reads before execution.
