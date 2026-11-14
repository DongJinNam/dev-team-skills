# Contributing to dev-team-skills

Thank you for contributing. This repository is a six-owner AI engineering
squad: a small set of skills plus a deterministic harness that proves the
package is intact before an agent runs it. Keep contributions small,
evidence-based, and consistent with the existing contracts below.

## What belongs here

- A new skill under `skills/<name>/`, or an improvement to an existing one.
- Fixes to the harness, catalog builder, evals, or documentation.
- Decision records under `docs/decisions/` when a change needs its
  alternatives, objections, and re-decision conditions written down.

Do not add a new installation method or a new host adapter without
discussing it first: the repository already supports Claude Code, Codex,
Antigravity, and Cursor (experimental), and the goal is one line per host,
not more options.

## Adding a skill

1. Create `skills/<name>/SKILL.md`. The frontmatter `name` must match the
   folder name (invariant SKL-002), and `description` must be a nonblank
   string. Keep the file UTF-8 without BOM.
2. Add `skills/<name>/SKILL_en.md` with the English version. Both files
   are checked by the harness.
3. Keep relative links resolvable (SKL-003). Supporting material goes in
   `skills/<name>/references/`; shared references live in
   `skills/references/`.
4. If the skill adapts an external source, follow the adoption contract in
   `skills/engineering-squad/references/tool-adoption.md`: record the
   source as DISCOVERED / INSPECTED / AVAILABLE / APPLIED / VERIFIED with
   actual PASS/FAIL/NOT_RUN evidence. External references are candidates,
   not proof of use.
5. Regenerate the catalog (see below). Never edit `skills/catalog.json`
   by hand; it is derived from the skill folders.
6. If the change affects behavior the harness is supposed to catch, add or
   update a test under `tests/`.

The compatibility entry at `skills/SKILL.md` is not a separate skill and
is excluded from the catalog. Do not add a second skill with an existing
name.

## Regenerating the catalog

```bash
python3 scripts/build-catalog.py
```

This rewrites `skills/catalog.json` from the `skills/<name>/SKILL.md`
frontmatter on disk. The harness fails (CAT-001/CAT-002) when the
committed catalog has drifted from the folders, so run the builder and
commit the result whenever a skill is added, renamed, or its frontmatter
`name` or `description` changes.

## Verifying locally

Requires Python 3.10+ and PyYAML:

```bash
python -m pip install -r scripts/requirements-harness.txt
python3 -m unittest discover -s tests
./scripts/verify-harness.sh
```

`verify-harness.sh` (Windows: `.\scripts\verify-harness.ps1`) runs
`scripts/verify-harness.py`. It checks the JSON manifests, skill
frontmatter (including duplicate-key rejection), SHA-256 synchronization
across the five constitution files, the coded invariants SKL-001/002/003,
CAT-001/002, and the `.agents/skills` mirror (MIR-001, a dry-run check
that the committed mirror equals what the setup script materializes from
`skills/`). Exit codes: `0` package PASS, `1` invalid package,
`2` missing prerequisites or invalid arguments.

The harness validates local package structure only. It does not run a
fresh model, prove installation on a host, or replace the independent
security review.

Agent decision regressions live in `evals/`. To replay a recorded run:

```bash
python evals/run_evals.py --replay evals/runs/2026-11-08-main-merge.json
```

## Opening a pull request

- Use the pull request template (`.github/pull_request_template.md`,
  English version: `.github/pull_request_template_en.md`). Fill in the
  Mandate header: source, requester, strength, matched rules, policy
  version, origin, and scope. The Mandate fields are not edited after
  the fact; if the scope needs to widen, open a new PR.
- Answer the template's eight questions: problem, why now, how, limits
  and trade-offs, impact on existing behavior, edge cases and failure
  scenarios, alternatives considered, and review points per file with a
  risk level.
- Every PR needs an independent security PASS on the current head before
  merge. The author's own checks, QA, and CI passing do not substitute
  for it. A new commit or a change to the merge inputs requires a fresh
  review.
- CI runs the verify-rules-sync workflow
  (`.github/workflows/verify-rules-sync.yml`): unit tests and the harness
  on Linux, Windows, and macOS, through both the Bash and PowerShell
  entry points.
- Keep the diff scoped to the Mandate. Unrelated cleanups go in a
  separate PR.

## Reporting problems

- Bugs and proposals: open an issue with the matching template under
  `.github/ISSUE_TEMPLATE/` (`bug`, `skill-proposal`, or `adoption`).
- Security vulnerabilities: do not open a public issue. Follow
  `SECURITY.md`.
- Questions about whether a change fits: open an issue first rather than
  a large PR.

## Code of conduct

All contributors follow the `CODE_OF_CONDUCT.md` in this repository.
