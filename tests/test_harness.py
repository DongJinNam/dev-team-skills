"""Black-box package regression cases shared by every launcher and OS."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
MANIFESTS = (
    "plugin.json", ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json", ".codex-plugin/plugin.json",
)
RULES = ("GEMINI.md", "CLAUDE.md", "CODEX.md", "AGENTS.md", "rules/AGENTS.md")
VALID_SKILL = "---\nname: example\ndescription: >-\n  A useful skill.\n---\n# Body\n"


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo with spaces 한글"
        self.root.mkdir()
        shutil.copytree(REPO / "scripts", self.root / "scripts",
                        ignore=shutil.ignore_patterns("__pycache__"))
        for path in MANIFESTS:
            data = {"name": "example", "description": "A package."}
            if path.endswith("marketplace.json"):
                data["plugins"] = [{"name": "example", "source": "./"}]
            self.write(path, json.dumps(data))
        for path in RULES:
            self.write(path, "Identical rules.\n")
        self.write("skills/example/SKILL.md", VALID_SKILL)

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value.encode("utf-8"))

    def run_harness(self, valid, extra_args=()):
        launcher = os.environ.get("HARNESS_LAUNCHER", "bash")
        scripts = self.root / "scripts"
        commands = {
            "bash": ["bash", (scripts / "verify-harness.sh").as_posix()],
            "pwsh": ["pwsh", "-NoLogo", "-NoProfile", "-NonInteractive", "-File",
                     str(scripts / "verify-harness.ps1")],
            "python": [sys.executable, str(scripts / "verify-harness.py")],
        }
        result = subprocess.run(commands[launcher] + list(extra_args), cwd=self.temp.name,
                                capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=30)
        output = result.stdout + result.stderr
        if valid:
            self.assertEqual(result.returncode, 0, output)
        else:
            self.assertEqual(result.returncode, 1, output)
            self.assertIn("Package structure: FAIL", output)
        self.assertNotIn("Traceback (most recent call last)", output)
        return output

    def test_valid_package(self):
        self.run_harness(True)

    def test_explicit_root_with_spaces(self):
        self.run_harness(True, ("--root", str(self.root)))

    def test_missing_yaml_dependency_fails_clearly(self):
        # -S starts the real Python interpreter without site-packages.
        result = subprocess.run(
            [sys.executable, "-S", str(self.root / "scripts/verify-harness.py")],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("PyYAML is required", result.stderr)

    def test_json_syntax_is_checked_in_each_manifest(self):
        for path in MANIFESTS:
            original = (self.root / path).read_text()
            with self.subTest(path=path):
                self.write(path, '{"name": "example", INVALID}')
                self.run_harness(False)
            self.write(path, original)

    def test_manifest_required_string_fields(self):
        for field in ("name", "description"):
            for value in (None, "", "  ", 42, True, [], {}):
                with self.subTest(field=field, value=value):
                    data = {"name": "example", "description": "Valid"}
                    data[field] = value
                    self.write("plugin.json", json.dumps(data))
                    self.run_harness(False)

    def test_missing_manifest_field(self):
        self.write("plugin.json", '{"name": "example"}')
        self.run_harness(False)

    def test_duplicate_json_keys(self):
        self.write("plugin.json", '{"name":"first","name":"second","description":"ok"}')
        self.run_harness(False)

    def test_nonstandard_json_number(self):
        self.write("plugin.json", '{"name":"example","description":"ok","other":NaN}')
        self.run_harness(False)

    def test_manifest_must_be_object(self):
        self.write("plugin.json", '[{"name":"example","description":"ok"}]')
        self.run_harness(False)

    def test_marketplace_plugins_type(self):
        for value in (None, "plugins", {}, ["plugin"]):
            with self.subTest(value=value):
                self.write(MANIFESTS[2], json.dumps(
                    {"name": "example", "description": "ok", "plugins": value}))
                self.run_harness(False)

    def test_missing_marketplace_plugins(self):
        self.write(MANIFESTS[2], '{"name":"example","description":"ok"}')
        self.run_harness(False)

    def test_skill_frontmatter_cases(self):
        cases = {
            "body_only": "# No frontmatter\nname: example\ndescription: text\n",
            "unclosed": "---\nname: example\ndescription: text\n",
            "broken_yaml": "---\nname: example\ndescription: [broken\n---\n",
            "duplicate": "---\nname: one\nname: two\ndescription: text\n---\n",
            "empty": "---\nname: example\ndescription: ''\n---\n",
            "wrong_type": "---\nname: example\ndescription: [one, two]\n---\n",
            "blank_name": "---\nname: ' '\ndescription: text\n---\n",
            "numeric_name": "---\nname: 123\ndescription: text\n---\n",
            "unhashable_key": "---\n? [a, b]\n: value\nname: example\ndescription: text\n---\n",
            "unsafe_tag": "---\nname: example\ndescription: !!python/object:builtins.object {}\n---\n",
            "not_mapping": "---\n- name: example\n- description: text\n---\n",
            "missing_field": "---\nname: example\n---\ndescription: body\n",
        }
        for label, text in cases.items():
            with self.subTest(case=label):
                self.write("skills/example/SKILL.md", text)
                self.run_harness(False)

    def test_bom_crlf_and_spaces_in_skill_path(self):
        (self.root / "skills/example/SKILL.md").unlink()
        self.write("skills/space 한글/SKILL.md", "\ufeff" + VALID_SKILL.replace("\n", "\r\n"))
        self.run_harness(True)

    def test_missing_manifest(self):
        (self.root / "plugin.json").unlink()
        self.run_harness(False)

    def test_no_skills(self):
        shutil.rmtree(self.root / "skills")
        self.run_harness(False)

    def test_rule_mismatch(self):
        self.write("CODEX.md", "Different rules.\n")
        self.run_harness(False)

    def test_missing_rule(self):
        (self.root / "AGENTS.md").unlink()
        self.run_harness(False)

    def test_english_rules_match(self):
        for path in RULES:
            self.write(path.replace(".md", "_en.md"), "English rules.\n")
        self.run_harness(True)

    def test_partial_english_rules(self):
        self.write("CLAUDE_en.md", "Orphan English rules.\n")
        self.run_harness(False)

    def test_english_rule_mismatch(self):
        for path in RULES:
            self.write(path.replace(".md", "_en.md"), "English rules.\n")
        self.write("CODEX_en.md", "Different English rules.\n")
        self.run_harness(False)

    def test_invalid_utf8_is_reported(self):
        (self.root / "plugin.json").write_bytes(b"\xff")
        self.run_harness(False)

    def test_pass_message_states_verification_scope(self):
        output = self.run_harness(True)
        self.assertIn("Package structure", output)
        self.assertIn("NOT_RUN", output)


if __name__ == "__main__":
    unittest.main()
