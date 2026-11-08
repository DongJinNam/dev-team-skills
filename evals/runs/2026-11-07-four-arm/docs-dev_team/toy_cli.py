import argparse
import json

parser = argparse.ArgumentParser(description="Toy installer")
commands = parser.add_subparsers(dest="command", required=True)
setup = commands.add_parser("setup", help="Install from a local source")
setup.add_argument("--source", required=True, help="Local source path")
verify = commands.add_parser("verify", help="Verify installation")
verify.add_argument("--json", action="store_true", help="Output JSON")
args = parser.parse_args()
if args.command == "setup":
    print("Configured source: " + args.source)
elif args.json:
    print(json.dumps({"status": "ok"}))
else:
    print("ok")
