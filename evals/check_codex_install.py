#!/usr/bin/env python3
"""Opt-in local CLI smoke test with disposable CODEX_HOME; no model calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--runs', type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.runs <= 10:
        parser.error('--runs must be between 1 and 10')
    root = Path(__file__).resolve().parents[1]
    executable = shutil.which('codex')
    if not executable:
        parser.error('codex not found; installation NOT_RUN')
    report = dict(scope='Local CLI install and cached skill files only; no agent invocation',
                  agent_activation='NOT_RUN', superiority='NOT_ESTABLISHED', runs=[])
    report['cli_version'] = subprocess.check_output([executable, '--version'], text=True).strip()
    report['platform'] = os.name
    report['base_revision'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    report['package_sha256'] = {p: hashlib.sha256((root / p).read_bytes()).hexdigest()
                                for p in ('.codex-plugin/plugin.json', '.claude-plugin/marketplace.json')}
    for index in range(args.runs):
        # Commands intentionally use only local package operations. Do not add exec/login.
        with tempfile.TemporaryDirectory(prefix='dev-team-install-') as directory:
            env = dict(os.environ, CODEX_HOME=directory)
            def run(argv):
                start = time.monotonic()
                try:
                    result = subprocess.run([executable, *argv], cwd=directory, env=env,
                                            capture_output=True, text=True, encoding='utf-8',
                                            errors='replace', timeout=60)
                    code, stdout, stderr = result.returncode, result.stdout, result.stderr
                except subprocess.TimeoutExpired:
                    code, stdout, stderr = 124, '', 'TIMEOUT: 60 seconds'
                def sanitize(value):
                    for path, label in ((directory, '<TEMP>'), (str(root), '<REPO>'),
                                        (str(Path(directory).parent), '<TEMP_PARENT>')):
                        for escaped in (path.replace('\\', '\\\\'), path):
                            value = value.replace(escaped, label)
                    return value
                return dict(argv=[a.replace(str(root), '<REPO>') for a in argv], exit_code=code,
                            elapsed_seconds=round(time.monotonic() - start, 3),
                            stdout=sanitize(stdout), stderr=sanitize(stderr))
            old = run(['plugin', 'install', 'dev-team-skills'])
            steps = []
            for argv in (['plugin', 'marketplace', 'add', str(root), '--json'],
                         ['plugin', 'add', 'dev-team-skills@dev-team-skills-marketplace', '--json'],
                         ['plugin', 'list', '--json']):
                steps.append(run(argv))
                if steps[-1]['exit_code'] != 0:
                    break
            cached = Path(directory) / 'plugins/cache/dev-team-skills-marketplace/dev-team-skills'
            expected = sorted((root / 'skills').glob('*/SKILL.md'))
            versions = list(cached.iterdir()) if cached.exists() else []
            matches = sum(any((v / p.relative_to(root)).is_file()
                              and (v / p.relative_to(root)).read_bytes() == p.read_bytes()
                              for v in versions) for p in expected)
            enabled = False
            if len(steps) == 3 and steps[-1]['exit_code'] == 0:
                enabled = any(p.get('pluginId') == 'dev-team-skills@dev-team-skills-marketplace'
                              and p.get('installed') and p.get('enabled')
                              for p in json.loads(steps[-1]['stdout']).get('installed', []))
            report['runs'].append(dict(index=index + 1, legacy_command=old, corrected_steps=steps,
                                       skill_files_matched=matches, skill_files_expected=len(expected),
                                       passed=len(steps) == 3 and all(s['exit_code'] == 0 for s in steps)
                                       and enabled and matches == len(expected) and bool(expected)))
    report['summary'] = dict(legacy_successes=sum(r['legacy_command']['exit_code'] == 0 for r in report['runs']),
                           corrected_successes=sum(r['passed'] for r in report['runs']), total=args.runs)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    print(json.dumps(report['summary']))
    return 0 if report['summary']['corrected_successes'] == args.runs else 1


if __name__ == '__main__':
    raise SystemExit(main())
