---
name: harness-engineering
description: >-
  Use this skill to design AI agent test harnesses, deterministic evaluation loops, MCP tool schemas, and package customizations for the 3rd-party Agent Marketplace.
---

# AI Agent Harness Engineering & Marketplace Packaging

이 스킬은 **AI Agent Engineer**가 대규모 언어 모델(LLM)과 자율 코딩 에이전트가 신뢰할 수 있는 방식으로 코드를 생성·검증할 수 있도록 **평가 하네스(Evaluation Harness)**를 구축하고, 에이전트 스킬/플러그인을 **3rd-Party Marketplace 규격**으로 패키징할 때 사용하는 표준 실행 지침입니다.

---

## 1. What is Agent Harness Engineering? (하네스 엔지니어링이란?)

**하네스 엔지니어링(Harness Engineering)**은 AI 에이전트가 "코드 작성을 완료했다"고 착각하는 환각(Hallucination)을 막고, 실제 환경에서 소프트웨어를 자율적으로 빌드하고, 테스트를 통과시키며, 오류를 스스로 치유(Self-healing)할 수 있도록 감싸는 **결정론적 평가 및 실행 인프라**를 설계하는 공학입니다.

### 핵심 4대 구성 요소
```mermaid
flowchart LR
    Prompt["Agent Prompt / Policy"] --> Action["Tool Invocation / Code Edit"]
    Action --> Sandbox["Sandboxed Environment"]
    Sandbox --> Eval["Deterministic Harness\n(Lint, Test, Schema, Healthz)"]
    Eval --> Feedback["Structured Feedback Loop\n(Pass / Fail + Diagnostics)"]
    Feedback --> Prompt
```

1. **Deterministic Oracles (결정론적 오라클)**:
   - LLM이 자신의 출력을 평가하게 하지 않습니다. 컴파일러, 린터, 유닛 테스트 러너, HTTP 헬스체크 등 결정론적 도구로 결과를 판정합니다.
2. **Standardized Tool Contracts (표준 툴 계약)**:
   - 도구(Tool) 및 MCP(Model Context Protocol) 서버의 입출력 스키마(JSON Schema)를 정의하고 잘못된 입력·출력의 거부를 검사합니다. 스키마 정의만으로 도구 오류 0%를 보장하지 않습니다.
3. **Self-Healing Feedback Loops (자가 치유 피드백 루프)**:
   - 테스트 실패 시 원시 스택 트레이스와 실패 입력값을 정형화된 JSON 또는 마크다운 진단 보고서로 에이전트에게 재전송하여 닫힌 루프(Closed-loop) 내에서 자가 수정하게 만듭니다.
4. **Regression Evaluation (회귀 평가 벤치마크)**:
   - 시스템 프롬프트, 룰, 스킬 수정 시 이전 정상 동작 케이스들이 깨지지 않는지 골든 태스크(Golden Tasks) 스위트로 회귀 평가를 수행합니다.

---

## 2. 3rd-Party Agent Marketplace Specification (마켓플레이스 규격)

다음은 이 저장소의 번들 구조 예시이며 모든 호스트의 공통 규격은 아닙니다. 대상 호스트의 현재 매니페스트·CLI 도움말과 실제 등록/설치 결과를 확인합니다. 한 호스트의 성공을 다른 호스트의 호환성 증거로 사용하지 않습니다.

### 1) Plugin Directory Layout
```text
<plugin-root>/
├── plugin.json              # 필수: 플러그인 메타데이터 매니페스트 (JSONC)
├── README.md                # 필수: 사용자 안내 및 퀵스타트 문서
├── skills/                  # 스킬 번들 디렉터리
│   └── <skill-name>/
│       ├── SKILL.md         # 필수: YAML frontmatter (name, description)
│       ├── references/      # 심화 지침 및 런북
│       └── scripts/         # 크로스 플랫폼 실행 스크립트 (.ps1 & .sh)
├── rules/                   # 플러그인 활성화 시 항시 적용되는 헌법
│   └── AGENTS.md
└── mcp_config.json          # 선택: MCP 도구 서버 연동 설정
```

### 2) `plugin.json` Manifest Schema
```json
{
  "name": "dev-team-skills",
  "displayName": "Dev Team Skills & Engineering Squad",
  "version": "1.1.0",
  "description": "Cross-platform Pragmatic Engineering Squad (8 Roles), Brainstorming, Code Review, AI Agent Harness & Ponytail Minimalism.",
  "author": "DongJinNam",
  "homepage": "https://github.com/DongJinNam/dev-team-skills",
  "repository": {
    "type": "git",
    "url": "https://github.com/DongJinNam/dev-team-skills.git"
  },
  "suggestedPrompts": [
    "기획자 및 AI 하네스 엔지니어를 포함해 신규 기능 개발 스쿼드를 구성해줘",
    "린 캔버스와 브레인스토밍 기법으로 요구사항을 정의하고 PRD를 작성해줘",
    "AI 에이전트의 자가 검증을 위한 Harness Test 및 Eval 루프를 설계해줘"
  ]
}
```

- **`name`**: 전역 고유한 소문자 kebab-case 식별자.
- **`description`**: 마켓플레이스 검색 엔진이 색인하는 1~2문장의 핵심 설명.
- **`suggestedPrompts`**: 마켓플레이스 UI 카드에 표시될 정확히 3개의 예시 프롬프트.

---

## 3. Harness Test Design & Verification Pattern (하네스 테스트 설계)

