# Single-skill install

Install only one skill instead of the whole repository. The supported single-skill
target is `engineering-squad`.

## Install

```bash
# Preview what the CLI sees in this repository first
npx skills add DongJinNam/dev-team-skills --list

# Install engineering-squad only
npx skills add DongJinNam/dev-team-skills --skill engineering-squad
```

Full install (all 9 skills) is the default when `--skill` is omitted:

```bash
npx skills add DongJinNam/dev-team-skills
```

## What a single install contains

In the repository layout, `engineering-squad` is self-contained:
`skills/engineering-squad/SKILL.md` links only to files under
`skills/engineering-squad/references/` (Korean translations live outside
`skills/` under `docs/i18n/ko/skills/` so SkillEvaluator Tier 2 stays
monolingual). The one exception is a single link in
`references/tool-adoption.md` to `evals/token-efficiency.md`, which lives outside
the skill folder and is not copied. Token comparisons that cite that file are
UNMEASURED without it; everything else in the skill still applies.

Two more limits of a single install:

- The Humanizer Editor step in `references/roles.md` names the sibling skills
  `skills/humanizer` and `skills/humanizer-kr`. They are not installed with
  `engineering-squad` alone. The contract already covers this: if the files cannot
  be read, do not claim they were applied; say so and apply the plain-language
  rules in that section directly.
- The other skills are not self-contained. `brainstorming`, `code-review`,
  `ponytail`, and `harness-engineering` link to
  `../engineering-squad/references/*`. Installing any of them alone leaves those
  links broken. Install `engineering-squad` alongside them, or install the full
  repository.

## Measured install behavior (2026-11-15, Node v24.22.1)

Re-measured after this PR (P0-3 removed `skills/SKILL.md`; the
compatibility entry now lives at `.compat/skills/SKILL.md`). The branch
was not pushed yet, so the install ran from the local worktree path
instead of the remote name:

```bash
npx skills add /path/to/dev-team-skills --skill engineering-squad -y
```

- Exit 0, "Installation complete". 1 skill installed to
  `./.agents/skills/engineering-squad/` (universal: Codex, Amp, Cline,
  Cursor, Deep Agents +15 more) with a symlink at
  `./.claude/skills/engineering-squad`.
- The installed tree is flat and byte-identical to the repository
  `skills/engineering-squad/` (verified with `diff -r`). The nesting
  defect measured 2026-11-14 is gone: no extra `engineering-squad/`
  level, and the top-level `SKILL.md` is the real skill.
- Every relative link in the installed `SKILL.md`, `SKILL_ko.md`, and
  `references/` resolves inside the installed folder, including the
  `roles.md` kickoff-contract anchor. The one exception is the
  already-known link in `references/tool-adoption.md` to
  `../../../evals/token-efficiency.md`, which lives outside the skill
  folder and is not copied. Token comparisons that cite that file are
  UNMEASURED without it.
- `skills-lock.json` records `"sourceType": "local"` with the worktree
  path; a remote install records the repository name instead.
  `npx skills list` shows `engineering-squad` with that source.
- Full install from the same worktree (`npx skills add
  /path/to/dev-team-skills -y`) also exits 0 and installs all 9 skills,
  each byte-identical to its repository folder. The shared
  `skills/references/` and `skills/scripts/` folders and
  `skills/catalog.json` are not installed (they are not skills).

Previous measurement (2026-11-14, remote main, before P0-3), kept as
the pre-fix record. The nesting defect below no longer applies to
this branch:

The CLI resolves `--skill engineering-squad` to `skills/SKILL.md`, the
compatibility entry whose frontmatter name is also `engineering-squad`
(`skills-lock.json` records `"skillPath": "skills/SKILL.md"`). It then installs
the whole `skills/` directory as `.agents/skills/engineering-squad/`, with the
real skill nested one level deeper at
`.agents/skills/engineering-squad/engineering-squad/`. The installed tree is
byte-identical to the repository `skills/` directory (verified with `diff -r`).

Consequences, all measured 2026-11-14:

- The installed top-level `SKILL.md` is the compatibility entry. Its link to
  `./engineering-squad/SKILL.md` does resolve to the nested real skill, so the
  squad itself still loads — through one extra hop.
- Other skills' `../engineering-squad/references/*` links do not resolve to the
  real contracts in the installed tree. That path holds only `roles.md` and
  `deployment-gate.md` from the shared `skills/references/`, which differ from
  the skill's own files; `security-review.md`, `superpowers-compatibility.md`,
  and the rest are missing there. Until P0-3 removes or relocates
  `skills/SKILL.md`, prefer the full install (`npx skills add
  DongJinNam/dev-team-skills` without `--skill`) and treat single-skill install
  as known-broken for cross-skill reference links. No file in this repository
  was changed to work around this; the fix belongs to P0-3.

## Verify after install

```bash
npx skills list
# Confirm engineering-squad is listed, then open its SKILL.md in the agent and
# check that references/decision-governance.md, references/roles.md, and
# references/security-review.md resolve inside the installed folder.
```

## Known state

- Full install (2026-11-15, local worktree path, Node v24.22.1):
  exit 0, "Installation complete". 9 skills installed to
  `./.agents/skills/<name>` (universal: Codex, Amp, Cline, Cursor, Deep Agents
  +15 more) with symlinks to `./.claude/skills/<name>`, plus `skills-lock.json`.
  Each installed skill folder is byte-identical to its repository folder;
  the `engineering-squad` nesting defect measured 2026-11-14 is gone.
  Without `-y` the CLI stops at an interactive multi-select prompt
  ("Select skills to install") and waits for input; in a non-interactive shell
  it hung until the 300 s timeout. `npx -y` alone does not answer it — the
  `-y`/`--yes` flag must go to the `skills` command itself.
  (2026-11-14, remote main: 8 skills, same nesting defect as the pre-fix
  record above.)
- `npx skills add <repo> --list` exits 0 and lists all 9 skills (2026-11-15,
  local worktree path; 8 skills on remote main 2026-11-14).
- skills.sh lists repositories automatically from install telemetry; there is no
  separate submission form. A successful `npx skills add` from a telemetry-enabled
  environment is the trigger, and the directory page can lag about a day.
  As of 2026-11-14 the skills.sh search API returns 0 hits for this repository
  (`https://skills.sh/api/search?q=dev-team-skills`).
