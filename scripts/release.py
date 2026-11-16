#!/usr/bin/env python3
"""Promote CHANGELOG.md [Unreleased] to a versioned release.

    python3 scripts/release.py 1.2.0 [--root <repo>] [--check]

- Requires a non-empty ## [Unreleased] section.
- Rewrites it as ## [<version>] - <today UTC> and inserts a fresh
  empty ## [Unreleased] above it. Also rewrites the preamble's
  "current packaged version" sentence to the new version when present.
- Bumps the version in plugin.json, .claude-plugin/plugin.json,
  .claude-plugin/marketplace.json (top level and every entry in plugins),
  and .codex-plugin/plugin.json. All four must agree before the bump.
- Prints the release notes (the version section body) on stdout.

The GitHub workflow (.github/workflows/release.yml) captures the
notes first with --print-notes, then promotes and opens a release PR;
the tag and the GitHub Release are created only after that PR is
reviewed and merged. This script never touches git or the network.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
UNRELEASED_RE = re.compile(r"^##\s+\[Unreleased\]\s*$")
HEADING_RE = re.compile(r"^##\s+")
BULLET_RE = re.compile(r"^\s*[-*]\s+\S")
# "The current packaged version is X.Y.Z (`plugin.json`)." in the
# CHANGELOG preamble. promote() rewrites it to the new version; if the
# sentence is absent the changelog is left as-is.
HEADER_VERSION_RE = re.compile(
    r"^(The current packaged version is )\d+\.\d+\.\d+( \(`plugin\.json`\)\.)$")

MANIFESTS = (
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
)


def promote(changelog_text, version, today):
    lines = changelog_text.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if UNRELEASED_RE.match(line)), None)
    if start is None:
        raise ValueError("CHANGELOG.md has no ## [Unreleased] section")
    end = next((i for i in range(start + 1, len(lines))
                if HEADING_RE.match(lines[i])), len(lines))
    body = lines[start + 1:end]
    if not any(BULLET_RE.match(line) for line in body):
        raise ValueError("## [Unreleased] has no entries; nothing to release")
    body = [line for line in body]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    versioned = [f"## [{version}] - {today}", ""] + body
    preamble = [HEADER_VERSION_RE.sub(rf"\g<1>{version}\g<2>", line)
                for line in lines[:start]]
    new_lines = (preamble + ["## [Unreleased]", ""]
                 + versioned + [""] + lines[end:])
    notes = "\n".join(body).strip() + "\n"
    return "\n".join(new_lines).rstrip() + "\n", notes


def bump_manifests(root, version):
    versions = {}
    for rel in MANIFESTS:
        path = root / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        versions[rel] = data["version"]
    if len(set(versions.values())) != 1:
        raise ValueError(f"manifest versions disagree: {versions}")
    for rel in MANIFESTS:
        path = root / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = version
        plugins = data.get("plugins")
        if isinstance(plugins, list):
            for plugin in plugins:
                plugin["version"] = version
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="release version, e.g. 1.2.0")
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true",
                        help="validate without writing")
    parser.add_argument("--print-notes", action="store_true",
                        help="print only the release notes, without writing")
    args = parser.parse_args()
    if not VERSION_RE.match(args.version):
        print(f"ERROR: version must be X.Y.Z, got {args.version!r}",
              file=sys.stderr)
        return 1
    root = args.root.resolve()
    changelog_path = root / "CHANGELOG.md"
    try:
        promoted, notes = promote(
            changelog_path.read_text(encoding="utf-8"), args.version,
            datetime.now(timezone.utc).date().isoformat())
        if args.print_notes:
            print(notes, end="")
            return 0
        if not args.check:
            changelog_path.write_text(promoted, encoding="utf-8")
            bump_manifests(root, args.version)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"release {args.version} ready")
    print("--- release notes ---")
    print(notes, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
