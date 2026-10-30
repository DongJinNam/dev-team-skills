#!/usr/bin/env bash
#
# Cross-platform verification harness script for macOS & Linux (Bash).
# Verifies plugin manifests, SKILL.md frontmatter, and rule files synchronization.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "========================================"
echo "🔍 AI Agent Harness Verification (macOS/Linux)"
echo "========================================"

FAILED=0

# 1. Verify plugin & marketplace manifests
echo ""
echo "[1/4] Checking plugin & marketplace manifests..."
MANIFESTS=("plugin.json" ".claude-plugin/plugin.json" ".claude-plugin/marketplace.json" ".codex-plugin/plugin.json")

for m in "${MANIFESTS[@]}"; do
    if [ ! -f "$m" ]; then
        echo "❌ Error: $m not found!"
        FAILED=1
    else
        if grep -q '"name":' "$m"; then
            echo "  ✅ $m is present and valid"
        else
            echo "❌ Error: $m missing 'name' field!"
            FAILED=1
        fi
    fi
done

# 2. Verify all SKILL.md frontmatter
echo ""
echo "[2/4] Checking SKILL.md frontmatters in skills/..."
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

# 3. Verify rule files synchronization (GEMINI, CLAUDE, CODEX, AGENTS, rules/AGENTS.md)
echo ""
echo "[3/4] Checking Constitution rule files sync..."

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
RULES_AGENTS_HASH=$(get_hash rules/AGENTS.md)

echo "  GEMINI.md       : ${GEMINI_HASH}"
echo "  CLAUDE.md       : ${CLAUDE_HASH}"
echo "  CODEX.md        : ${CODEX_HASH}"
echo "  AGENTS.md       : ${AGENTS_HASH}"
echo "  rules/AGENTS.md : ${RULES_AGENTS_HASH}"

if [ "${GEMINI_HASH}" != "${CLAUDE_HASH}" ] || [ "${GEMINI_HASH}" != "${CODEX_HASH}" ] || [ "${GEMINI_HASH}" != "${AGENTS_HASH}" ] || [ "${GEMINI_HASH}" != "${RULES_AGENTS_HASH}" ]; then
    echo "❌ Error: Rule files are out of sync! GEMINI, CLAUDE, CODEX, AGENTS, and rules/AGENTS.md must remain identical."
    FAILED=1
else
    echo "  ✅ All 5 rule files are strictly synchronized!"
fi

if [ -f "GEMINI_en.md" ]; then
    GEMINI_EN_HASH=$(get_hash GEMINI_en.md)
    CLAUDE_EN_HASH=$(get_hash CLAUDE_en.md)
    CODEX_EN_HASH=$(get_hash CODEX_en.md)
    AGENTS_EN_HASH=$(get_hash AGENTS_en.md)
    RULES_AGENTS_EN_HASH=$(get_hash rules/AGENTS_en.md)

    if [ "${GEMINI_EN_HASH}" != "${CLAUDE_EN_HASH}" ] || [ "${GEMINI_EN_HASH}" != "${CODEX_EN_HASH}" ] || [ "${GEMINI_EN_HASH}" != "${AGENTS_EN_HASH}" ] || [ "${GEMINI_EN_HASH}" != "${RULES_AGENTS_EN_HASH}" ]; then
        echo "❌ Error: English rule files are out of sync! GEMINI_en, CLAUDE_en, CODEX_en, AGENTS_en, and rules/AGENTS_en.md must remain identical."
        FAILED=1
    else
        echo "  ✅ All 5 English rule files are strictly synchronized!"
    fi
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
