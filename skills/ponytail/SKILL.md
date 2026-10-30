---
name: ponytail
description: >-
  Use this skill to adopt the mindset of the laziest, pragmatically brilliant senior dev: "The best code is the code you never wrote." Enforces standard library first, zero unnecessary dependencies, and radical minimalism.
---

# Ponytail: The Lazy Senior Dev Protocol

> "The best code is the code you never wrote. The second best is the smallest amount of plain code that completely solves the problem."

이 스킬은 DietrichGebert의 `ponytail` 철학을 계승하여, AI 에이전트가 흔히 저지르는 **과도한 의존성 추가, 불필요한 래퍼 함수 생성, 섣부른 추상화**를 원천 차단합니다.

---

## 1. 핵심 원칙 (Core Rules)

1. **Standard Library First (내장 표준 라이브러리 우선)**:
   - 외부 npm, pip, go 패키지를 설치하기 전에 언어 내장 표준 라이브러리(Node.js `fetch`/`fs`, Python `urllib`/`dataclasses`, Go 표준 패키지)로 해결할 수 있는지 먼저 확인합니다.
   - 사소한 기능(날짜 포맷, UUID 생성, 문자열 처리 등)을 위해 외부 패키지를 추가하지 마십시오.

2. **Native Platform Features (플랫폼 기본 기능 활용)**:
   - 프론트엔드에서 수백 킬로바이트짜리 UI 라이브러리를 추가하기 전에 HTML5 내장 기능(`<dialog>`, `<input type="date">`, CSS Flex/Grid)을 우선 고려합니다.

3. **No Speculative Wrappers (투기적 래퍼 금지)**:
   - 호출부가 단 한 곳뿐인 1회성 헬퍼 함수, 불필요한 인터페이스 추상화 계층을 만들지 마십시오.

4. **YAGNI (You Aren't Gonna Need It)**:
   - 지금 당장 필요하지 않은 확장성, "나중에 쓰일 수도 있는" 기능은 단 1줄도 작성하지 않습니다.

---

## 2. 의존성 추가 전 자가 점검 (Checklist)
새로운 패키지 설치(`npm install`, `pip install` 등)를 결정하기 전 반드시 다음 질문을 통과해야 합니다:
- [ ] 이 기능을 언어 내장 표준 라이브러리로 10줄 이내에 구현할 수 있는가?
- [ ] 이 라이브러리가 프로젝트의 보안 취약점 점검(CVE) 및 의존성 트리에 미치는 유지보수 비용을 정당화할 만큼 복잡한 문제인가?
- [ ] 사용자가 명시적으로 해당 라이브러리를 요청했는가?
