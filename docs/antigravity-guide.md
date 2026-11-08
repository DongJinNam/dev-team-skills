# Antigravity (AGY) 환경 적용 가이드

Google Antigravity(AGY) 환경에서 `dev-team-skills`를 한 번에 원활하게 인식시키고 즉시 활성화하는 방법을 설명합니다.

---

## 1. Antigravity에서 스킬이 한 번에 적용되지 않던 원인

Antigravity는 Claude Code나 일반 IDE 플러그인과 다른 고유한 아키텍처를 가지고 있습니다:

1. **디스커버리 경로 제한**:
   - Antigravity는 프로젝트 루트 직하의 `skills/` 폴더를 기본 스킬 디렉토리로 탐색하지 않습니다.
   - 프로젝트 레벨: `.agents/skills/<name>/SKILL.md` (또는 `.agent/skills/`)
   - 머신 전역(Global): `~/.gemini/config/skills/<name>/SKILL.md`
2. **점진적 공개(Progressive Disclosure) 메커니즘**:
   - 컨텍스트 토큰을 절약하기 위해 Antigravity는 대화 시작 시 모든 스킬 본문을 로드하지 않습니다.
   - 시스템 프롬프트에는 스킬의 `name`과 `description`만 주입되며, 사용자의 프롬프트가 해당 `description`의 의도에 부합할 때 모델이 비로소 해당 `SKILL.md`를 열어 읽습니다.
3. **Always-on Rule 부트스트랩 연계**:
   - `GEMINI.md`와 `AGENTS.md`는 항상 주입되는 Always-on Rule입니다. 이 규칙 파일에 스킬 참조 지침이 없으면, 에이전트가 스킬을 굳이 먼저 열어보지 않고 일반적인 단독 어시스턴트로 반응하게 됩니다.

---

## 2. 한 번에 적용하는 원클릭 셋업

원클릭 스크립트를 통해 Antigravity가 인식할 수 있는 `.agents/skills` 심볼릭 링크(또는 복사본)를 생성합니다.

### Windows (PowerShell)
```powershell
# 현재 프로젝트 워크스페이스에만 적용 (.agents/skills 생성)
.\scripts\setup-antigravity.ps1 -Target workspace

# 또는 모든 Antigravity 프로젝트에 전역 적용 (~/.gemini/config/skills에 설치)
.\scripts\setup-antigravity.ps1 -Target global
```

### macOS / Linux (Bash)
```bash
# 현재 프로젝트 워크스페이스에 적용
bash scripts/setup-antigravity.sh workspace

# 또는 전역 적용
bash scripts/setup-antigravity.sh global
```

---

## 3. 원샷 활성화(One-shot Activation) 팁

스킬이 Antigravity에서 즉각 1회차 답변부터 동작하도록 하는 모범 사례입니다:

1. **프로젝트 루트의 `GEMINI.md` 확인**:
   - Antigravity는 현재 디렉토리부터 상위 루트까지 탐색하며 `GEMINI.md`를 항상 로드합니다.
   - 저장소 루트에 있는 `GEMINI.md`가 에이전트에게 시니어 엔지니어링 헌법과 스쿼드 역할을 준수하도록 강제합니다.

2. **명시적 트리거 키워드 활용**:
   - Antigravity의 의도 매칭기는 프롬프트에 `스쿼드`, `설계`, `리뷰`, `배포`, `squad`, `review` 등의 키워드가 포함될 때 `engineering-squad` 및 `code-review` 스킬을 1순위로 즉시 호출합니다.
   - 예시: *"새로운 API 엔드포인트를 dev-team-skills 스쿼드로 개발해줘."*

3. **글로벌 스킬 등록 확인**:
   - `~/.gemini/config/skills/`에 스킬이 등록되어 있으면, 어떤 프로젝트를 열어도 Antigravity의 기본 스킬 목록(`Available skills`)에 자동으로 나타납니다.
