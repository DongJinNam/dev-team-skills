# Toy CLI

With Python 3 available as `python`, run these commands from the directory
containing `toy_cli.py`.

Install from the current directory:

```sh
python toy_cli.py setup --source .
```

Expected output:

```text
Configured source: .
```

Verify with JSON output:

```sh
python toy_cli.py verify --json
```

Expected output:

```json
{"status": "ok"}
```

View the available commands and their options:

```sh
python toy_cli.py --help
python toy_cli.py setup --help
python toy_cli.py verify --help
```
