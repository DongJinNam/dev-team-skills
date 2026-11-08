#!/usr/bin/env bash
# Antigravity (AGY) dev-team-skills setup script for macOS and Linux

set -euo pipefail

TARGET="${1:-workspace}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILLS_SOURCE_DIR="${REPO_ROOT}/skills"
GEMINI_RULE_SOURCE="${REPO_ROOT}/GEMINI.md"

echo "=== Antigravity (AGY) dev-team-skills Setup ==="
echo "Repository Root: ${REPO_ROOT}"

if [ ! -d "${SKILLS_SOURCE_DIR}" ]; then
    echo "ERROR: Skills directory not found at ${SKILLS_SOURCE_DIR}" >&2
    exit 1
fi

link_or_copy() {
    local src="$1"
    local dest="$2"

    if [ -e "${dest}" ]; then
        echo "  [Exists] ${dest}"
        return 0
    fi

    if ln -s "${src}" "${dest}" 2>/dev/null; then
        echo "  [Linked] ${dest} -> ${src}"
    else
        cp -R "${src}" "${dest}"
        echo "  [Copied] ${dest} (fallback from symlink)"
    fi
}

if [ "${TARGET}" = "workspace" ]; then
    AGENTS_SKILLS_DIR="${REPO_ROOT}/.agents/skills"
    mkdir -p "${AGENTS_SKILLS_DIR}"

    echo "[1/2] Linking workspace skills to .agents/skills/..."
    for skill_path in "${SKILLS_SOURCE_DIR}"/*; do
        if [ -d "${skill_path}" ]; then
            skill_name="$(basename "${skill_path}")"
            if [ "${skill_name}" != "references" ] && [ "${skill_name}" != "scripts" ]; then
                dest="${AGENTS_SKILLS_DIR}/${skill_name}"
                link_or_copy "${skill_path}" "${dest}"
            fi
        fi
    done

    echo "[2/2] Checking GEMINI.md at repository root..."
    if [ -f "${GEMINI_RULE_SOURCE}" ]; then
        echo "  [Ready] GEMINI.md is present at repository root."
    fi

    echo ""
    echo "Workspace setup complete!"
    echo "Antigravity CLI/IDE will now automatically discover workspace skills in .agents/skills/"

elif [ "${TARGET}" = "global" ]; then
    GLOBAL_SKILLS_DIR="${HOME}/.gemini/config/skills"
    mkdir -p "${GLOBAL_SKILLS_DIR}"

    echo "[1/1] Installing skills to Global config (~/.gemini/config/skills)..."
    for skill_path in "${SKILLS_SOURCE_DIR}"/*; do
        if [ -d "${skill_path}" ]; then
            skill_name="$(basename "${skill_path}")"
            if [ "${skill_name}" != "references" ] && [ "${skill_name}" != "scripts" ]; then
                dest="${GLOBAL_SKILLS_DIR}/${skill_name}"
                link_or_copy "${skill_path}" "${dest}"
            fi
        fi
    done

    echo ""
    echo "Global setup complete!"
    echo "All Antigravity sessions on this machine will now have access to these skills."
else
    echo "ERROR: Unknown target '${TARGET}'. Use 'workspace' or 'global'." >&2
    exit 2
fi
