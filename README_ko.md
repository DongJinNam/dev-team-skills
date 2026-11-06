# dev-team-skills

[English](README.md) | [한국어](README_ko.md)

> Andrej Karpathy의 엔지니어링 철학과 실용주의 시니어 개발 원칙을 기반으로 구축된 크로스 플랫폼(Windows/macOS) AI 코딩 에이전트 스킬 & 룰 모음 저장소입니다.  
> **Google Antigravity**, **Claude Code**, **OpenAI Codex**, **Cursor** 등 다양한 AI 코딩 환경에서 6개 책임 역할과 필요한 전문 역량으로 에이전트 조직을 꾸리고, **결정론적 하네스(Harness Engineering)**와 **3대 플랫폼 마켓플레이스 규격**을 통해 고품질 소프트웨어를 배포할 수 있도록 지원합니다.

---

## 🌟 왜 다른 스킬들보다 압도적으로 우수한가? (Why This Is Superior)

일반적인 프롬프트 모음이나 단편적인 에이전트 스킬들과 비교했을 때, `dev-team-skills`는 다음과 같은 명확한 비교 우위를 가집니다:

| 비교 항목 | 일반 에이전트 프롬프트 / 룰 모음 | **dev-team-skills** |
| :--- | :--- | :--- |
| **조직 커버리지** | 단일 코더 또는 단순 페어 프로그래밍에 한정 | **6개 책임 역할로 기획·개발·품질·보안·운영을 연결하고 전문 역량을 선택 활성화** |
| **품질 보증 방식** | LLM의 "완료했습니다"라는 환각에 의존 | **결정론적 평가 하네스(`verify-harness`) 및 자가 치유(Self-healing) 루프** |
| **확장성 & 생태계** | 로컬 텍스트 복사 및 수동 설정 | **Antigravity, Claude Code, OpenAI Codex 3대 마켓플레이스 규격 100% 호환** |
| **실용주의 철학** | 불필요한 보일러플레이트 및 라이브러리 남용 | **Andrej Karpathy 원칙 & Ponytail (Standard Library First, YAGNI, 최소 코드)** |
| **협업 & 인지 부하** | 장황하고 피로한 AI 번역투 설명 | **카카오페이 스타일 PR 템플릿, 결론 우선(ADHD 최적화), 자연스러운 한국어(Humanizer)** |
| **크로스 플랫폼** | 특정 OS 명령어(Linux 전용 curl/bash)로 실패 빈번 | **Windows(PowerShell) & macOS/Linux(Bash) 동등 지원 및 CI 자동 검증** |

---

## 🏛️ Constitution & Principles (기본 행동 헌법)

[`GEMINI.md`](./GEMINI.md) | [`CLAUDE.md`](./CLAUDE.md) | [`CODEX.md`](./CODEX.md) | [`AGENTS.md`](./AGENTS.md)

1. **Don't assume. Don't hide confusion. (추측 및 침묵 금지)**
   - 모호한 요구사항은 독단적으로 판단하지 않고 명확한 트레이드오프와 함께 사용자에게 확인받습니다.
2. **Minimum code & Standard library first. (Ponytail & YAGNI)**
   - "최고의 코드는 작성하지 않은 코드입니다." 외부 라이브러리 추가 전 언어 내장 표준 라이브러리와 네이티브 플랫폼 기능으로 해결합니다.
3. **Touch only what you must. Clean up your mess. (영역 한정 및 정리)**
   - 작업과 무관한 파일의 임의 수정(오지랖 리팩토링)을 금지하고 임시 파일은 작업 완료 전 깨끗이 정리합니다.
4. **Define success criteria. Loop until verified. (검증 완료 전 종료 금지)**
   - 완료 전 명확한 성공 검증 기준(DoD)을 수립하고 실제 빌드, 테스트, 헬스체크 명령어를 실행하여 증명합니다.
5. **High-Impact Communication & ADHD Optimization (소통 최적화)**
   - 서두의 미사여구를 배제하고 결론과 다음 행동(Lead with next action)을 가장 먼저 제시하며, 1단계 집중을 유도합니다.
6. **Cross-Platform Compatibility (Windows & macOS)**
   - Windows(PowerShell)와 macOS/Linux(Bash) 환경 모두를 지원하는 크로스 플랫폼 스크립트와 명령어를 제공합니다.

---

## 📦 스킬 모음 (Skills Collection)

