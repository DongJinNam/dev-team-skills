# dev-team-skills

[English](README.md) | [한국어](README_ko.md)

> Andrej Karpathy의 엔지니어링 철학과 실용주의 시니어 개발 원칙을 기반으로 구축된 크로스 플랫폼(Windows/macOS) AI 코딩 에이전트 스킬 & 룰 모음 저장소입니다.  
> **Google Antigravity**, **Claude Code**, **OpenAI Codex** 및 실험적 **Cursor** 연동을 위한 6개 책임 역할과 작업별 전문 역량을 제공합니다. 호스트별 검증 상태와 비교 결과의 한계는 아래에 구분해 기록합니다.

---

## 제공 기능과 검증 상태

6개 책임 역할, 독립 보안 검수, 패키지 검사, 판단 평가와 비용 비교 도구를 제공합니다. 같은 모델의 12회 예비 비교를 수행했으며, 작은 표본의 관찰 결과와 일반적인 우수성 주장을 구분합니다.

| 대상 | 확인한 증거 | 한계 |
| --- | --- | --- |
| Codex CLI 0.167.0 / Windows | 수정 명령의 로컬 설치 3/3 성공; BOM 수정 후 고유 스킬 발견 7/8→8/8 | 원격 설치·다른 OS 미검증; 설치와 작업 품질은 별도 지표 |
| Claude Code | 매니페스트와 안내 제공 | CLI 부재로 설치·호출 NOT_RUN; 100% 호환 보장 없음 |
| 판단 평가 | 병합 정책 19개 재검사; 이전 정책의 별도 3개 상황 검토 | 판단 증거이며 실제 도구 실행·독립 표본이 아님 |
| 타 스킬 비교 | 같은 gpt-6-astra/high에서 기본·Superpowers·ECC·dev-team 각 3과제 실행; 독립 검토 통과 2/3·3/3·3/3·3/3 | 작은 표본; 일반적 우수성·비열등성·금전 절감은 미입증 |

[실측·토론 기록](docs/decisions/2026-11-07-codex-update.md)과 [공정한 비교 절차](evals/skill-comparison.md)를 참조하세요. 미실행은 성공률 0%와 다릅니다.

[12회 비교 결과](docs/decisions/2026-11-07-four-arm-results.md): 이 표본에서 dev-team은 Superpowers보다 시간 7.35%·캐시 포함 처리 토큰 15.61%, ECC보다 시간 14.33%·처리 토큰 20.91%가 적었습니다. 기본 설정보다는 시간·토큰이 늘었고, 비캐시 입력은 두 스킬보다 많아 금전 비용 절감으로 해석하지 않습니다.

로컬 스킬 지침 계층만 비교했습니다. 일부 Windows 정책 읽기에 인코딩 오류가 있어 관측 차이를 스킬 품질만의 효과로 단정할 수 없습니다.

main에서 추가한 [벤치마크 집계기와 입력](evals/comparative-benchmark.md)도 유지합니다. 입력 수치의 재계산은 실제 모델 실행·공급자 사용량의 출처를 인증하지 않으며, 이번 병합에서 해당 데이터의 성과 주장을 검증한 것은 아닙니다. Antigravity 설치와 실험적 Cursor 안내는 아래에 유지했습니다.

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

플랫폼별 메타데이터를 제공합니다. 파일 구조 검사만으로 공급사 규격 전체 준수나 설치·실행 성공을 보장하지 않습니다. Antigravity 설치 안내도 이 작업에서 검증하지 않았습니다.

| 플랫폼 | 마켓플레이스 매니페스트 / 카탈로그 규격 | 활성화 헌법 룰 & 스킬 경로 |
| :--- | :--- | :--- |
| **Google Antigravity** | `plugin.json` (메타데이터 및 추천 프롬프트) | `rules/AGENTS.md` & `skills/*/SKILL.md` |
| **Claude Code** | `.claude-plugin/marketplace.json` & `.claude-plugin/plugin.json` | `CLAUDE.md` & `skills/*/SKILL.md` |
| **OpenAI Codex** | `.codex-plugin/plugin.json` 및 `plugin.json` | `CODEX.md` / `AGENTS.md` & `skills/*/SKILL.md` |

### 🔍 결정론적 하네스 무결성 검증 (Cross-Platform)

