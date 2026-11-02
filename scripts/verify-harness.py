#!/usr/bin/env python3
"""Validate local package structure, not agent behavior or security approval."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


def unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_json_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def require_text_fields(data, fields):
    if not isinstance(data, dict):
        raise ValueError("expected an object/mapping")
    for field in fields:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a nonblank string")


def main():
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ is required.", file=sys.stderr)
        return 2
    # Pipe output consistently even when Windows uses a legacy console locale.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML is required; install scripts/requirements-harness.txt "
              "with this Python interpreter.", file=sys.stderr)
        return 2

    # SafeLoader forbids Python object constructors. Duplicate keys must not
    # silently replace a policy field with a different value.
    class UniqueSafeLoader(yaml.SafeLoader):
        pass

    def unique_yaml_mapping(loader, node):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            try:
                if key in result:
                    raise ValueError(f"duplicate YAML key: {key}")
                result[key] = loader.construct_object(value_node)
            except TypeError as error:
                raise ValueError("YAML mapping keys must be scalar values") from error
        return result

    UniqueSafeLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_yaml_mapping)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="package root (defaults to the parent of scripts/)")
    root = parser.parse_args().root.resolve()
    failed = False

    def check(label, action):
        nonlocal failed
        try:
            action()
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
            print(f"FAIL {label}: {error}")
            failed = True
        else:
            print(f"PASS {label}")

    def manifest(path):
        data = json.loads((root / path).read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique_json_object,
                          parse_constant=reject_json_constant)
        require_text_fields(data, ("name", "description"))
        if path.endswith("marketplace.json"):
            plugins = data.get("plugins")
            if not isinstance(plugins, list) or not all(isinstance(p, dict) for p in plugins):
                raise ValueError("plugins must be an array of objects")

    print("Package structure verification (local repository contract)")
    for path in ("plugin.json", ".claude-plugin/plugin.json",
                 ".claude-plugin/marketplace.json", ".codex-plugin/plugin.json"):
        check(path, lambda path=path: manifest(path))

    def skill(path):
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        if not lines or lines[0] != "---":
            raise ValueError("YAML frontmatter must start at the first line")
        try:
            closing = lines.index("---", 1)
        except ValueError as error:
            raise ValueError("YAML frontmatter is missing its closing ---") from error
        data = yaml.load("\n".join(lines[1:closing]), Loader=UniqueSafeLoader)
        require_text_fields(data, ("name", "description"))

    skills = sorted((root / "skills").rglob("SKILL.md"))
    if not skills:
        print("FAIL skills/: no SKILL.md files found")
        failed = True
    for path in skills:
        check(path.relative_to(root).as_posix(), lambda path=path: skill(path))

    def synchronized(paths):
        hashes = [hashlib.sha256((root / path).read_bytes()).digest() for path in paths]
        if len(set(hashes)) != 1:
            raise ValueError("rule files differ (SHA-256 byte comparison)")

    rules = ("GEMINI.md", "CLAUDE.md", "CODEX.md", "AGENTS.md", "rules/AGENTS.md")
    check("constitution synchronization", lambda: synchronized(rules))
    english = tuple(path.replace(".md", "_en.md") for path in rules)
    if any((root / path).exists() for path in english):
        check("English constitution synchronization", lambda: synchronized(english))

    print("NOT_RUN: agent behavior, product tests, installation compatibility, "
          "independent security review.")
    print("Package structure: " + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
