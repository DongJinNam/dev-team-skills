#!/usr/bin/env python3
"""Generate a security-review packet draft for a pull request.

Observe-stage automation (docs/automation-promotion.md): this script only
drafts the packet a human submitter would otherwise write by hand. It does
not judge, submit, or merge anything. Standard library only.

Usage:
    python3 scripts/security_packet.py --base <sha> --head <sha> [--pr N]
        [--title "..."] [--out packet.md]
"""

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- security-packet-draft -->"


def load_policies():
    spec = importlib.util.spec_from_file_location("run_evals", ROOT / "evals" / "run_evals.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(module.POLICIES)


def current_capture_name():
    workflow = (ROOT / ".github" / "workflows" / "verify-rules-sync.yml").read_text(encoding="utf-8")
    match = re.search(r"evals/runs/([A-Za-z0-9._-]+\.json)", workflow)
    return match.group(1) if match else None


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def collect_changes(base, head):
    changes = []
    for line in git("diff", "--name-status", f"{base}..{head}").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        blob = ""
        if not status.startswith("D"):
            blob = git("rev-parse", f"{head}:{path}").strip()
        changes.append({"status": status, "path": path, "blob": blob})
    shortstat = git("diff", "--shortstat", f"{base}..{head}").strip()
    return changes, shortstat


def classify(changes, policies, capture_name):
    paths = [c["path"] for c in changes]
    policies_changed = sorted(p for p in paths if p in policies)
    capture_path = f"evals/runs/{capture_name}" if capture_name else None
    capture_changed = capture_path in paths if capture_path else False
    if policies_changed and not capture_changed:
        capture_status = (
            "경고: 정책 파일이 변경됐으나 현재 캡처 파일이 변경되지 않았다. "
            "캡처 snapshot이 STALE일 수 있으니 제출자가 재생 결과를 확인해야 한다."
        )
    elif policies_changed and capture_changed:
        capture_status = "정책 파일과 캡처 파일이 함께 변경됐다. 재생 PASS 여부는 CI 결과로 확인한다."
    else:
        capture_status = "정책 파일 변경이 없어 기존 캡처 유효성에 영향이 없다."
    low_risk_prefixes = ("docs/", "evals/runs/")
    if paths and all(p.startswith(low_risk_prefixes) for p in paths):
        tier = "T1"
        tier_reason = "변경이 문서와 eval 캡처 기록에만 있다."
    else:
        tier = "T2"
        tier_reason = "정책·실행 파일이 포함돼 있다."
    return {
        "policies_changed": policies_changed,
        "capture_changed": capture_changed,
        "capture_status": capture_status,
        "tier": tier,
        "tier_reason": tier_reason,
    }


def render(base, head, pr, title, changes, shortstat, info):
    lines = [MARKER, "", "## 보안 검수 패킷 초안 (자동 생성, observe 단계)", ""]
    lines.append("이 초안은 자동화가 만든 초안이다. 판정이 아니다. 제출자가 내용을 확인하고 검증 근거를 채운 뒤 검수자에게 제출한다.")
    lines.append("")
    if pr:
        lines.append(f"- 대상 PR: #{pr} {title or ''}".rstrip())
    lines.append(f"- base: {base}")
    lines.append(f"- head: {head}")
    lines.append(f"- 변경 범위: 파일 {len(changes)}개, {shortstat}")
    lines.append("")
    lines.append("| 파일 | 상태 | blob |")
    lines.append("| --- | --- | --- |")
    for c in changes:
        blob = c["blob"][:8] if c["blob"] else "-"
        lines.append(f"| {c['path']} | {c['status']} | {blob} |")
    lines.append("")
    lines.append(f"- 캡처 상태: {info['capture_status']}")
    if info["policies_changed"]:
        lines.append(f"- 변경된 정책 파일: {', '.join(info['policies_changed'])}")
    lines.append(f"- 등급 제안: {info['tier']} ({info['tier_reason']} 자동 제안이며 판정은 검수자가 한다.)")
    lines.append("")
    lines.append("검증 근거 (제출자가 채운다):")
    lines.append("- 원격 CI 결과: ")
    lines.append("- 로컬 검증 (verify-harness, unittest, 캡처 재생): ")
    lines.append("- 원격 blob과 로컬 트리 일치 확인: ")
    lines.append("")
    lines.append("검수 포인트 (해당하는 항목을 제출자가 조정한다):")
    lines.append("1. 변경이 기존 게이트(독립 보안 판정, 승인, 중단 조건)를 약화하지 않는지")
    lines.append("2. 문서·설정에 프롬프트 인젝션으로 읽힐 지시문이나 내부 정보가 없는지")
    lines.append("3. 효과·수치 주장의 출처와 미확인 표기가 정확한지")
    lines.append("4. 자동화가 만든 초안을 사람이 확인 없이 제출하지 않았는지")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--pr", type=int, default=None)
    parser.add_argument("--title", default="")
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    changes, shortstat = collect_changes(args.base, args.head)
    info = classify(changes, load_policies(), current_capture_name())
    text = render(args.base, args.head, args.pr, args.title, changes, shortstat, info)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
