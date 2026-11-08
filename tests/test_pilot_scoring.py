import tempfile
import unittest
from pathlib import Path

from evals.pilot.tasks import TASKS
from evals.pilot.score import score


REFERENCES = {
    'bugfix': '''import json
def summarize(text):
    result, seen = {}, set()
    for line in text.splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError('object required')
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in ('id', 'category')):
            raise ValueError('invalid identifier')
        if type(row.get('amount')) is not int or row['amount'] < 0:
            raise ValueError('invalid amount')
        if row['id'] in seen:
            continue
        seen.add(row['id'])
        result[row['category']] = result.get(row['category'], 0) + row['amount']
    return result
''',
    'feature': '''def paginate(items, page=1, page_size=20):
    if any(type(n) is not int or n <= 0 for n in (page, page_size)):
        raise ValueError('positive integers required')
    total = len(items)
    return dict(items=items[(page-1)*page_size:page*page_size], total=total,
                page=page, page_size=page_size, pages=(total+page_size-1)//page_size)
''',
    'docs': 'Run `python toy_cli.py setup --source .` to install.\n'
            'Then run `python toy_cli.py verify --json`.\n'
            'Platform support has not been independently tested.\n',
}


class PilotScoringTests(unittest.TestCase):
    def populate(self, root, task):
        for name, content in TASKS[task]['files'].items():
            (root / name).write_text(content, encoding='utf-8')

    def test_incorrect_baselines_fail(self):
        for task in TASKS:
            with self.subTest(task=task), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.populate(root, task)
                self.assertFalse(score(task, root)['passed'])

    def test_reference_implementations_pass(self):
        for task in TASKS:
            with self.subTest(task=task), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.populate(root, task)
                filename = 'README.md' if task == 'docs' else 'app.py'
                (root / filename).write_text(REFERENCES[task], encoding='utf-8')
                result = score(task, root)
                self.assertTrue(result['passed'], result)
                self.assertEqual(result['checks_passed'], result['checks_total'])

    def test_docs_cannot_change_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.populate(root, 'docs')
            (root / 'README.md').write_text(REFERENCES['docs'], encoding='utf-8')
            (root / 'toy_cli.py').write_text('print("changed")', encoding='utf-8')
            self.assertFalse(score('docs', root)['passed'])

    def test_candidate_exception_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'app.py').write_text('raise RuntimeError("bad")', encoding='utf-8')
            self.assertFalse(score('bugfix', root)['passed'])

    def test_unknown_task_is_rejected(self):
        with self.assertRaises(ValueError):
            score('unknown', Path('.'))

    def test_premature_success_exit_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'app.py').write_text('raise SystemExit(0)', encoding='utf-8')
            self.assertFalse(score('feature', root)['passed'])

    def test_mutating_input_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            code = REFERENCES['feature'].replace('    total = len(items)',
                                                '    items.reverse()\n    total = len(items)')
            (root / 'app.py').write_text(code, encoding='utf-8')
            self.assertFalse(score('feature', root)['passed'])

    def test_float_total_is_not_integer_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            code = REFERENCES['feature'].replace('total=total,', 'total=float(total),')
            (root / 'app.py').write_text(code, encoding='utf-8')
            self.assertFalse(score('feature', root)['passed'])
