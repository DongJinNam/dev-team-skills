<!-- Based on Kakao Pay Tech Blog: 'Slow PR, Fast Dev' (https://tech.kakaopay.com/post/kakaopayins-slow-pr-fast-dev/) -->

# What problem does this PR solve?
<!-- Clearly describe the current situation, the bug, or the feature request. -->

# Why do we need this?
<!-- Explain why this work is important right now (business value or technical reason). -->

# How was it solved?
<!-- Briefly explain your solution and main changes (patterns, architecture, libraries). -->

# Limitations & Trade-offs
<!-- Be honest about what is not fully solved, technical compromises (e.g., speed vs. simplicity), or leftover technical debt. -->

# Impact on Existing Features
<!-- Does this break anything? How does this affect other services, modules, or database schemas? -->

# Edge Cases & Failure Scenarios
<!-- What corner cases did you consider (e.g. network timeout, bad input, concurrency), and how do we handle them? -->

# Alternatives Considered & Reason for Choice
<!-- What other options did you think about, and why did you pick this one? -->

# Review Points (Risk Level by File/Area 🔴🟡🟢)
<!-- Mark files that need special attention and their risk level.
🔴 Must Fix (High Risk / Breaking Change / Core Logic)
🟡 Review Needed (Medium Risk / Interface Change / Performance Impact)
🟢 Suggestion (Low Risk / Minor UI / Style / Documentation)
-->

| Risk | File / Area | Review Request |
| :---: | :--- | :--- |
| 🔴 | `path/to/file` | Check business logic and error handling |
| 🟡 | `path/to/file` | Check query index and performance impact |
| 🟢 | `path/to/file` | Check component names and UI responsiveness |

---

## 🛠️ Author Self-Verification Checklist
- [ ] Ran local health check script (`verify-health.ps1` or `verify-health.sh`) and it passed.
- [ ] Cleaned up temporary files and debug logs.
- [ ] Checked `git diff` to make sure there are no unintended changes.


## Required Security Review — Merge Gate

Do not merge until an independent Security Review Engineer has issued PASS for the latest PR head. Author-ticked checkboxes, QA and green CI do not replace the report. New commits or changed merge inputs require re-review.

- Reviewer (separate from author/implementer):
- Reviewed PR head SHA / target base SHA:
- Review date / report link / current-advisory evidence:
- Disposition: PENDING
<!-- Update to PASS or BLOCKED only after independent review. -->
- [ ] Independent security PASS matches the latest head and merge inputs.
- [ ] Required evidence is complete and no unresolved merge blockers remain.


## Compliance Review
- Reviewer / applicable Korean or U.S. IT requirements / official sources:
- Findings and actions, or N/A rationale:
- Disposition: PENDING
<!-- Use PASS / BLOCKED / N/A with evidence after reviewing applicability. -->


## Decision ballots
- Proposal/version / decision-log link (all 14 roles, owners, YES/NO and reasons):
- YES / NO / missing / outcome / minority views and reconsideration triggers:
- SNS ideas, evidence and small experiment, or N/A rationale:
- [ ] Each decision discussion includes 13 specialists + Lead, including inactive roles: one vote each, all 14 collected, at least 8 YES to adopt. Changes without a decision discussion have a reasoned N/A.
- [ ] Ties/nonresponse defer; voting did not waive security/compliance blockers.
