#!/usr/bin/env python3
"""Query native Codex skill discovery with no credentials or model turn."""
import argparse
import json
import os
from pathlib import Path
from queue import Queue, Empty
import shutil
import subprocess
import tempfile
from threading import Thread
import time


def discover(cwd):
    executable = shutil.which('codex')
    if not executable:
        raise ValueError('codex not found')
    with tempfile.TemporaryDirectory(prefix='skill-discovery-') as directory:
        env = dict(os.environ, CODEX_HOME=directory)
        for key in ('OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL'):
            env.pop(key, None)
        process = subprocess.Popen([executable, 'app-server', '--stdio'], cwd=cwd, env=env,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, text=True, encoding='utf-8')
        messages = Queue()
        def read():
            for line in process.stdout:
                messages.put(line)
        reader = Thread(target=read, daemon=True)
        reader.start()
        def send(payload):
            process.stdin.write(json.dumps(payload) + '\n')
            process.stdin.flush()
        def receive(request_id):
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                try:
                    item = json.loads(messages.get(timeout=max(0.01, deadline - time.monotonic())))
                except Empty as error:
                    raise ValueError('skill discovery timed out') from error
                if item.get('id') == request_id:
                    if 'error' in item:
                        raise ValueError(str(item['error']))
                    return item['result']
            raise ValueError('skill discovery timed out')
        try:
            send(dict(id=1, method='initialize', params=dict(clientInfo=dict(name='skill-probe', version='1.0'))))
            receive(1)
            send(dict(method='initialized', params={}))
            send(dict(id=2, method='skills/list', params=dict(cwds=[str(cwd)], forceReload=True)))
            return receive(2)
        finally:
            process.stdin.close()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.terminate()
                process.wait(timeout=5)
            reader.join(timeout=5)
            process.stdout.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cwd', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = discover(args.cwd.resolve())
    args.output.write_text(json.dumps(result, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps([dict(skills=len(item.get('skills', [])), errors=item.get('errors', []))
                      for item in result.get('data', [])], ensure_ascii=True))


if __name__ == '__main__':
    main()