| 스킬 이름 | 설명 | 주요 특징 |
| :--- | :--- | :--- |
| **`engineering-squad`** | 6개 책임 역할 & 작업 크기에 맞춘 실행 | 기획, 마케팅, 재무, AI 하네스, 개발, QA, 배포, SRE 협업 및 체계적 파이프라인 |
| **`brainstorming`** | 제품 기획, 문제 정의 및 체계적 아이디어 도출 | SCAMPER, HMW, RICE 점수표, 린 PRD 템플릿, `research` 서브에이전트 연계 |
| **`harness-engineering`** | AI 에이전트 평가 하네스 및 마켓플레이스 패키징 | 결정론적 오라클, 3대 Marketplace 규격(`plugin.json`, `.claude-plugin`, `.codex-plugin`), 자가 치유 루프 |
| **`code-review`** | ROI 중심의 역할별 디자인 패턴 코드 리뷰 | 3단계 심각도(🔴필수 / 🟡확인요청 / 🟢권장), 필요한 전문 역량별 체크리스트 |
| **`ponytail`** | 극단적 미니멀리즘 시니어 개발자 사고방식 | Standard Library First, 무분별한 래퍼/의존성 제거 |
| **`humanizer`** | 영문 AI 문체 패턴 제거 (English) | Wikipedia AI 작성 징후 가이드 기반 작위적 수사, 삼분법, 과장, 로봇투 제거 |
| **`humanizer-kr`** | 자연스러운 한국어 테크니컬 라이팅 | AI 번역투, 이중 피동 제거, 의도 보존 윤문 |
| **`i-have-adhd`** | 인지 과부하 방지 및 초집중 워크플로우 | 결론 우선, 단일 액션 종결, 불필요 곁가지 차단 |

---

## 👥 Engineering Squad: 6개 책임 역할

기존 15개 역할명(14개 전문 역할+Lead)을 6개 책임 역할로 통합합니다. Tier 1/2 결정 책임자는 8개에서 6개로 줄어듭니다. 어느 수치도 실제 호출 인원이나 토큰 절감률을 뜻하지 않습니다.

| 책임 역할 | 통합 업무 |
| --- | --- |
| Tech Lead | 분야 간 결정·FinOps·인계·최종 쉬운 설명 |
| Product Lead | 기획·마케팅·근거·반론 실험 |
| Engineering Lead | 프론트엔드·백엔드·데이터·AI/하네스 역량 |
| Quality Lead | 완료 기준·테스트 설계·QA 실행·AC 증거 |
| Delivery Lead | DevOps·SRE·배포·복구 |
| Security Review Engineer | 독립 보안 판정과 별도 컴플라이언스 적용성/조치 |

문서 수정은 Lead 겸임과 독립 Security를 기본으로 하고, 기능 변경에는 Engineering/Quality를 활성화합니다. 제품·운영 변경은 해당 책임자를 추가하며 독립 산출물이나 전문성이 필요할 때만 범위를 나눕니다. 겸임해도 필수 검증을 생략하지 않습니다.

[정본 실행 지침](skills/engineering-squad/SKILL.md), [역량·기존 명칭 매핑](skills/engineering-squad/references/roles.md), [Tier별 결정](skills/engineering-squad/references/decision-governance.md)을 적용합니다. 모든 PR의 머지 전 최신 head/base 독립 보안 PASS와 미해결 컴플라이언스 위반 차단, 기존 시작/중단 질문과 사용자 이의를 유지합니다.

외부 자료는 후보이며 사용 증거가 아닙니다. [활용 계약](skills/engineering-squad/references/tool-adoption.md)은 DISCOVERED / INSPECTED / AVAILABLE / APPLIED / VERIFIED와 실제 PASS/FAIL/NOT_RUN을 구분합니다. [확인일을 남긴 후보 목록](skills/engineering-squad/references/external-skill-references.md)에서 Superpowers·skill-creator·Playwright CLI·Agent Skills 규격 중 작업에 필요한 부분만 읽습니다.

[개선안·토론안](docs/superpowers/specs/2026-11-06-lean-squad-design.md)에 대안·반론·검증 한계를 기록했습니다. 문서 분량 감소를 토큰 실측 절감으로 표현하지 않습니다.

---

## 🛍️ 3대 플랫폼 마켓플레이스 패키징 규격 및 하네스 검증

본 저장소는 **Google Antigravity**, **Claude Code**, **OpenAI Codex** 3대 AI 코딩 에이전트 마켓플레이스 규격을 모두 충족하여, 단일 번들 형태로 손쉽게 검색·설치·배포할 수 있습니다:

