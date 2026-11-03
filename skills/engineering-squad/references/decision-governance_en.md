# Tiered decision governance

## 1. Authority and role map

This contract replaces automatic majority selection. Record scope, reversibility, affected domains, accountable decision owner and delegation evidence first. User goals, budgets, authorization and higher-priority instructions govern. Tiers describe responsibility, not model pricing or mandatory agent calls.

| Tier | Existing role / responsibility | Escalation |
| --- | --- | --- |
| 1 | **Tech Lead (same role as Squad Lead / Main Agent)**: architecture, shared contracts, cross-domain priorities and risk | User for undelegated strategy, budget or authorization changes |
| 2 | **Product Planner / Product Lead**: priorities, PRD and message alignment within approved goals | Tech Lead |
| 2 | **AI Agent Engineer / Engineering Lead**: harness and implementation direction within approved architecture; coordinate technical evidence | Tech Lead |
| 2 | **Test Engineer / Quality Lead**: acceptance criteria, verification plans and test gaps | Tech Lead; cannot pass required unverified criteria |
| 2 | **DevOps Engineer / Delivery Lead**: delivery plan, operational handoff and recovery readiness | Tech Lead; deployment authorization remains separate |
| 2 | **Finance / FinOps**: cost evidence and savings within limits | Tech Lead; user for limit changes |
| 2 | **Security Review Engineer**: independent security verdict | Direct blocker report to Tech Lead; apply security-review_en.md |
| 2 | **Compliance Reviewer**: applicable law/license review and blockers | Direct report to Tech Lead; expert review for uncertain interpretation |
| 3 | **Frontend Engineer, Backend Engineer, Data Engineer**: implementation and layer tests within approved contracts | Engineering Lead |
| 3 | **QA Engineer**: functional/regression execution and evidence | Quality Lead |
| 3 | **SRE Engineer**: reliability, observability and recovery validation | Delivery Lead; Tech Lead for SLO/architecture conflicts |
| 3 | **Product Marketing, Creative Rookie**: messaging/user evidence, dissent and small experiments | Product Lead; direct to Tech Lead for safety/authority concerns |

Reuse the fourteen roles and Lead. Humanizer Editor and Ponytail edit/simplify without additional decision rights. Lead may cover domain responsibilities on small tasks; disclose combined roles. Do not invent assent or summon every role. Independent security review cannot be combined with implementation/Lead. Engineering ownership coordinates specialist evidence rather than claiming universal expertise.

## 2. Decision routing

| Observed condition | Accountable owner and action |
| --- | --- |
| Local reversible implementation within approved contracts | Tier 3 uses implementation discretion and reports evidence; Tier 2 chooses alternatives when a decision is needed |
| Single-domain alternatives preserving goals, budget and shared contracts | Relevant Tier 2 decides after evidence and dissent; no waiting for unrelated ballots |
| Shared API/data-contract changes, cross-domain conflict, architecture/schedule/cost tradeoffs | Tier 2 presents options, effects and recommendation; **Tech Lead** resolves within delegation |
| Undelegated goals/acceptance criteria, budget limits, publication/deployment authority or hard-to-reverse external effects | **User** receives options and impact; affected execution remains PENDING until required authorization |
| Required QA, independent security or applicable compliance failure/missing evidence, or agreed stop trigger | Affected execution BLOCKED; resolve/review or obtain explicit resumption from the existing authority |

Consult peers without binding changes outside your domain. Escalate within-domain conflict to Tier 2 and Tier 2 conflicts to Tech Lead. Tech Lead assigns missing owners. An unavailable Tech Lead without a designated deputy leaves upper-level decisions PENDING. Disclose material self-interest or missing expertise and escalate to an appropriate reviewer/user.

## 3. Evidence, dissent and accountable decision

1. Share a versioned question, scope, 2–3 alternatives (current/proposed for simple tasks), verification evidence, cost/risk and rollback. Separate facts, hypotheses and unknowns.
2. Consult relevant roles and review one rebuttal, including Rookie counterexamples on their merits. Do not discard dissent without reasons or infer absent consent. Extra rounds need new evidence and expected value.
3. Explain the selection through correctness, user value, simplicity, maintainability, testability, cost and reversibility. A decision against majority advice must explain rejected objections and reconsideration triggers. Insufficient evidence is **PENDING**; mandatory blockers are **BLOCKED**. Seniority does not establish facts or waive blockers.
4. **15 ballots / 8 votes are advisory when requested**. Eight votes do not automatically adopt, authorize execution or permit merge. Seven supporters and eight missing ballots do not block an authorized domain owner with sufficient evidence. Record only received ballots; counts do not prove safety or truth.
5. Accept **user reconsideration/revote requests** immediately without team permission. Version the proposal, record grounds and pause unexecuted follow-ups. Preserve prior decisions/dissent; do not carry old ballots into fresh advice. The accountable owner reassesses; the user resolves appeals against Tech Lead decisions. Follow a user-specified outcome within its scope while preserving mandatory gates and tool permissions.

## 4. Separate selection from execution

`DECIDED` means the accountable owner selected an alternative, `PENDING` means evidence/required authorization is missing, and `BLOCKED` means a mandatory gate/stop prevents execution. A DECIDED selection can still have BLOCKED execution. Separately verify current-head/base independent security PASS, functional QA, resolution of applicable compliance violations and existing deployment gates. This contract does not configure GitHub protections or host permissions.

For explicit user delegation, record **task, duration, decision scope, budget/authority limits and end condition**. A delegation limited to this process expires on completion/cancellation and never carries into the next project. Silence is neither approval nor resumption. Do not repeatedly ask routine in-scope decisions; preserve user requirements and mandatory security/compliance/stop contracts. This contract alone cannot waive kickoff questions. Generic decision delegation does not substitute for direct kickoff questions/agreement or resumption after a stop. If a separate explicit user instruction changes an existing procedure for this task, record its exact wording, scope and expiry; never represent Lead judgment as user answers. Existing kickoff questions apply to future projects.

## 5. Required decision record

```text
proposal ID/version, scope, affected domains, reversibility:
owner/tier, actual actor/combined roles, delegation evidence and validity:
alternatives, verified evidence, hypotheses/unknowns, cost/risk, rollback:
consulted roles, dissent, accepted/rejected reasons, absent input/gaps:
selection/rationale, verdict (DECIDED/PENDING/BLOCKED):
execution readiness (READY/PENDING/BLOCKED), QA/security/compliance, required authorization:
executor, verification criteria, reconsideration/stop triggers:
user appeal, prior decision, delegation expiry:
```

Use brief fields in existing task records for small decisions. No mandatory organization-wide meeting or agent recalls.

## 6. Sources and limits

Checked 2026-11-04: [Claude Code Game Studios README](https://github.com/Donchitos/Claude-Code-Game-Studios/blob/05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418/README.md), [technical director](https://github.com/Donchitos/Claude-Code-Game-Studios/blob/05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418/.claude/agents/technical-director.md), [top-level configuration](https://github.com/Donchitos/Claude-Code-Game-Studios/blob/05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418/CLAUDE.md). Independently adapt vertical delegation, horizontal consultation and upward conflict resolution to existing roles. Do not import game roles, model assignments or per-write approval procedures. Tiers do not guarantee better decisions or lower cost; measure actual outcomes per case.
