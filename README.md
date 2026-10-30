# dev-team-skills

> Andrej Karpathy의 엔지니어링 철학(Karpathy Protocol) 기반의 AI 코딩 에이전트 스킬 및 규칙 모음 저장소입니다.  
> Google Antigravity, Claude Code, Cursor 등 다양한 AI 코딩 환경에서 4개 전문 역할(Frontend, Backend, Data Engineer, DevOps)로 에이전트 조직을 꾸려 서비스를 안정적으로 개발하고 배포할 수 있도록 지원합니다.

---

## 🏛️ Karpathy Protocol (기본 행동 헌법)

[`GEMINI.md`](./GEMINI.md) / [`CLAUDE.md`](./CLAUDE.md)에 정의된 4대 원칙:

1. **Don't assume. Don't hide confusion. (추측 및 침묵 금지)**
   - 모호한 요구사항은 자의적으로 판단하지 않고 질문과 트레이드오프를 제시합니다.
2. **Minimum code that solves the problem. Nothing speculative. (최소 코드 원칙)**
   - YAGNI 원칙을 철저히 준수하며 불필요한 미래 대비용 추상화와 의존성 라이브러리를 배제합니다.
3. **Touch only what you must. Clean up only your own mess. (영역 한정 및 정리)**
   - 작업과 무관한 파일의 임의 수정(오지랖 리팩토링)을 금지하고 임시 파일은 작업 완료 전 정리합니다.
4. **Define success criteria. Loop until verified. (검증 완료 전 종료 금지)**
   - 완료 전 명확한 성공 검증 기준(DoD)을 세우고 실제 빌드, 테스트, 헬스체크 명령어를 실행하여 증명합니다.

---

## 🚀 포함된 스킬 (Skills)

### `skills/engineering-squad/`
프론트엔드, 백엔드, 데이터 엔지니어, DevOps 엔지니어라는 4개 전문 역할을 서브에이전트 조직으로 구성하여 소프트웨어를 개발하고 안정적으로 서비스를 배포하는 풀스택 오케스트레이션 스킬입니다.

```text
skills/engineering-squad/
├── SKILL.md                          # 메인 오케스트레이션 및 4단계 배포 파이프라인
├── references/
│   ├── roles.md                      # 직무별(Frontend, Backend, Data, DevOps) 전문 프롬프트 & 가이드라인
│   └── deployment-gate.md            # 배포 완료 검증 게이트 (DoD 5단계 체크리스트)
└── scripts/
    └── verify-health.ps1             # 헬스체크 엔드포인트 자동 재시도 검증 스크립트 (PowerShell)
```

#### 에이전트 조직 역할 분담

| 역할 | 담당 영역 | 필수 검증 기준 |
| :--- | :--- | :--- |
| **Squad Lead (Main Agent)** | 요구사항 분해, 인터페이스/계약 정의, 서브에이전트 조율 | 엔드투엔드 시나리오 통합 |
| **Frontend Engineer** | UI 컴포넌트, 클라이언트 상태, API 연동, 브라우저 인터랙션 | 프로덕션 번들 빌드 (`npm run build`) 통과 |
| **Backend Engineer** | REST/GraphQL API, 도메인 로직, 인증, 에러 핸들링 | 단위/통합 테스트 통과 & API 응답 확인 |
| **Data Engineer** | DB 스키마(DDL), 마이그레이션(Up/Down), 쿼리 최적화, 시드 데이터 | 마이그레이션 실행 & 롤백 테스트 통과 |
| **DevOps Engineer** | Dockerfile/Compose, 환경 설정(`.env.example`), 배포 스크립트 | 컨테이너 빌드 & `/health` 200 응답 확인 |

---

## 💻 로컬 설치 및 적용 방법

### 1. Google Antigravity

#### 방법 A: 전역 적용 (모든 프로젝트에서 사용)
```powershell
# 1. 룰 파일 복사
Copy-Item GEMINI.md ~/.gemini/config/GEMINI.md

# 2. 스킬 디렉터리 복사
Copy-Item -Recurse skills/engineering-squad ~/.gemini/config/skills/engineering-squad
```

#### 방법 B: 개별 프로젝트 전용 적용
```powershell
# 프로젝트 루트 디렉터리에서 실행
Copy-Item GEMINI.md ./GEMINI.md
New-Item -ItemType Directory -Path .agents/skills -Force
Copy-Item -Recurse skills/engineering-squad ./.agents/skills/engineering-squad
```

### 2. Claude Code
프로젝트 루트에 `CLAUDE.md`를 배치하면 Claude Code가 세션 시작 시 지침을 자동으로 적용합니다.

---

## 📜 License
MIT License
