# Capture Renewal Runbook

When a policy file changes, the eval capture must be renewed before the PR
can merge. This runbook fixes the procedure that PR #30 (five failed
attempts) and PR #31 established. Follow it in order. Do not improvise the
parts marked **fixed**.

## 1. When renewal is needed

Renew the capture when any file in `POLICIES` (see `run_evals.py`),
`evals/scenarios.json`, or `evals/run_evals.py` changes. The CI replay
compares the snapshot of those files against the referenced capture; a
mismatch fails the build. `scripts/capture_plan.py --base <base> --head
<head>` prints the renewal plan for a given change: which policies changed,
the current capture reference, the case list, and the expected output paths.

## 2. Roles

- **Operator**: plans the renewal, runs the actors, assembles the capture,
  verifies replay. The operator may read `scenarios.json`.
- **Per-case actor** (fixed): one isolated session per case (19 sessions).
  Each actor reads only its own request file (the public prompt plus the
  current policies) and records only its response object. Actors never see
  other cases' requests or responses.
- **Reviewer** (fixed): a separate session that checks meaning using only
  the prompts and the policies. The reviewer never sees `scenarios.json`
  expected values and never sees the rubric.

### 역할별 최소 읽기 번들 (P3, 고정)

역할마다 필요한 파일만 읽는다. SKILL 전문과 references 전부를 매번 읽으면
토큰이 배로 든다. 번들 밖 파일은 읽지 않는다.

| 역할 | 읽는 것 | 읽지 않는 것 |
| --- | --- | --- |
| Operator | runbook, 계획서 출력, 바뀐 정책 파일(계획서가 가리킨 것만), 모델 라우팅 계약(등급 확인용), 회의록 | SKILL 전문, 바뀌지 않은 정책 파일 |
| Per-case actor | 자기 케이스의 request 파일, POLICIES 9개 파일 | POLICIES 밖 references, 다른 케이스의 request·응답 |
| Reviewer | 프롬프트, 응답 객체, 응답이 인용한 정책 구절 | `scenarios.json`, 루브릭, 계획서 출력, 회의록 |

인계는 요약만 한다. 브리핑에는 케이스 id·request 경로·등급만 싣는다.
actor는 응답 객체만 반환한다. reviewer는 케이스별 pass/fail과 근거 한 줄만
반환한다. 추론 과정과 전체 컨텍스트를 인계하지 않는다.

## 3. Integrity boundary (fixed)

Anyone who has read the expected values in `scenarios.json` must not write
actor briefs afterwards. Case information in a brief may only come from the
public prompt and the policies. This rule exists because a single-session
actor that saw many cases in one session repeatedly failed the structure
check (10, 12, 15, 18, 18 out of 19). Do not "help" an actor by hinting at
the expected answer.

## 4. Steps

1. Generate the plan: `python3 scripts/capture_plan.py --base <base>
   --head <head> --date <YYYY-MM-DD> --slug <slug>`.
2. For each case, run one isolated actor session and collect its response
   object. Record the model used for each response (see the model-routing
   contract: judgement steps are DEEP).
3. Run the independent reviewer session. All 19 cases must pass meaning
   review; a failed case gets a fresh actor session, not a repair of the
   old response.
4. Assemble `evals/runs/<YYYY-MM-DD>-<slug>.json` with `review.response_sha256`
   and `snapshot_sha256` included.
5. Point the workflow (`verify-rules-sync.yml`) and `evals/README.md` at the
   new capture file.
6. Verify: `bash evals/run-evals.sh --replay evals/runs/<new-capture>.json`
   must PASS, `scripts/verify-harness.sh` must PASS, and unit tests must pass.
7. Submit the PR. The security review packet is a separate, manual step.

## 5. Failure preservation (fixed)

Failed attempts are kept, never deleted and never overwritten. Name them
`evals/runs/<YYYY-MM-DD>-<slug>-attempt<N>.json` and mention them in the PR
body. PR #30 kept five failed attempts; PR #31 kept the first lean-doc-routing
attempt. The preserved failures are the evidence that the procedure was
followed, not a blemish to hide.

## 6. What this runbook does not do

It does not run the actors itself. Execution is still agent work; this
runbook only fixes the steps, the roles, and the integrity boundary so the
next renewal does not rediscover them. Full automation of execution is
Phase 3, decided separately after the Phase 2 pilot.

## 7. 검수 범위 (P6)

독립 검수는 diff로 한정한다. 검수 대상은 바뀐 파일과 게이트 관련 부분이다.
바뀌지 않은 부분은 이전 PASS를 인용한다. 인용할 때는 head SHA와 보고서
경로를 적고, 해당 검사 항목은 N/A 근거로 남긴다. 문서·설정만 바꾼 PR은
범위를 줄여 검수한다(정책에 이미 있는 규칙이다).

새 head마다 새 판정을 발행한다. 이전 PASS를 재사용하지 않는다. 등급
T1/T2 구분은 유지한다.
