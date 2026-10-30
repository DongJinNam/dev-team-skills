#!/usr/bin/env bash
#
# Cross-platform verification harness script for macOS & Linux (Bash).
# Verifies plugin manifest, SKILL.md frontmatter, and rule files synchronization.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "========================================"
echo "🔍 AI Agent Harness Verification (macOS/Linux)"
echo "========================================"

FAILED=0

# 1. Verify plugin.json
echo ""
echo "[1/3] Checking plugin.json manifest..."
if [ ! -f "plugin.json" ]; then
    echo "❌ Error: plugin.json not found at repo root!"
    FAILED=1
else
    # Check for name and description using grep
    if grep -q '"name":' plugin.json && grep -q '"description":' plugin.json; then
        echo "  ✅ plugin.json is present and has required fields"
    else
        echo "❌ Error: plugin.json missing required 'name' or 'description'!"
        FAILED=1
    fi
fi

# 2. Verify all SKILL.md frontmatter
echo ""
echo "[2/3] Checking SKILL.md frontmatters in skills/..."
SKILL_FILES=$(find skills -name "SKILL.md")
if [ -z "${SKILL_FILES}" ]; then
    echo "❌ Error: No SKILL.md files found in skills/!"
    FAILED=1
else
    for file in ${SKILL_FILES}; do
        if grep -q '^name:' "$file" && grep -q '^description:' "$file"; then
            echo "  ✅ $file (valid frontmatter)"
        else
            echo "❌ Error: $file invalid frontmatter (missing name or description)"
            FAILED=1
        fi
    done
fi

# 3. Verify rule files synchronization (GEMINI, CLAUDE, CODEX, AGENTS)
echo ""
echo "[3/3] Checking Constitution rule files sync..."

get_hash() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | awk '{print $1}'
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | awk '{print $1}'
    else
        echo "No sha256sum or shasum found"
        exit 1
    fi
}

GEMINI_HASH=$(get_hash GEMINI.md)
CLAUDE_HASH=$(get_hash CLAUDE.md)
CODEX_HASH=$(get_hash CODEX.md)
AGENTS_HASH=$(get_hash AGENTS.md)

echo "  GEMINI.md : ${GEMINI_HASH}"
echo "  CLAUDE.md : ${CLAUDE_HASH}"
echo "  CODEX.md  : ${CODEX_HASH}"
echo "  AGENTS.md : ${AGENTS_HASH}"

if [ "${GEMINI_HASH}" != "${CLAUDE_HASH}" ] || [ "${GEMINI_HASH}" != "${CODEX_HASH}" ] || [ "${GEMINI_HASH}" != "${AGENTS_HASH}" ]; then
    echo "❌ Error: Rule files are out of sync! GEMINI, CLAUDE, CODEX, and AGENTS must remain identical."
    FAILED=1
else
    echo "  ✅ All 4 rule files are strictly synchronized!"
fi

echo ""
echo "========================================"
if [ ${FAILED} -ne 0 ]; then
    echo "❌ Harness verification FAILED."
    exit 1
else
    echo "🎉 Harness verification PASSED successfully!"
    exit 0
fi
