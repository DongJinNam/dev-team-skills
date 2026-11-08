# Codex 적용·Claude 검증 상태·비교 수치

Codex 설치 명령 오류는 로컬에서 수정 효과를 확인했으며 타 스킬 대비 우수성은 판단을 보류한다.
설치 전후 기록과 공통 과제 비교 집계기를 제공하고, 인증·유료 실행 조건을 확인한 뒤 실제 비교 표본을 확보해야 한다.
Windows Codex CLI 0.167.0에서 기존 명령은 0/3, 수정 절차는 3/3 성공했지만 Claude와 타 스킬 비교 모델 실행은 미실행이기 때문이다.

## 합의·담당·범위

이 문서는 초기 설치 수정 단계의 기록이다. 아래 모델 비교 NOT_RUN 상태는 이후 승인된 [12회 비교 실험과 BOM 추가 수정](2026-11-07-four-arm-results.md) 이전의 상태이며, 최신 성과 판단은 후속 보고서를 따른다.

2026-11-07 사용자는 재안내 없는 적용 성공률·동일 과제 성공률/시간/전체 토큰 측정, 유료 실행·인증 문제·근거 부족 시 중단·보고 기준에 “동의”했다. [계획](../superpowers/plans/2026-11-07-codex-update.md)을 따른다. base/head는 `633e36d8dc6ea75956bc86d717bbb5738775b22f`이며 변경은 feature 브랜치의 미커밋 diff다. 사용자 실패 당시 환경·로그는 받지 못했으므로 같은 증상이라고 단정하지 않는다.

COMBINED 모드로 저장소 `engineering-squad`, `brainstorming`, `harness-engineering`, `humanizer`/`humanizer-kr`과 설치된 Superpowers 7.0.1 원인 분석·계획·TDD 절차를 사용했다. Lead가 구현/품질/설명을 맡고 `/root/eval_review`가 비교 설계에 독립 반론을 제출했다. 별도 보안 검토자는 최종 변경을 검수한다. 배포·운영·외부 게시·머지는 범위 밖이다.

## 원인과 최소 수정

- CLI `plugin --help`와 실제 명령에서 README의 `plugin install`이 종료 코드 2로 실패했다. 지원 명령은 `plugin add`이며 marketplace를 포함한 이름으로 지정한다.
- 기존 `.claude-plugin/marketplace.json`은 Codex에서도 등록되고 기존 manifest로 설치됐다. 따라서 새 카탈로그/스키마를 추가하거나 기존 manifest를 변경할 근거는 없었다. 계획의 조건부 패키지 수정/경로 시험은 N/A로 정리했다.
- 양쪽 README의 근거 없는 우수성·100% 호환 비교표를 검증 상태로 교체했다. `CODEX.md` 복사와 스킬 설치를 혼동하지 않도록 지침을 정정했다.
- Claude CLI는 `Get-Command`에서 발견되지 않았다. 실제 설치·호출·호환성은 NOT_RUN이며 문서 확인만으로 성공을 주장하지 않는다.

## 실제 토론과 반영

Lead 제안: 기존 평가·토큰 비교기를 재사용하고 성공률·시간 집계와 설치 재현을 추가한다. 새 평가 플랫폼이나 의존성은 도입하지 않는다.

독립 반론(`/root/eval_review`): 기존 19개 문제는 자사 정책 시험이므로 다른 스킬의 품질을 공정하게 비교할 수 없다. 평가 기능 추가나 재채점 19/19만으로 우수성을 입증했다고 할 수 없으며, 결과가 열등하거나 차이가 없을 가능성을 허용해야 한다.

반영: 공통 과제·숨겨진 수용 테스트·동일 모델/환경·고정 버전·새 세션·사전 표본 등록을 비교 절차로 정했다. 실패도 분모에 포함하고 설치→활성화→완료의 불가능한 상태를 거부한다. 누락 시간/토큰의 평균은 null이며 표본 개수는 남긴다. 단순 집계는 `evidence_authenticated=false`, `superiority=NOT_ESTABLISHED`를 출력한다. 가상 역할의 투표·동의는 만들지 않았다.

## 실측과 검증

원본 명령·종료 코드·시간·정규화한 출력은 [설치 시험 JSON](../../evals/runs/2026-11-07-codex-install.json)에 보존했다. `python evals/check_codex_install.py --output install-report.json --runs 3`으로 재현할 수 있다.

| 항목 | 결과 | 해석 |
| --- | --- | --- |
| 기존 `plugin install` | 성공 0/3, 각 종료 코드 2 | 명령 오류 재현 |
| 수정 등록→설치→목록 확인 | 성공 3/3, 각 명령 종료 코드 0 | Windows / CLI 0.167.0 로컬 절차 |
| 캐시 스킬 파일 | 매회 8/8 원본 바이트 일치 | 실제 모델 발견·호출 증거는 아님 |
| 실제 과제·토큰·스킬 간 비교 | NOT_RUN, 비교 표본 0 | 우수성 NOT_ESTABLISHED |
| Claude 설치·호출 | NOT_RUN | CLI 부재 |

