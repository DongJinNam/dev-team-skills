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
    def _fixture_repo(self, tmp):
        # Two commits: the first references capture-a, the second capture-b.
        # The test must not depend on this repo's own history depth, because
        # CI checks out shallowly and old commits are not available there.
        import subprocess

        def run(*args):
            subprocess.run(["git", *args], cwd=tmp, check=True, capture_output=True, text=True)

        run("init", "-q")
        run("config", "user.email", "test@example.com")
        run("config", "user.name", "test")
        workflow = tmp / ".github" / "workflows"
        workflow.mkdir(parents=True)
        (workflow / "verify-rules-sync.yml").write_text("run: bash evals/run-evals.sh --replay evals/runs/capture-a.json\n", encoding="utf-8")
        run("add", ".")
        run("commit", "-q", "-m", "first")
        first = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp, check=True, capture_output=True, text=True).stdout.strip()
        (workflow / "verify-rules-sync.yml").write_text("run: bash evals/run-evals.sh --replay evals/runs/capture-b.json\n", encoding="utf-8")
        run("add", ".")
        run("commit", "-q", "-m", "second")
        second = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp, check=True, capture_output=True, text=True).stdout.strip()
        return first, second

    def test_capture_reference_comes_from_base(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            first, second = self._fixture_repo(Path(tmp))
            self.assertEqual(cp.current_capture_name(first, repo_root=Path(tmp)), "capture-a.json")
            self.assertEqual(cp.current_capture_name(second, repo_root=Path(tmp)), "capture-b.json")

    def test_missing_base_commit_fails_loudly(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            self._fixture_repo(Path(tmp))
            with self.assertRaises(RuntimeError):
                cp.current_capture_name("0" * 40, repo_root=Path(tmp))


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
