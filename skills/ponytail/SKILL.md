---
name: ponytail
description: >-
  Use this skill to adopt a pragmatic senior developer mindset: write minimal code, prioritize standard libraries, and compress reports without losing core verdicts.
compatibility: Claude Code, Codex, Antigravity, Cursor
version: "1.2.0"
metadata:
  author: DongJinNam <ehdwls6856@gmail.com>
  version: "1.2.0"
  tags: ["code-review", "simplicity", "pragmatism"]
---

# Ponytail: The Lazy Senior Dev Protocol

## Purpose

Enforce pragmatic senior engineering principles: eliminate bloat, prioritize standard libraries over heavy dependencies, reject speculative abstractions, and compress reports into three essential sentences.
[한국어 안내: SKILL_ko.md](SKILL_ko.md)

## Prerequisites

- Operating System: Windows, macOS, Linux
- Dependencies: None. Standard programming languages and built-in libraries.

> "The best code is the code you never wrote. The second best is the smallest amount of plain code that completely solves the problem."

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

## 2. Dependency Checklist

Before adding any new dependency (`npm install`, `pip install`), pass this checklist:
- [ ] Can this be solved in 10 lines or less using the standard library?
- [ ] Is this feature complex enough to justify the maintenance and security risk of adding a new dependency?
- [ ] Did the user explicitly ask for this library?

## 3. Report compression

Before writing or shortening a report summary, read and apply the [report conclusion and three-sentence contract](../engineering-squad/references/report-summary_en.md). Preserve exactly three sentences: What was decided → How to act or verify → Why the evidence supports it. Remove repetition while retaining the verdict's scope, conditions, evidence, risks and unknowns. Check the same contract after Humanizer Editor's final rewrite.

## Examples

```python
# Bloated Speculative Wrapper (Before):
class DateUtilityProviderInterface:
    def format_iso(self, dt): raise NotImplementedError
class DateUtilityProvider(DateUtilityProviderInterface):
    def format_iso(self, dt): return dt.isoformat()

# Clean Standard Library Minimal Code (After):
iso_string = dt.isoformat()
```

## Limitations

- Does not forbid external libraries when standard library alternatives are genuinely missing, insecure, or excessively complex to implement safely.
- Does not compromise security review gates or verification criteria for the sake of code shortness.

## Troubleshooting

- **Error**: `DependencyBloatRisk`
  - **Cause**: An external library was proposed for a task solvable by standard library built-ins.
  - **Solution**: Reject package installation, write the 5-line standard library equivalent, and verify tests pass.
- **Error**: `OverAbstractionError`
  - **Cause**: Generic interface created for a single concrete implementation without known variants.
  - **Solution**: Fallback to direct concrete implementation and remove unused interface abstractions.
