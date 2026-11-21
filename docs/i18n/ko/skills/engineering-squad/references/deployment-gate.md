# Deployment Verification Gate (Definition of Done)

서비스 배포 작업 완료를 선언하기 전에 아래 8개 검증 게이트를 순차적으로 통과해야 합니다. 각 단계의 통과 증거(로그, 응답 코드, 테스트 결과 등)를 기록하십시오.

---

## 8개 종합 검증 게이트 체크리스트

| 게이트 | 담당 역할 | 검증 영역 | 실행 명령어 예시 | 통과 기준 |
| :--- | :--- | :--- | :--- | :--- |
| **Gate 1** | **Frontend / Backend** | **빌드 및 컴파일** | `npm run build` / `cargo build` / `go build` | Exit Code 0, 컴파일/타입 에러 0건 |
| **Gate 2** | **Backend / Data** | **단위/통합 테스트** | `npm test` / `pytest` / `go test ./...` | 실패한 테스트 0건 |
| **Gate 3** | **QA Engineer** | **E2E & 품질 게이트** | `npx playwright test` / `cypress run` | 핵심 시나리오 100% 통과 |
| **Gate 3a** | **Security Review Engineer (독립)** | **보안·개인정보 검수** | [security-review.md](./security-review.md) 적용 | 대상 리비전 보안 PASS 및 보고서, 출시 차단 사유 없음 |
| **Gate 4** | **DevOps Engineer** | **환경 변수 일치** | `.env.example` vs `.env` 누락 키 검사 | 누락된 필수 환경변수 0개 |
| **Gate 5** | **DevOps Engineer** | **컨테이너 기동** | `docker compose up -d --build` | 컨테이너 상태 `Up (healthy)` 유지 |
| **Gate 6** | **DevOps Engineer** | **런타임 헬스체크** | `powershell -File ./scripts/verify-health.ps1` | HTTP 상태 코드 `200 OK` |
| **Gate 7** | **SRE Engineer** | **신뢰성 & 메트릭 점검** | `curl -f http://localhost:PORT/metrics` | 메트릭 엔드포인트 응답 & 에러율 0% |

Gate 3a는 Stage 3의 기능 QA 이후, Stage 4 배포 전에 수행한다. 검수·증거 부재는 BLOCKED다. QA 통과로 대체할 수 없으며 commit/lockfile/배포 설정 변경 시 새 판정이 필요하다.

---

## 헬스체크 및 신뢰성 검증 실패 시 조치 요령 (Troubleshooting)

1. **컨테이너 로그 확인**:
   ```powershell
   docker compose logs --tail=100 <service-name>
   ```
2. **포트 충돌 확인**:
   ```powershell
   Get-NetTCPConnection -LocalPort <PORT> -ErrorAction SilentlyContinue
   ```
3. **환경 변수 주입 확인**:
   실행 중인 프로세스나 컨테이너 내부에 필요한 환경 변수가 올바르게 주입되었는지 확인합니다.
4. **미해결 시 보고**:
   오류를 숨기지 않고(Karpathy 원칙 1), 발생한 에러 로그와 함께 현재 상황을 Squad Lead 및 사용자에게 즉시 공유합니다.
