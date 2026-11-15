# Benchmark — how to reproduce the numbers

The numbers on the README are measurements, not slogans. This page
says exactly how each one was produced, what it costs to reproduce,
and what it does not prove.

## The headline numbers

| Claim | Source |
| --- | --- |
| vs Superpowers −15.6% tokens / −7.4% time | 4-arm pilot, same model, 3 tasks each — [protocol](../evals/skill-comparison.md), [results](decisions/2026-11-07-four-arm-results.md) |
| vs ECC −20.9% tokens / −14.3% time | Same pilot |
| Decision scenarios 19/19 defense | [comparative benchmark](../evals/comparative-benchmark.md), data in `evals/runs/2026-11-07-comparative-benchmark.json` |

Limits, stated in the same sources: 3 tasks per condition is a
small sample. It does not establish general superiority,
noninferiority, or monetary savings. Defaults were cheaper than
either skill layer in that pilot.

## Reproduce the benchmark table (no API, no cost)

```bash
python evals/benchmark_metrics.py evals/runs/2026-11-07-comparative-benchmark.json
```

Runs locally in about 0.07 s (measured 2026-11-15 in this repo).
No model call, no API cost. It prints the 4-metric table (defense
rate, tokens, turns, defect detection) from the recorded run.

## Reproduce the 4-arm pilot (needs a model)

The pilot itself is not re-runnable here. Requirements, from the
results record:

- Codex CLI 0.167.0 on Windows, ChatGPT login, model `gpt-6-astra`,
  reasoning `high`.
- Three tasks: JSONL aggregation bug fix, pagination implementation,
  documentation fix against the real CLI.
- Every run finished within 300 s. No extra user hints, no model
  retries, no model substitution.
- Protocol: [../evals/skill-comparison.md](../evals/skill-comparison.md).
  Independent review was blinded to the condition names.

Expected API cost: NOT_RUN. No pricing data lives in this repo, and
the results record explicitly does not claim monetary savings. Do not
quote a dollar figure for this pilot.

## Reproduce the skill trigger checks

Positive/negative trigger evaluation is the discovery check plus the
entry-layer tests:

```bash
python3 evals/check_skill_discovery.py --cwd . --output /tmp/discovery.json
python3 -m unittest tests.test_entry_layer
```

Measured 2026-11-15 at head `6df7d15`: 14 skills found, 0 errors.
The entry-layer tests assert the trigger phrases
("fix this bug", "build this feature", "이 버그 고쳐줘",
"이 기능 만들어줘") route to `using-dev-team-skills`, and that the
SessionStart hook injects the same entry skill.

## Failure disclosure

- Failed runs are kept, not deleted: `evals/runs/` holds failed
  capture attempts alongside the passing ones, and the PR body names
  them.
- A benchmark that cannot run here says NOT_RUN instead of a number.
  The README details block lists the same limits (small sample,
  NOT_RUN hosts) next to the claims.
- If a reproduction disagrees with a published number, the published
  number is wrong until re-measured. Open an issue with the command,
  the output, and the head SHA.
