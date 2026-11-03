# Tiered Decisions Implementation Plan

> 실행 방식: 이번 작업의 사용자 위임에 따라 Tech Lead가 직접 구현하고 별도 검토자가 판단/보안을 검토한다.

**Goal:** 근거와 책임자를 중심으로 계층별 의사결정 계약을 적용한다.
**Architecture:** 기존 14개 역할을 재사용하고 단일 결정 계약을 연결한다. 투표를 자문으로 전환하되 권한·독립 검수·중단 경계는 유지한다.
**Tech Stack:** Markdown, 기존 Python unittest/행동 평가 실행기.
**Spec:** ../specs/2026-11-04-tiered-decisions-design.md

## Global Constraints
- 기존 역할 수·외부 의존성 추가 없음; 한/영·호환 진입점 동기화.
- 이번 위임은 이번 변경에만 적용; 미래 kickoff 질문과 독립 보안 게이트 유지.
- 과거 평가 해시를 새 정책에 맞춰 고치지 않음; 새 응답·검토 증거 수집.

## Review Focus
- 7표·미제출이 가역적인 분야 결정을 막지 않는지.
- 분야 충돌이 하위 역할 임의 수정이나 전원 투표로 흐르지 않는지.
- Tech Lead/다수 의견이 보안 차단을 무효화하지 않는지.
- 만료된 위임을 다음 작업의 승인으로 취급하지 않는지.
- 사용자 재검토가 미실행 후속 행동을 중단하고 이전 근거를 보존하는지.

## Task 1: 결정 계약과 연결 지침
- [x] 기존 규칙으로 사례 판단을 수집해 현재 문제 확인.
- [x] references/decision-governance.md 및 _en.md에 tier·경로·판정·위임·재검토 계약 작성.
- [x] 정식/호환 SKILL·roles, 호환성·리뷰 체크리스트·README의 충돌 규칙 교체.
- [x] 사례를 새 계약으로 독립 실행하고 결과/누락 점검.

## Task 2: 회귀 평가 및 전달
- [x] evals/scenarios.json의 투표 사례 갱신 및 5개 경계 사례 추가; tests/test_behavior_evals.py fixture/부정 검사 갱신.
- [x] evals/run_evals.py에 새 정책 snapshot과 actions 추가; 새 독립 검토 응답을 기록하고 CI 재생 대상 갱신.
- [x] python -m unittest discover -s tests -v, bash scripts/verify-harness.sh, 새 행동 기록 재생, git diff --check 실행.

전달 절차: 변경 commit 이후 최신 head/base 독립 보안 검수를 확인하고 브랜치 push·PR 생성. 결과는 PR 본문에 기록하며 머지는 수행하지 않는다.
