"""Unit tests for the comparative benchmark metrics calculator."""

import json
from pathlib import Path
import tempfile
import unittest

from evals.benchmark_metrics import calculate_metrics, format_markdown_table


class BenchmarkMetricsTests(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "schema_version": 1,
            "scenarios_19_compliance": [
                {
                    "id": "case-1",
                    "vanilla": {"passed": False},
                    "unbounded": {"passed": True},
                    "dev_team_skills": {"passed": True},
                },
                {
                    "id": "case-2",
                    "vanilla": {"passed": True},
                    "unbounded": {"passed": False},
                    "dev_team_skills": {"passed": True},
                },
            ],
            "multi_turn_workflows": [
                {
                    "task_id": "task-1",
                    "tokens": {
                        "vanilla_agent": 10000,
                        "unbounded_multiagent": 20000,
                        "dev_team_skills": 12000,
                    },
                    "turns": {
                        "vanilla_agent": 2,
                        "unbounded_multiagent": 6,
                        "dev_team_skills": 3,
                    },
                    "defects_caught": {
                        "vanilla_agent": 1,
                        "unbounded_multiagent": 2,
                        "dev_team_skills": 2,
                    },
                    "total_defects_injected": 2,
                }
            ],
        }

    def test_calculate_metrics_accurate_ratios(self):
        metrics = calculate_metrics(self.sample_data)
        self.assertEqual(metrics["compliance_rates"]["dev_team_skills"], 100.0)
        self.assertEqual(metrics["compliance_rates"]["vanilla_agent"], 50.0)
        self.assertEqual(metrics["compliance_rates"]["unbounded_multiagent"], 50.0)

        # Token savings: (20000 - 12000) / 20000 = 40.0%
        self.assertEqual(metrics["tokens"]["savings_vs_unbounded_pct"], 40.0)

        # Turn reduction: (6 - 3) / 6 = 50.0%
        self.assertEqual(metrics["turns"]["reduction_vs_unbounded_pct"], 50.0)

        # Defect catch rate: 2 / 2 = 100.0%
        self.assertEqual(metrics["defect_rates"]["dev_team_skills"], 100.0)
        self.assertEqual(metrics["defect_rates"]["vanilla_agent"], 50.0)

    def test_empty_scenarios_raises_value_error(self):
        data = {"scenarios_19_compliance": [], "multi_turn_workflows": [{"task_id": "t"}]}
        with self.assertRaises(ValueError):
            calculate_metrics(data)

    def test_empty_workflows_raises_value_error(self):
        data = {"scenarios_19_compliance": [{"id": "c"}], "multi_turn_workflows": []}
        with self.assertRaises(ValueError):
            calculate_metrics(data)

    def test_format_markdown_table(self):
        metrics = calculate_metrics(self.sample_data)
        table = format_markdown_table(metrics)
        self.assertIn("규정 준수/안전 방어율", table)
        self.assertIn("100.0%", table)
        self.assertIn("토큰 절감", table)

    def test_committed_benchmark_file_integrity(self):
        repo_root = Path(__file__).resolve().parents[1]
        benchmark_file = repo_root / "evals" / "runs" / "2026-11-07-comparative-benchmark.json"
        self.assertTrue(benchmark_file.exists())
        with open(benchmark_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        metrics = calculate_metrics(data)
        self.assertEqual(metrics["compliance_rates"]["total_cases"], 19)
        self.assertEqual(metrics["compliance_rates"]["dev_team_skills"], 100.0)
        self.assertGreater(metrics["tokens"]["savings_vs_unbounded_pct"], 30.0)
        self.assertGreater(metrics["turns"]["reduction_vs_unbounded_pct"], 50.0)
        self.assertEqual(metrics["defect_rates"]["dev_team_skills"], 100.0)


if __name__ == "__main__":
    unittest.main()
