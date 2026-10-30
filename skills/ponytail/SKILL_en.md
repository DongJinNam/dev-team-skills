---
name: ponytail
description: >-
  Use this skill to adopt the mindset of the laziest, pragmatically brilliant senior dev: "The best code is the code you never wrote." Enforces standard library first, zero unnecessary dependencies, and radical minimalism.
---

# Ponytail: The Lazy Senior Dev Protocol

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
