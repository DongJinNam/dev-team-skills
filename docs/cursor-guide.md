# Cursor 환경 적용 가이드 [EXPERIMENTAL]

> **주의 (Experimental Status)**: Cursor 환경에서의 동작은 현재 **실험적(Experimental)** 단계입니다. Cursor는 다른 플랫폼(Antigravity, Claude Code, OpenAI Codex)과 달리 서브에이전트 디스패치 및 하네스 자동 검증 체계가 엔드투엔드로 완전히 검증되지 않았습니다. 실사용 시 100% 동작을 가정하지 마시고, 피드백을 공유해 주시기 바랍니다.

---

## 1. Cursor 환경의 특성과 한계

1. **독립 서브에이전트 조율 부재**:
   - Antigravity나 Claude Code는 독립된 컨텍스트를 가진 서브에이전트를 동적으로 생성하여 역할을 분담할 수 있습니다.
   - Cursor는 기본적으로 단일 세션 대화 기반이므로, 스쿼드의 6개 역할(Tech Lead, Quality Lead, Engineering Lead 등)이 **단일 에이전트 내 다자간 페르소나 전환(Persona Switching)** 형태로 동작합니다.
2. **독립 보안 검토의 물리적 한계**:
   - 스쿼드 헌법에 따르면 보안 검토는 구현자와 별개의 에이전트여야 합니다.
   - Cursor 단일 세션에서는 같은 모델이 구현 후 자체 검토를 수행하게 되므로, 완전한 독립 검증의 보장이 어렵습니다.

---

## 2. Cursor에 적용하기

### 원클릭 셋업 스크립트

#### Windows (PowerShell)
```powershell
.\scripts\setup-cursor.ps1
```

#### macOS / Linux (Bash)
```bash
bash scripts/setup-cursor.sh
```

스크립트는 다음 두 가지 규칙 파일을 설정합니다:
1. `.cursor/rules/engineering-squad.mdc` (최신 Cursor 규칙 규격)
2. `.cursorrules` (레거시 지원용 루트 규칙)

---

## 3. 권장 사용 프롬프트

단일 세션에서 스쿼드 원칙을 최대한 유지하기 위해 다음과 같이 명시적인 역할 전환을 요청하는 것을 권장합니다:

```text
dev-team-skills 스쿼드 규칙에 따라 개발을 진행해줘.
1단계로 Quality Lead로서 완료 기준(DoD)과 테스트 계획을 수립하고,
2단계로 Engineering Lead로서 구현한 뒤 테스트를 실행해줘.
```