Bash와 PowerShell이 같은 Python 검증기를 호출합니다. JSON 매니페스트 4개의 문법과 비어 있지 않은 문자열 `name`·`description`, 마켓플레이스 `plugins`의 객체 배열 여부를 검사합니다. 각 스킬은 파일 첫머리에 닫힌 YAML Frontmatter가 있어야 하며, 안전한 파서로 `name`·`description`을 확인하고 중복 키를 거부합니다. 헌법 5개 파일은 SHA-256으로 바이트 단위 동기화를 검사하고, 영문 파일이 하나라도 있으면 영문 5개도 모두 존재하고 일치해야 합니다. 코드가 붙은 스킬 불변 규칙도 검사합니다. SKL-001은 스킬 파일 위치, SKL-002는 frontmatter 이름과 폴더 이름의 일치, SKL-003은 상대 링크 무결성입니다. `scripts/build-catalog.py`가 스킬 폴더에서 생성하는 `skills/catalog.json`은 스키마(CAT-001)와 폴더와의 drift 여부(CAT-002)를 검사합니다. dry-run materialize diff(MIR-001)는 아무것도 쓰지 않고, 커밋된 `.agents/skills` 미러가 setup 스크립트가 `skills/`에서 만들 결과와 바이트 단위로 같은지 검사합니다.

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

`--root <경로>`로 다른 패키지 디렉터리를 선택할 수 있습니다. 종료 코드는 패키지 PASS `0`, 잘못된 패키지 `1`, 필수 실행 환경 부재·잘못된 인자 `2`입니다. 스킬은 Codex가 읽을 수 있도록 BOM 없는 UTF-8을 요구하며 `SKILL.md`와 `SKILL_en.md`를 검사합니다. LF/CRLF와 공백·한글 경로는 지원합니다. CI는 Linux·Windows·macOS에서 동일한 정상·오류 입력을 Bash·PowerShell로 각각 검사합니다. Windows의 Bash 시험은 Git Bash에서 실행해야 WSL의 `bash.exe` 대신 Git Bash를 선택합니다. PowerShell에서 실행할 때는 `HARNESS_LAUNCHER=pwsh`를 지정합니다:

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
python evals/run_evals.py --replay evals/runs/2026-11-08-main-merge.json
```

### Superpowers와 함께 사용

[단계별 담당·승인 자료 재사용 계약](skills/engineering-squad/references/superpowers-compatibility.md)을 적용합니다. COMBINED에서는 dev-team이 시작 질문·게이트·비용·최종 설명을 맡고, Superpowers가 확인된 설계·계획·구현 절차를 맡습니다. 패키지 출처와 현재 승인을 확인해 공유하고 누락·변경분만 보완합니다. 선택 사항이 없으면 STANDALONE으로 진행하되 필수 선행조건 부재는 해당 단계를 차단합니다. 자동 설치나 측정하지 않은 비용 절감 수치를 주장하지 않습니다.

---

## 💻 플랫폼별 마켓플레이스 설치 및 사용 가이드

### 1. Google Antigravity (설치 안내 제공; 실제 호스트 실행은 별도 검증)

#### 방법 A: 원터치 셋업 스크립트로 한 번에 적용 (가장 추천)
Antigravity의 스킬 검색 경로(`.agents/skills/`) 및 전역 경로(`~/.gemini/config/skills/`)에 원클릭으로 스킬을 연결합니다:
```powershell
# Windows (PowerShell): 현재 워크스페이스에 적용
.\scripts\setup-antigravity.ps1 -Target workspace

# 또는 모든 프로젝트에서 사용할 수 있도록 전역(~/.gemini/config/skills) 설치
.\scripts\setup-antigravity.ps1 -Target global
```
```bash
# macOS / Linux (Bash): 현재 워크스페이스에 적용
bash scripts/setup-antigravity.sh workspace

