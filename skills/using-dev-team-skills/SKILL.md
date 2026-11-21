---
name: using-dev-team-skills
description: Route plain-language build, fix, review, verify, or ship requests (EN/KR) to the six-owner engineering squad contract.
metadata:
  author: DongJinNam
  version: "1.2.0"
  tags: ["entry-point", "routing"]
---

# Using dev-team-skills

## Purpose

Route plain-language engineering requests to the six-owner squad contract when no explicit skill or slash command was named, preventing ad-hoc workflows.

## Prerequisites

- Sibling `engineering-squad` and `code-review` skills installed under `skills/`
- Optional host `SessionStart` / `Stop` hooks configured via [hooks/hooks.json](../../hooks/hooks.json)

Entry point. Read this skill when a plain-language engineering request
arrives and no skill was named. It routes the request to the squad
contract instead of letting the agent improvise a workflow.

## Trigger phrases

Any of these, in English or Korean, means this skill applies:

- "fix this bug", "이 버그 고쳐줘", "버그 수정해줘"
- "build this feature", "이 기능 만들어줘", "기능 추가해줘"
- "review this code", "이 코드 리뷰해줘"
- "check that the package is intact", "검증해줘", "하네스 돌려줘"
- "ship it", "배포해줘", "머지해줘"

A named skill (`engineering-squad`, `code-review`, a slash command)
takes precedence over this entry skill. Do not re-route a request the
user already aimed at a specific skill.

## Entry procedure

1. **Read the squad contract.** Open
   [engineering-squad](../engineering-squad/SKILL.md) and follow its
   Step 0 kickoff: the two start questions (expected effect with a
   number, stop conditions and who to tell). If the request is clear,
   state the assumptions and go straight to implementation (0-turn
   Adaptive Kickoff). If it is vague or unagreed, ask and hold
   PENDING. Never invent the answers.
2. **Route by workflow, not by role count.**
   - New feature or fix → the squad flow (`/dev-team-skills:squad`,
     [commands/squad.md](../../commands/squad.md)).
   - Review only → [code-review](../code-review/SKILL.md)
     (`/dev-team-skills:review`). The reviewer must differ from the
     implementer.
   - Verify only → the harness and unit tests
     (`/dev-team-skills:verify`). Report actual results, never a
     claimed pass.
   - Ship or merge → the delivery gate plus an independent security
     PASS on the current head (`/dev-team-skills:ship`). No PASS, no
     merge.
3. **Do not claim what did not run.** Auto-invocation happens only
   through the SessionStart hook ([hooks/hooks.json](../../hooks/hooks.json))
   or an explicit slash command. If neither fired, say the entry was
   manual. A hook that never ran is NOT_RUN, not a success.

## What this skill is not

- It is not a seventh owner. The six owners in
  [engineering-squad](../engineering-squad/SKILL.md) still do the work.
- It is not a shortcut past Step 0. Skipping the kickoff questions to
  save a turn is a contract violation, not efficiency.
- It does not replace the Stop gate. The hook in
  [hooks/hooks.json](../../hooks/hooks.json) still blocks a stop when
  `verify-harness` fails.

## Examples

```text
User: "이 버그 고쳐줘"
Route: engineering-squad -> Step 0 kickoff -> scoped fix -> verify -> independent security PASS
```

## Limitations

- Requires host hook support for automatic invocation; without hooks, entry is manual and must be reported as `NOT_RUN` for hook execution.
- Does not grant merge or deployment authority by itself.

## Troubleshooting

| Error / Symptom | Cause | Solution |
| --- | --- | --- |
| Entry skill did not auto-trigger | Host does not execute `SessionStart` hooks | Invoke `/dev-team-skills:squad` manually and report hook status as `NOT_RUN` |
| Stop hook blocks completion | `verify-harness` failed on package or link checks | Fix the reported harness error and re-run `scripts/verify-harness.py` |
