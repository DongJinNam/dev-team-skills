"""Synthetic contract tests, not model usage measurements."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'evals/compare_usage.py'


def fixture():
    def arm(name, tokens):
        return {'revision': name, 'complete': True, 'samples': [
            {'id': 'task-1:repeat-1', 'actor': name,
             'quality': {'passed': True, 'reviewer': 'independent',
                         'evidence': 'private:quality/' + name},
             'discussion_rounds': 1,
             'calls': [{'id': name + '-root', 'actor': name, 'kind': 'main',
                        'input_tokens': tokens, 'output_tokens': 20,
                        'cached_input_tokens': 10, 'reasoning_output_tokens': 5,
                        'evidence': 'private:provider/' + name}]}]}
    result = {'schema_version': 1, 'origin': 'measured',
            'accounting': 'input_includes_cache_output_includes_reasoning',
            'config': {'model': 'fixture-model', 'settings': '{}',
                       'tasks_sha256': 'a' * 64, 'rubric_sha256': 'b' * 64},
            'sample_ids': ['task-1:repeat-1'],
            'baseline': arm('before', 100), 'candidate': arm('after', 70)}
    for name in ('baseline', 'candidate'):
        result[name]['config'] = copy.deepcopy(result['config'])
    return result


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'usage.json'
        self.data = fixture()

    def run_cli(self, data=None, raw=None, code=2, no_input=False, extra=()):
        args = [sys.executable, str(SCRIPT)]
        if not no_input:
            self.path.write_text(raw if raw is not None else json.dumps(
                self.data if data is None else data), encoding='utf-8')
            args.append(str(self.path))
        args.extend(extra)
        result = subprocess.run(args, capture_output=True, text=True,
                                encoding='utf-8', timeout=10)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        return json.loads(result.stdout)

    def test_paired_totals_cache_and_reasoning_are_not_added_twice(self):
        report = self.run_cli(code=0)
        self.assertEqual(report['status'], 'RECORDED_IMPROVEMENT')
        self.assertEqual(report['baseline']['total_tokens'], 120)
        self.assertEqual(report['candidate']['total_tokens'], 90)
        self.assertEqual(report['reduction_percent'], 25)
        self.assertFalse(report['provider_usage_authenticated'])

    def test_children_retries_review_and_edit_calls_are_counted(self):
        sample = self.data['candidate']['samples'][0]
        for kind in ('child', 'retry', 'review', 'edit'):
            call = copy.deepcopy(sample['calls'][0])
            call.update(id=kind, kind=kind, input_tokens=100)
            sample['calls'].append(call)
        report = self.run_cli(code=1)
        self.assertEqual(report['candidate']['calls'], 5)
        self.assertEqual(report['candidate']['total_tokens'], 570)
        self.assertEqual(report['status'], 'NO_IMPROVEMENT')

    def test_missing_usage_is_pending_not_zero(self):
        del self.data['candidate']['samples'][0]['calls'][0]['input_tokens']
        self.assertEqual(self.run_cli()['status'], 'PENDING')

    def test_missing_independent_quality_evidence_is_pending(self):
        for patch in ({'reviewer': 'after'}, {'evidence': ''}, {'passed': None}):
            data = fixture()
            data['candidate']['samples'][0]['quality'].update(patch)
            self.assertEqual(self.run_cli(data)['status'], 'PENDING')

    def test_quality_failure_blocks_savings(self):
        self.data['candidate']['samples'][0]['quality']['passed'] = False
        self.assertEqual(self.run_cli(code=1)['status'], 'QUALITY_FAILED')

    def test_fixtures_never_get_measured_success(self):
        self.data['origin'] = 'fixture'
        self.assertEqual(self.run_cli()['status'], 'HARNESS_ONLY')

    def test_incomplete_capture_is_pending(self):
        self.data['candidate']['complete'] = False
        self.assertEqual(self.run_cli()['status'], 'PENDING')

    def test_bad_counts_and_duplicate_calls_are_errors(self):
        for value in (-1, True, 1.5, '10'):
            data = fixture()
            data['candidate']['samples'][0]['calls'][0]['input_tokens'] = value
            self.assertEqual(self.run_cli(data)['status'], 'ERROR')
        sample = self.data['candidate']['samples'][0]
        sample['calls'].append(copy.deepcopy(sample['calls'][0]))
        self.assertEqual(self.run_cli()['status'], 'ERROR')

    def test_missing_or_duplicate_samples_are_errors(self):
        for samples in ([], self.data['candidate']['samples'] * 2):
            data = fixture()
            data['candidate']['samples'] = samples
            self.assertEqual(self.run_cli(data)['status'], 'ERROR')

    def test_changed_model_or_settings_is_not_comparable(self):
        self.data['candidate']['config']['model'] = 'other-model'
        self.assertEqual(self.run_cli()['status'], 'ERROR')

    def test_wrong_accounting_and_unknown_origin_are_errors(self):
        for field, value in (('accounting', 'add_cache'), ('origin', 'estimated')):
            data = fixture()
            data[field] = value
            self.assertEqual(self.run_cli(data)['status'], 'ERROR')

    def test_zero_baseline_has_no_percentage(self):
        for arm in ('baseline', 'candidate'):
            call = self.data[arm]['samples'][0]['calls'][0]
            call.update(input_tokens=0, output_tokens=0,
                        cached_input_tokens=0, reasoning_output_tokens=0)
        self.assertIsNone(self.run_cli(code=1)['reduction_percent'])

    def test_cache_subset_cannot_exceed_input(self):
        self.data['candidate']['samples'][0]['calls'][0]['cached_input_tokens'] = 1000
        self.assertEqual(self.run_cli()['status'], 'ERROR')

    def test_strict_json_and_wrong_root_do_not_crash(self):
        for raw in ('{"origin":"fixture","origin":"measured"}', '{"n":NaN}', '[]', '{}'):
            self.assertEqual(self.run_cli(raw=raw)['status'], 'ERROR')

    def test_report_is_refreshed_to_error_after_invalid_input(self):
        report_path = self.path.with_name('report.json')
        self.run_cli(code=0, extra=('--report', str(report_path)))
        self.run_cli(raw='{}', extra=('--report', str(report_path)))
        self.assertEqual(json.loads(report_path.read_text())['status'], 'ERROR')

    def test_report_cannot_overwrite_source_via_hardlink(self):
        self.path.write_text(json.dumps(self.data), encoding='utf-8')
        report_path = self.path.with_name('alias.json')
        try:
            os.link(self.path, report_path)
        except OSError:
            self.skipTest('hardlinks unavailable on this filesystem')
        original = self.path.read_bytes()
        report = self.run_cli(extra=('--report', str(report_path)))
        self.assertEqual(report['status'], 'ERROR')
        self.assertEqual(self.path.read_bytes(), original)

    def test_report_cannot_overwrite_same_source_path(self):
        report = self.run_cli(extra=('--report', str(self.path)))
        self.assertEqual(report['status'], 'ERROR')
        self.assertEqual(json.loads(self.path.read_text()), self.data)

    def test_input_size_is_bounded(self):
        raw = json.dumps(self.data) + ' ' * 5_000_001
        self.assertEqual(self.run_cli(raw=raw)['status'], 'ERROR')

    def test_no_input_is_not_run(self):
        self.assertEqual(self.run_cli(no_input=True)['status'], 'NOT_RUN')


if __name__ == '__main__':
    unittest.main()
