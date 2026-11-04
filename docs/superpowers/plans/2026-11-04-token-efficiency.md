# Token efficiency validator implementation plan

Spec: ../specs/2026-11-04-token-efficiency-design.md
Execution: inline; scope approved in chat. Existing isolated task clone, branch feat/token-efficiency-validation.

1. Add tests/test_token_efficiency.py CLI contract tests first; observe missing validator RED. Cover paired arithmetic, missing counts, quality failure, fixtures, malformed JSON, duplicate invocation IDs, noninteger/negative counts, config/sample mismatch, zero baseline and no input.
2. Implement evals/compare_usage.py with standard library: strict parsing, compare(record) -> report and CLI [record] [--report path]. No record returns NOT_RUN/2; invalid records ERROR/2; quality failures QUALITY_FAILED/1; incomplete evidence PENDING/2; fixture HARNESS_ONLY/2; recorded decrease RECORDED_IMPROVEMENT/0; no decrease NO_IMPROVEMENT/1. Fix until full suite green.
3. Document exact normalized schema, private evidence handling, invocation inclusion and limits in evals/token-efficiency.md, link from evals/README.md. Add explicitly synthetic example and label it as such.
4. Run unittest discovery, verify-harness, existing fourteen-case replay and diff check. One independent code/security review of final diff; correct material findings. Commit, push feature branch and open PR (next number expected 17). No merge.

Review focus: zero/boolean/negative counts, missing sample and subagent records, cache/reasoning double counting, fabricated provenance, quality false positives, untrusted reference execution. Provider traces are operator attestations and cannot be authenticated by this offline tool.
