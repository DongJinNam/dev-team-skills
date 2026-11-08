#!/usr/bin/env python3
"""Validate local package structure, not agent behavior or security approval."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
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
        # Codex requires --- at byte zero; stripping a BOM masks a load failure.
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            raise ValueError("YAML frontmatter must start at the first line")
        try:
            closing = lines.index("---", 1)
        except ValueError as error:
            raise ValueError("YAML frontmatter is missing its closing ---") from error
        data = yaml.load("\n".join(lines[1:closing]), Loader=UniqueSafeLoader)
        require_text_fields(data, ("name", "description"))
        return data

    skills = sorted((root / "skills").rglob("SKILL.md"))
    if not skills:
        print("FAIL skills/: no SKILL.md files found")
        failed = True
    parsed = {}
    for path in skills:
        def capture(path=path):
            parsed[path] = skill(path)
        check(path.relative_to(root).as_posix(), capture)

    for path in sorted((root / "skills").rglob("SKILL_en.md")):
        check(path.relative_to(root).as_posix(), lambda path=path: skill(path))

    # Coded skill invariants (decision 2026-11-08, Phase 1 item A1).
    # SKL-001: a SKILL.md lives only at skills/SKILL.md (compatibility
    # entry) or skills/<folder>/SKILL.md, never nested deeper.
    # SKL-002: a skill folder's frontmatter name equals the folder name.
    # SKL-003: relative links in a SKILL.md resolve to existing files.
    # CAT-001: skills/catalog.json exists and matches the catalog schema.
    # CAT-002: the committed catalog equals a fresh filesystem derivation;
    # regenerate with scripts/build-catalog.py instead of editing it.
    skills_root = root / "skills"
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

    def skl001():
        for path in skills:
            if len(path.relative_to(skills_root).parts) > 2:
                raise ValueError(
                    f"{path.relative_to(root).as_posix()} is nested below a skill folder")

    def skl002():
        for path in skills:
            parts = path.relative_to(skills_root).parts
            data = parsed.get(path)
            if len(parts) == 2 and data is not None and data.get("name") != parts[0]:
                raise ValueError(
                    f"{path.relative_to(root).as_posix()}: frontmatter name "
                    f"{data.get('name')!r} does not match folder {parts[0]!r}")

    def skl003():
        for path in skills:
            text = path.read_text(encoding="utf-8-sig")
            for target in link_pattern.findall(text):
                target = target.strip().strip("<>").split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                if not (path.parent / target).exists():
                    raise ValueError(
                        f"{path.relative_to(root).as_posix()}: broken relative link {target!r}")

    def catalog_data():
        data = json.loads((skills_root / "catalog.json").read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique_json_object,
                          parse_constant=reject_json_constant)
        if not isinstance(data, dict):
            raise ValueError("catalog must be an object")
        return data

    def cat001():
        data = catalog_data()
        if data.get("catalog_version") != 1:
            raise ValueError("catalog_version must be 1")
        entries = data.get("skills")
        if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
            raise ValueError("skills must be an array of objects")
        for entry in entries:
            require_text_fields(entry, ("name", "description", "path"))
        if data.get("skill_count") != len(entries):
            raise ValueError("skill_count must equal the number of skill entries")

    def cat002():
        spec = importlib.util.spec_from_file_location(
            "build_catalog", root / "scripts" / "build-catalog.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        committed = (skills_root / "catalog.json").read_text(encoding="utf-8-sig")
        if committed != module.catalog_text(root):
            raise ValueError("catalog has drifted from the skill folders; "
                             "regenerate with scripts/build-catalog.py")

    # MIR-001 (Phase 1 item C2): the committed .agents/skills mirror must
    # equal what setup-antigravity materializes from skills/ — every skill
    # folder except the shared references/ and scripts/ folders, byte for
    # byte, with no missing or extra files. The check is a dry run: it
    # writes nothing.
    def mir001():
        expected = {}
        for folder in sorted(skills_root.iterdir()):
            if folder.is_dir() and folder.name not in ("references", "scripts"):
                for path in sorted(folder.rglob("*")):
                    if path.is_file():
                        expected[path.relative_to(skills_root).as_posix()] = path
        mirror_root = root / ".agents" / "skills"
        actual = {}
        if mirror_root.exists():
            for path in sorted(mirror_root.rglob("*")):
                if path.is_file():
                    actual[path.relative_to(mirror_root).as_posix()] = path
        if set(actual) != set(expected):
            raise ValueError(
                f"mirror file set differs (missing: {sorted(set(expected) - set(actual))}, "
                f"extra: {sorted(set(actual) - set(expected))})")
        for rel, path in expected.items():
            if path.read_bytes() != actual[rel].read_bytes():
                raise ValueError(
                    f".agents/skills/{rel} differs from skills/{rel}; "
                    "refresh the mirror from the canonical skills/ tree")

    if skills:
        check("SKL-001 skill locations", skl001)
        check("SKL-002 skill name matches folder", skl002)
        check("SKL-003 skill relative links", skl003)
        check("CAT-001 skills/catalog.json schema", cat001)
        check("CAT-002 skills/catalog.json is current", cat002)
        check("MIR-001 .agents/skills mirror is current", mir001)

    def synchronized(paths):
        hashes = [hashlib.sha256((root / path).read_bytes()).digest() for path in paths]
        if len(set(hashes)) != 1:
            raise ValueError("rule files differ (SHA-256 byte comparison)")

    rules = ("GEMINI.md", "CLAUDE.md", "CODEX.md", "AGENTS.md", "rules/AGENTS.md")
    check("constitution synchronization", lambda: synchronized(rules))
    english = tuple(path.replace(".md", "_en.md") for path in rules)
    if any((root / path).exists() for path in english):
        check("English constitution synchronization", lambda: synchronized(english))

    print("NOT_RUN: agent behavior, product tests, installer execution, "
          "independent security review.")
    print("Package structure: " + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
