# Four-arm pilot execution plan

> Implementer: Tech Lead; independent Quality and Security reviewers use the same evidence.

**Goal:** Observe 12 bounded task attempts on one model without claiming general superiority.

**Architecture:** Native Codex CLI with fresh CODEX_HOME and task git root per attempt; local skill layer only. Shared public fixtures and frozen hidden tests. Capture model outputs first; remove temporary authentication; independently inspect generated code before invoking the scorer.

**Spec:** [Comparison design](../specs/2026-11-07-four-arm-comparison.md).

## Authorization and limits

- User approved the proposed 12 runs by replying “오케이” on 2026-11-07.
- ChatGPT login confirmed by `codex login status`; force `chatgpt` login and remove API-key fallback variables.
- Exact requested local configuration: `gpt-6-astra`, reasoning `high`, 300 seconds per attempt; no model substitution or automatic model retry.
- Four arms: default, Superpowers 7.0.1 installed package, ECC 2.2.3 commit `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`, current dev-team skills tree identified by SHA-256.
- Each arm uses Codex's bundled system skills plus only its own additional native `.agents/skills` tree. No candidate MCP/hooks, child model calls, network research, package installation or publishing.
- New temporary homes do not contain the user's AGENTS.md, plugin configuration or skills. User-level `~/.agents/skills` was absent. Machine-enforced constraints remain in effect. Prompt requests observed policy reads; inspect logs for loading failures/contamination.
- Three tasks are independently initialized; order rotates by task. One attempt per task/arm. No cherry-picking and no follow-up hints. A question-only response is an observed non-completion, not a reason to grant that arm extra attempts.
- Common prompt supplies the requested effect, stop conditions and implementation/design authorization to all arms. This narrows the experiment to autonomous execution of well-specified small tasks.

## Steps

- [x] Read-only login/config/source checks; explicit user execution authorization.
- [x] Write public tasks and independent subprocess scorer; fail/pass reference fixtures, 8 self-tests.
- [x] Review invocation and credential boundaries; remove automatic generated-code execution after independent Security objection.
- [x] Captured all 12 trials without model fallback/retry; all finished within 300 seconds.
- [x] Confirmed gpt-6-astra/high in every session, usage, unchanged policies and auth removal. Found humanizer BOM load errors in all three dev-team trials; fixed only after the experiment.
- [x] Independently inspected 12 anonymized artifacts before credential-free scoring. Preserved 58/58 frozen checks per arm and separately reported one review failure plus five posthoc JSON probes.
- [x] Published per-task scores and time/tokens, all failures and limitations; 79 repository tests and both package launchers PASS. Independent Security PASS after policy-output redaction and scope/encoding caveats. See the [final report](../../decisions/2026-11-07-four-arm-results.md).

## Measurement contract

Elapsed time includes per-trial local provisioning/login/model execution and excludes offline harness construction and later independent evaluation. Record model-execution time separately. `turn.completed.usage` is CLI-reported session usage, not cost in currency. Missing final usage is UNMEASURED; do not invent counts for timeout or startup failure. Independent review overhead is separate from actor tokens.

Functional hidden-test PASS does not establish whole-task PASS: require exit 0, unchanged policies, allowed edit scope and independent review. Scorer subprocess separation alone is not a sandbox. This pilot uses manually reviewed code for scoring; no arbitrary unreviewed code execution.

The raw trial output stays in a temporary experiment directory while reviewed. Public evidence must replace local user paths and exclude auth files, environment secrets and hidden reasoning records. Keep task prompt, commands/outcomes, final messages, output files, summary usage, model IDs and artifact hashes. No current-user setting changes, commits or pushes are requested.
