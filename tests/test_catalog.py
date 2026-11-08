"""Direct tests for scripts/build-catalog.py (Phase 1 item A1)."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_catalog", REPO / "scripts" / "build-catalog.py")
CATALOG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CATALOG)

SKILL = "---\nname: {name}\ndescription: >-\n  {description}\n---\n# Body\n"


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding="utf-8")

    def test_entries_come_from_skill_folders_sorted_by_name(self):
        self.write("skills/zeta/SKILL.md", SKILL.format(name="zeta", description="Z."))
        self.write("skills/alpha/SKILL.md", SKILL.format(name="alpha", description="A."))
        catalog = CATALOG.build_catalog(self.root)
        self.assertEqual(catalog["skill_count"], 2)
        self.assertEqual([e["name"] for e in catalog["skills"]], ["alpha", "zeta"])
        self.assertEqual(catalog["skills"][0]["path"], "skills/alpha/SKILL.md")

    def test_compatibility_entry_and_plain_folders_are_excluded(self):
        self.write("skills/SKILL.md", SKILL.format(name="root", description="Compat."))
        self.write("skills/references/notes.md", "Not a skill.\n")
        self.write("skills/real/SKILL.md", SKILL.format(name="real", description="R."))
        catalog = CATALOG.build_catalog(self.root)
        self.assertEqual([e["name"] for e in catalog["skills"]], ["real"])

    def test_output_is_deterministic(self):
        self.write("skills/one/SKILL.md", SKILL.format(name="one", description="1."))
        self.assertEqual(CATALOG.catalog_text(self.root),
                         CATALOG.catalog_text(self.root))
        self.assertTrue(CATALOG.catalog_text(self.root).endswith("\n"))

    def test_duplicate_frontmatter_key_is_rejected(self):
        self.write("skills/bad/SKILL.md",
                   "---\nname: bad\nname: again\ndescription: B.\n---\n")
        with self.assertRaises(ValueError):
            CATALOG.build_catalog(self.root)

    def test_blank_description_is_rejected(self):
        self.write("skills/bad/SKILL.md", SKILL.format(name="bad", description=""))
        with self.assertRaises(ValueError):
            CATALOG.build_catalog(self.root)

    def test_generated_json_round_trips(self):
        self.write("skills/one/SKILL.md", SKILL.format(name="one", description="1."))
        data = json.loads(CATALOG.catalog_text(self.root))
        self.assertEqual(data["catalog_version"], 1)
        self.assertEqual(data["skill_count"], len(data["skills"]))


if __name__ == "__main__":
    unittest.main()