### 1) 에이전트 자가 검증 하네스 스크립트 구축 원칙
- **크로스 플랫폼 필수**: Windows(PowerShell `.ps1`)와 macOS/Linux(Bash `.sh`) 양쪽 스크립트를 반드시 페어로 제공합니다.
- **명시적 종료 코드 (Exit Codes)**: 성공 시 `0`, 실패 시 `1`을 명확히 반환하여 CI/CD 및 에이전트 루프가 즉각 감지하게 합니다.
- **최소 외부 의존성**: 별도 패키지 매니저 설치 없이 기본 OS 셸 내장 기능(PowerShell 내장 cmdlet, POSIX 셸 문법)으로 동작해야 합니다.

### 2) 골든 태스크(Golden Task) Eval 구조
```text
evals/
├── tasks/
│   ├── task_01_feature_scaffold/
│   │   ├── prompt.txt           # 에이전트에게 부여할 입력 지침
│   │   ├── expected_files.json   # 생성되어야 하는 파일 목록
│   │   └── verify.sh (.ps1)      # 하네스 검증 스크립트
│   └── task_02_refactor_minimal/
└── run-evals.ps1 (.sh)          # 전체 태스크 실행 및 통과율 집계
```

---

## 4. AI Agent Engineer Responsibilities in Squad

엔지니어링 스쿼드 파이프라인에서 AI Agent Engineer는 다음 책임을 수행합니다:

1. **Stage 1 (하네스 & 스펙 정의)**:
   - 기획서(PRD)를 수신하여 각 서브에이전트가 검증할 수 있는 자동화 테스트 하네스 기준(Definition of Done)을 Squad Lead와 함께 설계.
2. **Stage 3 (통합 품질 & 에이전트 하네스 검증)**:
   - 서브에이전트들이 생성한 코드의 스키마 적합성 및 툴 호출 안전성을 평가.
   - 플러그인 번들 유효성 검사기(`verify-harness.ps1`, `verify-harness.sh`)로 로컬 패키지 계약을 검사. 설치·스킬 발견·실제 호출은 대상 호스트에서 별도로 검증.
3. **Stage 4~5 (배포 및 모니터링 하네스 연동)**:
   - CI/CD 파이프라인(`verify-rules-sync.yml` 등)에 에이전트 룰 및 스킬 동기화 하네스 연결.


## 5. 에이전트 판단·보고 회귀시험

### 파일 읽기와 실제 발견

`SKILL.md`와 `SKILL_en.md`는 BOM 없는 UTF-8로 저장하고 첫 줄부터 YAML frontmatter를 시작합니다. CRLF/LF 지원과 BOM 허용은 별개입니다. Windows PowerShell 읽기는 `Get-Content -LiteralPath <경로> -Encoding UTF8`처럼 명시하고, 읽기 오류·깨진 문자·로더 경고를 숨기지 않습니다. 정적 검사 PASS만으로 호스트 로더 PASS를 주장하지 않습니다.

설치 목록 확인 뒤 해당 호스트의 실제 스킬 발견 결과를 확인합니다. 고유 스킬 수와 호환 별칭 엔트리 수를 분리하고 누락·오류를 남깁니다. Codex에서는 지원 버전을 확인한 뒤 `evals/check_skill_discovery.py`의 모델 호출 없는 조회를 사용할 수 있습니다. 프로젝트 설정이 검토된 격리 테스트 경로를 사용하며, Claude 등 미실행 환경은 NOT_RUN으로 남깁니다. 저장소 도구가 설치 패키지에 없으면 사용할 수 있는 호스트 도구로 확인하고 미확인 범위를 기록합니다.

### 비교와 생성 코드 실행

스킬 간 과제 성과는 [활용 증거 계약](../engineering-squad/references/tool-adoption.md#성과-비교를-수행할-때)의 고정 조건·실패 분모·사후 검사·사용량 경계를 따릅니다. 자기 보고나 고정 검사 통과만으로 모든 요구 충족을 단정하지 않고 독립 검토에서 발견한 결함도 기록합니다.

평가 대상이 생성한 코드는 수집과 실행을 분리합니다. 실행 전에 임시 인증 사본·불필요한 시크릿 환경을 제거하고, 별도 검토자가 산출물과 해시를 확인합니다. subprocess나 새 작업 폴더는 보안 sandbox가 아닙니다. 실제 파일·네트워크 접근 통제를 확인하고, 통제가 없으면 사전 검토한 로컬 코드로 범위를 제한해 잔여 노출을 기록합니다. 필요한 통제를 확보하지 못한 미검토 코드는 실행하지 않습니다.

공개 증거에는 필요한 명령·종료 상태·산출물·사용량·버전/해시만 남깁니다. 인증 파일·비공개 추론 기록은 제외하고 개인 경로는 제외하거나 마스킹합니다. 제삼자 스킬 전문은 재배포 조건을 충족하지 않으면 출력 해시·크기·생략 이유로 대체합니다. 원본 전체인지 정제한 로그인지 명시합니다.

### 기존 판단 계약 보존

규칙·스킬을 수정할 때는 [행동 판단 회귀시험](../../evals/README.md)의 19개 압박 상황을 확인합니다. `python evals/run_evals.py`는 입력 없이 `NOT_RUN`이며, 실제 에이전트 응답 또는 명시적으로 선택한 실행 어댑터가 필요합니다. 후보에게는 정책·상황·응답 형식만 제공하고 기대 답안은 분리합니다. 구조화된 결정·행동·사실은 자동 검사하고, 요약의 의미·조건·미확인 상태는 응답자와 별도 검토자가 확인합니다.

기록 재검사(`REPLAY`), 예제 기반 하네스 자체 시험, 새 에이전트 실행을 구분합니다. 정책·상황·채점기 해시 불일치, 필수 사례 누락, 독립 의미 검토 부재는 행동 검증 PASS가 아닙니다. 판단 응답의 PASS는 실제 도구 실행·운영 안전성·독립 보안 승인을 증명하지 않습니다. Tier별 책임 결정·자문 표결 및 보안 게이트를 유지합니다.
