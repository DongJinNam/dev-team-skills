# Agent decision regression implementation plan

> **For agentic workers:** Implement inline with test-driven-development; request an independent final review.

**Goal:** Make six previously agreed pressure scenarios repeatable and distinguish live agent decisions, replayed records, fixture tests and unverified execution.

**Spec:** The user requested the second researched improvement and latest main fetch. Base: 7e35020d3567fb28fabcdbe44eef3d88f97f5e2e.

**Architecture:** Python standard-library runner exports requests or invokes an explicit argv adapter in a fresh subprocess per case. Structured decisions receive deterministic checks; free-text meaning needs a separate review bound to the response hash. Native subagent runs supply an initial recorded baseline. No new behavioral policy is introduced.

## Constraints and review focus
- Six fixed cases: unrun tests, stale security, pending votes, stop conditions, partial evidence, scoped rechecks.
- Policy and scenario content hashes invalidate old results after changes.
- Never equate fixtures/replay with a fresh model run, or a decision with an actual tool action.
- Missing/duplicate/unknown cases, malformed output, timeout, stale hashes or absent semantic review cannot produce overall PASS.
- Runner commands are explicit argv, never shell strings; CI uses fixtures/replay only and no model credentials.
- Goal: all six recorded decisions satisfy applicable checks and separate semantic review. This is one sample per case, not a reliability estimate.
- Stop and report if a run needs production changes, secrets, or weakening existing gates; none are needed for decision-only scenarios.

## Tasks
- [x] Write six prompts and collect fresh-context baseline decisions using current policy files, with no expected answers in prompts.
- [x] Write failing black-box runner tests for pass/fail, missing/stale evidence and fixture labeling.
- [x] Implement export, explicit adapter invocation, replay and review-bound scoring.
- [x] Run positive/negative scorer tests and all existing package tests.
- [x] Link the workflow from harness documentation; add CI replay with truthful labeling.
- [ ] Independently review decisions and code/security, publish branch and PR with evidence and limitations.

Baseline: six native decision tasks, one sample per case. All six passed structured checks and separate semantic review by /root/behavior_semantics. Initial scorer tests failed before the runner existed; the implemented suite has 37 passing test methods on Linux. These are decision outputs, not tool-execution or reliability evidence.
