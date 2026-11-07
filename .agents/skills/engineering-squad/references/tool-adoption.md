# 외부 스킬·오픈소스 활용 증거 계약

새 도구 선택·도입 평가·활용 점검 때 필요한 후보만 읽는다. Product는 문제/시장 근거, Engineering은 호환·실행, Quality는 검증, Security는 권한/권리를 확인하고 Lead가 비용과 선택을 기록한다. 별도 상설 도구 평가 역할은 만들지 않는다.

## 선택 순서

1. 해결할 문제와 AC를 적고 현재 제공된 도구·프로젝트 의존성·표준 라이브러리로 해결되는지 확인한다.
2. 외부 비교가 필요하면 적합한 후보 최대 3개를 같은 기준으로 비교한다. 추가 후보는 기존 후보가 AC를 충족하지 못하는 이유가 있을 때 조사한다. 관련 없는 작업은 조사 N/A 사유만 기록한다.
3. 공식 원출처의 유지보수 상태·확인일·revision/version·라이선스/파일별 조건·호스트/OS 호환·권한/데이터 전송·의존성·예상 비용을 확인한다. SNS·stars·다운로드 수는 발견 지표일 뿐 실사용률·품질·안전성 증거가 아니다. 단일 시점으로 최근 성장률을 만들지 않는다.
4. 선택한 후보의 정확한 패키지 ID/경로를 읽고 작은 실제 작업에 적용한다. 사용한 부분·산출물·실행 결과·품질을 기록한다. 문서 방법의 적용과 스크립트/CLI 실행을 구분한다. 설치/권한/외부 전송은 기존 사용자 권한·호스트 규칙 안에서만 한다.
5. 같은 AC에서 기존 방법과 비교해 채택·보류·기각한다. 기능·독립 보안·적용 컴플라이언스 실패를 비용 절감으로 상쇄하지 않는다. 선택형 도구가 없거나 읽히지 않으면 기존 방법으로 진행하고 공백을 남긴다. 사용자가 필수 지정한 도구는 해당 의존 단계 BLOCKED다.

## 증거 상태

상태는 주장 종류이며 자동 승격 단계가 아니다. 아래 증거가 충족된 가장 높은 범위를 기록하고 누락을 별도로 남긴다. 문서만으로 방법을 채택한 경우 설치 가능(AVAILABLE)을 주장할 필요가 없다.

| 상태 | 필요한 증거 | 뜻하지 않는 것 |
| --- | --- | --- |
| DISCOVERED | 원출처 URL·확인일·관련 문제 | 검토·설치·활용 |
| INSPECTED | 실제 읽은 파일/문서·revision 또는 확인일·권리/제약·적용 판단 | 실행 완료 |
| AVAILABLE | 현재 환경의 정확한 패키지/경로/버전·읽기 또는 실행 가능 확인 | AC 통과 |
| APPLIED | 사용한 방법/명령·대상·실제 산출물/로그 | 효과 검증 |
| VERIFIED | APPLIED 증거 + 해당 revision/환경에서 AC 결과·품질 검토·비교 범위 | 모든 작업의 효율·보안 보증 |

`result: PASS / FAIL / NOT_RUN`은 상태와 별도다. 실패한 적용은 APPLIED + FAIL, 미실행은 NOT_RUN이며 VERIFIED + PASS로 바꾸지 않는다. 필수 증거가 없으면 마지막으로 입증된 상태에 머문다. VERIFIED에는 실제 통과한 AC와 한계를 적고, 보안 승인 여부는 별도 보안 계약으로 판단한다.

## 하나의 작업 기록

기존 PR/작업 기록에 아래 한 행/블록을 추가한다. 새 평가 문서를 중복 생성하지 않는다.

```text
problem/AC | owner | candidate/source/file/revision-or-checked-at
license/maintenance/host/OS/permissions/data/cost/unknowns
state | actual_method_or_command | artifact_or_log | result/AC/reviewer
baseline_or_existing_option | decision(adopt/defer/reject)/reason | scope/limits
recheck_trigger | next_owner
```

예: 설치 목록에 없고 README만 읽은 CLI는 INSPECTED, result NOT_RUN이다. 명령을 제시했다는 이유로 APPLIED가 되지 않는다. 외부 방법으로 새 인수 테스트를 만들고 검증했다면 해당 테스트 산출물 범위의 활용이며 외부 CLI를 실행한 것은 아니다.

도입 전과 버전·권한·데이터 경계·보안 공지·AC 변경 시 관련 근거를 다시 확인한다. 같은 범위의 최신 검증은 재사용한다. 지난 프로젝트 PASS를 새 환경 PASS로 복사하지 않는다. 토큰 비교는 [사용량 평가](../../../evals/token-efficiency.md)의 동일 조건·전체 호출/재시도/리뷰·품질 게이트를 사용한다. 로그가 없으면 UNMEASURED다.
