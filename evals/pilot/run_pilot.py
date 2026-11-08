#!/usr/bin/env python3
"""Opt-in 12-trial, ChatGPT-login-only skill-layer pilot. No API-key fallback."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from evals.pilot.tasks import TASKS

ARMS = ('basic', 'superpowers', 'ecc', 'dev_team')
ENTRIES = {'basic': None, 'superpowers': 'using-superpowers',
           'ecc': 'tdd-workflow', 'dev_team': 'engineering-squad'}
COMMON = '''This is an authorized, isolated coding benchmark. Complete the task in this workspace.
Use only the supplied task files and local skills. Do not search outside the workspace for answers,
read credentials, install software, use network services, launch other models, or change model settings.
The expected effect is correct behavior on the specified cases, measured by common acceptance tests.
Stop and report if credentials, network, payment, or work outside this workspace is needed.
You have up to five minutes. The specification and local implementation are authorized; choose routine
implementation details yourself. Do not ask for another design/plan approval. Do not create commits.
No subagent tools are available in this bounded trial. An independent reviewer will inspect your
artifact after you finish; do not claim an independent review that has not happened.
Use Python standard library only. Unless the task restricts edits further, put new tests under tests/
and any planning notes under docs/. Do not edit supplied
policy files. Run relevant tests and report actual results and any limitations briefly.
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hash(root):
    entries = [(p.relative_to(root).as_posix(), digest(p)) for p in sorted(root.rglob('*'))
               if p.is_file() and '__pycache__' not in p.parts]
    return hashlib.sha256(json.dumps(entries).encode()).hexdigest()


def redact(value, roots):
    for path, label in roots:
        for form in (str(path).replace('\\', '\\\\'), str(path), Path(path).as_posix()):
            value = value.replace(form, label)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True, help='Dedicated experiment directory')
    parser.add_argument('--superpowers', type=Path, required=True)
    parser.add_argument('--ecc', type=Path, required=True)
    parser.add_argument('--auth-home', type=Path, required=True)
    parser.add_argument('--execute', action='store_true', help='Actually launch up to 12 model trials')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    root = args.root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if (root / 'manifest.json').exists():
        parser.error('Refusing to overwrite or rerun an existing experiment')
    executable = shutil.which('codex')
    if not executable:
        parser.error('codex not available')
    sources = {'superpowers': args.superpowers / 'skills', 'ecc': args.ecc / 'skills',
               'dev_team': repo / 'skills'}
    manifest = dict(schema_version=1, model='gpt-6-astra', reasoning_effort='high',
                    auth='chatgpt-only', api_fallback=False, deadline_seconds=300,
                    surface='native local skills only; no hooks/MCP/child models',
                    repeats_per_task=1, arms=ARMS, tasks=list(TASKS), results=[])
    manifest['cli_version'] = subprocess.check_output([executable, '--version'], text=True).strip()
    manifest['policy_sha256'] = {name: tree_hash(path) for name, path in sources.items()}
    manifest['task_sha256'] = digest(Path(__file__).with_name('tasks.py'))
    manifest['scorer_sha256'] = digest(Path(__file__).with_name('score.py'))
    manifest['runner_sha256'] = digest(Path(__file__))
    manifest['ecc_revision'] = subprocess.check_output(['git', '-C', str(args.ecc), 'rev-parse', 'HEAD'], text=True).strip()
    order = [(task, ARMS[(i + offset) % 4]) for offset, task in enumerate(TASKS) for i in range(4)]
    manifest['order'] = [f'{task}-{arm}' for task, arm in order]
    def save():
        (root / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    save()
    for task_id, arm in order:
        trial_started = time.monotonic()
        trial_id = f'{task_id}-{arm}'
        trial = root / trial_id
        workspace, home = trial / 'workspace', trial / 'codex-home'
        workspace.mkdir(parents=True)
        home.mkdir()
        for name, content in TASKS[task_id]['files'].items():
            target = workspace / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
        skills = workspace / '.agents/skills'
        if arm != 'basic':
            shutil.copytree(sources[arm], skills, ignore=shutil.ignore_patterns('__pycache__', '.git'))
        # A new git root prevents discovery of ancestor repository instructions.
        subprocess.run(['git', 'init', '-q', str(workspace)], check=True)
        config = '''model = "gpt-6-astra"
model_reasoning_effort = "high"
forced_login_method = "chatgpt"
approval_policy = "never"
sandbox_mode = "workspace-write"
web_search = "disabled"
[features]
multi_agent = false
[windows]
sandbox = "unelevated"
'''
        (home / 'config.toml').write_text(config, encoding='utf-8')
        entry = ENTRIES[arm]
        policy_prompt = ('Use the applicable installed skills. First read .agents/skills/' + entry + '/SKILL.md.\n'
                         if entry else 'Use the default Codex instructions; no additional skill package is installed.\n')
        if arm == 'ecc' and task_id == 'docs':
            policy_prompt = 'Use the applicable installed skills; first read .agents/skills/verification-loop/SKILL.md.\n'
        prompt = COMMON + policy_prompt + '\nTASK:\n' + TASKS[task_id]['prompt']
        (trial / 'prompt.txt').write_text(prompt, encoding='utf-8')
        row = dict(id=trial_id, arm=arm, task=task_id, state='PREPARED',
                   installed_skills=len(list(skills.glob('*/SKILL.md'))) if skills.exists() else 0)
        manifest['results'].append(row)
        save()
        if not args.execute:
            continue
        env = dict(os.environ, CODEX_HOME=str(home), PYTHONDONTWRITEBYTECODE='1')
        for name in ('OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL'):
            env.pop(name, None)
        auth = home / 'auth.json'
        roots = [(trial, '<TRIAL>'), (args.auth_home.parent, '<USER>'), (repo, '<REPO>')]
        started = time.monotonic()
        try:
            shutil.copyfile(args.auth_home / 'auth.json', auth)
            status = subprocess.run([executable, 'login', 'status'], env=env, capture_output=True,
                                    text=True, encoding='utf-8', timeout=20)
            if status.returncode or 'ChatGPT' not in status.stdout + status.stderr:
                row.update(state='AUTH_BLOCKED', auth_status='Not confirmed as ChatGPT')
                save()
                return 2
            argv = [executable, 'exec', '--json', '--color', 'never', '-C', str(workspace),
                    '-m', 'gpt-6-astra', '-o', str(workspace / 'final.txt'), '-']
            with (trial / 'events.jsonl').open('w', encoding='utf-8') as out, (trial / 'stderr.txt').open('w', encoding='utf-8') as err:
                process = subprocess.Popen(argv, env=env, cwd=workspace, stdin=subprocess.PIPE,
                                           stdout=out, stderr=err, text=True, encoding='utf-8')
                try:
                    process.communicate(prompt, timeout=300)
                    row.update(state='FINISHED', exit_code=process.returncode)
                except subprocess.TimeoutExpired:
                    # Terminate only this trial's process tree, never other Codex sessions.
                    subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
                    process.wait(timeout=20)
                    row.update(state='TIMEOUT', exit_code=124)
            row['elapsed_seconds'] = round(time.monotonic() - trial_started, 3)
            row['execution_seconds'] = round(time.monotonic() - started, 3)
            events = (trial / 'events.jsonl').read_text(encoding='utf-8')
            row['usage'] = None
            for line in events.splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get('type') == 'turn.completed':
                    row['usage'] = event.get('usage')
            # Generated code is not executed by this controller. Review artifacts first,
            # then score separately after all credential copies have been removed.
            row['score'] = {'status': 'PENDING_INDEPENDENT_CODE_REVIEW'}
            row['observed_models'] = []
            for session in (home / 'sessions').rglob('*.jsonl'):
                for line in session.read_text(encoding='utf-8').splitlines():
                    event = json.loads(line)
                    if event.get('type') == 'turn_context':
                        actual = event.get('payload', {}).get('model')
                        if actual and actual not in row['observed_models']:
                            row['observed_models'].append(actual)
            row['workspace_files'] = sorted(p.relative_to(workspace).as_posix() for p in workspace.rglob('*')
                                            if p.is_file() and '.git' not in p.parts and '.agents' not in p.parts)
            row['policy_unchanged'] = not skills.exists() or tree_hash(skills) == manifest['policy_sha256'][arm]
            for file in (trial / 'events.jsonl', trial / 'stderr.txt'):
                file.write_text(redact(file.read_text(encoding='utf-8'), roots), encoding='utf-8')
            print(json.dumps({k: row[k] for k in ('id', 'state', 'exit_code', 'elapsed_seconds', 'score', 'usage')}), flush=True)
            save()
            if row['exit_code'] not in (0, 124):
                manifest['stop_reason'] = 'CLI execution barrier; inspect before any further calls, no fallback or retry'
                save()
                return 2
        finally:
            auth.unlink(missing_ok=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
