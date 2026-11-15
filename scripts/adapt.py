#!/usr/bin/env python3
"""Generate host mirrors from the canonical skills/ tree (Pickle #2).

Single source: skills/<name>/ (every folder with a SKILL.md, except
the shared references/ and scripts/ folders). Target: .agents/skills/
(byte for byte, the same file set MIR-001 checks).

    python3 scripts/adapt.py            # regenerate the mirror
    python3 scripts/adapt.py --check    # fail when the mirror drifted

Scope is deliberately narrow: only .agents/skills. The Cursor rule
(.cursor/rules/engineering-squad.mdc) derives from the constitution
(AGENTS.md), not from skills/, and there is no .codex mirror in this
repo, so neither is generated here. CI verifies no drift with
--check; it never writes.
"""

import argparse
import shutil
import sys
from pathlib import Path

EXCLUDED = ("references", "scripts")


def expected_files(skills_root):
    """Map relative path -> source file for every mirrored file."""
    expected = {}
    for folder in sorted(skills_root.iterdir()):
        if not folder.is_dir() or folder.name in EXCLUDED:
            continue
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                expected[path.relative_to(skills_root).as_posix()] = path
    return expected


def drift(root):
    """Return (missing, extra, differing) relative paths."""
    skills_root = root / "skills"
    mirror_root = root / ".agents" / "skills"
    expected = expected_files(skills_root)
    actual = {}
    if mirror_root.exists():
        for path in sorted(mirror_root.rglob("*")):
            if path.is_file():
                actual[path.relative_to(mirror_root).as_posix()] = path
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    differing = sorted(
        rel for rel in set(expected) & set(actual)
        if expected[rel].read_bytes() != actual[rel].read_bytes())
    return missing, extra, differing


def generate(root):
    """Rewrite the mirror from skills/. Returns the list of written paths."""
    skills_root = root / "skills"
    mirror_root = root / ".agents" / "skills"
    expected = expected_files(skills_root)
    written = []
    for rel, source in expected.items():
        target = mirror_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != source.read_bytes():
            shutil.copy2(source, target)
            written.append(rel)
    actual = {}
    if mirror_root.exists():
        for path in sorted(mirror_root.rglob("*")):
            if path.is_file():
                actual[path.relative_to(mirror_root).as_posix()] = path
    for rel in sorted(set(actual) - set(expected)):
        actual[rel].unlink()
        written.append(f"removed {rel}")
    for path in sorted(mirror_root.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true",
                        help="report drift instead of regenerating")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.check:
        missing, extra, differing = drift(root)
        if missing:
            print(f"missing in mirror: {missing}")
        if extra:
            print(f"extra in mirror: {extra}")
        if differing:
            print(f"mirror differs: {differing}")
        if missing or extra or differing:
            print("mirror drifted; regenerate with scripts/adapt.py")
            return 1
        print("mirror matches skills/ (adapt --check)")
        return 0
    written = generate(root)
    print(f"adapt: {len(written)} file(s) updated")
    for rel in written:
        print(f"  {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
