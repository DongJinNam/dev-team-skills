# Model Routing Contract

How model tiers are assigned by task type. Reasoning, analysis, and judgment go to the top tier; routine work under a settled design goes to the cost-effective tier. Host-level instructions and an explicit model choice by the user take precedence. This contract does not switch models by itself. It defines the assignment criteria and the recording method: where the host provides a pinning mechanism, apply it through that mechanism, and report applicability and the actual model only as verified.

## 1. Tiers and default assignment

| Tier | Tasks |
| --- | --- |
| DEEP | Design and architecture decisions, analysis and root-cause work, counterexamples for material alternatives, Tier decisions, security verdicts and independent review, compliance judgments, summaries of analysis and the final explanation |
| STANDARD | Implementation of a settled design, test writing, routine edits, general documentation, running verification commands and organizing results |
| LIGHT (optional) | High-volume low-judgment work such as exploration, search, classification, and format conversion |

- The Security Review Engineer and any role making a decision or verdict stay on DEEP. Judgment work is never moved down to STANDARD or below to save cost.
- Engineering implementation and Quality's verification runs default to STANDARD. Quality's completion-criteria design and evidence judgment are DEEP.
- In the Lead's final explanation, analysis summaries are DEEP and plain progress reports are STANDARD.
- Escalation: when STANDARD or LIGHT work fails repeatedly or the failure cause is unclear, redo it on DEEP. When a result feeds a security or decision gate, the judgment step itself runs on DEEP.
- Do not rerun the same task on a different tier just to duplicate it. On escalation, hand over the failure evidence from the previous attempt.

## 2. Host application (verified 2026-11-11)

Model names are examples as of the verification date. The contract itself is the tiers; update only this table as models retire or are renamed. Alias resolution differs by provider, so verify the actual model in the running environment.

| Host | DEEP | STANDARD | LIGHT | Pinning mechanism and enforcement level |
| --- | --- | --- | --- | --- |
| Claude Code | `opus` (Opus 5.5; `fable` for the hardest work) | `sonnet` (Sonnet 5.5) | `haiku` (Haiku 5.5) | Enforceable via `model`/`effort` in SKILL and subagent frontmatter. `opusplan` (Opus for planning, Sonnet for execution) is the built-in pattern with the same shape |
| Codex | `gpt-6.1-sol`, effort high (`gpt-6-astra` for the hardest work) | `gpt-6-luna` (`gpt-6.1-terra` when the work is document/summary-heavy) | `gpt-6-luna` | Skill prose is request-level only. Pin via `model`/`model_reasoning_effort` in `.codex/agents/*.toml` and the `[agents]` defaults in `config.toml` |
| Cursor | Explicit model ID (e.g. `claude-opus-5-5[effort=high]`) | `composer-2.5` or Sonnet 5.5 | Haiku 5.5 / Luna class | Pin via `model` in `.cursor/agents/*.md` frontmatter. Admin-blocked or out-of-plan models are silently substituted, so verify the actual model |
| Antigravity | `pro`-tier subagents (the main agent's Gemini 4 Argon/Carbon or Opus 5.5 is a manual user choice) | `flash` (Gemini 3.8 Flash) | `flash` | Subagent `model` accepts only the `flash`/`pro` tiers and cannot name third-party models. The main model is manual selection only. There are unconfirmed reports that `pro` pinning may not take effect on personal accounts, so verify the actual model |

Sources: official Claude Code model configuration, skills, and subagents documentation; official Codex models and subagents documentation; official Cursor models and subagents documentation; official Antigravity models and subagents documentation (all verified 2026-11-11).

## 3. Recording and verification

- Record the tier, actual model, and pinning mechanism per task in the work record (work minutes). If the actual model could not be verified, write it as unverified; do not report assignment intent as applied routing.
- Having assigned tiers is not evidence of token savings. Claim cost effects only from measurements under the existing cost contract, with the same scope and quality conditions.
- If the host does not support routing or the user pinned a model directly, record that fact. If a required step's tier cannot be guaranteed, report the step as limited and do not claim routing was applied where it was not guaranteed.

Review criteria, checked per case: zero DEEP-assignment misses on judgment work, zero cases of unverified actual models reported as applied, zero tier changes without a recorded reason.
