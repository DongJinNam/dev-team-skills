## 무엇을

작업 종류별 모델 등급 배정 계약(모델 라우팅)을 engineering-squad에 추가합니다. DEEP는 설계·분석·판정·보안 검수와 분석 요약, STANDARD는 확정된 구현·테스트 작성, LIGHT는 판단이 얇은 대량 작업입니다. 보안 판정은 DEEP 고정이며 비용을 이유로 내리지 않습니다.

## 어떻게

- 신규 참조 `references/model-routing.md`·`model-routing_en.md` (+ `.agents/skills` 미러): 등급 정의, 역할 기본 배정, 승격 규칙, 호스트별 모델표와 고정 수단·강제 수준 (확인일 2026-11-11), 기록·검증 기준
- 호스트별 강제 수준을 실제와 다르게 쓰지 않았습니다. Claude Code는 SKILL·서브에이전트 frontmatter로 강제 가능, Codex는 에이전트 TOML 필요, Cursor는 서브에이전트 파일로 모델 ID 고정 가능, Antigravity는 flash/pro 등급만 지정 가능합니다
- SKILL.md/SKILL_en.md 비용 절 첫머리에 라우팅 연결 한 문단 추가
- 결정 기록 `docs/decisions/2026-11-11-model-routing.md`에 대안과 기각 이유, 한계와 재판단 조건을 남겼습니다

## 왜

지금까지 비용 절은 사용량 비교 방법만 정했고 어떤 작업을 어떤 모델로 보낼지는 정하지 않았습니다. 사용자의 운용 방식(고급 모델은 추론·분석, 가성비 모델은 설계 확정 후 구현·테스트)을 호스트가 바뀌어도 재현되게 등급 단위로 계약화했습니다. 계약의 본체는 모델명이 아니라 등급이라 모델 은퇴·개명 시 표만 갱신합니다.

## 검증

- 로컬: verify-harness PASS, unittest 100개 OK
- SKILL.md가 eval 캡처 snapshot 대상이라 캡처를 갱신했습니다. `evals/runs/2026-11-11-model-routing.json`은 케이스별 독립 세션 actor 19개가 공개 프롬프트 19개에 답하고 별도 리뷰어가 의미 검수 19/19를 마친 기록이며 재생 PASS입니다. lean-doc-routing 첫 시도는 필수 액션 누락으로 실패해 새 actor로 재답했고, 실패 응답은 `2026-11-11-model-routing-lean-attempt1.json`으로 보존했습니다
- 워크플로와 evals README의 현재 캡처 참조를 새 파일로 교체했습니다

## 한계

- 이 계약은 라우팅 효과의 실측이 아닙니다. 토큰·비용 변화는 compare_usage 실측이 있을 때만 주장합니다
- Antigravity 개인 계정에서 pro 등급 지정의 실효성은 미확인 보고 수준이라 표에 그대로 적었습니다
