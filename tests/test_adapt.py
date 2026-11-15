"""Tests for scripts/adapt.py (Pickle #2 single-source mirrors)."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "adapt", ROOT / "scripts" / "adapt.py")
ADAPT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPT)


def make_tree(base, skills):
    for name, files in skills.items():
        for filename, content in files.items():
            target = base / "skills" / name / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")


class AdaptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        make_tree(self.root, {
            "alpha": {"SKILL.md": "---\nname: alpha\n---\nA\n"},
            "beta": {"SKILL.md": "---\nname: beta\n---\nB\n",
                     "notes.md": "notes\n"},
            "references": {"shared.md": "shared\n"},
        })

    def test_generate_copies_skill_folders_except_shared(self):
        written = ADAPT.generate(self.root)
        mirror = self.root / ".agents" / "skills"
        self.assertTrue((mirror / "alpha" / "SKILL.md").is_file())
        self.assertTrue((mirror / "beta" / "notes.md").is_file())
        self.assertFalse((mirror / "references").exists())
        self.assertEqual(
            (mirror / "alpha" / "SKILL.md").read_bytes(),
            (self.root / "skills" / "alpha" / "SKILL.md").read_bytes())
        self.assertTrue(written)

    def test_generate_removes_stale_mirror_files(self):
        ADAPT.generate(self.root)
        stale = self.root / ".agents" / "skills" / "beta" / "old.md"
        stale.write_text("stale\n", encoding="utf-8")
        ADAPT.generate(self.root)
        self.assertFalse(stale.exists())

    def test_check_passes_after_generate_and_fails_on_drift(self):
        ADAPT.generate(self.root)
        self.assertEqual(ADAPT.drift(self.root), ([], [], []))
        tampered = self.root / ".agents" / "skills" / "alpha" / "SKILL.md"
        tampered.write_text("tampered\n", encoding="utf-8")
        _, _, differing = ADAPT.drift(self.root)
        self.assertEqual(differing, ["alpha/SKILL.md"])

    def test_check_on_real_repo_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "adapt.py"),
             "--root", str(ROOT), "--check"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
