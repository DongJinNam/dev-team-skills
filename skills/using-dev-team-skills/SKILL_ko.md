---
name: using-dev-team-skills
description: 스킬 이름을 지정하지 않고 평이한 말로 만들고 고치고 검토하고 검증하고 배포해달라고 할 때 쓴다 ("fix this bug", "build this feature", "이 버그 고쳐줘", "이 기능 만들어줘"). 6인 책임자 엔지니어링 스쿼드의 진입점이다.
version: "1.2.0"
metadata:
  author: DongJinNam <ehdwls6856@gmail.com>
  version: "1.2.0"
  tags: ["entry-point", "routing"]
---

# Using dev-team-skills

진입점이다. 스킬 이름 없이 평이한 말로 된 엔지니어링 요청이 오면 이
스킬을 읽는다. 에이전트가 즉흥적으로 워크플로를 만들지 않고 스쿼드
계약으로 연결한다.

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

1. **스쿼드 계약을 읽는다.**
   [engineering-squad](../engineering-squad/SKILL_ko.md)를 열고 Step 0
   kickoff를 따른다. 시작 질문 2개(숫자가 있는 기대효과, 중단 조건과
   보고 대상)다. 요청이 명확하면 가정을 명시하고 바로 구현으로 간다
   (0턴 Adaptive Kickoff). 모호하거나 미합의면 질문하고 PENDING으로
   둔다. 답을 지어내지 않는다.
2. **역할 수가 아니라 워크플로로 연결한다.**
   - 새 기능·수정 → 스쿼드 흐름 (`/dev-team-skills:squad`,
     [commands/squad.md](../../commands/squad.md)).
   - 검토만 → [code-review](../code-review/SKILL_ko.md)
     (`/dev-team-skills:review`). 검토자는 구현자와 달라야 한다.
   - 검증만 → 하네스와 단위 테스트 (`/dev-team-skills:verify`).
     실제 결과만 보고하고 통과를 주장하지 않는다.
   - 배포·머지 → 배포 게이트 + 최신 head 독립 보안 PASS
     (`/dev-team-skills:ship`). PASS가 없으면 머지하지 않는다.
3. **실행하지 않은 것을 실행했다고 하지 않는다.** 자동 호출은
   SessionStart 훅([hooks/hooks.json](../../hooks/hooks.json))이나
   명시적 슬래시 커맨드 통해서만 일어난다. 둘 다 안 떴으면 수동
   진입이라고 말한다. 안 뜬 훅은 NOT_RUN이지 성공이 아니다.

## 이 스킬이 아닌 것

- 일곱 번째 책임자가 아니다. 일은 여전히
  [engineering-squad](../engineering-squad/SKILL_ko.md)의 6명이 한다.
- Step 0을 건너뛰는 지름길이 아니다. 턴을 아끼려고 kickoff 질문을
  생략하는 건 효율이 아니라 계약 위반이다.
- Stop 게이트를 대체하지 않는다.
  [hooks/hooks.json](../../hooks/hooks.json)의 훅은 `verify-harness`
  실패 시 여전히 종료를 막는다.
