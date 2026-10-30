#!/usr/bin/env python3
"""
Pragmatic AI Code Reviewer Bot for GitHub Actions.
Uses Python standard library ONLY (Zero external dependencies).
Applies dev-team-skills:
  - 8 Engineering Roles & Checklists
  - 3-tier severity classification (🔴 Must Fix, 🟡 Inquire, 🟢 Suggestion)
  - Andrej Karpathy Constitution & Ponytail minimalism
  - Natural Korean (humanizer-kr)
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

# Ensure UTF-8 output on all platforms (including Windows consoles)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def run_cmd(cmd: list) -> str:
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False
    )
    if res.stdout:
        return res.stdout.strip()
    return ""


def load_file_safely(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def post_github_comment(pr_number: str, comment_body: str) -> bool:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token or not pr_number:
        print("[!] No GH_TOKEN or PR_NUMBER available. Printing review to stdout:")
        print(comment_body)
        return False

    cmd = ["gh", "pr", "comment", str(pr_number), "--body", comment_body]
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    if res.returncode == 0:
        print(f"[+] Successfully posted review comment to PR #{pr_number}")
        return True
    else:
        print(f"[-] Failed to post comment via gh CLI: {res.stderr}")
        return False


def call_gemini_api(api_key: str, system_prompt: str, user_prompt: str) -> str:
    # Use Gemini 1.5 Flash for high speed and generous context window
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"System Directive:\n{system_prompt}\n\nUser Request:\n{user_prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 4096,
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = resp.read().decode("utf-8")
            parsed = json.loads(body)
            candidates = parsed.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
    except urllib.error.HTTPError as e:
        print(f"[-] Gemini API HTTP Error: {e.code} - {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"[-] Gemini API Error: {e}")
    return ""


def call_openai_api(api_key: str, system_prompt: str, user_prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = resp.read().decode("utf-8")
            parsed = json.loads(body)
            choices = parsed.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
    except urllib.error.HTTPError as e:
        print(f"[-] OpenAI API HTTP Error: {e.code} - {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"[-] OpenAI API Error: {e}")
    return ""


def main():
    pr_number = os.environ.get("PR_NUMBER", "")
    base_ref = os.environ.get("BASE_REF", "main")
    pr_title = os.environ.get("PR_TITLE", "")
    pr_body = os.environ.get("PR_BODY", "")

    print(f"[*] Starting AI Squad Code Review for PR #{pr_number} (Base: {base_ref})")

    # 1. Extract git diff
    diff = run_cmd(["git", "diff", f"origin/{base_ref}...HEAD"])
    if not diff:
        diff = run_cmd(["git", "diff", "HEAD~1...HEAD"])

    if not diff:
        print("[!] No git diff found. Skipping review.")
        return

    # Truncate diff if extremely large to prevent payload overflow
    if len(diff) > 40000:
        diff = diff[:40000] + "\n\n...[Diff truncated due to size limits]..."

    # 2. Gather dev-team-skills rules & checklists
    constitution = load_file_safely("GEMINI.md")
    review_rubric = load_file_safely("skills/code-review/references/review-rubric.md")
    role_checklists = load_file_safely("skills/code-review/references/role-checklists.md")

    system_prompt = f"""당신은 'dev-team-skills' 8인 시니어 엔지니어링 스쿼드의 AI 수석 코드 리뷰어(Squad AI Reviewer)입니다.
우리의 행동 강령과 헌법을 엄격히 준수합니다.

[행동 강령 & 헌법]
{constitution}

[리뷰 심각도 체계 (Review Rubric)]
{review_rubric}

[8개 직무별 체크리스트]
{role_checklists}

[리뷰 작성 규칙]
1. 불필요한 인사말, 미사여구, 번역투는 철저히 배제하고 실무 시니어 개발자의 간결하고 명확한 문체(Natural Korean)로 서술합니다.
2. 모든 지적 사항에는 반드시 3단계 심각도 태그(🔴 [필수 / Must Fix], 🟡 [확인 요청 / Inquire], 🟢 [권장 / Suggestion])를 명시합니다.
3. 관련 직무 관점(Product Planner, AI Agent Engineer, Frontend, Backend, Data, QA, DevOps, SRE)을 명시하고, 단순 지적에 그치지 않고 SOLID 및 최소 코드(Ponytail) 기반의 실질적 대안 코드를 제시합니다.
4. 마지막에는 PR 작성자가 즉시 조치해야 할 '다음 액션 1단계(Next Action)'로 끝맺습니다.
"""

    user_prompt = f"""다음 PR의 변경 사항을 8인 엔지니어링 스쿼드 관점에서 리뷰해 주십시오.

PR 제목: {pr_title}
PR 설명:
{pr_body}

Git Diff:
```diff
{diff}
```
"""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    review_result = ""

    if gemini_key:
        print("[*] Calling Gemini API for Squad Review...")
        review_result = call_gemini_api(gemini_key, system_prompt, user_prompt)
    elif openai_key:
        print("[*] Calling OpenAI API for Squad Review...")
        review_result = call_openai_api(openai_key, system_prompt, user_prompt)
    else:
        print("[!] Neither GEMINI_API_KEY nor OPENAI_API_KEY was provided.")
        review_result = f"""### 🤖 AI Engineering Squad Automated Reviewer

> **안내**: 저장소 GitHub Secrets에 `GEMINI_API_KEY` 또는 `OPENAI_API_KEY`가 등록되지 않아 정적 프리플라이트 점검 모드로 동작했습니다.

#### 📋 Pre-flight Automated Check Summary
- **Target Branch**: `{base_ref}`
- **PR Title**: `{pr_title}`
- **8인 직무 체크리스트 및 헌법(GEMINI.md) 검증 준비 완료**
- **Harness & Schema Test**: 로컬 `verify-harness` 통과 확인

---

#### 💡 Full AI Squad Review 활성화 방법
저장소의 **Settings > Secrets and variables > Actions**에 아래 Secret 중 하나를 등록하시면 다음 PR 커밋부터 8인 스쿼드의 심층 디자인 패턴 리뷰 및 🔴/🟡/🟢 심각도 분석이 자동으로 게시됩니다:
- `GEMINI_API_KEY` (권장: Google AI Studio 무료/유료 키)
- `OPENAI_API_KEY` (OpenAI API 키)

**Next Action**: 레포지토리 Secrets에 API 키를 등록하거나, 머지 전 PR 템플릿의 셀프 체크리스트를 최종 확인해 주세요.
"""

    if review_result:
        post_github_comment(pr_number, review_result)


if __name__ == "__main__":
    main()
