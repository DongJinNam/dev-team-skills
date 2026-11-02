# Combined workflow ownership implementation plan

> **For agentic workers:** Implement inline with test-first verification and an independent final review.

**Goal:** Define one owner per overlapping phase, reuse valid artifacts, and preserve dev-team gates when Superpowers is present.

**Spec:** User requested the third researched improvement after fetching latest main. Base 071242f9a609524b0d1a673def39c9686991468a includes PR #14.

**Architecture:** Add a bilingual compatibility reference linked from squad/root/planning/review entry points. No plugin auto-install, runtime dispatcher or renaming of existing skills. Test three additional decision situations using the existing scorer, and collect a fresh nine-case baseline because policy/scorer snapshots change.

## Constraints and review focus
- Host instructions and explicit user scope remain authoritative; integration cannot grant permissions or waive mandatory gates.
- Confirmed kickoff questions remain mandatory; reuse the current kickoff's evidence, not unconfirmed historical answers.
- Record COMBINED/STANDALONE mode, verified package-qualified skill identity, phase owners, scope/artifact IDs and approval evidence.
- Reuse unchanged approved artifacts; scope/trust-boundary changes need affected delta confirmation and fresh review.
- Missing optional Superpowers permits explicit dev-team fallback; a higher-priority mandatory missing prerequisite remains BLOCKED.
- Preserve 15/8 voting, user-grounded revote, independent head-bound security, compliance and stop/resume contracts.
- Never report an external skill as invoked unless actually available/read/invoked; no new performance percentages.
- Old baseline stays historical/STALE; fresh nine-case native samples plus separate meaning review are required.

## Tasks
- [x] Fetch main, inspect overlapping entry points and run a before-reference application check.
- [x] Add reuse/fallback/scope-change scorer tests, observe failures before implementation.
- [x] Add owner/reuse/conflict contract and qualified references in both languages.
- [x] Collect fresh nine-case outputs without expected-answer leakage, independently review and bind hashes.
- [ ] Run full tests, package checks, both shell replays and hosted OS matrix.
- [ ] Independently review final diff/security, publish branch and PR without merging.

Before-reference observation: an agent correctly proposed reusing S1/P1/K1 but found owner_contract=null and planning_owner=UNDEFINED. This is evidence of an absent explicit repository contract, not evidence that the old policy always causes repeated work or that the new text improves model reliability.

Verification so far: scorer tests first failed 6 assertions for unsupported new actions; all 38 unittest methods then passed. New native samples (one per case) pass 9 structural and independent meaning checks; old six-case record returns STALE. No token/time savings or model reliability estimate claimed.
