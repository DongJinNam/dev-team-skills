# Claude Code

The Claude CLI was unavailable: installation and invocation are **NOT_RUN**.
Check `claude --version` and `claude plugin --help` before using these commands.
Reviewing the [official manifest documentation](https://code.claude.com/docs/en/plugins-reference)
does not verify this package in use.

## Option A: Add Marketplace Catalog

```bash
# 1. Add repository as a Claude Code marketplace
/plugin marketplace add DongJinNam/dev-team-skills

# 2. Install dev-team-skills plugin
/plugin install dev-team-skills@dev-team-skills-marketplace
```

> **Via CLI directly**:
> ```bash
> claude plugin marketplace add DongJinNam/dev-team-skills
> claude plugin install dev-team-skills@dev-team-skills-marketplace
> ```

## Option B: Validate Plugin Locally

```bash
claude plugin validate .
```

## Option C: Project Memory Integration

- Place `CLAUDE.md` in your project root to load the constitution, and call skills from `skills/`.
