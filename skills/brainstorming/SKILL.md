---
name: brainstorming
description: >-
  Use this skill for product planning, ideation, requirement refinement, problem discovery, and market/technical research using structured brainstorming frameworks and research subagents.
---

# Product Planning & Structured Brainstorming

이 스킬은 **기획자(Product Planner / PM)**와 엔지니어링 리드가 새로운 제품이나 기능을 기획할 때, 사용자의 진짜 문제를 발굴하고, 구조화된 브레인스토밍과 리서치를 통해 검증 가능한 최소 기능 제품(MVP) 및 PRD(Product Requirement Document)로 구체화하는 표준 실행 지침입니다.

---

## 1. Core Planning Principles (기획 3대 원칙)

1. **Problem-First, Not Solution-First (솔루션보다 문제 우선)**
   - "어떤 기술/기능을 만들까?"가 아니라 "사용자가 겪는 핵심 고통(Pain Point)이 무엇인가?"에서 출발합니다.
   - 안티패턴: 해결할 명확한 문제 없이 최신 유행 기술이나 복잡한 기능을 추가하는 행위.
2. **Diverge then Converge (발산 후 수렴)**
   - 처음부터 실현 가능성에 갇혀 아이디어를 검열하지 마십시오. 가능한 많은 가설과 대안을 발산(Diverge)한 뒤, 데이터와 명확한 프레임워크로 우선순위를 수렴(Converge)합니다.
3. **Hypothesis-Driven & Testable (가설 기반 검증성)**
   - 모든 기획 내용은 검증 가능한 가설이어야 합니다.
   - 형식: *"우리가 [특정 기능]을 제공하면, [타겟 사용자]는 [기대 결과]를 달성할 것이며, 이는 [정량 지표]로 입증된다."*

---

## 2. Structured Brainstorming Frameworks (발산 및 수렴 기법)

### 발산(Divergence) 기법
- **SCAMPER**:
  - **S**ubstitute (대체): 기존 프로세스나 요소를 다른 것으로 바꿀 수 있는가?
  - **C**ombine (결합): 서로 다른 두 기능을 하나로 결합할 수 있는가?
  - **A**dapt (적용): 다른 도메인의 성공 사례를 우리 문제에 적용할 수 있는가?
  - **M**odify/Magnify (변형/확대): 강조하거나 극대화할 수 있는 핵심 가치는 무엇인가?
  - **P**ut to other use (용도 변경): 기존 자산을 다른 타겟 고객에게 제공할 수 있는가?
  - **E**liminate (제거): 불필요한 단계, 화면, 입력을 완전히 없앨 수 있는가? (Ponytail 원칙과 연계)
  - **R**everse (역발상): 순서를 뒤집거나 반대로 접근하면 어떻게 되는가?
- **How Might We (HMW)**:
  - 문제를 기회로 전환하는 질문 공식: *"어떻게 하면 [사용자]가 [장애물 없이] [목표를 달성]하도록 도울 수 있을까?"*

### 수렴(Convergence) 기법: RICE & MoSCoW
아이디어 풀에서 개발 착수 우선순위를 객관적 수치로 결정합니다:

$$\text{RICE Score} = \frac{\text{Reach (영향받는 사용자 수)} \times \text{Impact (사용자당 영향도: 0.25~3)} \times \text{Confidence (확신도: 50%~100\%)}}{\text{Effort (공수: 인월 or 스토리포인트)}}$$

- **MoSCoW 우선순위화**:
  - **Must Have**: 출시를 위한 필수 기능 (없으면 제품 가치 성립 불가).
  - **Should Have**: 중요하지만 대체 수단이 있는 기능.
  - **Could Have**: 있으면 좋으나 리소스 부족 시 생략 가능한 기능.
  - **Won't Have (this time)**: 이번 버전(MVP)에서는 의도적으로 배제할 범위(Non-Goals).

---

## 3. Research & Data-Driven Discovery (리서치 연계)

기획자는 감에 의존하지 않고 적극적인 시장/기술 리서치를 병행합니다.

### Research Workflow & Antigravity 내장 도구 연계
1. **리서치 서브에이전트 위임**:
   - 광범위한 시장 조사나 기술 스택 조사가 필요할 때 내장 `research` 서브에이전트를 호출(`invoke_subagent`)하여 컨텍스트 오염 없이 팩트 기반 요약본을 수신합니다.
2. **웹 검색 및 벤치마킹**:
   - `search_web` 도구를 활용하여 유사 서비스의 UX 패턴, 가격 정책, API 명세, 사용자 불만 사항을 조사합니다.
3. **인터뷰 및 요구사항 인터랙션**:
   - 기획 결정의 트레이드오프나 불확실성이 있을 경우 사용자에게 `/grill-me` 인터뷰 모드를 제안하거나 `ask_question`으로 의사결정을 확인합니다.

---

## 4. Lean PRD (Product Requirement Document) Template

기획자는 엔지니어링 스쿼드가 즉시 착수할 수 있도록 아래 표준 양식의 린 PRD를 도출합니다:

```markdown
# [PRD] 기능/제품 이름

## 1. Problem & Context (해결하려는 문제)
- **배경**: 사용자가 현재 겪고 있는 불편함과 비효율.
- **타겟 사용자**: 누구를 위한 기능인가?

## 2. Hypothesis & Value Proposition (가설 및 핵심 가치)
- **가설**: [기능]을 통해 [사용자 고통]을 해소한다.
- **핵심 성공 지표 (KPI)**: 어떻게 성공을 측정할 것인가? (예: 작업 소요 시간 50% 단축, 전환율 15% 상승)

## 3. MVP Scope (최소 기능 범위)
### Must Have (핵심 기능)
- [ ] 기능 1: 상세 설명
- [ ] 기능 2: 상세 설명

### Non-Goals (이번 스코프에서 제외할 사항)
- [ ] 제외 사항 1 (YAGNI 원칙 준수)
- [ ] 제외 사항 2

## 4. User Journey & Acceptance Criteria (사용자 여정 및 인수 조건)
- **시나리오**: 사용자가 진입하여 목표를 완수하는 단계별 흐름.
- **Given-When-Then 인수 기준**:
  - *Given* 사용자가 로그인 상태일 때
  - *When* 특정 버튼을 클릭하면
  - *Then* 결과 화면이 즉시 표시된다.

## 5. Risks & Trade-offs (위험 요소 및 트레이드오프)
- 기술적 불확실성, 보안 요구사항, 외부 의존성.
```

---

## 5. Squad Hand-off (엔지니어링 스쿼드 이관)

기획이 수립되면 다음 순서로 엔지니어링 스쿼드에 이관합니다:
1. **AI Agent Engineer & Squad Lead 리뷰**: 기획 스코프의 실현 가능성 및 하네스/테스트 가능 여부 검토.
2. **인터페이스 계약 확정**: PRD의 사용자 여정을 바탕으로 API 엔드포인트 및 DB 엔티티 정의.
3. **Stage 1~5 파이프라인 가동**: 프론트엔드, 백엔드, 데이터 엔지니어가 구현 착수.
