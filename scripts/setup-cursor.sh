#!/usr/bin/env bash
# Cursor dev-team-skills setup script for macOS and Linux [EXPERIMENTAL]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_DIR="${1:-${REPO_ROOT}}"

echo "=== Cursor dev-team-skills Setup [EXPERIMENTAL] ==="
echo "Target Directory: ${TARGET_DIR}"

CURSOR_RULES_DIR="${TARGET_DIR}/.cursor/rules"
mkdir -p "${CURSOR_RULES_DIR}"

SOURCE_MDC="${REPO_ROOT}/.cursor/rules/engineering-squad.mdc"
DEST_MDC="${CURSOR_RULES_DIR}/engineering-squad.mdc"
cp "${SOURCE_MDC}" "${DEST_MDC}"
echo "  [OK] Created ${DEST_MDC}"

SOURCE_LEGACY="${REPO_ROOT}/.cursorrules"
DEST_LEGACY="${TARGET_DIR}/.cursorrules"
cp "${SOURCE_LEGACY}" "${DEST_LEGACY}"
echo "  [OK] Created ${DEST_LEGACY}"

echo ""
echo "Cursor setup complete!"
echo "NOTE: Cursor support is currently EXPERIMENTAL. Feedback is welcome!"
