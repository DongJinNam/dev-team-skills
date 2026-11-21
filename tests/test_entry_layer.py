"""Entry-layer tests: entry skill, slash commands, hook wiring (Pickle #1).

The auto-invocation check is a unit test, not a capture case: the
decision contract (decision/actions/facts/summary) cannot express
"the skill was invoked". The test asserts the trigger surface the
hook and the commands share: the same entry skill, the same trigger
phrases, the same kickoff contract.
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "skills" / "using-dev-team-skills"
COMMANDS = ("squad", "review", "verify", "ship")
# Plain-language prompts that must route to the entry skill.
TRIGGER_PHRASES = ("fix this bug", "build this feature",
                   "이 버그 고쳐줘", "이 기능 만들어줘")


def frontmatter(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "---"
    closing = lines.index("---", 1)
    data = {}
    for line in lines[1:closing]:
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


class EntrySkillTests(unittest.TestCase):
    def test_entry_skill_frontmatter_matches_folder(self):
        data = frontmatter(ENTRY / "SKILL.md")
        self.assertEqual(data["name"], "using-dev-team-skills")
        self.assertTrue(data["description"].strip())

    def test_entry_skill_lists_plain_language_triggers(self):
        text = (ENTRY / "SKILL.md").read_text(encoding="utf-8")
        for phrase in TRIGGER_PHRASES:
            self.assertIn(phrase, text, f"trigger phrase missing: {phrase}")

    def test_entry_skill_links_resolve(self):
        text = (ENTRY / "SKILL.md").read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().split("#", 1)[0]
            if not target or "://" in target:
                continue
            self.assertTrue((ENTRY / target).exists(),
                            f"broken link in entry skill: {target}")

    def test_entry_skill_mirrored(self):
        mirror = ROOT / ".agents" / "skills" / "using-dev-team-skills"
        self.assertTrue((mirror / "SKILL.md").is_file(), "mirror missing SKILL.md")
        self.assertEqual((ENTRY / "SKILL.md").read_bytes(),
                         (mirror / "SKILL.md").read_bytes())
        ko_doc = ROOT / "docs" / "i18n" / "ko" / "skills" / "using-dev-team-skills" / "SKILL_ko.md"
        self.assertTrue(ko_doc.is_file(), "Korean translation missing under docs/i18n/ko/skills/")

    def test_catalog_lists_entry_skill(self):
        catalog = json.loads((ROOT / "skills" / "catalog.json")
                             .read_text(encoding="utf-8"))
        names = [entry["name"] for entry in catalog["skills"]]
        self.assertIn("using-dev-team-skills", names)
        self.assertEqual(catalog["skill_count"], len(names))


class SlashCommandTests(unittest.TestCase):
    def test_four_commands_exist_with_descriptions(self):
        for name in COMMANDS:
            path = ROOT / "commands" / f"{name}.md"
            self.assertTrue(path.is_file(), f"missing command: {name}")
            data = frontmatter(path)
            self.assertTrue(data.get("description", "").strip(),
                            f"command {name} has no description")

    def test_squad_command_points_at_entry_skill(self):
        text = (ROOT / "commands" / "squad.md").read_text(encoding="utf-8")
        self.assertIn("skills/using-dev-team-skills/SKILL.md", text)
        self.assertIn("engineering-squad", text)


class HookWiringTests(unittest.TestCase):
    def test_session_start_injects_entry_skill(self):
        hooks = json.loads((ROOT / "hooks" / "hooks.json")
                           .read_text(encoding="utf-8"))
        self.assertIn("SessionStart", hooks["hooks"])
        script = ROOT / "hooks" / "session_start.py"
        self.assertIn("skills/using-dev-team-skills/SKILL.md",
                      script.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
