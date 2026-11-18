---
name: using-dev-team-skills
description: 스킬 이름을 지정하지 않고 평이한 말로 만들고 고치고 검토하고 검증하고 배포해달라고 할 때 쓴다 ("fix this bug", "build this feature", "이 버그 고쳐줘", "이 기능 만들어줘"). 6인 책임자 엔지니어링 스쿼드의 진입점이다.
version: "1.2.0"
metadata:
  author: DongJinNam
  version: "1.2.0"
  tags: ["entry-point", "routing", "squad"]
---

# Using dev-team-skills

## 목적 (Purpose)

스킬 이름 없이 평이한 말로 들어온 엔지니어링 요청을 에이전트가 임의로 처리하지 않고, 6인 책임자 엔지니어링 스쿼드 계약으로 즉시 연결하는 공식 진입점입니다.
[English specification: SKILL.md](SKILL.md)

## 사전 요구사항 (Prerequisites)

- 운영체제: Windows, macOS, Linux
- 필수 환경: 표준 dev-team-skills 패키지 환경

## 트리거 문구

아래 중 하나라도 해당하면 이 스킬이 적용된다 (영어·한국어 공통):

- "fix this bug", "이 버그 고쳐줘", "버그 수정해줘"
- "build this feature", "이 기능 만들어줘", "기능 추가해줘"
- "review this code", "이 코드 리뷰해줘"
- "check that the package is intact", "검증해줘", "하네스 돌려줘"
- "ship it", "배포해줘", "머지해줘"

이미 이름을 지정한 스킬(`engineering-squad`, `code-review`,
슬래시 커맨드)이 있으면 그 스킬이 우선이다. 사용자가 이미 겨냥한
스킬로 간 요청을 다시 돌리지 않는다.

## 진입 절차

1. **스쿼드 계약을 읽는다.** [engineering-squad](../engineering-squad/SKILL_ko.md)
   를 열고 0단계 킥오프를 따른다: 시작 질문 둘(숫자가 든 기대 효과,
   중단 조건과 알릴 대상). 요청이 명확하면 가정을 밝히고 곧장 구현으로
   간다 (0턴 적응형 킥오프). 모호하거나 합의가 안 됐으면 묻고 PENDING을
   유지한다. 답을 지어내지 않는다.
2. **역할 수가 아니라 워크플로로 연결한다.**
   - 새 기능 또는 수정 → 스쿼드 흐름 (`/dev-team-skills:squad`,
     [commands/squad.md](../../commands/squad.md)).
   - 검토만 → [code-review](../code-review/SKILL_ko.md)
     (`/dev-team-skills:review`). 검토자는 구현자와 달라야 한다.
   - 검증만 → 하네스와 단위 테스트 (`/dev-team-skills:verify`). 추측이
     아니라 실제 결과를 보고한다.
   - 배포 또는 머지 → 배포 게이트와 현재 헤드의 독립 보안 PASS
     (`/dev-team-skills:ship`). PASS 없이는 머지하지 않는다.
3. **실행하지 않은 것을 실행했다고 하지 않는다.** 자동 호출은
   SessionStart 훅([hooks/hooks.json](../../hooks/hooks.json))이나
   명시적 슬래시 커맨드로만 일어난다. 둘 다 실행되지 않았으면 수동
   진입이라고 밝힌다. 실행되지 않은 훅은 성공이 아니라 NOT_RUN이다.

## 예시 (Examples)

```bash
# 본 스킬이 자동 라우팅하는 평이한 사용자 프롬프트 예시:
"이 버그 고쳐줘" -> engineering-squad 킥오프로 연결 (/dev-team-skills:squad)
"이 PR 코드 리뷰해줘" -> code-review로 연결 (/dev-team-skills:review)
"하네스 검증 돌려줘" -> verify-harness.py 실행 (/dev-team-skills:verify)
```

## 한계 및 제약 (Limitations)

- 일곱 번째 책임자가 아니다. 일은 여전히 [engineering-squad](../engineering-squad/SKILL_ko.md)
  의 여섯 책임자가 한다.
- 0단계를 건너뛰는 지름길이 아니다. 한 턴 아끼겠다고 킥오프 질문을 생략하는
  것은 효율이 아니라 계약 위반이다.
- 중단 게이트를 대체하지 않는다. `verify-harness`가 실패할 때 중단을
  막는 것은 여전히 [hooks/hooks.json](../../hooks/hooks.json)의 훅이다.

## 문제 해결 (Troubleshooting)

- **Error**: `RoutingAmbiguityError`
  - **Cause**: 사용자의 요청이 복수 도메인에 걸쳐 있거나 명확한 의도를 특정할 수 없는 경우.
  - **Solution**: 0단계 킥오프 질문으로 되돌아가 사용자에게 목적과 범위를 확인한 뒤 라우팅 진행.
- **Error**: `HookExecutionSkipped`
  - **Cause**: SessionStart 훅이 환경 이슈로 트리거되지 않은 경우.
  - **Solution**: `/dev-team-skills:squad` 커맨드로 수동 진입하며 미실행 훅을 PASS로 조작하지 않음.
