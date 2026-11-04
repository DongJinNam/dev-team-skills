# Token efficiency log comparison

이 검증기는 같은 과제의 baseline/candidate 사용량 기록을 비교한다. 모델 호출이나 실제 토큰 수집은 하지 않는다. 실제 사용량을 수집할 수 없는 현재 상태는 **미측정**이며, 이 PR은 검증기 구현 범위다. 문서 길이·문자 수를 토큰 측정값으로 대신하지 않는다.

## Execute / 실행

Python 3.10+ 표준 라이브러리만 사용한다. Bash와 PowerShell 모두 같은 명령을 실행한다. Windows에서 `python` 대신 `py -3`도 사용할 수 있다.

```sh
python evals/compare_usage.py /path/to/private/usage.json --report /path/to/private/report.json
python -m unittest discover -s tests -v
# 합성 예제: exit 2 / HARNESS_ONLY가 정상이다.
python evals/compare_usage.py evals/usage-example.json
# 입력 없음: exit 2 / NOT_RUN
python evals/compare_usage.py
```

## Normalized record

완전한 예제는 [usage-example.json](usage-example.json)이다. 예제 수치는 합성이며 실제 절감 증거가 아니다. 아래 필드는 모두 필요하다. 불필요한 원문·키·개인정보는 넣지 않는다.

| Field | Meaning |
| --- | --- |
| `schema_version` | 정수 `1` |
| `origin` | `measured`: 운영자가 실제 사용량이라고 확인한 기록; `fixture`: 합성 테스트 |
| `accounting` | `input_includes_cache_output_includes_reasoning` |
| `config` | `model`, `settings`(직렬화한 설정 문자열), `tasks_sha256`, `rubric_sha256`(64자리 소문자 hex) |
| `sample_ids` | 실행 전에 정한 전체 과제·반복 목록, 예: `task-1:repeat-1`; 중복 금지 |
| `baseline`, `candidate` | 각각 `revision`, 동일한 `config`, `complete`, `samples` |
| `complete` | 운영자가 모든 호출 수집을 확인한 경우만 `true` |
| `samples[].id` | 양쪽 모두 `sample_ids` 전체와 정확히 일치 |
| `samples[].actor` | 해당 결과를 만든 구현자/주 에이전트 식별자 |
| `samples[].quality` | `passed`(boolean), 구현자와 다른 `reviewer`, `evidence`(비공개 검수 기록 식별자) |
| `samples[].discussion_rounds` | 0 이상의 정수; 사용자·검토자와의 토론 라운드 |
| `samples[].calls` | 아래 호출 목록; 없음은 측정되지 않은 것으로 처리 |
| `calls[].id`, `actor`, `kind` | 전체 양쪽 로그에서 유일한 실제 호출 ID, 실제 수행자, `main/child/retry/review/edit` |
| `calls[].input_tokens`, `output_tokens` | 공급사 사용량에서 정규화한 0 이상의 정수 |
| `calls[].cached_input_tokens` | input에 이미 포함된 캐시 부분; 중복 합산하지 않음 |
| `calls[].reasoning_output_tokens` | output에 이미 포함된 추론 부분; 중복 합산하지 않음 |
| `calls[].evidence` | 해당 공급사 사용량 증거 식별자; URL/경로를 열거나 실행하지 않음 |

공유 `config`는 양쪽 실행 조건이 같다는 운영자 확인이다. 실행 전 동일 모델/버전·설정·과제 입력·품질 기준·독립 세션 조건을 고정하고 각 arm에도 복사한다. 모델별 공급사 카운터에서 캐시/추론이 포함되는지 확인하고 이 형식으로 정규화한다. 알 수 없는 값은 `null`로 남긴다. 알려진 0만 `0`으로 기록한다. 작업/기준 해시는 비공개 원본의 SHA-256이며 검증기는 원본을 읽어 확인하지 않는다.

`complete=true` 전에 주 에이전트, 하위 에이전트, 실패·취소·재시도(사용량이 발생했다면 포함), 독립 검수 및 최종 편집 호출을 모두 수집한다. 공급사가 부모 합계에 자식 사용량을 포함하면 부모 합계와 자식 상세를 함께 넣지 않는다. 실제 호출의 원자적 사용량만 한 번씩 넣는다. 고유 ID여도 숨겨진 호출·합계 중복·조작 로그는 자동 탐지할 수 없으므로 공급사 원장과 대조한다. 재시도 요청마다 고유한 ID를 유지한다.

