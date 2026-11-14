# OpenAI Codex

Codex CLI `0.167.0` provides `plugin add`. The previous `plugin install` fails with
`unrecognized subcommand`. Check `codex plugin --help` for other versions.

## Option A: Install a local checkout

Run from the repository root. Use the same commands in PowerShell and Bash; local
testing was performed on Windows.

```bash
codex plugin marketplace add .
codex plugin add dev-team-skills@dev-team-skills-marketplace
codex plugin list --json
```

For remote registration, replace the first command with
`codex plugin marketplace add DongJinNam/dev-team-skills --ref main`. Only the local
path was tested here. Inspect `codex plugin marketplace --help` for version-specific
update commands for existing installations.

## Option B: Interactive Plugin Manager

- In Codex CLI, type `/plugins` to open the interactive manager, search for
  `dev-team-skills`, and enable it.

## Option C: Project Agent Instructions

- Use `AGENTS.md` for project instructions. Copying `CODEX.md` alone does not establish
  that skills are installed. Review and merge needed rules without overwriting existing
  project instructions.
- Start a new session, inspect the actual skill list and source, and explicitly select
  `engineering-squad` for a small task. Record the loaded `SKILL.md` path, test results
  and additional guidance count before calling the whole workflow successful. Model
  invocation was not tested here. See the [official skills guide](https://learn.chatgpt.com/docs/build-skills)
  and [plugin packaging guide](https://developers.openai.com/plugins/build/plugins).
