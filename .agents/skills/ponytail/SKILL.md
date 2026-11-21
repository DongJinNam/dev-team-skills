---
name: ponytail
description: Apply minimum-code, standard-library-first engineering and compress report conclusions without losing verdicts, evidence, or risks.
compatibility: Claude Code, Codex, Antigravity, Cursor
metadata:
  author: DongJinNam
  version: "1.2.0"
  tags: ["code-review", "simplicity"]
---

# Ponytail: The Lazy Senior Dev Protocol

## Purpose

Prevent over-engineering, unnecessary third-party dependencies, and verbose report conclusions by enforcing standard-library-first code and lossless compression.

## Prerequisites

- Access to the target codebase or draft report and [report-summary.md](../engineering-squad/references/report-summary.md) for summary checks

> "The best code is the code you never wrote. The second best is the smallest amount of plain code that completely solves the problem."

This skill adopts the `ponytail` mindset. It blocks common bad habits in AI agents: **adding heavy third-party packages, making useless wrapper functions, and creating premature abstractions**.

---

## 1. Core Rules

1. **Standard Library First**:
   - Before running `npm install`, `pip install`, or `go get`, check if the standard library can do it (e.g. Node.js built-in `fetch`/`fs`, Python `urllib`/`dataclasses`, Go standard library).
   - Never add an external package for trivial tasks (date formatting, UUID generation, simple string checks).

2. **Native Platform Features**:
   - In frontend code, look at native HTML5 & CSS features (`<dialog>`, `<input type="date">`, Flexbox/Grid) before installing heavy UI packages.

3. **No Speculative Wrappers**:
   - Don't write one-line wrapper functions or abstract interfaces when code is only used in a single place.

4. **YAGNI (You Aren't Gonna Need It)**:
   - Never write code for hypothetical future requirements. Solve today's problem cleanly.

---

## 2. Dependency Checklist

Before adding any new dependency (`npm install`, `pip install`), pass this checklist:
- [ ] Can this be solved in 10 lines or less using the standard library?
- [ ] Is this feature complex enough to justify the maintenance and security risk of adding a new dependency?
- [ ] Did the user explicitly ask for this library?


## 3. Report compression

Before writing or shortening a report summary, read and apply the [report conclusion and three-sentence contract](../engineering-squad/references/report-summary.md). Preserve exactly three sentences: What was decided → How to act or verify → Why the evidence supports it. Remove repetition while retaining the verdict's scope, conditions, evidence, risks and unknowns. Check the same contract after Humanizer Editor's final rewrite.

## Examples

```python
# Prefer standard library over adding a package for a one-line check
import uuid
request_id = str(uuid.uuid4())
```

## Limitations

- Simplicity must never bypass required error handling, input validation, security checks, or explicit user-requested libraries.
- Report compression removes repetition only; it cannot drop `BLOCKED`/`PENDING` states, conditions, or unverified risks.

## Troubleshooting

| Error / Symptom | Cause | Solution |
| --- | --- | --- |
| Summary dropped a risk or condition | Over-aggressive shortening | Re-check against the source facts and restore the exact 3-sentence What/How/Why contract |
| Standard library cannot cover crypto/parsing edge cases | Complex security or protocol requirement | Document the failure/risk and adopt a vetted, minimal dependency with explicit user approval |
