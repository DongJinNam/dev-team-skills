# Cross-platform harness validation implementation plan

> **For agentic workers:** Use superpowers:executing-plans; implement inline and request one independent final review.

**Goal:** Bash and PowerShell reject the same malformed package inputs and accept the same valid inputs.

**Architecture:** Both entry points delegate to one Python 3.10+ validator. Use Python's JSON parser and PyYAML SafeLoader; a handwritten YAML parser would add unnecessary complexity. Preserve rule-file SHA-256 synchronization and existing command names.

**Spec:** The user approved the first improvement from the comparison research: shared normal/error inputs, matching cross-platform verdicts, and explicit limits on what package validation proves.

## Global constraints

- Scope: package manifests, skill frontmatter, rule synchronization, regression tests and CI; no role/voting/security-policy changes.
- JSON objects require nonblank string name/description; marketplace plugins must be an array of objects. Reject malformed syntax and duplicate keys.
- Skills require a leading, closed YAML frontmatter block with nonblank string name/description. Accept folded descriptions, BOM and CRLF; use safe YAML loading.
- Preserve exit 0 for valid packages and nonzero for invalid packages or unavailable prerequisites.
- A package PASS does not imply agent-behavior validation, installation compatibility or security approval.
- Stop/report if satisfying these criteria requires changing existing security gates or production credentials; no merge is authorized.

## Review focus

- Valid input must pass, so a validator rejecting everything cannot satisfy the tests.
- Missing runtime/parser must fail clearly rather than silently skipping validation.
- Paths with spaces and non-ASCII text must survive both launchers.
- Partially missing English rule sets and byte mismatches must fail.
- Unsafe YAML tags and wrong JSON/YAML field types must be rejected.

### Task 1: Shared package validator and launcher parity

**Files:** `scripts/verify-harness.py`, existing `.sh`/`.ps1`, `scripts/requirements-harness.txt`, `tests/test_harness.py`, verification workflow and both README files.

**Interfaces:** launchers forward arguments and exit status to `verify-harness.py`; tests invoke the real launcher against isolated fixture repositories. `HARNESS_LAUNCHER=bash|pwsh|python` selects the entry point and must not silently skip a missing selected shell.

- [x] Write subprocess regression tests and run them against the original scripts; original Bash produced 38 failing assertions across 20 test methods.
- [x] Implement the shared validator and thin launchers; pin PyYAML and document the prerequisite.
- [x] Run the full test suite and repository verification; 22 test methods pass through Bash, PowerShell 7.4.6 and direct Python on Linux.
- [ ] Run the same suite in CI on Linux, Windows and macOS with both shell entry points.
- [ ] Review the final diff independently, commit, push a feature branch and open a PR with evidence and remaining limitations.
