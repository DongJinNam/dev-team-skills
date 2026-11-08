#!/usr/bin/env python3
"""Summarize paired outcome logs; never certify skill superiority."""
import argparse
import json
import math
from pathlib import Path
import re
from statistics import mean
import sys


def parse(value):
    def unique(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = item
        return result

    def reject(value):
        raise ValueError('nonfinite JSON constant: ' + value)

    return json.loads(value, object_pairs_hook=unique, parse_constant=reject)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def compare(data):
    if (not isinstance(data, dict) or type(data.get('schema_version')) is not int
            or data['schema_version'] != 1 or data.get('origin') not in ('fixture', 'measured')):
        raise ValueError('schema_version=1 and origin=fixture|measured required')
    config = data.get('config')
    fields = {'model', 'settings', 'environment', 'tasks_sha256', 'rubric_sha256'}
    if (not isinstance(config, dict) or set(config) != fields
            or not all(text(v) for v in config.values())
            or not all(re.fullmatch('[0-9a-f]{64}', config[k]) for k in ('tasks_sha256', 'rubric_sha256'))):
        raise ValueError('complete config with task/rubric SHA-256 required')
    ids = data.get('sample_ids')
    if not isinstance(ids, list) or not ids or not all(text(i) for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('nonempty unique preregistered sample_ids required')
    report = dict(origin=data['origin'], evidence_authenticated=False,
                  superiority='NOT_ESTABLISHED', sample_ids=ids, config=config)
    for name in ('baseline', 'candidate'):
        arm = data.get(name)
        if not isinstance(arm, dict) or not text(arm.get('revision')) or arm.get('config') != config:
            raise ValueError(name + ': fixed revision and identical config required')
        samples = arm.get('samples')
        if (not isinstance(samples, list) or not all(isinstance(s, dict) and text(s.get('id')) for s in samples)
                or len(samples) != len(ids) or {s['id'] for s in samples} != set(ids)):
            raise ValueError(name + ': all preregistered samples required exactly once')
        counts = dict(installation=0, activation=0, completion=0, first_pass=0)
        measures = dict(elapsed_seconds=[], total_tokens=[])
        for sample in samples:
            if (not all(type(sample.get(k)) is bool for k in ('installed', 'activated', 'passed'))
                    or not text(sample.get('evidence'))
                    or type(sample.get('interventions')) is not int or sample['interventions'] < 0):
                raise ValueError(name + ': invalid status, interventions or evidence')
            if ((sample['activated'] and not sample['installed'])
                    or (sample['passed'] and not sample['activated'])):
                raise ValueError(name + ': impossible install/activation/completion state')
            counts['installation'] += sample['installed']
            counts['activation'] += sample['activated']
            counts['completion'] += sample['passed']
            counts['first_pass'] += sample['passed'] and sample['interventions'] == 0
            for key in measures:
                value = sample.get(key)
                if value is not None:
                    types = (int,) if key == 'total_tokens' else (int, float)
                    try:
                        valid = type(value) in types and value >= 0 and math.isfinite(value)
                    except OverflowError:
                        valid = False
                    if not valid:
                        raise ValueError(name + ': invalid ' + key)
                    measures[key].append(value)
        result = {key: dict(passed=n, total=len(ids), percent=100 * n / len(ids)) for key, n in counts.items()}
        for key, values in measures.items():
            result[key] = dict(measured=len(values), total=len(ids),
                               mean=mean(values) if len(values) == len(ids) else None)
        result['revision'] = arm['revision']
        report[name] = result
    report['delta_percentage_points'] = {
        key: report['candidate'][key]['percent'] - report['baseline'][key]['percent']
        for key in ('installation', 'activation', 'completion', 'first_pass')}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        result = compare(parse(args.input.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
