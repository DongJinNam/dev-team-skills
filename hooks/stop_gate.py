#!/usr/bin/env python3
"""Stop gate for dev-team-skills (Claude Code only).

Runs the package verifier (scripts/verify-harness.py) when the agent
tries to stop. Exit 2 blocks the stop and feeds stderr back to Claude
as the reason; exit 0 allows it.

Loop guard: when the payload says stop_hook_active is true, Claude is
already continuing because of this hook, so allow the stop. Failing
open on purpose: if the verifier cannot be found, warn and allow.
"""

import json
import subprocess
import sys
from pathlib import Path


def decide(stop_hook_active, harness_ok):
    """Return (allow, reason). Pure decision, unit-tested."""
    if stop_hook_active:
        return True, "already continuing because of this hook; allowing stop"
    if harness_ok:
        return True, ""
    return False, (
        "dev-team-skills package check failed (scripts/verify-harness.sh). "
        "Fix the failure (catalog drift, mirror drift, broken skill link) "
        "before stopping; do not claim the package is intact."
    )


def run_harness(root):
    """Run verify-harness.py. None when the verifier cannot be found."""
    verifier = root / "scripts" / "verify-harness.py"
    if not verifier.is_file():
        return None
    result = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=root, capture_output=True, text=True, timeout=120,
    )
    return result.returncode == 0, result.stdout + result.stderr


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeError):
        payload = {}
    stop_hook_active = bool(payload.get("stop_hook_active"))
    root = Path(__file__).resolve().parents[1]
    outcome = run_harness(root)
    if outcome is None:
        print("dev-team-skills stop hook: verifier not found; allowing stop",
              file=sys.stderr)
        return 0
    harness_ok, output = outcome
    allow, reason = decide(stop_hook_active, harness_ok)
    if allow:
        return 0
    print(reason, file=sys.stderr)
    print(output, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
