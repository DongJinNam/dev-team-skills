#!/usr/bin/env python3
"""Generate skills/catalog.json from the skill folders on disk.

The catalog is derived, never hand-edited: one entry per skills/<name>/
folder that contains a SKILL.md, keyed by that file's frontmatter. The
compatibility entry at .compat/skills/SKILL.md is not a separate skill and
is excluded. verify-harness.py regenerates the catalog in memory (rules
CAT-001/CAT-002) and fails when the committed file has drifted.
"""

import argparse
import json
from pathlib import Path
import sys


def parse_frontmatter(path):
    """Return the YAML frontmatter mapping of a SKILL.md file.

    Mirrors verify-harness.py: frontmatter must start at the first line
    and be closed, parse with a safe loader, and reject duplicate keys.
    """
    import yaml

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

    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: YAML frontmatter must start at the first line")
    try:
        closing = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{path}: YAML frontmatter is missing its closing ---") from error
    data = yaml.load("\n".join(lines[1:closing]), Loader=UniqueSafeLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    for field in ("name", "description"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{path}: {field} must be a nonblank string")
    return data


def build_catalog(root):
    skills_dir = root / "skills"
    entries = []
    for folder in sorted(skills_dir.iterdir()):
        skill_file = folder / "SKILL.md"
        if not folder.is_dir() or not skill_file.exists():
            continue
        data = parse_frontmatter(skill_file)
        entries.append({
            "name": data["name"],
            "description": data["description"],
            "path": skill_file.relative_to(root).as_posix(),
        })
    entries.sort(key=lambda entry: entry["name"])
    return {
        "catalog_version": 1,
        "generated_by": "scripts/build-catalog.py - do not edit by hand",
        "skill_count": len(entries),
        "skills": entries,
    }


def catalog_text(root):
    return json.dumps(build_catalog(root), ensure_ascii=False, indent=2,
                      sort_keys=True) + "\n"


def main():
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ is required.", file=sys.stderr)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        import yaml  # noqa: F401 - fail early with the harness message
    except ImportError:
        print("ERROR: PyYAML is required; install scripts/requirements-harness.txt "
              "with this Python interpreter.", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[1],
                        help="package root (defaults to the parent of scripts/)")
    root = parser.parse_args().root.resolve()
    try:
        text = catalog_text(root)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    target = root / "skills" / "catalog.json"
    target.write_text(text, encoding="utf-8")
    count = json.loads(text)["skill_count"]
    print(f"Wrote {target} ({count} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