| 플랫폼 | 마켓플레이스 매니페스트 / 카탈로그 규격 | 활성화 헌법 룰 & 스킬 경로 |
| :--- | :--- | :--- |
| **Google Antigravity** | `plugin.json` (메타데이터 및 추천 프롬프트) | `rules/AGENTS.md` & `skills/*/SKILL.md` |
| **Claude Code** | `.claude-plugin/marketplace.json` & `.claude-plugin/plugin.json` | `CLAUDE.md` & `skills/*/SKILL.md` |
| **OpenAI Codex** | `.codex-plugin/plugin.json` 및 `plugin.json` | `CODEX.md` / `AGENTS.md` & `skills/*/SKILL.md` |

### 🔍 결정론적 하네스 무결성 검증 (Cross-Platform)

Bash와 PowerShell이 같은 Python 검증기를 호출합니다. JSON 매니페스트 4개의 문법과 비어 있지 않은 문자열 `name`·`description`, 마켓플레이스 `plugins`의 객체 배열 여부를 검사합니다. 각 스킬은 파일 첫머리에 닫힌 YAML Frontmatter가 있어야 하며, 안전한 파서로 `name`·`description`을 확인하고 중복 키를 거부합니다. 헌법 5개 파일은 SHA-256으로 바이트 단위 동기화를 검사하고, 영문 파일이 하나라도 있으면 영문 5개도 모두 존재하고 일치해야 합니다.

**Python 3.10 이상과 PyYAML이 필요합니다.** JSON·해시는 표준 라이브러리로 처리하고, YAML은 직접 파서를 구현하는 대신 안전한 파서를 사용합니다. 실행기가 선택하는 인터프리터(`python3`, `python`, Windows의 `py -3` 순서)와 같은 Python으로 고정 버전 의존성을 설치합니다:

```bash
python -m pip install -r scripts/requirements-harness.txt
```

```bash
# Windows (PowerShell)
.\scripts\verify-harness.ps1

# macOS / Linux (Bash)
./scripts/verify-harness.sh
```

`--root <경로>`로 다른 패키지 디렉터리를 선택할 수 있습니다. 종료 코드는 패키지 PASS `0`, 잘못된 패키지 `1`, 필수 실행 환경 부재·잘못된 인자 `2`입니다. UTF-8 BOM, LF/CRLF, 공백을 포함한 경로를 지원합니다. CI는 Linux·Windows·macOS에서 동일한 정상·오류 입력을 Bash·PowerShell로 각각 검사합니다. Windows의 Bash 시험은 Git Bash에서 실행해야 WSL의 `bash.exe` 대신 Git Bash를 선택합니다. PowerShell에서 실행할 때는 `HARNESS_LAUNCHER=pwsh`를 지정합니다:

```bash
python -m unittest discover -s tests -v
# HARNESS_LAUNCHER=bash|pwsh|python 으로 실행기 선택 (기본값: bash)
# PowerShell 예: $env:HARNESS_LAUNCHER = 'pwsh'
# Windows Git Bash: export HARNESS_BASH="$(cygpath -w "$BASH")"
```

이 검사는 **저장소의 패키지 구조 계약**을 확인합니다. 공급사 전체 스키마나 설치 호환성을 보장하지 않습니다. 에이전트 행동·제품 테스트·독립 보안 검수는 이 명령에서 `NOT_RUN`으로 표시하며, 기존 승인 게이트는 그대로 적용합니다.

### 에이전트 판단·보고 회귀시험

[19개 압박 상황과 실행기](evals/README.md)로 테스트 미실행 보고, 보안 승인 만료, 계층별 책임 결정, 중단 조건, 요약의 근거 보존, 필요한 범위의 재검증을 검사합니다. CI는 채점기 자체 시험과 기록된 실제 에이전트 응답의 재검사를 수행하며, 새 모델 실행이나 실제 도구 실행을 검증한 것으로 표시하지 않습니다. 정책·상황·채점기 해시와 별도 의미 검토를 확인해 오래되거나 누락된 기록이 판단 PASS로 보고되지 않도록 합니다.

```bash
python evals/run_evals.py --replay evals/runs/2026-11-06-lean-squad.json
```

### Superpowers와 함께 사용

[단계별 담당·승인 자료 재사용 계약](skills/engineering-squad/references/superpowers-compatibility.md)을 적용합니다. COMBINED에서는 dev-team이 시작 질문·게이트·비용·최종 설명을 맡고, Superpowers가 확인된 설계·계획·구현 절차를 맡습니다. 패키지 출처와 현재 승인을 확인해 공유하고 누락·변경분만 보완합니다. 선택 사항이 없으면 STANDALONE으로 진행하되 필수 선행조건 부재는 해당 단계를 차단합니다. 자동 설치나 측정하지 않은 비용 절감 수치를 주장하지 않습니다.

---

## 💻 플랫폼별 마켓플레이스 설치 및 사용 가이드

### 1. Google Antigravity