품질 `evidence`에는 원본 응답과 검토한 정책/과제/기준 버전을 연결한다. 기존 14개 판단 회귀와 필수 보안 조건 등 합의한 품질 기준 전체를 같은 방식으로 양쪽에 적용한다. 요약 점수만으로 위험한 한 사례를 숨기지 않는다. 품질 검토자는 자식 구현자와도 독립이어야 하며 운영자가 확인한다. 검증기는 boolean과 식별자만 검사하므로 품질 검토·기존 행동 평가기를 대체하지 않는다.

## Calculation and interpretation

- 호출별 총량 = `input_tokens + output_tokens`; 캐시·추론 부분은 더하지 않는다.
- 양쪽 전체 합계, 샘플별 총량, 호출 수/종류, 토론 라운드, 절감 토큰을 보고한다.
- 절감률 = `(baseline - candidate) / baseline * 100`; baseline 0은 `null`이다.
- 전체 절감은 토큰 가중 합계다. 샘플별 증가를 함께 검토하고 이를 신뢰도·평균 사용자 효과로 해석하지 않는다. 단일 표본은 통계적 효과 검증이 아니다.
- 토큰은 과금액과 다르다. 캐시 요금·모델 단가·시간·대기 비용을 추정하지 않는다. 검증기 자체의 측정용 모델 호출은 없으며, 별도 측정 에이전트를 썼다면 로그에 포함한다.

| Status | Exit | Meaning |
| --- | --- | --- |
| `RECORDED_IMPROVEMENT` | 0 | 제출된 measured 기록에서 품질 PASS·증거·수집 확인이 있고 총 토큰 감소 |
| `NO_IMPROVEMENT` | 1 | 측정값은 완전하나 전체 토큰이 감소하지 않음 |
| `QUALITY_FAILED` | 1 | 한쪽이라도 품질 실패; 절감 판정 차단 |
| `PENDING` | 2 | 사용량·증거·독립 검토·전체 수집 확인 누락; 부분 합계를 완전한 값으로 출력하지 않음 |
| `HARNESS_ONLY` | 2 | 완전한 합성 예제; 실제 효율 판정 아님 |
| `NOT_RUN` | 2 | 입력 미제공 |
| `ERROR` | 2 | 잘못된 값·중복·과제/설정 불일치·읽기/쓰기 실패 |

실패 품질이 누락보다 우선하며 누락이 있으면 fixture도 PENDING이다. 기록 검증 결과에 `provider_usage_authenticated=false`, `security_approval=NOT_ASSESSED`를 남긴다. 운영자 기록은 서명/공급사 인증이 없고 `origin=measured`도 독립 입증이 아니다. 기준선 측정 전 목표 절감률은 만들지 않는다. 절감 성공을 머지 권한·보안 PASS로 해석하지 않는다.

## Evidence and CI

실제 프롬프트/응답/공급사 원장은 비공개로 보관하고 공개 PR에는 마스킹된 집계와 식별자만 넣는다. 집계 JSON도 actor/id/evidence에 민감정보를 포함할 수 있으므로 자동 공개하지 않는다. 입력은 최대 5,000,000바이트로 제한하며 초과하면 ERROR다. 이 도구는 입력 파일 한 개를 읽고 지정한 report를 같은 디렉터리의 임시 파일에서 원자적으로 교체한다. 실행 코드·네트워크·API 키·외부 의존성이 없다. 보고서로 원본 입력을 덮어쓰는 것은 하드링크도 포함해 거부한다. 입력 오류 시 report도 ERROR로 교체한다. report 쓰기 자체가 실패하면 기존 파일이 남을 수 있으므로 호출자는 반드시 종료 코드와 stdout을 함께 확인한다.

CI의 기존 unittest discovery가 합성 계약 테스트를 자동 실행한다. 기존 14개 기록 replay는 별도로 그대로 유지하며 새 사용량/품질 실험으로 표시하지 않는다. 실제 비교 기록이 없는 동안 효율은 **NOT_RUN / 미측정**이다. 실제 공급사 수집기, 자동 GitHub 보호 규칙 설정, 통계적 반복 실험은 이 변경에 포함되지 않는다.
