#!/usr/bin/env python3
"""Compare paired operator-supplied usage logs; never execute trace references."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile

KINDS = ('main', 'child', 'retry', 'review', 'edit')
ACCOUNTING = 'input_includes_cache_output_includes_reasoning'
COUNTS = ('input_tokens', 'output_tokens', 'cached_input_tokens', 'reasoning_output_tokens')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('nonstandard JSON constant: ' + value)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def count(value):
    return type(value) is int and value >= 0


def compare(record):
    report = {'status': 'PENDING', 'provider_usage_authenticated': False,
              'security_approval': 'NOT_ASSESSED',
              'scope': 'Operator-supplied paired logs only; no causal or reliability claim.'}
    if not isinstance(record, dict) or type(record.get('schema_version')) is not int or record['schema_version'] != 1:
        raise ValueError('schema_version must be 1')
    if record.get('origin') not in ('measured', 'fixture') or record.get('accounting') != ACCOUNTING:
        raise ValueError('unsupported origin or token accounting')
    config = record.get('config')
    if (not isinstance(config, dict) or set(config) != {'model', 'settings', 'tasks_sha256', 'rubric_sha256'}
            or not all(text(v) for v in config.values())
            or not all(re.fullmatch('[0-9a-f]{64}', config[k]) for k in ('tasks_sha256', 'rubric_sha256'))):
        raise ValueError('config requires model, serialized settings and task/rubric SHA-256')
    ids = record.get('sample_ids')
    if not isinstance(ids, list) or not ids or not all(text(i) for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('sample_ids must be a nonempty unique list')
    pending, quality_failures, seen_calls = [], [], set()
    totals, per_sample = {}, {}
    for name in ('baseline', 'candidate'):
        arm = record.get(name)
        if not isinstance(arm, dict) or not text(arm.get('revision')) or arm.get('config') != config:
            raise ValueError(name + ': revision and identical config required')
        if arm.get('complete') is not True:
            pending.append(name + ': full call capture not attested')
        samples = arm.get('samples')
        if not isinstance(samples, list) or not all(isinstance(s, dict) and text(s.get('id')) for s in samples):
            raise ValueError(name + ': samples must be objects with ids')
        actual = [s['id'] for s in samples]
        if len(set(actual)) != len(actual) or set(actual) != set(ids):
            raise ValueError(name + ': missing, duplicate or unknown samples')
        total = {'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0,
                 'calls': 0, 'discussion_rounds': 0,
                 'calls_by_kind': {k: 0 for k in KINDS}}
        per_sample[name] = {}
        for sample in samples:
            label = name + '/' + sample['id']
            if not text(sample.get('actor')):
                raise ValueError(label + ': actor required')
            quality = sample.get('quality')
            if isinstance(quality, dict) and quality.get('passed') is False:
                quality_failures.append(label)
            if (not isinstance(quality, dict) or type(quality.get('passed')) is not bool
                    or not text(quality.get('reviewer')) or quality['reviewer'] == sample['actor']
                    or not text(quality.get('evidence'))):
                pending.append(label + ': independent quality evidence missing')
            rounds = sample.get('discussion_rounds')
            if rounds is None:
                pending.append(label + ': discussion rounds missing')
            elif not count(rounds):
                raise ValueError(label + ': invalid discussion rounds')
            else:
                total['discussion_rounds'] += rounds
            calls = sample.get('calls')
            if calls is None or calls == []:
                pending.append(label + ': invocation usage missing')
                continue
            if not isinstance(calls, list):
                raise ValueError(label + ': calls must be an array')
            sample_tokens = 0
            for call in calls:
                if (not isinstance(call, dict) or not text(call.get('id'))
                        or not text(call.get('actor')) or call.get('kind') not in KINDS):
                    raise ValueError(label + ': invalid invocation identity/kind')
                if call['id'] in seen_calls:
                    raise ValueError('duplicate invocation id (including across arms)')
                seen_calls.add(call['id'])
                total['calls'] += 1
                total['calls_by_kind'][call['kind']] += 1
                if not text(call.get('evidence')):
                    pending.append(label + ': provider evidence missing')
                for key in COUNTS:
                    value = call.get(key)
                    if value is None:
                        pending.append(label + ': ' + key + ' missing')
                    elif not count(value):
                        raise ValueError(label + ': invalid token count: ' + key)
                if any(call.get(k) is None for k in COUNTS):
                    continue
                if (call['cached_input_tokens'] > call['input_tokens']
                        or call['reasoning_output_tokens'] > call['output_tokens']):
                    raise ValueError(label + ': cache/reasoning must be subsets')
                total['input_tokens'] += call['input_tokens']
                total['output_tokens'] += call['output_tokens']
                sample_tokens += call['input_tokens'] + call['output_tokens']
            per_sample[name][sample['id']] = sample_tokens
        total['total_tokens'] = total['input_tokens'] + total['output_tokens']
        totals[name] = total
    report['origin'] = record['origin']
    if quality_failures:
        report.update(status='QUALITY_FAILED', quality_failures=quality_failures)
    elif pending:
        report.update(status='PENDING', missing_evidence=pending)
    else:
        before, after = (totals[k]['total_tokens'] for k in ('baseline', 'candidate'))
        report.update(totals, sample_tokens=per_sample, saved_tokens=before - after,
                      reduction_percent=(100 * (before - after) / before if before else None),
                      sample_count=len(ids))
        report['status'] = ('HARNESS_ONLY' if record['origin'] == 'fixture' else
                            'RECORDED_IMPROVEMENT' if after < before else 'NO_IMPROVEMENT')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', nargs='?', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    error_report = {'status': 'ERROR', 'reason':
                    'Invalid record or inaccessible input/report. See schema and private logs.'}
    protected = False
    try:
        if args.report and args.record:
            # samefile covers hardlinks; resolve also covers nonexistent same paths.
            protected = (args.report.resolve() == args.record.resolve()
                         or (args.report.exists() and args.record.exists()
                             and args.report.samefile(args.record)))
            if protected:
                raise ValueError('report aliases source')
        if args.record is None:
            report = {'status': 'NOT_RUN', 'reason': 'Supply a normalized usage record.'}
        else:
            with args.record.open('rb') as source:
                raw = source.read(5_000_001)
            if len(raw) > 5_000_000:
                raise ValueError('record exceeds five million bytes')
            record = json.loads(raw.decode('utf-8-sig'),
                                object_pairs_hook=unique_object, parse_constant=reject_constant)
            report = compare(record)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, OverflowError, RecursionError):
        report = dict(error_report)
    if args.report and not protected:
        temporary = None
        try:
            # Atomic replacement preserves evidence even if a path alias changes.
            # Refresh ERROR reports too, so an earlier success cannot survive bad input.
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                             dir=args.report.parent, delete=False) as output:
                temporary = Path(output.name)
                output.write(json.dumps(report, ensure_ascii=True, indent=2) + '\n')
            os.replace(temporary, args.report)
        except OSError:
            report = dict(error_report)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return (0 if report['status'] == 'RECORDED_IMPROVEMENT' else
            1 if report['status'] in ('QUALITY_FAILED', 'NO_IMPROVEMENT') else 2)


if __name__ == '__main__':
    sys.exit(main())
