---
name: using-dev-team-skills
description: >-
  Use when the user requests building, fixing, reviewing, verifying, or shipping code without naming a skill. Routes plain requests to the six-owner engineering squad.
version: "1.2.0"
metadata:
  author: DongJinNam <ehdwls6856@gmail.com>
  version: "1.2.0"
  tags: ["entry-point", "routing", "squad"]
---

# Using dev-team-skills

## Purpose

Entry point for plain-language engineering requests. Routes ambiguous user requests directly to the six-owner engineering squad contract instead of letting the agent improvise a workflow.
[한국어 안내: SKILL_ko.md](SKILL_ko.md)

## Prerequisites

- Operating System: Windows, macOS, Linux
- Dependencies: None. Standard dev-team-skills environment.

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

## Examples

```bash
# Plain language requests routed by this skill:
"이 버그 고쳐줘" -> Routes to engineering-squad kickoff (/dev-team-skills:squad)
"review this PR" -> Routes to code-review (/dev-team-skills:review)
"verify package intact" -> Runs verify-harness.py (/dev-team-skills:verify)
```

## Limitations

- It is not a seventh owner. The six owners in [engineering-squad](../engineering-squad/SKILL.md) still do the work.
- It is not a shortcut past Step 0. Skipping the kickoff questions to save a turn is a contract violation.
- It does not replace the Stop gate. The hook in [hooks/hooks.json](../../hooks/hooks.json) still blocks a stop when `verify-harness` fails.

## Troubleshooting

- **Error**: `RoutingAmbiguityError`
  - **Cause**: User request does not match standard trigger phrases or overlaps multiple scopes.
  - **Solution**: Fallback to Step 0 kickoff questions to clarify user intent before delegating to owners.
- **Error**: `HookExecutionSkipped`
  - **Cause**: SessionStart hook did not trigger automatically.
  - **Solution**: Explicitly invoke `/dev-team-skills:squad` command or enter manually without claiming unexecuted hooks.
