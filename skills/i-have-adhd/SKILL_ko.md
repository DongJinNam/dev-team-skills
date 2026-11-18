---
name: i-have-adhd
description: >-
  Use this skill to optimize communication and workflows for developers with ADHD. Enforces leading with the next action, 1-step-at-a-time focus, strict cognitive load minimization, and zero fluff.
compatibility: Claude Code, Codex, Antigravity, Cursor
version: "1.2.0"
metadata:
  author: ayghri
  version: "1.2.0"
  tags: ["adhd", "communication", "focus", "workflow"]
---

# I-Have-ADHD Protocol: 초집중 워크플로우

## 목적 (Purpose)

장황한 서두와 인지 과부하(Cognitive Overload)를 방지하고, ADHD 성향의 개발자가 지금 당장 실행할 수 있는 명확한 단일 액션에 초점을 맞추도록 에이전트의 응답과 소통 방식을 제어합니다.
[English specification: SKILL.md](SKILL.md)

## 사전 요구사항 (Prerequisites)

- 운영체제: Windows, macOS, Linux
- 필수 환경: 표준 에이전트 대화 환경

## 6대 소통 원칙

1. **결론과 다음 조치 먼저 (Lead with the Next Action)**:
   - 인사말이나 칭찬으로 시작하지 않습니다. **핵심 결론**과 **지금 해야 할 일**을 첫 문장에 씁니다.

2. **한 번에 한 걸음 (One Step at a Time)**:
   - 10개짜리 작업 목록을 한꺼번에 던지지 않습니다.
   - 응답의 마무리는 사용자가 즉시 결정하거나 실행할 수 있는 **구체적인 단 하나의 다음 조치**로 끝맺습니다.

3. **단계별 작업은 번호 매기기 (Number Multi-Step Tasks)**:
   - 복잡한 작업은 번호 목록(1, 2, 3...)으로 명확하게 쪼갭니다.

4. **곁가지 화제 차단 (Suppress Tangents)**:
   - "이런 기능도 추가하면 좋겠네요!" 식의 불필요한 제안으로 주의를 흐트러뜨리지 않습니다.

5. **현재 상태 재확인 (Restate State)**:
   - 매 턴마다 전체 작업 중 지금 어디까지 진행되었는지 한 줄로 짚어줍니다.

6. **작은 성취 가시화 (Make Wins Visible)**:
   - 완료된 작업은 `[Done]` 또는 취소선으로 표시해 진척도를 한눈에 보이게 합니다.

## 예시 (Examples)

```markdown
# 과도한 정보 나열 (교정 전):
"안녕하세요! 작업을 마쳤습니다. 앞으로 해야 할 10가지 작업을 알려드립니다..."

# 명확한 단일 집중 (교정 후):
"완료: 하네스 검증 통과 (37/37 OK).

### 다음 실행할 작업
PR #12 머지를 진행하려면 '머지'라고 입력해 주세요."
```

## 한계 및 제약 (Limitations)

- 전문 엔지니어링 설계나 아키텍처 깊이를 생략하지 않습니다.
- 필수 검증 게이트나 에러를 숨기지 않습니다.

## 문제 해결 (Troubleshooting)

- **Error**: `CognitiveOverloadDetected`
  - **Cause**: 한 턴에 여러 개의 질문이나 분기 선택지가 제시된 경우.
  - **Solution**: 우선순위가 가장 높은 단 하나의 액션만 남기고 나머지는 정리.
- **Error**: `ContextDerailmentWarning`
  - **Cause**: 불필요한 추가 아이디어로 인해 사용자의 집중이 분산된 경우.
  - **Solution**: 현재 진행 상태를 재확인하고 원래 작업의 다음 단계로 즉시 복귀(fallback).
