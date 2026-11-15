import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("security_packet", ROOT / "scripts" / "security_packet.py")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

POLICIES = {"skills/engineering-squad/SKILL.md", "AGENTS.md"}
CAPTURE = "2026-11-11-model-routing.json"


def change(path, status="M", blob="abcdef0123456789"):
    return {"status": status, "path": path, "blob": blob}


class ClassifyTest(unittest.TestCase):
    def test_policy_change_without_capture_warns_stale(self):
        info = sp.classify([change("skills/engineering-squad/SKILL.md")], POLICIES, CAPTURE)
        self.assertIn("STALE", info["capture_status"])
        self.assertFalse(info["capture_changed"])
        self.assertEqual(info["tier"], "T2")

    def test_policy_change_with_capture_is_not_stale_warning(self):
        changes = [change("skills/engineering-squad/SKILL.md"), change(f"evals/runs/{CAPTURE}")]
        info = sp.classify(changes, POLICIES, CAPTURE)
        self.assertTrue(info["capture_changed"])
        self.assertNotIn("STALE", info["capture_status"])

    def test_docs_only_change_is_t1_and_no_stale(self):
        info = sp.classify([change("docs/decisions/example.md", status="A")], POLICIES, CAPTURE)
        self.assertEqual(info["tier"], "T1")
        self.assertEqual(info["policies_changed"], [])

    def test_workflow_change_is_t2(self):
        info = sp.classify([change(".github/workflows/example.yml")], POLICIES, CAPTURE)
        self.assertEqual(info["tier"], "T2")


class ValidateShaTest(unittest.TestCase):
    def test_accepts_short_and_full_hex(self):
        sp.validate_sha("abc1234", "--base")
        sp.validate_sha("0" * 40, "--head")

    def test_rejects_non_hex_short_uppercase_and_ref_names(self):
        for bad in ("main", "HEAD", "abc", "ABCDEF1234", "ab cd", "--upload-pack=x"):
            with self.assertRaises(ValueError, msg=bad):
                sp.validate_sha(bad, "--base")

    def test_main_rejects_bad_base_without_touching_git(self):
        self.assertEqual(sp.main(["--base", "main", "--head", "abc1234"]), 2)


class RenderTest(unittest.TestCase):
    def test_render_includes_marker_head_and_manual_notice(self):
        changes = [change("docs/example.md", status="A")]
        info = sp.classify(changes, POLICIES, CAPTURE)
        text = sp.render("base123", "head456", 32, "title", changes, "1 file changed", info)
        self.assertTrue(text.startswith(sp.MARKER))
        self.assertIn("head456", text)
        self.assertIn("판정이 아니다", text)
        self.assertIn("검증 근거 (제출자가 채운다)", text)


if __name__ == "__main__":
    unittest.main()
