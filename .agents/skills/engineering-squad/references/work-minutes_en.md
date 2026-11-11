# Work Minutes Contract

This record exists so the person who delegated the work does not have to ask later how it proceeded or why it was done that way. Write one file per task at `docs/worklogs/YYYY-MM-DD-<task-slug>.md` in the target repo. The minutes invent no new record format. They bind records that already exist separately — the kickoff agreement, [decision records](./decision-governance_en.md), verification records and cost records — into one index per task.

## 1. Timing and ownership

- Tech Lead writes the minutes once, when the task ends or stops under an agreed stop condition. Stopped tasks are recorded too.
- Each role row is copied from that role's outputs and handoff records. Do not create new facts in the minutes; mark anything unverified as unverified.
- Inactive roles get no row. Combined duties are marked as combined.

## 2. Format

The summary at the top follows the [three-sentence summary contract](./report-summary_en.md) unchanged. The body uses fixed fields only, so a human reader and an agent parser read the same table.

```markdown
# Work minutes: <task name>

<What/How/Why in three sentences>
Verdict: complete | stopped | incomplete

## Meta
- Task ID/date:
- Request source:
- Base revision: base <sha> / head <sha>
- Kickoff agreement: <record link or AGREED/PENDING>

## Per-role record
| Role | Actual assignee/combined | What was done | Why (evidence, rejected alternatives) | Output/evidence path | Status |
| --- | --- | --- | --- | --- | --- |
| Tech Lead |  |  |  |  | complete/not run/N/A (reason) |

## Decision index
- <decision record link> — do not copy the body

## Verification summary
- AC -> test -> actual result: <evidence path>

## Cost
- Added calls and cost: link the Lead record, separating measured/estimated/unknown

## Open items and next
- Open items:
- Next action/owner:
- Resume/revisit conditions:
```

## 3. Writing rules

- Do not paste full conversations or long execution logs. Link evidence by path. The minutes must not become a source of context bloat.
- Decision, verification and cost bodies stay in their original records; the minutes hold only links and one-line summaries. Writing the same fact in two places makes them drift.
- Status values distinguish complete, not run, and N/A (with reason). Never write not run as complete.
- Security verdicts and compliance status are copied from the original records unchanged. The minutes never change a verdict.

## 4. Size tiers

| Observed condition | Format |
| --- | --- |
| Documentation/local edit without external behavior or trust-boundary changes | Short form: three-sentence summary + verdict + per-role table only, within 10 lines |
| User feature, API or agent-behavior change; product or deployment change | Full format |

The tier boundary matches the task-size activation table in SKILL_en.md. If writing the minutes grows larger than the work, drop to the short form.

## 5. Pilot and revisit

No measured effect exists yet. After applying this contract to three real tasks, record the following and revisit whether to keep, shrink or remove it.

- Whether the user understood the progress and decision reasons from the minutes alone (follow-up questions asked or not)
- The cost of writing the minutes (line count and the Lead's measured/estimated cost record)
- Whether a third agent, reading only the minutes, can state the open items and resume conditions accurately

This pilot stays out of the nineteen pressure-scenario scores. Keep it as a separate supplemental record.

## 6. Adoption basis and limits

Checked 2026-11-11: the [agent handoff (HANDOFF.md) practice](http://umatechnology.org/how-to-hand-off-a-coding-project-between-ai-coding-assistants-without-losing-context/) uses objective, done/not-done separation, decisions with evidence, exact work state and next action as fields. The session log in [SYNTAX Methods Note v1.0](https://www.qntxlabs.com/research/syntax-methods-note-v1.0.pdf) carries objective, actions, evidence, corrections, tests, costs and unresolved risks, and defines itself as a compact handoff record, not a transcript dump. [Agent run-log practice](https://dev.to/web4browser/what-ai-browser-agents-should-log-after-every-run-ikg) records evidence instead of confident summaries. The three sources' fields overlap with this repo's existing record fields, so this is adopted as a per-task binding of existing records, not a new concept. No claim that minutes improve comprehension or speed is made before the pilot measures it.
