"""Schema and behavior tests for the Claude Code hooks (Vooy #2)."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOOKS_JSON = ROOT / "hooks" / "hooks.json"
KNOWN_EVENTS = {
    "SessionStart", "SessionEnd", "UserPromptSubmit", "Stop", "StopFailure",
    "PreToolUse", "PostToolUse", "PostToolUseFailure", "PreCompact",
    "SubagentStart", "SubagentStop", "Notification", "PreToolUseFailure",
}


def load_json_no_duplicates(path):
    def unique_object(pairs):
        data = {}
        for key, value in pairs:
            if key in data:
                raise ValueError(f"duplicate JSON key: {key}")
            data[key] = value
        return data
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HooksSchemaTests(unittest.TestCase):
    def test_hooks_json_wrapper_and_events(self):
        data = load_json_no_duplicates(HOOKS_JSON)
        self.assertEqual(set(data), {"hooks"})
        self.assertIn("SessionStart", data["hooks"])
        self.assertIn("Stop", data["hooks"])
        for event, groups in data["hooks"].items():
            self.assertIn(event, KNOWN_EVENTS, f"unknown hook event: {event}")
            self.assertIsInstance(groups, list)
            self.assertTrue(groups, f"{event} has no matcher groups")
            for group in groups:
                self.assertIsInstance(group["hooks"], list)
                self.assertTrue(group["hooks"])
                for hook in group["hooks"]:
                    self.assertEqual(hook["type"], "command")
                    self.assertIsInstance(hook["command"], str)
                    self.assertTrue(hook["command"].strip())
                    self.assertIn("${CLAUDE_PLUGIN_ROOT}", hook["command"])
                    timeout = hook.get("timeout", 60)
                    self.assertIsInstance(timeout, int)
                    self.assertTrue(1 <= timeout <= 600)

    def test_hook_scripts_exist_and_are_python(self):
        data = load_json_no_duplicates(HOOKS_JSON)
        for groups in data["hooks"].values():
            for group in groups:
                for hook in group["hooks"]:
                    command = hook["command"]
                    script = command.split("${CLAUDE_PLUGIN_ROOT}/", 1)[1]
                    script = script.split('"')[0].strip()
                    path = ROOT / script
                    self.assertTrue(path.is_file(), f"hook script missing: {script}")
                    self.assertEqual(path.suffix, ".py")

    def test_plugin_json_declares_hooks_file(self):
        manifest = load_json_no_duplicates(ROOT / ".claude-plugin" / "plugin.json")
        self.assertEqual(manifest["hooks"], "./hooks/hooks.json")
        self.assertTrue((ROOT / manifest["hooks"]).is_file())

    def test_session_start_prints_entry_skill_and_exits_zero(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "hooks" / "session_start.py")],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0)
        self.assertIn("skills/using-dev-team-skills/SKILL.md", result.stdout)
        self.assertIn("verify-harness", result.stdout)


class StopGateTests(unittest.TestCase):
    def setUp(self):
        self.gate = load_module("stop_gate", ROOT / "hooks" / "stop_gate.py")

    def test_allow_when_harness_passes(self):
        allow, _ = self.gate.decide(False, True)
        self.assertTrue(allow)

    def test_block_when_harness_fails(self):
        allow, reason = self.gate.decide(False, False)
        self.assertFalse(allow)
        self.assertIn("verify-harness", reason)

    def test_allow_on_second_stop_to_avoid_loop(self):
        allow, _ = self.gate.decide(True, False)
        self.assertTrue(allow)

    def test_stop_gate_allows_on_clean_tree(self):
        payload = json.dumps({"stop_hook_active": False})
        result = subprocess.run(
            [sys.executable, str(ROOT / "hooks" / "stop_gate.py")],
            input=payload, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_stop_gate_blocks_when_verifier_fails(self):
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp)
            (fake / "hooks").mkdir()
            (fake / "scripts").mkdir()
            shutil.copy(ROOT / "hooks" / "stop_gate.py",
                        fake / "hooks" / "stop_gate.py")
            verifier = fake / "scripts" / "verify-harness.py"
            verifier.write_text("import sys; sys.exit(1)\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(fake / "hooks" / "stop_gate.py")],
                input=json.dumps({"stop_hook_active": False}),
                capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("verify-harness", result.stderr)

    def test_stop_gate_allows_when_verifier_missing(self):
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp)
            (fake / "hooks").mkdir()
            shutil.copy(ROOT / "hooks" / "stop_gate.py",
                        fake / "hooks" / "stop_gate.py")
            result = subprocess.run(
                [sys.executable, str(fake / "hooks" / "stop_gate.py")],
                input=json.dumps({"stop_hook_active": False}),
                capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
