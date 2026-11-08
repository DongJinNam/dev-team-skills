"""Keep native discovery copies aligned with the canonical packaged skills."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillMirrorTests(unittest.TestCase):
    def test_native_skill_tree_matches_canonical_directories(self):
        source = ROOT / 'skills'
        mirror = ROOT / '.agents/skills'
        # Compatibility entries and their shared resources are not native skills.
        expected = {p.relative_to(source): p for directory in source.iterdir()
                    if (directory / 'SKILL.md').is_file()
                    for p in directory.rglob('*') if p.is_file()}
        actual = {p.relative_to(mirror): p for p in mirror.rglob('*') if p.is_file()}
        self.assertEqual(set(expected), set(actual))
        for relative, original in expected.items():
            with self.subTest(path=str(relative)):
                self.assertEqual(original.read_bytes(), actual[relative].read_bytes())
