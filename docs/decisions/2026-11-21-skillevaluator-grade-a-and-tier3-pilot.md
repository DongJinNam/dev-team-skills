# Decision & Work Minutes: SkillEvaluator Tier 1 Grade A (9/9) & Tier 3 Live Pilot

- Date: 2026-11-21
- Branch: `feature/20261121_skillevaluator-grade-a`
- Base: `ee1ae6d` (`origin/main`, PR #45 merged)
- Tooling: NVIDIA `skillevaluator 1.0.1` (`skillevaluator[tier3]` / `harbor 0.25.0` / Docker `29.4.0` / `nv_build`)

## 1. Activated Roles & Outputs

| Owner | Scope & Action | Evidence |
| --- | --- | --- |
| Tech Lead (Ponytail · Humanizer Editor) | Branch isolation, minimal Grade A edits without Tier 2 bloat, Tier 3 pilot scoping & work minutes | This file |
| Engineering Lead | Upgraded 4 Grade B skills (`engineering-squad`, `using-dev-team-skills`, `ponytail`, `humanizer-kr`), rebuilt `skills/catalog.json`, synced `.agents/skills/` | `git diff ee1ae6d`, `verify-harness.py` PASS |
| Quality Lead | Verified 9/9 Grade A, 0 Tier 2 regressions, 19/19 eval capture renewal (`2026-11-21-skillevaluator-grade-a.json`), full `unittest`, Tier 3 Harbor pilot | `evals/runs/2026-11-21-skillevaluator-grade-a.json` (19/19 PASS) |
| Security Review Engineer (Independent) | Revision-bound independent diff review + separate compliance check on committed HEAD | Recorded on final PR head |

Product Lead and Delivery Lead: `N/A` (no product launch or deployment change).

## 2. Track 1: Tier 1 Grade A (9/9) & Tier 2 Regression Verification

| Skill | Before (`ee1ae6d`) | After (`feature/20261121_skillevaluator-grade-a`) | Tier 2 (`context-optimization-check`) |
| --- | --- | --- | --- |
| `engineering-squad` | 84.8 / B | **98.5 / A** (`100/100/100/90`) | **PASS** (71 chunks, 0 clusters) |
| `using-dev-team-skills` | 88.2 / B | **97.5 / A** (`100/90/100/100`) | **PASS** (8 chunks, 0 clusters) |
| `ponytail` | 89.5 / B | **97.5 / A** (`100/90/100/100`) | **PASS** (8 chunks, 0 clusters) |
| `humanizer-kr` | 89.5 / B | **97.5 / A** (`100/90/100/100`) | **PASS** (6 chunks, 0 clusters) |
| `harness-engineering` | 95.0 / A | **95.0 / A** (unchanged) | **PASS** (verified in PR #45) |
| `code-review` | 93.5 / A | **93.5 / A** (unchanged) | **PASS** (verified in PR #45) |
| `brainstorming` | 92.5 / A | **92.5 / A** (unchanged) | **PASS** (verified in PR #45) |
| `humanizer` | 92.0 / A | **92.0 / A** (unchanged) | **PASS** (verified in PR #45) |
| `i-have-adhd` | 90.8 / A | **90.8 / A** (unchanged) | **PASS** (verified in PR #45) |

- `skillevaluator similarity-check skills` (desc, `0.75`): **PASS** (0 duplicates).

> **Provenance & Limitations**: SkillEvaluator Tier 1, Tier 2, and Tier 3 runs were executed locally via the operator CLI (`skillevaluator 1.0.1`); raw JSON/HTML reports were stored outside the repository. Eval capture replay verifies decision policy only (`tool_execution: NOT_OBSERVED`, `provider token usage UNMEASURED`).

## 3. Track 2: Tier 3 Live Harbor Pilot (`engineering-squad`, 1-case starter)

- **Readiness (`skillevaluator doctor --tier 3`)**: **ALL PASS** (`skillevaluator 1.0.1`, `nv_build / nvidia/nemotron-3.5-lightning-30b-a3b`, `opencode`, Docker `29.4.0`).
- **Windows finding**: Using a long `--results-dir` path triggered Windows `MAX_PATH` (`[WinError 3]`); passing a short path (`--results-dir %TEMP%\t3`) resolved staging cleanly.
- **Pilot execution (`--max-cases 1 --n-attempts 1`, elapsed `720.7s`, exit `0`, 0 execution/judge errors)**:
  - `QUALITY VERDICT`: **`INCONCLUSIVE`** (provisional 1-case unreviewed starter; policy `dataset-sufficiency-v1` requires 10 positive + 1 negative cases).
  - `SECURITY CLEAN`: **1/1 | 1/1**.
  - **Key diagnostic finding**: `opencode` **never activated `engineering-squad`** (`discoverability: 0.00`, `with skill 0.51` vs `without skill 0.75`). SkillEvaluator recommended widening `SKILL.md` frontmatter `description` to match real deployment/API release coordination prompts.
  - Temporary unreviewed starter `skills/engineering-squad/evals/` was removed from this PR so Grade A ships cleanly; full Tier 3 dataset authoring (`evals/EVAL.md`, 10+1 cases) and description activation tuning belong in a dedicated follow-up PR.

## 4. Capture Renewal Model Calls & Batch Progress (P1 / P4)

Capture target: `evals/runs/2026-11-21-skillevaluator-grade-a.json` (Attempt 1: **19/19 PASS**).

| Model Tier (`model-routing.md`) | Role | Call Count | Batches |
| --- | --- | --- | --- |
| DEEP (inherited host frontier model) | Per-case isolated eval actors | 19 | 4 batches (5, 5, 5, 4) |
| DEEP (inherited host frontier model) | Independent semantic reviewer | 1 | 19/19 PASS |
| **Total** | | **20** | |
