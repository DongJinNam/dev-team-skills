"""Hidden functional checks. Run candidates only in a subprocess, not this process.

Process separation is not a sandbox: execute only in the authorized pilot workspace.
Do not give this module or its reference tests to the candidate agent.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

from evals.pilot.tasks import TASKS


WORKER = '''import copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
requests = json.load(sys.stdin)
answers = []
for request in requests:
    args = request['args']
    original = copy.deepcopy(args)
    try:
        value = getattr(module, request['function'])(*args, **request.get('kwargs', {}))
        answers.append({'result': value, 'unchanged': args == original})
    except ValueError:
        answers.append({'error': 'ValueError', 'unchanged': args == original})
    except Exception as error:
        answers.append({'error': type(error).__name__, 'unchanged': args == original})
print(json.dumps(answers, allow_nan=False))
'''


def _cases(task):
    cases = []
    if task == 'bugfix':
        valid = [('', {}), (' \n\t\n', {}),
                 ('{"id":"a","category":"x","amount":0}', {'x': 0}),
                 ('\n{"id":"a","category":"x","amount":2}\n\n'
                  '{"id":"b","category":"x","amount":3}\n'
                  '{"id":"a","category":"y","amount":100}', {'x': 5}),
                 ('{"id":" a","category":" x","amount":4}\n'
                  '{"id":"a","category":"x","amount":7}', {' x': 4, 'x': 7}),
                 (json.dumps({'id': '한', 'category': '글', 'amount': 10**30}), {'글': 10**30})]
        cases.extend(({'function': 'summarize', 'args': [text]}, {'result': expected, 'unchanged': True})
                     for text, expected in valid)
        invalid = ['no-json', '[]', 'null', 'true', '12', '{}']
        base = {'id': 'a', 'category': 'x', 'amount': 1}
        for field, values in [('id', ['', '  ', None, 1, False]),
                              ('category', ['', '\t', None, [], True]),
                              ('amount', [-1, 1.5, True, False, '2', None])]:
            for value in values:
                invalid.append(json.dumps(dict(base, **{field: value})))
            invalid.append(json.dumps({k: v for k, v in base.items() if k != field}))
        invalid.append(json.dumps(base) + '\n' + json.dumps(dict(base, amount=-1)))
        cases.extend(({'function': 'summarize', 'args': [text]}, {'error': 'ValueError', 'unchanged': True})
                     for text in invalid)
    else:
        for items, kwargs in [([], {}), ([1, 2, 3], {}), (list(range(23)), {}),
                              (list(range(7)), {'page': 2, 'page_size': 3}),
                              ([3, 1, 2], {'page': 3, 'page_size': 1}),
                              ([3, 1, 2], {'page': 4, 'page_size': 1}),
                              ([{'x': 1}, None, 'a'], {'page_size': 2})]:
            page, size = kwargs.get('page', 1), kwargs.get('page_size', 20)
            expected = dict(items=items[(page-1)*size:page*size], total=len(items),
                            page=page, page_size=size, pages=(len(items)+size-1)//size)
            cases.append(({'function': 'paginate', 'args': [items], 'kwargs': kwargs},
                          {'result': expected, 'unchanged': True}))
        for key in ('page', 'page_size'):
            for value in [0, -1, True, False, 1.0, '2', None]:
                cases.append(({'function': 'paginate', 'args': [[]], 'kwargs': {key: value}},
                              {'error': 'ValueError', 'unchanged': True}))
    return cases


def score(task_id, workspace):
    if task_id not in TASKS:
        raise ValueError('unknown task')
    root = Path(workspace).resolve()
    failures = []
    if task_id == 'docs':
        total = 5
        try:
            text = (root / 'README.md').read_text(encoding='utf-8')
            checks = [
                bool(re.search(r'(?:python(?:3)?|py -3)\s+toy_cli\.py\s+setup\s+--source\s+["\']?\.["\']?(?=\s|`|$)', text)),
                bool(re.search(r'(?:python(?:3)?|py -3)\s+toy_cli\.py\s+verify\s+--json(?=\s|`|$)', text)),
                not re.search(r'\bdeploy\b|--repo\b', text),
                '100%' not in text,
                (root / 'toy_cli.py').read_text(encoding='utf-8') == TASKS['docs']['files']['toy_cli.py'],
            ]
            failures = [f'docs-check-{i+1}' for i, passed in enumerate(checks) if not passed]
        except (OSError, UnicodeError):
            failures = [f'docs-check-{i+1}' for i in range(total)]
    else:
        cases = _cases(task_id)
        total = len(cases)
        try:
            completed = subprocess.run(
                [sys.executable, '-I', '-B', '-c', WORKER, str(root / 'app.py')],
                input=json.dumps([request for request, _ in cases]),
                text=True, encoding='utf-8', capture_output=True, cwd=root, timeout=15)
            answers = json.loads(completed.stdout) if completed.returncode == 0 else None
            if not isinstance(answers, list) or len(answers) != total:
                raise ValueError('invalid candidate response')
            failures = [f'case-{i+1}' for i, (answer, (_, expected)) in enumerate(zip(answers, cases))
                        if json.dumps(answer, sort_keys=True) != json.dumps(expected, sort_keys=True)]
        except (OSError, ValueError, UnicodeError, subprocess.TimeoutExpired):
            failures = [f'case-{i+1}' for i in range(total)]
    return dict(passed=not failures, checks_passed=total-len(failures),
                checks_total=total, failures=failures)
