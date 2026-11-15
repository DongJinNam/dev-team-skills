#!/usr/bin/env python3
"""SessionStart bootstrap for dev-team-skills (Claude Code only).

Prints the entry rules as plain text; Claude Code injects hook stdout as
session context on exit 0. Never blocks: any failure prints a short
warning and exits 0 so a broken hook can never trap session start.
"""

import sys


BOOTSTRAP = """[dev-team-skills] Entry rules (injected by the SessionStart hook):
- Engineering work (build, fix, review, ship): read skills/using-dev-team-skills/SKILL.md first, then follow the engineering-squad contract it points to.
- Six accountable owners every time: Tech Lead, Product, Engineering, Quality, Delivery, Security. Independent security PASS on the current head before any merge.
- Never claim the package is intact without running: bash scripts/verify-harness.sh
- Slash commands: /dev-team-skills:squad, /dev-team-skills:review, /dev-team-skills:verify, /dev-team-skills:ship.
- Hooks are Claude Code only. To disable, delete hooks/hooks.json from the installed plugin copy.
"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.stdout.write(BOOTSTRAP)
    except (BrokenPipeError, OSError):
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
