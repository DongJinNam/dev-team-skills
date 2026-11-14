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

Full install (all 8 skills) is the default when `--skill` is omitted:

```bash
npx skills add DongJinNam/dev-team-skills
```

## What a single install contains

In the repository layout, `engineering-squad` is self-contained:
`skills/engineering-squad/SKILL.md` (and `SKILL_en.md`) link only to files under
`skills/engineering-squad/references/`. The one exception is a single link in
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

## Measured install behavior (2026-11-14, Node v24.22.1)

The CLI resolves `--skill engineering-squad` to `skills/SKILL.md`, the
compatibility entry whose frontmatter name is also `engineering-squad`
(`skills-lock.json` records `"skillPath": "skills/SKILL.md"`). It then installs
the whole `skills/` directory as `.agents/skills/engineering-squad/`, with the
real skill nested one level deeper at
`.agents/skills/engineering-squad/engineering-squad/`. The installed tree is
byte-identical to the repository `skills/` directory (verified with `diff -r`).

Consequences, all measured:

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

- Full install (`npx skills add DongJinNam/dev-team-skills -y`, 2026-11-14):
  exit 0, "Installation complete". 8 skills installed to
  `./.agents/skills/<name>` (universal: Codex, Amp, Cline, Cursor, Deep Agents
  +15 more) with symlinks to `./.claude/skills/<name>`, plus `skills-lock.json`.
  The same `engineering-squad` nesting defect as above applies.
  Without `-y` the CLI stops at an interactive multi-select prompt
  ("Select skills to install") and waits for input; in a non-interactive shell
  it hung until the 300 s timeout. `npx -y` alone does not answer it — the
  `-y`/`--yes` flag must go to the `skills` command itself.
- `npx skills add DongJinNam/dev-team-skills --list` exits 0 and lists all 8 skills.
- skills.sh lists repositories automatically from install telemetry; there is no
  separate submission form. A successful `npx skills add` from a telemetry-enabled
  environment is the trigger, and the directory page can lag about a day.
  As of 2026-11-14 the skills.sh search API returns 0 hits for this repository
  (`https://skills.sh/api/search?q=dev-team-skills`).
