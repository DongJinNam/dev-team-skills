import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("capture_plan", ROOT / "scripts" / "capture_plan.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

POLICIES = {"skills/engineering-squad/SKILL.md", "AGENTS.md"}
CAPTURE = "2026-11-11-model-routing.json"
CASES = ["test-pressure", "stale-security"]


class ClassifyTest(unittest.TestCase):
    def test_policy_change_needs_renewal(self):
        info = cp.classify(["skills/engineering-squad/SKILL.md"], POLICIES, CAPTURE)
        self.assertTrue(info["needs_renewal"])
        self.assertEqual(info["policies_changed"], ["skills/engineering-squad/SKILL.md"])
        self.assertFalse(info["capture_changed"])

    def test_docs_only_change_needs_no_renewal(self):
        info = cp.classify(["docs/decisions/example.md"], POLICIES, CAPTURE)
        self.assertFalse(info["needs_renewal"])
        self.assertEqual(info["policies_changed"], [])

    def test_scenarios_change_needs_renewal(self):
        info = cp.classify(["evals/scenarios.json"], POLICIES, CAPTURE)
        self.assertTrue(info["needs_renewal"])
        self.assertTrue(info["scenarios_changed"])

    def test_new_capture_in_range_is_flagged(self):
        info = cp.classify([f"evals/runs/{CAPTURE}"], POLICIES, CAPTURE)
        self.assertTrue(info["capture_changed"])


class CaptureNameTest(unittest.TestCase):
    def test_capture_reference_comes_from_base(self):
        # Before PR #31 the workflow referenced the work-minutes capture;
        # at its head it referenced the model-routing capture.
        self.assertEqual(cp.current_capture_name("8f890bfa9a67e282a172b54c50485fb186fb72a2"), "2026-11-11-work-minutes.json")
        self.assertEqual(cp.current_capture_name("c76c05c9fc35054a5bec04d3ddb53e1cc711c4c9"), "2026-11-11-model-routing.json")


class RenderTest(unittest.TestCase):
    def test_plan_lists_cases_and_output_path(self):
        info = cp.classify(["skills/engineering-squad/SKILL.md"], POLICIES, CAPTURE)
        text = cp.render("base1", "head2", "2026-11-12", "example", CASES, CAPTURE, info)
        self.assertIn("evals/runs/2026-11-12-example.json", text)
        self.assertIn("1. test-pressure", text)
        self.assertIn("2. stale-security", text)
        self.assertIn("capture-runbook.md", text)
        self.assertIn("attempt<N>", text)

    def test_no_renewal_plan_says_so(self):
        info = cp.classify(["docs/example.md"], POLICIES, CAPTURE)
        text = cp.render("base1", "head2", "2026-11-12", "example", CASES, CAPTURE, info)
        self.assertIn("No renewal is needed", text)


if __name__ == "__main__":
    unittest.main()
