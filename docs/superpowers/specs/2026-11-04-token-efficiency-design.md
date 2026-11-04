# Token efficiency log validator

User-approved scope: implement the validator first; real model usage collection and an efficiency claim remain pending. No new paid calls, provider installation or runtime policy change.

Compare paired samples from baseline/candidate under identical model, generation settings, task inputs and quality rubric. Policy revisions are recorded separately. Consume operator-supplied JSON only; never execute referenced traces. Count every model invocation including children, retries, reviewers and final editing exactly once. Require explicit completeness attestation; absent usage is unknown, never zero. Cached input is already included in input; reasoning is already included in output. Do not add either again. No dollar inference.

Reject malformed logs, duplicate calls/samples, mismatched configurations or sample coverage. Quality failure blocks a savings result. Missing evidence is PENDING. Fixtures remain HARNESS_ONLY. A positive result means only RECORDED_IMPROVEMENT in supplied logs, not independently verified provider usage, causal effect, reliability or merge/security approval.

Approaches: static prompt length is inexpensive but misses actual calls; provider-specific live adapters cost integration and credentials. Choose a standard-library offline comparator now, with documented normalized usage contract and tests. No tokenizer dependency or model selection.

Acceptance: correct token totals and percentages; cache not double counted; all sample pairs present; actual nonnegative integer counts; independent quality evidence references; explicit unmeasured/fixture outcomes; CLI errors never produce success. Preserve existing fourteen-case replay and security gates unchanged. Baseline-zero percent is undefined. No minimum reduction percentage is invented.

Stop/report: real usage collection unavailable, quality failure or required validation failure blocks efficiency claims. User authorized validator-only continuation after usage collection was unavailable. PR creation is authorized; merge is not.
