# Security Policy

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability.

Report it privately through a
[GitHub Security Advisory](https://github.com/DongJinNam/dev-team-skills/security/advisories/new)
for this repository. If that route is unavailable, open a regular issue
only after removing every detail that would let someone else reproduce
the vulnerability, and state that the report is security-sensitive so a
maintainer can move it to a private channel.

Include, as far as you know them:

- What is affected (file, skill, script, or workflow) and the version or
  commit you tested.
- What an attacker can do with it, and what they need first (local
  access, a crafted file, a network response, and so on).
- Steps to reproduce, or a minimal proof of concept.
- Whether you have already disclosed it anywhere else.

There is no dedicated security contact email for this project, so no
email address is listed here. Do not invent one from a commit author
address: commit metadata is not a support channel.

## What happens next

- The report is triaged privately. You will hear back through the
  advisory thread.
- A fix is prepared privately, then released with a changelog entry that
  describes the impact without publishing exploit details first.
- Public disclosure follows the fix, not the report.

## Scope

This policy covers the contents of this repository: skills, harness
scripts, evals, workflows, and documentation. It does not cover the
security of the hosts the skills run on (Claude Code, Codex,
Antigravity, Cursor) or of third-party providers named in the skills;
report those to their own vendors.

## No scope for testing

Do not probe the maintainer's personal accounts, infrastructure, or any
deployed service in the course of testing a report. Keep testing to a
local checkout of this repository.
