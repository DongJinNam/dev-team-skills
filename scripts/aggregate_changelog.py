#!/usr/bin/env python3
"""Merge .changelog/ fragments into CHANGELOG.md [Unreleased].

Fragment format (one file per PR): `<PR-number>-<short-slug>.md` with
one `### <Section>` heading and bullet lines. Sections follow
Keep-a-Changelog order: Added, Changed, Deprecated, Removed, Fixed,
Security. Files named README.md or starting with `_` are not
fragments (documentation/templates).

    python3 scripts/aggregate_changelog.py [--root <repo>] [--check]

--check reports what would change without writing (used by CI on
pull requests). Without --check, fragments are merged and deleted.
With no fragments, exits 0 without touching CHANGELOG.md.
"""

import argparse
import re
import sys
from pathlib import Path

SECTIONS = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security")
SECTION_RE = re.compile(r"^###\s+(Added|Changed|Deprecated|Removed|Fixed|Security)\s*$")
BULLET_RE = re.compile(r"^\s*[-*]\s+\S")
UNRELEASED_RE = re.compile(r"^##\s+\[Unreleased\]\s*$")
HEADING_RE = re.compile(r"^##\s+")


def read_fragments(changelog_dir):
    """Return {section: [bullets]} and the list of fragment paths."""
    fragments = {}
    paths = []
    for path in sorted(changelog_dir.iterdir()):
        if not path.is_file() or path.suffix != ".md":
            continue
        if path.name == "README.md" or path.name.startswith("_"):
            continue
        section = None
        bullets = []
        for line in path.read_text(encoding="utf-8").splitlines():
            match = SECTION_RE.match(line.strip())
            if match:
                if section is not None:
                    raise ValueError(
                        f"{path.name}: only one ### section per fragment")
                section = match.group(1)
                continue
            if BULLET_RE.match(line):
                if section is None:
                    raise ValueError(
                        f"{path.name}: bullet before any ### section")
                bullets.append(line.strip())
                continue
            if line.startswith((" ", "\t")) and bullets:
                # Wrapped bullet continuation; keep it on the same bullet.
                bullets[-1] += " " + line.strip()
        if section is None or not bullets:
            raise ValueError(
                f"{path.name}: fragment needs one ### section and bullets")
        fragments.setdefault(section, []).extend(bullets)
        paths.append(path)
    return fragments, paths


def merge(changelog_text, fragments):
    """Insert fragment bullets into the [Unreleased] section.

    Bullets written before any ### heading (preamble) are kept verbatim
    at the top; sectioned bullets merge under their ### heading in
    Keep-a-Changelog order.
    """
    lines = changelog_text.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if UNRELEASED_RE.match(line)), None)
    if start is None:
        raise ValueError("CHANGELOG.md has no ## [Unreleased] section")
    end = next((i for i in range(start + 1, len(lines))
                if HEADING_RE.match(lines[i])), len(lines))
    body = lines[start + 1:end]
    existing = {}
    current = None
    order = []
    preamble = []
    for line in body:
        match = SECTION_RE.match(line.strip())
        if match:
            current = match.group(1)
            existing.setdefault(current, [])
            order.append(current)
            continue
        if current is not None and BULLET_RE.match(line):
            existing[current].append(line.strip())
            continue
        if current is not None and line.startswith((" ", "\t")) and existing[current]:
            existing[current][-1] += " " + line.strip()
            continue
        if current is None:
            preamble.append(line.rstrip())
    for section in SECTIONS:
        if section not in fragments:
            continue
        existing.setdefault(section, []).extend(fragments[section])
        if section not in order:
            order.append(section)
    ordered = [s for s in SECTIONS if s in order]
    new_body = []
    while preamble and not preamble[0].strip():
        preamble.pop(0)
    while preamble and not preamble[-1].strip():
        preamble.pop()
    new_body.extend(preamble)
    if preamble and ordered:
        new_body.append("")
    for section in ordered:
        new_body.append(f"### {section}")
        new_body.extend(existing[section])
        new_body.append("")
    if new_body and new_body[-1] == "":
        new_body.pop()
    merged = lines[:start + 1] + [""] + new_body + [""] + lines[end:]
    return "\n".join(merged).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true",
                        help="report what would change without writing")
    args = parser.parse_args()
    root = args.root.resolve()
    changelog_dir = root / ".changelog"
    changelog_path = root / "CHANGELOG.md"
    try:
        fragments, paths = read_fragments(changelog_dir)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if not paths:
        print("no changelog fragments; nothing to do")
        return 0
    merged = merge(changelog_path.read_text(encoding="utf-8"), fragments)
    if args.check:
        print(f"would merge {len(paths)} fragment(s): "
              + ", ".join(p.name for p in paths))
        return 0
    changelog_path.write_text(merged, encoding="utf-8")
    for path in paths:
        path.unlink()
    print(f"merged {len(paths)} fragment(s) into CHANGELOG.md [Unreleased]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
