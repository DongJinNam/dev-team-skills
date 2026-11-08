# Workflow ownership with Superpowers

Use this contract when both packages participate. Follow higher-priority host instructions and explicit user scope/authorization. This reference cannot override another package's mandatory approvals or verification, or grant tool permissions.

## 1. Record mode and verified source

At kickoff, Lead checks the actual skill inventory, metadata and readable files, then records availability and source in the current work record.

- `COMBINED`: required Superpowers guidance is actually discoverable/readable; use the phase ownership below.
- `STANDALONE`: optional Superpowers is unavailable/unreadable; record the limitation and use existing dev-team procedures. Do not auto-install/enable it or transmit data, or claim it was invoked.
- If higher-priority instructions or the user make an unavailable external skill mandatory, mark its dependent phase `BLOCKED`. Optional fallback cannot bypass a mandatory prerequisite.

Resolve colliding names such as `brainstorming` using a verified package-qualified ID (for example, actually discovered `superpowers:brainstorming`) or exact file path. Local planning guidance is `skills/brainstorming/SKILL.md`. A descriptive label such as `dev-team-skills/brainstorming` is not an invented executable command. Distinguish verified version/path from actual invocation.

## 2. One owner for each overlapping phase

| Phase | COMBINED owner | Shared artifact and boundary |
| --- | --- | --- |
| Kickoff, benefits and stop conditions | dev-team Quality Lead / Lead (`DEV_TEAM`) | Mandatory two questions, historical-answer reconfirmation and current user evidence K from the kickoff/stop section in roles_en.md |
| Design exploration, design approval and implementation planning | Superpowers (`SUPERPOWERS`) | Verified brainstorming / writing-plans process produces design S and plan P; dev Planner supplies user/market evidence and missing acceptance criteria |
| Implementation, TDD and root-cause diagnosis | Verified Superpowers execution / TDD / debugging process | dev Lead connects role scope/interfaces; preserve the selected execution method and do not invent unavailable agent tools |
| Verification before completion | One evidence record maintained by Lead | Share actual commands/results/NOT_RUN for the applicable revision/scope; do not repeat identical checks per package |
| QA, independent security, compliance, merge/deployment | dev-team gates | Generic Superpowers code-quality approval does not replace independent security PASS for the latest head/base |
| Cost, voting and final explanation | dev-team Lead (FinOps / Humanizer duties) | Preserve tiered accountable decisions, advisory ballots, user-grounded reconsideration, measured/estimated/unknown costs and three-sentence report contract |

In `STANDALONE`, existing dev-team owners handle planning and implementation too. Both modes preserve mandatory gates. Record owners and actual guidance per phase rather than declaring one entire package superior. If mandatory rules cannot be satisfied together, stop the affected work and report the conflict, evidence and alternatives to the user.

## 3. Reuse confirmed answers and approved artifacts

1. Directly ask and agree on the two Test Engineer questions for the current kickoff. Present historical answers for reconfirmation as already required. Other phases reference K when it was already reconfirmed for this same kickoff/scope. Merely finding an old answer does not waive current confirmation.
2. Reuse S/P when approval evidence matches the same task and scope. Reference paths, revisions and user approval. Encountering another package or document format does not restart full SCAMPER/PRD/design/planning or repeat the same questions. Check required fields from each package and supplement only gaps.
3. Scope, assumptions, data/trust boundaries or acceptance criteria changes invalidate affected answers/approvals/plans. Record the delta, request relevant confirmation/design/security review and retain unaffected materials as evidence.
4. Verification records identify head/base or artifact, commands/results and scope. Do not relabel invalidated evidence or historical runtime PASS as a fresh execution. A wording-only change still needs relevant diff/documentation checks and new-head independent security review required by the existing contract.
5. Stop conditions halt affected work, require reporting and explicit resumption by the agreed authority. A Superpowers plan, majority vote or deadline is not resume authorization. Generic review, quality PASS and cost savings cannot waive security/compliance gates.

## 4. One handoff record

Add these fields to the existing work record, PRD or plan; do not create a duplicate document merely for this contract.

```text
mode: COMBINED | STANDALONE | BLOCKED (mandatory prerequisite absent)
availability: verified version, exact ID/path, read success/failure, actual invocation per package
owners: kickoff / planning / implementation / verification / security / final explanation
scope: current scope, revision and delta
artifacts: K (current two-question confirmation), S (design), P (plan), approval evidence/scope
verification: actual target, commands/results, NOT_RUN/historical evidence
open: gaps/conflicts/blockers, next owner and reassessment trigger
```

To conserve tokens, these fields may be compressed into a single-line Compact State Fingerprint:  
`[SQUAD:mode | owners | scope | artifacts | verification | open]`  
e.g.: `[SQUAD:COMBINED | K:DEV,P:SUPER | scope:v1 | K1,S1,P1 | DoD:PASS,Sec:NOT_RUN | open:none]`

Check one owner per phase, zero duplicate questions/plans within the same confirmed scope, zero missing mandatory confirmations and zero security/stop bypasses in scenario tests. Do not claim numeric token/time savings before measuring them.

Reference baseline: locally read Superpowers 7.0.1 using-superpowers, brainstorming, writing-plans, TDD, systematic-debugging, verification-before-completion and execution/review guidance. Keep the [upstream repository](https://github.com/obra/superpowers) as provenance and recheck version-specific mandatory steps and host capabilities at runtime. This is not automatic compatibility or installation assurance.