# 또는 전역 설치
bash scripts/setup-antigravity.sh global
```
> 📖 스킬이 한 번에 로드되지 않는 이유 및 해결책: [Antigravity 환경 적용 가이드](docs/antigravity-guide.md)

#### 방법 B: Marketplace 카탈로그 또는 UI로 추가
- Antigravity IDE 상단 메뉴의 **Customizations** > **Marketplace** 진입
- 검색창에 `dev-team-skills`를 검색한 뒤 **[Install]** 클릭
- 또는 채팅창 내 플러그인 카드를 통해 원클릭 설치:
  ```markdown
  <plugin-card catalog-id="dev-team-skills"></plugin-card>
  ```

#### 방법 C: 로컬 전역 플러그인 디렉터리에 설치
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

이 환경에서는 Claude CLI를 찾지 못해 실제 설치·호출은 **NOT_RUN**입니다. 아래 안내 실행 전 `claude --version`과 `claude plugin --help`로 지원 여부를 확인하세요. [공식 매니페스트 문서](https://code.claude.com/docs/en/plugins-reference) 확인은 실사용 검증이 아닙니다.

#### 방법 A: 마켓플레이스 등록 및 설치

```bash
# 1. GitHub 저장소를 Claude Code 마켓플레이스로 추가
/plugin marketplace add DongJinNam/dev-team-skills

# 2. dev-team-skills 플러그인 원클릭 설치
/plugin install dev-team-skills@dev-team-skills-marketplace
```

> **CLI 직접 실행 시**:
> ```bash
> claude plugin marketplace add DongJinNam/dev-team-skills
> claude plugin install dev-team-skills@dev-team-skills-marketplace
> ```

#### 방법 B: 플러그인 유효성 로컬 검증
```bash
claude plugin validate .
```

#### 방법 C: 로컬 프로젝트 메모리 연동
- 대상 프로젝트 루트에 `CLAUDE.md`를 심어 헌법 규칙을 주입하고, `skills/` 디렉터리의 직무 가이드를 호출합니다.

---

### 3. OpenAI Codex

Codex CLI `0.167.0`은 `plugin add`를 제공합니다. 기존 `plugin install`은 `unrecognized subcommand`로 실패했습니다. 다른 버전은 `codex plugin --help`를 확인하세요.

#### 방법 A: 로컬 checkout 설치

저장소 루트에서 실행합니다. Windows PowerShell과 macOS/Linux Bash에 같은 명령을 쓰며, 실제 로컬 시험은 Windows에서 수행했습니다.

```bash
codex plugin marketplace add .
codex plugin add dev-team-skills@dev-team-skills-marketplace
codex plugin list --json
```

원격 등록은 첫 명령 대신 `codex plugin marketplace add DongJinNam/dev-team-skills --ref main`을 사용합니다. 이번 시험은 로컬 경로만 확인했습니다. 기존 설치 갱신 명령은 `codex plugin marketplace --help`에서 확인하세요.

#### 방법 B: Codex CLI 대화형 관리자
- Codex CLI 프롬프트에서 `/plugins`를 입력하여 인터랙티브 플러그인 매니저를 열고 `dev-team-skills`를 검색하여 활성화합니다.

#### 방법 C: 프로젝트 코딩 에이전트 지침 연동
- 프로젝트 지침은 `AGENTS.md`로 연결합니다. `CODEX.md`만 복사하면 스킬까지 자동 설치된다고 가정하지 마세요. 기존 지침을 덮어쓰지 말고 필요한 규칙을 검토해 합칩니다.
- 설치 후 새 세션에서 실제 스킬 목록·출처를 확인하고 `engineering-squad`를 명시적으로 선택해 작은 과제를 실행합니다. 읽은 `SKILL.md` 경로·테스트 결과·추가 안내 횟수를 기록해야 전체 적용 성공으로 셉니다. 모델 호출은 이번 시험에 포함하지 않았습니다. [공식 스킬 안내](https://learn.chatgpt.com/docs/build-skills), [플러그인 패키징](https://developers.openai.com/plugins/build/plugins).

---

### 4. Cursor [EXPERIMENTAL] (실험적 지원)

> ⚠️ **주의**: Cursor 환경은 서브에이전트 조율 기능 부재 및 자동 검증 하네스 미완료로 인해 현재 **실험적(Experimental)** 단계입니다. 100% 동작을 가정하지 마십시오.

#### 방법 A: 원터치 셋업 스크립트 실행
Cursor의 최신 규칙(`.cursor/rules/engineering-squad.mdc`) 및 레거시(`.cursorrules`)를 자동 설정합니다:
```powershell
# Windows (PowerShell)
.\scripts\setup-cursor.ps1
```
```bash
# macOS / Linux (Bash)
bash scripts/setup-cursor.sh
```
> 📖 Cursor 한계와 사용 팁: [Cursor 환경 가이드](docs/cursor-guide.md)

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