#### 방법 A: Marketplace 카탈로그 또는 UI로 추가 (권장)
- Antigravity IDE 상단 메뉴의 **Customizations** > **Marketplace** 진입
- 검색창에 `dev-team-skills`를 검색한 뒤 **[Install]** 클릭
- 또는 채팅창 내 플러그인 카드를 통해 원클릭 설치:
  ```markdown
  <plugin-card catalog-id="dev-team-skills"></plugin-card>
  ```

#### 방법 B: 로컬 전역 플러그인 디렉터리에 설치
```bash
# Windows (PowerShell)
git clone https://github.com/DongJinNam/dev-team-skills.git ~/.gemini/config/plugins/dev-team-skills

# macOS / Linux (Bash)
git clone https://github.com/DongJinNam/dev-team-skills.git ~/.gemini/config/plugins/dev-team-skills
```

#### 방법 C: 프로젝트 워크스페이스 전용 플러그인
- 작업 프로젝트 루트에 `.agents/plugins/dev-team-skills` 경로로 클론하거나 `.agents/plugins.json`에 선언하여 팀원들과 Git으로 공유할 수 있습니다.

---

### 2. Claude Code

#### 방법 A: Claude Code 마켓플레이스 명령어로 등록 및 설치 (공식 권장)
Claude Code CLI 또는 대화형 프롬프트에서 원격 마켓플레이스로 등록하고 즉시 설치합니다:

```bash
# 1. GitHub 저장소를 Claude Code 마켓플레이스로 추가
/plugin marketplace add DongJinNam/dev-team-skills

# 2. dev-team-skills 플러그인 원클릭 설치
/plugin install dev-team-skills
```

> **CLI 직접 실행 시**:
> ```bash
> claude plugin marketplace add DongJinNam/dev-team-skills
> claude plugin install dev-team-skills
> ```

#### 방법 B: 플러그인 유효성 로컬 검증
```bash
claude plugin validate
```

#### 방법 C: 로컬 프로젝트 메모리 연동
- 대상 프로젝트 루트에 `CLAUDE.md`를 심어 헌법 규칙을 주입하고, `skills/` 디렉터리의 직무 가이드를 호출합니다.

---

### 3. OpenAI Codex

#### 방법 A: Codex CLI 마켓플레이스 추가 (권장)
```bash
# 1. 마켓플레이스 카탈로그 등록
codex plugin marketplace add DongJinNam/dev-team-skills --ref main

# 2. 플러그인 설치
codex plugin install dev-team-skills
```

#### 방법 B: Codex CLI 대화형 관리자
- Codex CLI 프롬프트에서 `/plugins`를 입력하여 인터랙티브 플러그인 매니저를 열고 `dev-team-skills`를 검색하여 활성화합니다.

#### 방법 C: 프로젝트 코딩 에이전트 지침 연동
- 프로젝트 루트에 `CODEX.md` 또는 `AGENTS.md`를 배치하면 코딩 에이전트 세션 시작 시 호스트 지원 범위에서 헌법을 읽고 필요한 전문 역량 지침을 선택합니다.

---

## 📝 Pull Request 템플릿 (카카오페이 스타일)

카카오페이 기술블로그 [「PR을 더 느리게 만들기 위한 고민 (Slow PR, Fast Dev)」](https://tech.kakaopay.com/post/kakaopayins-slow-pr-fast-dev/)의 실천 철학을 기반으로 한 [`.github/pull_request_template.md`](./.github/pull_request_template.md)가 포함되어 있습니다:

- `# 해결하려는 문제가 무엇인가요?`
- `# 왜 해야 하나요?`
- `# 어떻게 해결했나요?`
- `# 이 PR의 한계 & 트레이드오프`
- `# 기존 기능에 미치는 영향`
- `# Edge Case & 실패 시나리오`
- `# 검토한 대안과 선택 이유`
- `# 리뷰 포인트 (파일/영역별 Risk 🔴🟡🟢)`

---

### Tier별 의사결정과 Creative Rookie

6개 책임 역할과 위임한 전문 역량을 **Tier 1 Tech Lead → Tier 2 분야 책임자 → Tier 3 실행 역할**로 구성합니다. 분야 내 결정은 해당 책임자가, 분야 간 충돌은 Tech Lead가 근거·반론으로 판단합니다. 신입의 아이디어·반론과 사용자 재검토 권한은 유지하며 15표·8표는 요청 시 자문으로만 사용합니다. 보안·컴플라이언스 차단과 예산·권한을 직급으로 면제할 수 없습니다. [상세 역할·결정 계약](skills/engineering-squad/references/decision-governance.md).

## 📜 License
MIT License