임시 CODEX_HOME에서 CLI가 PATH helper 생성을 거부하는 경고를 출력했다. 경고는 원본 기록에 보존했으며 위 세 로컬 플러그인 명령의 성공과 별개로 helper 실행은 검증하지 않았다. 성공률 0%→100%(+100%p)는 이 세 반복에만 해당하며 일반 신뢰도나 성능 우수성 추정이 아니다. 모델 호출 비용·토큰은 측정하지 않았다.

집계기 신규 테스트는 모듈 부재로 실패한 뒤 구현 후 5개 테스트가 통과했다. 독립 검토에서 거대 정수 변환 예외와 유한한 큰 값의 합계 overflow를 발견해 실패를 재현한 뒤 수정했으며, 최종 신규 테스트는 6개다. 합성 fixture는 실제 측정과 분리한다.

### 최종 검증 기록

- `HARNESS_LAUNCHER=python`으로 `python -m unittest discover -s tests`: **69/69 PASS, 33.377초**. 최초 전체 실행은 67/68 통과였고 기존 캡처 테스트의 `read_text()`가 cp949로 UTF-8 JSON을 읽다 실패했다. 해당 읽기에 UTF-8을 명시해 해결했다. 테스트의 모델 호출 메시지는 mock 기반 회귀시험 출력이며 실제 외부 모델 실행이 아니다.
- Windows PowerShell `scripts/verify-harness.ps1`, Git Bash `scripts/verify-harness.sh`: 각각 패키지 구조 PASS. macOS/Linux 현지 실행은 NOT_RUN이다.
- `python evals/run_evals.py --replay evals/runs/2026-11-06-lean-squad.json`: **19/19 REPLAY PASS**, 실제 도구 실행 NOT_OBSERVED. 새 모델 실행으로 집계하지 않는다.
- `git diff --check`: PASS.
- 독립 검토자 `/root/security_review`, 2026-11-07: **보안 PASS, 기능 HOLD 해제, 컴플라이언스 N/A**. argv 배열/기본 shell=False, 임시 설정 격리, 로그 경로 마스킹, 새 의존성·CI 권한·hook/MCP 부재를 수동 확인했다. 자동 보안 스캐너는 NOT_RUN이며 이 국소 변경의 경계·diff·manifest·로그 검토를 대체 증거로 채택했다. 서비스 인증·웹 입력 검사는 서비스 변경이 없어 N/A다.
- 공식 [Codex GHSA-w5fx-fh39-j5rw](https://github.com/openai/codex/security/advisories/GHSA-w5fx-fh39-j5rw)(2025-09-19 공개, <=0.38.0 영향, 0.39.0 수정)를 확인했으며 실행 버전 0.167.0은 영향 범위 밖이다. [Python subprocess 보안 문서](https://docs.python.org/3/library/subprocess.html#security-considerations)를 대조했다. 확인일 2026-11-07.

검토 파일 SHA-256: `check_codex_install.py` = `16D3E071591BBE53CA4E4523BCD452AC4E7B6B59978690E8ABA7D0DA6CDDC794`, `compare_outcomes.py` = `0C2C50058D98B1FBB83973E7B7E6B7F989322EC0A585CEFD5B549FB17999DC50`, `test_outcomes.py` = `435BCB8E4FDBE9BBA0252EEA1507F7A87948690268D662DECD3ED00B0F9A7F43`, `test_behavior_evals.py` = `58D3D84EBA79CD5C1B9F3ED2106BF830749335B9E3DA1C3DFC3746719E6E0D11`다. 현재 미커밋 파일 상태에 대한 검수이며 향후 commit/merge 변경에 대한 자동 승인이 아니다.

## 출처와 남은 조건

확인일 2026-11-07: [OpenAI 패키징](https://developers.openai.com/plugins/build/plugins), [스킬 안내](https://learn.chatgpt.com/docs/build-skills), [Claude 매니페스트](https://code.claude.com/docs/en/plugins-reference), 로컬 `codex --version` 및 `plugin`/`plugin add`/`plugin marketplace add --help`. 실제 CLI 결과를 해당 버전 명령의 근거로 사용했다.

초기 단계에서는 실제 모델 비교를 유료 실행·인증 및 근거 부족 중단 조건에 따라 보류했다. 이후 별도 승인된 12회 비교는 [후속 보고서](2026-11-07-four-arm-results.md)에 기록했다. 작은 표본의 성과 수치는 확보했지만, 다른 스킬보다 일반적으로 우수하다는 입증은 아직 충족하지 못했다.
