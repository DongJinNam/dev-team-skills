"""Outcome reports must retain failures and distinguish unknown measurements."""
import copy
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('outcomes', Path(__file__).resolve().parents[1] / 'evals/compare_outcomes.py')
outcomes = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(outcomes)


def record():
    config = dict(model='fixed', settings='fixed', environment='Windows/client/version/clean',
                  tasks_sha256='a' * 64, rubric_sha256='b' * 64)
    samples = [dict(id='one', installed=True, activated=True, passed=True,
                    interventions=0, elapsed_seconds=10, total_tokens=100, evidence='log-1'),
               dict(id='two', installed=False, activated=False, passed=False,
                    interventions=0, elapsed_seconds=5, total_tokens=None, evidence='log-2')]
    arm = dict(revision='fixed-revision', config=config, samples=samples)
    return dict(schema_version=1, origin='fixture', sample_ids=['one', 'two'],
                config=config, baseline=copy.deepcopy(arm), candidate=copy.deepcopy(arm))


class OutcomeTests(unittest.TestCase):
    def test_failures_in_denominator_and_fixture_label(self):
        report = outcomes.compare(record())
        self.assertEqual(report['origin'], 'fixture')
        self.assertEqual(report['candidate']['first_pass'], {'passed': 1, 'total': 2, 'percent': 50.0})
        self.assertEqual(report['candidate']['elapsed_seconds']['mean'], 7.5)
        self.assertIsNone(report['candidate']['total_tokens']['mean'])
        self.assertEqual(report['candidate']['total_tokens']['measured'], 1)
        self.assertEqual(report['superiority'], 'NOT_ESTABLISHED')
        self.assertFalse(report['evidence_authenticated'])

    def test_intervention_prevents_first_pass_but_not_completion(self):
        data = record()
        data['candidate']['samples'][0]['interventions'] = 1
        report = outcomes.compare(data)
        self.assertEqual(report['candidate']['completion']['percent'], 50)
        self.assertEqual(report['candidate']['first_pass']['percent'], 0)
        self.assertEqual(report['delta_percentage_points']['first_pass'], -50)

    def test_invalid_records_rejected(self):
        mutations = [
            lambda d: d.update(sample_ids=[]),
            lambda d: d.update(schema_version=True),
            lambda d: d['candidate']['samples'].pop(),
            lambda d: d['candidate']['samples'][1].update(id='one'),
            lambda d: d['candidate']['config'].update(environment='different'),
            lambda d: d['candidate']['samples'][1].update(activated=True),
            lambda d: d['candidate']['samples'][1].update(passed=True),
            lambda d: d['candidate']['samples'][0].update(elapsed_seconds=float('nan')),
            lambda d: d['candidate']['samples'][0].update(elapsed_seconds=-1),
            lambda d: d['candidate']['samples'][0].update(elapsed_seconds=10**400),
            lambda d: d['candidate']['samples'][0].update(total_tokens=10**400),
            lambda d: d['candidate']['samples'][0].update(total_tokens=True),
            lambda d: d['candidate']['samples'][0].update(interventions=-1),
            lambda d: d['candidate']['samples'][0].update(evidence=''),
        ]
        for mutation in mutations:
            data = record()
            mutation(data)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                outcomes.compare(data)

    def test_json_rejects_duplicates_and_nonfinite_constants(self):
        for value in ('{"a":1,"a":2}', '{"x":NaN}'):
            with self.assertRaises(ValueError):
                outcomes.parse(value)

    def test_measured_is_not_authentication_or_superiority(self):
        data = record()
        data['origin'] = 'measured'
        report = outcomes.compare(data)
        self.assertFalse(report['evidence_authenticated'])
        self.assertEqual(report['superiority'], 'NOT_ESTABLISHED')

    def test_large_finite_measurements_do_not_overflow_mean(self):
        data = record()
        for sample in data['candidate']['samples']:
            sample['elapsed_seconds'] = 1e308
        self.assertEqual(outcomes.compare(data)['candidate']['elapsed_seconds']['mean'], 1e308)


if __name__ == '__main__':
    unittest.main()
