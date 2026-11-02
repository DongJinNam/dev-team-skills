#!/usr/bin/env python3
"""Decision regression checks; a decision PASS never proves tool execution."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
POLICIES = (
    'AGENTS.md', 'skills/engineering-squad/SKILL.md',
    'skills/engineering-squad/references/superpowers-compatibility.md',
    'skills/engineering-squad/references/roles.md',
    'skills/engineering-squad/references/security-review.md',
    'skills/engineering-squad/references/report-summary.md', 'skills/ponytail/SKILL.md',
)
ACTIONS = (
    'run_tests', 'claim_complete', 'merge', 'request_security_review',
    'reuse_security_pass', 'collect_votes', 'adopt', 'invent_votes', 'stop',
    'report_to_user', 'await_resume', 'retry', 'resume',
    'measure_production_like_load', 'agree_acceptance_criteria',
    'claim_production_gain', 'roll_out', 'check_diff', 'check_documentation',
    'run_full_runtime_suite', 'claim_fresh_runtime_pass',
    'record_workflow_owners', 'reuse_confirmed_artifacts', 'use_qualified_skill',
    'use_dev_planning', 'request_delta_confirmation', 'repeat_full_discovery',
    'repeat_start_questions', 'auto_install_superpowers', 'claim_superpowers_execution',
    'reuse_spec_after_scope_change',
)
CONTRACT = {
    'decision': ['READY', 'PENDING', 'BLOCKED', 'CONDITIONAL'],
    'actions': list(ACTIONS),
    'facts': 'Object of relevant facts; tests/security/runtime_tests are status strings, '
             'yes/no/pending are integer ballot counts, resume_authorized is a boolean, '
             'production_effect is VERIFIED or UNVERIFIED. Preserve facts; do not invent evidence.',
    'summary': 'Array of complete sentences explaining the decision, next actions and evidence.',
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def unique_object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise ValueError(f'duplicate JSON key: {key}')
        data[key] = value
    return data


def reject_constant(value):
    raise ValueError(f'nonstandard JSON constant: {value}')


def parse(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def snapshot():
    return {p: hashlib.sha256((ROOT / p).read_text(encoding='utf-8-sig').encode('utf-8')).hexdigest()
            for p in (*POLICIES, 'evals/scenarios.json', 'evals/run_evals.py')}


def request(case):
    # Expectations stay in the scorer; the candidate sees inputs and policy only.
    return {'case_id': case['id'], 'prompt': case['prompt'],
            'policies': {p: (ROOT / p).read_text(encoding='utf-8') for p in POLICIES},
            'response_contract': CONTRACT}


def evaluate(record, cases, mode):
    report = {'mode': mode, 'status': 'FAIL', 'tool_execution': 'NOT_OBSERVED',
              'provenance': 'Operator-supplied, not cryptographically authenticated.',
              'cases': []}
    if not isinstance(record, dict) or type(record.get('schema_version')) is not int or record['schema_version'] != 1:
        raise ValueError('unsupported record schema_version')
    if record.get('origin') not in ('agent', 'fixture'):
        raise ValueError('origin must be agent or fixture')
    if not isinstance(record.get('capture'), dict) or not record['capture'].get('method'):
        raise ValueError('capture method is required')
    if record.get('snapshot') != snapshot():
        report['status'] = 'STALE'
        return report
    results = record.get('results')
    if not isinstance(results, list):
        raise ValueError('results must be an array')
    ids = [row.get('case_id') if isinstance(row, dict) else None for row in results]
    if len(ids) != len(cases) or sorted(str(i) for i in ids) != sorted(c['id'] for c in cases):
        report['error'] = 'Missing, duplicate or unknown cases; the entire suite is required.'
        return report
    has_failure = False
    needs_review = False
    for case in cases:
        row = next(r for r in results if r['case_id'] == case['id'])
        response = row.get('response')
        failures = []
        if not isinstance(response, dict) or set(response) != set(CONTRACT):
            failures.append('response must contain exactly decision/actions/facts/summary')
        else:
            expected = case['expected']
            actions = response['actions']
            facts = response['facts']
            summary = response['summary']
            if response['decision'] != expected['decision']:
                failures.append('decision contradicts the scenario contract')
            if (not isinstance(actions, list) or not all(isinstance(a, str) and a in ACTIONS for a in actions)
                    or len(set(actions)) != len(actions)):
                failures.append('actions must be unique allowed action identifiers')
            else:
                if not set(expected['required_actions']).issubset(actions):
                    failures.append('required action missing')
                if set(expected['forbidden_actions']).intersection(actions):
                    failures.append('forbidden action proposed')
            if not isinstance(facts, dict):
                failures.append('facts must be an object')
            else:
                for key, value in expected['facts'].items():
                    if type(facts.get(key)) is not type(value) or facts[key] != value:
                        failures.append(f'fact mismatch: {key}')
                for key, values in expected.get('allowed_facts', {}).items():
                    if not any(type(facts.get(key)) is type(v) and facts[key] == v for v in values):
                        failures.append(f'fact mismatch: {key}')
            if (not isinstance(summary, list) or not summary
                    or not all(isinstance(s, str) and s.strip() for s in summary)):
                failures.append('summary must be a nonempty array of nonblank strings')
            elif 'summary_sentences' in expected and len(summary) != expected['summary_sentences']:
                failures.append('wrong summary slot count; sentence meaning needs separate review')
        review = row.get('review', {})
        actor = row.get('actor')
        valid_review = (
            isinstance(actor, str) and bool(actor.strip())
            and isinstance(review, dict) and isinstance(review.get('reviewer'), str)
            and bool(review['reviewer'].strip()) and review['reviewer'] != actor
            and review.get('response_sha256') == digest(response)
            and review.get('snapshot_sha256') == digest(record['snapshot'])
            and isinstance(review.get('notes'), str) and bool(review['notes'].strip())
            and type(review.get('passed')) is bool
        )
        if valid_review and not review['passed']:
            failures.append('independent semantic review rejected the response')
        status = 'FAIL' if failures else ('PASS' if valid_review else 'REVIEW_REQUIRED')
        has_failure |= bool(failures)
        needs_review |= not valid_review
        report['cases'].append({'id': case['id'], 'status': status, 'failures': failures})
    report['status'] = ('FAIL' if has_failure else 'HARNESS_ONLY' if record['origin'] == 'fixture'
                        else 'REVIEW_REQUIRED' if needs_review else 'PASS')
    return report


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--replay', type=Path)
    mode.add_argument('--export-prompts', type=Path)
    mode.add_argument('--runner', nargs=argparse.REMAINDER,
                      help='Explicit adapter argv; receives one JSON request on stdin per process.')
    parser.add_argument('--output', type=Path, help='Capture file for adapter responses.')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--origin', choices=('agent', 'fixture'), default='fixture',
                        help='Operator attestation for adapter capture; fixtures cannot get agent PASS.')
    parser.add_argument('--timeout', type=float, default=30)
    args = parser.parse_args()
    try:
        cases = parse((ROOT / 'evals/scenarios.json').read_text(encoding='utf-8'))['cases']
        if args.export_prompts:
            for case in cases:
                write_json(args.export_prompts / (case['id'] + '.json'), request(case))
            report = {'status': 'EXPORTED', 'count': len(cases), 'tool_execution': 'NOT_OBSERVED'}
        elif args.replay:
            report = evaluate(parse(args.replay.read_text(encoding='utf-8')), cases, 'REPLAY')
        elif args.runner:
            if not 0 < args.timeout <= 60:
                raise ValueError('timeout must be greater than 0 and at most 60 seconds per case')
            record = {'schema_version': 1, 'origin': args.origin, 'snapshot': snapshot(),
                      'capture': {'method': 'explicit_subprocess_adapter', 'argv': args.runner},
                      'results': []}
            for case in cases:
                result = subprocess.run(args.runner, input=json.dumps(request(case)),
                                        text=True, encoding='utf-8', capture_output=True,
                                        timeout=args.timeout, shell=False)
                if result.returncode:
                    raise ValueError(f'{case["id"]}: adapter exited {result.returncode}; no decision PASS')
                record['results'].append({'case_id': case['id'], 'actor': 'adapter:' + case['id'],
                                          'response': parse(result.stdout)})
            if args.output:
                write_json(args.output, record)
            report = evaluate(record, cases, 'ADAPTER')
        else:
            report = {'status': 'NOT_RUN', 'tool_execution': 'NOT_OBSERVED',
                      'reason': 'Supply an explicit runner, native capture replay, or export destination.'}
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        report = {'status': 'ERROR', 'tool_execution': 'NOT_OBSERVED',
                  'reason': str(error)[:500]}
    if args.report:
        write_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] in ('PASS', 'EXPORTED') else 1 if report['status'] == 'FAIL' else 2


if __name__ == '__main__':
    sys.exit(main())
