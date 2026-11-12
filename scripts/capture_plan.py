#!/usr/bin/env python3
"""Generate a capture-renewal execution plan for a policy change.

Implements Phase 2 of the automation pipeline: the procedure is fixed by
evals/capture-runbook.md; this script only computes the per-change plan
(which policies changed, the current capture reference, the case list, the
expected output paths). It does not run actors or assemble captures.
Standard library only.

Usage:
    python3 scripts/capture_plan.py --base <sha> --head <sha>
        --date YYYY-MM-DD --slug <slug> [--out plan.md]
"""

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_policies():
    spec = importlib.util.spec_from_file_location("run_evals", ROOT / "evals" / "run_evals.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(module.POLICIES)


def load_case_ids():
    scenarios = json.loads((ROOT / "evals" / "scenarios.json").read_text(encoding="utf-8"))
    return [c["id"] for c in scenarios["cases"]]


def current_capture_name(base):
    """The capture referenced at base, not in the working tree.

    A renewal plan is generated before the renewal happens, so the working
    tree may already point at the new capture. The base commit is the
    reference that the plan replaces.
    """
    try:
        workflow = git("show", f"{base}:.github/workflows/verify-rules-sync.yml")
    except subprocess.CalledProcessError:
        workflow = (ROOT / ".github" / "workflows" / "verify-rules-sync.yml").read_text(encoding="utf-8")
    match = re.search(r"evals/runs/([A-Za-z0-9._-]+\.json)", workflow)
    return match.group(1) if match else None


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def changed_paths(base, head):
    paths = []
    for line in git("diff", "--name-status", f"{base}..{head}").splitlines():
        if not line.strip():
            continue
        paths.append(line.split("\t")[-1])
    return paths


def classify(paths, policies, capture_name):
    policies_changed = sorted(p for p in paths if p in policies)
    scenarios_changed = "evals/scenarios.json" in paths
    harness_changed = "evals/run_evals.py" in paths
    capture_path = f"evals/runs/{capture_name}" if capture_name else None
    capture_changed = capture_path in paths if capture_path else False
    needs_renewal = bool(policies_changed or scenarios_changed or harness_changed)
    return {
        "policies_changed": policies_changed,
        "scenarios_changed": scenarios_changed,
        "harness_changed": harness_changed,
        "capture_changed": capture_changed,
        "needs_renewal": needs_renewal,
    }


def render(base, head, date, slug, case_ids, capture_name, info):
    new_capture = f"evals/runs/{date}-{slug}.json"
    lines = [
        f"# Capture Renewal Plan ({date}-{slug})",
        "",
        f"- base: {base}",
        f"- head: {head}",
        f"- current capture: {capture_name or '(unknown)'}",
        f"- renewal needed: {'yes' if info['needs_renewal'] else 'no'}",
        "",
    ]
    if info["policies_changed"]:
        lines.append(f"- changed policy files: {', '.join(info['policies_changed'])}")
    if info["scenarios_changed"]:
        lines.append("- scenarios.json changed: the case set itself changed; the plan's case list comes from the new file.")
    if info["harness_changed"]:
        lines.append("- run_evals.py changed: the snapshot definition changed; replay against the new file only.")
    if info["capture_changed"]:
        lines.append("- a capture file is already changed in this range; verify it is the new one, not an edit of the old one.")
    lines.append("")
    if not info["needs_renewal"]:
        lines.append("No policy, scenario, or harness file changed. No renewal is needed; the existing capture stays valid.")
        return "\n".join(lines)
    lines.append("## Execution (see evals/capture-runbook.md)")
    lines.append("")
    lines.append(f"1. One isolated actor session per case ({len(case_ids)} sessions), in order:")
    for i, case_id in enumerate(case_ids, 1):
        lines.append(f"   {i}. {case_id}")
    lines.append("2. One independent reviewer session (prompts and policies only, no scenarios.json).")
    lines.append(f"3. Assemble {new_capture} with review.response_sha256 and snapshot_sha256.")
    lines.append("4. Point .github/workflows/verify-rules-sync.yml and evals/README.md at the new capture.")
    lines.append(f"5. Verify: `bash evals/run-evals.sh --replay {new_capture}` must PASS, plus verify-harness and unit tests.")
    lines.append("6. Preserve failed attempts as `<date>-<slug>-attempt<N>.json`; never delete or overwrite them.")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    paths = changed_paths(args.base, args.head)
    capture_name = current_capture_name(args.base)
    info = classify(paths, load_policies(), capture_name)
    text = render(args.base, args.head, args.date, args.slug, load_case_ids(), capture_name, info)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
