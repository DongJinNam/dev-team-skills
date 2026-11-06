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


## Tiered decision review
- Proposal/version / scope / affected domains / reversibility:
- Accountable owner/tier / delegation evidence and expiry / actual actor and combined roles:
- Alternatives / evidence / dissent / accepted or rejected reasons / reconsideration triggers:
- Selection verdict (DECIDED/PENDING/BLOCKED) / execution readiness and remaining gates:
- Advisory ballots if requested (received YES/NO/missing; never automatic adoption):
- User appeal / paused follow-ups / reassessment and prior history (or N/A):
- [ ] Domain decisions use the relevant Tier 2; shared-contract/cross-domain conflicts go to Tech Lead; undelegated changes go to the user.
- [ ] Neither seniority nor votes waive required QA, independent security, compliance or explicit resumption.
- [ ] Process-limited delegation is not reused for another project; user appeals are accepted without team permission.

## Quality Lead Review (Test Engineer / QA)
- Mandatory pre-project questions / user answers and confirmation evidence / agreement status (PENDING/AGREED):
- Expected benefit (hypothesis) / quantifiability / metric, baseline, target, method and period or alternative verification:
- Stop triggers, thresholds and scope / human recipient and resume authority / stop, report and resume record (or not triggered):
- Reviewer / clear and measurable AC / feature-test-evidence matrix:
- Missing-test recommendations (scenario, expected result, layer/technique, priority, owner, acceptance evidence):
- QA/developer dispositions / follow-up / unverified AC or reasoned N/A:


## External tool use (if relevant)

- Problem/AC, candidate/source/revision or check date, owner:
- State, actual method/command, artifact/log, result and limits:
- Existing alternative, decision/reason, cost status, recheck trigger:
- Otherwise: N/A with reason. See the [contract](../skills/engineering-squad/references/tool-adoption_en.md).
