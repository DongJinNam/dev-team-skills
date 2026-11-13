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
   contract: judgement steps are DEEP). Record the per-model call count
   and elapsed time for the renewal in the work-minutes record (P1).
   Run cases in batches of at most 5; if interrupted, resume by batch
   and record batch progress in the work-minutes record (P4).
3. Run the independent reviewer session. All 19 cases must pass meaning
   review; a failed case gets a fresh actor session, not a repair of the
   old response. Retry only a failed case, one grade higher, in a fresh
   session; do not raise the whole run. Keep the reviewer at DEEP (P2).
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
