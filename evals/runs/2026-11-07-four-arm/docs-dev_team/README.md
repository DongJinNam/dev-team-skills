# Toy CLI

From the directory containing `toy_cli.py`, install from the current directory:

```sh
python toy_cli.py setup --source .
```

Expected output: `Configured source: .`

Verify with JSON output:

```sh
python toy_cli.py verify --json
```

Expected output:

```json
{"status": "ok"}
```

For available commands and options:

```sh
python toy_cli.py --help
python toy_cli.py setup --help
python toy_cli.py verify --help
```
