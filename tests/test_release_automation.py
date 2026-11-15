"""Tests for scripts/aggregate_changelog.py and scripts/release.py (I-1)."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AGGREGATE = load_module("aggregate_changelog",
                        ROOT / "scripts" / "aggregate_changelog.py")
RELEASE = load_module("release", ROOT / "scripts" / "release.py")

CHANGELOG = """# Changelog

## [Unreleased]

- Governance files: `CONTRIBUTING.md`,
  `SECURITY.md`, and issue templates.

## [1.1.0] - 2026-11-01

- Initial packaged release.
"""


class AggregateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".changelog").mkdir()
        (self.root / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

    def fragment(self, name, text):
        (self.root / ".changelog" / name).write_text(text, encoding="utf-8")

    def test_merges_sections_in_canonical_order(self):
        self.fragment("41-b.md", "### Fixed\n\n- Fixed the mirror drift.\n")
        self.fragment("40-a.md", "### Added\n\n- Entry skill.\n")
        fragments, paths = AGGREGATE.read_fragments(self.root / ".changelog")
        merged = AGGREGATE.merge(
            (self.root / "CHANGELOG.md").read_text(encoding="utf-8"),
            fragments)
        self.assertLess(merged.index("### Added"), merged.index("### Fixed"))
        self.assertIn("- Entry skill.", merged)
        self.assertIn("- Fixed the mirror drift.", merged)
        # Preamble bullets survive the merge verbatim.
        self.assertIn("Governance files: `CONTRIBUTING.md`,", merged)
        self.assertIn("`SECURITY.md`, and issue templates.", merged)

    def test_no_fragments_is_a_noop(self):
        fragments, paths = AGGREGATE.read_fragments(self.root / ".changelog")
        self.assertEqual((fragments, paths), ({}, []))

    def test_malformed_fragments_raise(self):
        self.fragment("41-bad.md", "### Added\n\n### Fixed\n\n- X.\n")
        with self.assertRaises(ValueError):
            AGGREGATE.read_fragments(self.root / ".changelog")
        (self.root / ".changelog" / "41-bad.md").unlink()
        self.fragment("41-bad.md", "- Bullet with no section.\n")
        with self.assertRaises(ValueError):
            AGGREGATE.read_fragments(self.root / ".changelog")

    def test_readme_and_underscore_files_are_not_fragments(self):
        (self.root / ".changelog" / "README.md").write_text(
            "### Added\n\n- Not a fragment.\n", encoding="utf-8")
        (self.root / ".changelog" / "_template.md").write_text(
            "### Added\n\n- Not a fragment.\n", encoding="utf-8")
        fragments, paths = AGGREGATE.read_fragments(self.root / ".changelog")
        self.assertEqual((fragments, paths), ({}, []))

    def test_check_does_not_write(self):
        self.fragment("41-a.md", "### Added\n\n- Entry skill.\n")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "aggregate_changelog.py"),
             "--root", str(self.root), "--check"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / ".changelog" / "41-a.md").exists())
        self.assertNotIn("Entry skill.",
                         (self.root / "CHANGELOG.md").read_text(encoding="utf-8"))


def manifest(version):
    return {"name": "dev-team-skills", "version": version}


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
        for rel in RELEASE.MANIFESTS:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            data = manifest("1.1.0")
            if rel.endswith("marketplace.json"):
                data["plugins"] = [{"name": "dev-team-skills",
                                    "version": "1.1.0"}]
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def test_promote_creates_version_section_and_fresh_unreleased(self):
        promoted, notes = RELEASE.promote(
            (self.root / "CHANGELOG.md").read_text(encoding="utf-8"),
            "1.2.0", "2026-11-15")
        self.assertIn("## [1.2.0] - 2026-11-15", promoted)
        self.assertIn("## [Unreleased]\n\n## [1.2.0]", promoted)
        self.assertIn("Governance files:", notes)
        self.assertIn("## [1.1.0] - 2026-11-01", promoted)

    def test_bump_manifests_keeps_all_four_in_sync(self):
        RELEASE.bump_manifests(self.root, "1.2.0")
        for rel in RELEASE.MANIFESTS:
            data = json.loads((self.root / rel).read_text(encoding="utf-8"))
            self.assertEqual(data["version"], "1.2.0")
        marketplace = json.loads(
            (self.root / ".claude-plugin" / "marketplace.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(marketplace["plugins"][0]["version"], "1.2.0")

    def test_disagreeing_manifests_refuse_to_bump(self):
        path = self.root / "plugin.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = "9.9.9"
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            RELEASE.bump_manifests(self.root, "1.2.0")

    def test_empty_unreleased_refuses_to_release(self):
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n## [1.1.0] - 2026-11-01\n\n- Old.\n",
            encoding="utf-8")
        with self.assertRaises(ValueError):
            RELEASE.promote(
                (self.root / "CHANGELOG.md").read_text(encoding="utf-8"),
                "1.2.0", "2026-11-15")

    def test_print_notes_does_not_write(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "release.py"),
             "1.2.0", "--root", str(self.root), "--print-notes"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Governance files:", result.stdout)
        self.assertIn("[Unreleased]",
                      (self.root / "CHANGELOG.md").read_text(encoding="utf-8"))
        data = json.loads((self.root / "plugin.json")
                          .read_text(encoding="utf-8"))
        self.assertEqual(data["version"], "1.1.0")


if __name__ == "__main__":
    unittest.main()
