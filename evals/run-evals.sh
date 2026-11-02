#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for interpreter in python3 python; do
    if command -v "$interpreter" >/dev/null 2>&1; then
        exec "$interpreter" "$SCRIPT_DIR/run_evals.py" "$@"
    fi
done
printf '%s\n' 'ERROR: Python 3.10+ is required.' >&2
exit 2
