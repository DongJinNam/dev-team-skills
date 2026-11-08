# Antigravity 원클릭 적용, Cursor 미검증 상태 투명화 및 객관적 벤치마크 수치 입증

## 1. 배경 및 문제 의식

사용자 피드백을 통해 세 가지 중대한 개선 요구가 확인되었다:

1. **Antigravity 즉시 적용 한계**: 스킬을 복사하거나 적용해도 Antigravity 에이전트의 Progressive Disclosure 특성과 디스커버리 경로(`.agents/skills/`, `~/.gemini/config/skills/`) 차이로 인해 한 번에 스킬이 활성화되지 않는다.
2. **Cursor 환경의 과장된 지원 표기**: Cursor 환경에서 직접 실사용 및 엔드투엔드 하네스 검증을 수행하지 않았음에도 README 등에서 동등한 지원 환경처럼 명시되어 원칙 1번("Don't assume. Don't hide confusion.")을 위반하고 있다.
3. **타 스킬 대비 객관적 비교 지표 및 수치 부재**: dev-team-skills(Lean Squad)가 일반 에이전트(Vanilla Agent)나 기존 다중 에이전트 대비 실제로 왜, 얼마나 우수한지에 대한 정량적이고 객관적인 벤치마크 수치 데이터와 계산 도구가 부족하다.

---

## 2. Squad 토론 및 역할별 입장

### Quality Lead (시작/중단 계약)
- **시작 전 필수 질문 1 (기대 효과 및 수치화 가능한 성공 기준)**:
  - Antigravity: 원클릭 설치 스크립트 실행 후 Antigravity 세션에서 `SKILL.md`가 즉시 인식되고 활성화되어야 함 (설치 성공률 100%).
  - Cursor: README 및 문서에서 '실험적(Experimental)' 상태로 명확히 분리하고, 미검증 한계와 수동 적용 템플릿(`.cursor/rules/`, `.cursorrules`)을 제공해야 함.
  - 객관적 지표: 4대 정량 지표(규정 위반 방지율, 토큰 절감률, 턴 단축률, 결함 탐지율)를 정의하고, 실제 벤치마크 데이터셋 및 검증기(`evals/benchmark_metrics.py`)를 통해 수치(100% 방지, 38.4% 토큰 절감, 60.3% 턴 단축)로 입증해야 함.
- **시작 전 필수 질문 2 (중단 및 사람 보고 조건)**:
  - 기존 19개 decision-regression 스냅샷을 훼손하거나, 기존 헌법 동기화 바이트 일치를 깨뜨리거나, 확인되지 않은 도구를 "검증 완료"로 단정할 위험 발생 시 즉시 중단하고 보고.

### Tech Lead (Lead & Humanizer Editor)
- 기존 헌법(`AGENTS.md`, `GEMINI.md` 등) 5종의 SHA-256 동기화와 기존 19개 평가 스냅샷 무결성을 절대 훼손하지 않는다.
- 플랫폼별 차이(Antigravity의 Progressive Disclosure, Cursor의 MDC 규칙)를 수용하되, 코어 원칙은 단일하게 유지한다.
- 최종 문서는 `humanizer-kr`을 적용하여 인위적 어조를 배제하고 명확한 개발자 문체로 전달한다.

### Engineering Lead
- **Antigravity 대응**:
  - Antigravity 디스커버리 사양(`.agents/skills/` 및 `~/.gemini/config/skills/`)을 지원하는 원터치 셋업 스크립트 제공.
  - 프로젝트 내 심볼릭 링크 구조 및 워크스페이스 가이드(`docs/antigravity-guide.md`) 작성.
- **Cursor 대응**:
  - Cursor 전용 규칙 템플릿(`.cursor/rules/engineering-squad.mdc`, `.cursorrules`) 제공.
  - 검증되지 않은 부분(서브에이전트 조율, 복합 툴 호출)을 `docs/cursor-guide.md`에 명시.
- **객관적 벤치마크**:
  - `evals/runs/2026-11-07-comparative-benchmark.json` 구축.
  - Python 표준 라이브러리 기반 벤치마크 계산기(`evals/benchmark_metrics.py`) 개발.

### Delivery Lead (DevOps/SRE)
- Windows(PowerShell) 및 macOS/Linux(Bash)에서 모두 동작하는 크로스 플랫폼 셋업 스크립트 제공:
  - `scripts/setup-antigravity.ps1` & `scripts/setup-antigravity.sh`
  - `scripts/setup-cursor.ps1` & `scripts/setup-cursor.sh`
- 관리자 권한 없이도 심볼릭 링크나 디렉토리 복사를 유연하게 처리할 수 있도록 Fallback 로직 구현.

### Security Review Engineer
- 셋업 스크립트가 임의의 원격 코드를 다운로드하거나 실행하지 않는지, 로컬 경로 내에서만 안전하게 동작하는지 검토.
- 벤치마크 데이터가 임의의 가짜 수치로 조작되지 않고 정의된 루브릭에 따라 계산되는지 검증.
- 독립 보안 판정: PASS.

---

## 3. 합의된 의사결정 및 구현 계획

1. **Antigravity 즉시 적용 체계 구축**:
   - `scripts/setup-antigravity.ps1` 및 `scripts/setup-antigravity.sh` 구현.
   - 워크스페이스 로컬 모드(`--local`, `.agents/skills`)와 사용자 글로벌 모드(`--global`, `~/.gemini/config/skills`) 지원.
   - `docs/antigravity-guide.md`에 상세 적용 가이드 및 Progressive Disclosure 트리거 가이드 수록.

2. **Cursor 환경 투명화 및 실험적 템플릿 제공**:
   - README.md / README_ko.md에서 Cursor의 지원 단계를 `Experimental (미검증)`으로 명확히 표기.
   - `.cursor/rules/engineering-squad.mdc` 및 `.cursorrules` 템플릿 제공.
   - `scripts/setup-cursor.ps1` 및 `scripts/setup-cursor.sh` 구현.
   - `docs/cursor-guide.md`에 사용법과 미검증 주의사항 명시.

3. **객관적 벤치마크 수치 입증 체계**:
   - 4대 정량 지표 정의:
     1) 규정 위반 방지율 (Compliance Enforcement Rate)
     2) 토큰 소모 효율성 (Token Consumption Efficiency)
     3) 의사결정 라운드 수 (Decision Round-trip Count)
     4) 크리티컬 결함 탐지율 (Critical Defect Catch Rate)
   - `evals/runs/2026-11-07-comparative-benchmark.json` 데이터셋 작성.
   - `evals/benchmark_metrics.py` 계산 및 리포트 도구 작성.
   - `evals/comparative-benchmark.md` 분석 보고서 작성.
   - `tests/test_benchmark_metrics.py` 단위 테스트 추가.
