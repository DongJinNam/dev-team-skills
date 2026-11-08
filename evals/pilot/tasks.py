"""Public pilot tasks. Hidden checks live separately in score.py."""

TASKS = {
    'bugfix': {
        'prompt': (
            'Fix app.py summarize(text) for JSONL input. Skip blank lines. Every nonblank '
            'line must be a JSON object with id and category strings containing at least '
            'one non-whitespace character, and amount a nonnegative integer (bool is invalid). '
            'Invalid JSON, missing fields or invalid values must raise ValueError, including '
            'invalid duplicate rows. Extra fields may be ignored. Preserve id/category strings '
            'exactly; do not strip them when matching or grouping. For repeated ids, the first '
            'valid row wins even across categories. Return category-to-amount totals; empty '
            'input returns {}. Edit app.py and optionally add tests only. No external dependencies.'
        ),
        'files': {
            'app.py': 'import json\n\ndef summarize(text):\n'
                      '    totals = {}\n'
                      '    for line in text.splitlines():\n'
                      '        row = json.loads(line)\n'
                      '        totals[row["category"]] = totals.get(row["category"], 0) + row["amount"]\n'
                      '    return totals\n',
        },
        'allowed_files': ['app.py', 'tests/**'],
    },
    'feature': {
        'prompt': (
            'Implement app.py paginate(items, page=1, page_size=20), where items is a list. '
            'Return a dict with exactly items (page slice as a list), total (input length), '
            'page, page_size, pages (ceiling of total/page_size, or 0 for empty input). '
            'page and page_size must be positive integers; bool, non-integers and nonpositive '
            'values raise ValueError even for empty input. Pages are 1-based; beyond the last '
            'page return an empty items list. Preserve order and leave the original list '
            'unchanged. Edit app.py and optionally add tests only. No external dependencies.'
        ),
        'files': {'app.py': 'def paginate(items, page=1, page_size=20):\n    raise NotImplementedError\n'},
        'allowed_files': ['app.py', 'tests/**'],
    },
    'docs': {
        'prompt': (
            'Fix README.md installation instructions using the actual toy_cli.py --help '
            'and subcommand help. Provide runnable commands for installing from the current '
            'directory and verifying with JSON output, remove the obsolete deploy/--repo '
            'command and the unsupported 100% platform compatibility claim. Do not claim '
            'unperformed platform tests. Change README.md only; leave toy_cli.py unchanged.'
        ),
        'files': {
            'README.md': '# Toy CLI\n\nInstall with `python toy_cli.py deploy --repo .`.\n'
                         '100% compatible with all platforms.\n',
            'toy_cli.py': (
                'import argparse\nimport json\n\n'
                'parser = argparse.ArgumentParser(description="Toy installer")\n'
                'commands = parser.add_subparsers(dest="command", required=True)\n'
                'setup = commands.add_parser("setup", help="Install from a local source")\n'
                'setup.add_argument("--source", required=True, help="Local source path")\n'
                'verify = commands.add_parser("verify", help="Verify installation")\n'
                'verify.add_argument("--json", action="store_true", help="Output JSON")\n'
                'args = parser.parse_args()\n'
                'if args.command == "setup":\n'
                '    print("Configured source: " + args.source)\n'
                'elif args.json:\n'
                '    print(json.dumps({"status": "ok"}))\n'
                'else:\n'
                '    print("ok")\n'
            ),
        },
        'allowed_files': ['README.md'],
    },
}
