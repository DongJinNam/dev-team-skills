#!/usr/bin/env bash
# Shell entry point; validation rules live in verify-harness.py.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for interpreter in python3 python; do
    if command -v "$interpreter" >/dev/null 2>&1; then
        exec "$interpreter" "$SCRIPT_DIR/verify-harness.py" "$@"
    fi
done
printf '%s\n' 'ERROR: Python 3.10+ is required to run the package verifier.' >&2
exit 2
