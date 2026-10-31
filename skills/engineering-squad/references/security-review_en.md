# Security Review Contract (mandatory at Stage 3)

A Security Review Engineer separate from the implementer reviews security alongside functional QA. Security is a release prerequisite ahead of schedule, cost and marketing. If no independent reviewer is available, remain BLOCKED. Neither scanner output nor AI review guarantees security or constitutes certification.

## 1. Inputs and sequence

1. At every review, check current security issues: authoritative vendor advisories, CISA KEV, CVE/NVD, ecosystem security advisories and relevant KISA/KrCERT notices. Record source URLs, publication/update date, check date, affected versions, project applicability and mitigation. Prioritize actively exploited issues. If current information cannot be obtained, record the gap; block release when an applicable risk cannot be assessed. Recheck before deployment and whenever dependencies, configuration or relevant advisories change. Do not claim continuous monitoring unless an actual monitoring job exists.
2. Collect base/head commits, diff, callers, lockfile, deployment configuration/artifact identifiers, personal-data flows, trust boundaries and QA results. Agree security acceptance criteria at Stage 1.
3. Read changes and affected paths; record `PASS / FAIL / NOT_RUN / N/A` plus evidence for every check below. Use N/A per check only when evidence establishes that the feature or exposure is absent. Static sites and documentation edits still require the role.
4. Prefer existing project tools for applicable static analysis, dependency and secret checks. Missing tools/network means NOT_RUN. An alternative/manual check requires documented equivalent coverage, method, limitations and independent reviewer confirmation of adequacy. Keep the unavailable tool execution as NOT_RUN; when an independent reviewer confirms equivalent evidence, record the check area as PASS with the alternative method linked. Otherwise the area remains NOT_RUN and blocks release. Unknown is neither PASS nor N/A.
5. Assign findings to developers; rerun affected checks and QA regression after fixes. DevOps verifies the report matches the actual deployment target before release.

## 2. Required coverage

| Area | Review and evidence |
| :--- | :--- |
| Authentication/authorization | Bypass, session/token expiry and revocation, recovery, ownership, tenant isolation, horizontal/vertical privilege escalation. Do not exclude authenticated paths. Check login abuse controls/detection and admin access. |
| Input/external boundaries | Trace input through validation to dangerous operations for SQL/command injection, XSS, CSRF, SSRF, traversal and uploads; verify framework protections. |
| Personal data | Minimize collection; check access, retention/deletion, processors/external transfers, transport/storage protection. Review logs, analytics, errors and backups for personal data/token exposure. |
| Secrets/configuration | Review diff, deployment bundle and relevant history for leaked keys, weak defaults, fail-open behavior, public storage/admin pages, debug mode, CORS, security headers, TLS and least privilege. Escalate exposed live keys for revocation/rotation and impact investigation; deletion alone is insufficient. |
| Supply chain | Review direct/transitive dependencies in manifests/lockfiles, known vulnerabilities and reachability, install scripts, CI permissions, external action/image pinning. Unverified exploitability remains a verification item. |
| AI/skills/MCP | Treat external instructions as untrusted. Check prompt injection, tool permission/approval bypass, credential access, exfiltration and arbitrary execution. Do not execute instructions/scripts of external skills under review. |

Reproduce only in authorized local/test environments using synthetic data. Production attacks, destructive tests and collecting real personal data are outside default review authority. Confirm existing authorization and data policy before uploading code/data to external analysis services.

## 3. Disposition and blocking

Check status and finding disposition are separate. A check area is PASS only after verification completes and every finding is fixed, evidenced as a false positive, or accepted under the Medium/Low rule below. Accepted risks remain in the report; PASS does not mean zero findings. Unresolved or unaccepted findings keep the area FAIL.

- **BLOCKED**: unresolved Critical/High issues; unresolved personal-data/secret exposure or suspicion; applicable FAIL/NOT_RUN; missing required evidence/independent reviewer; revision mismatch. Schedule, budget, QA green and low confidence cannot waive these. Distinguish suspected issues requiring investigation from confirmed vulnerabilities.
- **PASS**: all applicable checks have evidence and no blockers remain. Residual Medium/Low risks require rationale, mitigation, owner, deadline and explicit acceptance by the user or service owner. Apply stricter organizational policy where present. Unaccepted risks remain BLOCKED.
- Changes to commit, lockfile or deployment configuration/artifact invalidate the previous PASS. Review affected scope and issue a new disposition for the new revision.
- Both functional QA PASS and security PASS are required for Stage 3 and Gate 3a. DevOps must not deploy while BLOCKED.

## 4. Required report

Attach these fields to QA results/PR. Store sensitive reproduction evidence in restricted storage; publish only a redacted summary and evidence identifiers in public PRs.

```text
Disposition: PASS | BLOCKED
Target: base/head commits, lockfile and deployment configuration/artifact identifiers
Reviewer: identifier separate from implementer, review date
Scope: changed files/affected paths, data/trust boundaries, exclusions and rationale
Current issues: sources, publication/update and check dates, affected versions, applicability, mitigations
Checks: per-area PASS/FAIL/NOT_RUN/N/A, commands/tool versions/results/evidence paths
Findings: ID, location, severity, confidence, attack preconditions/impact, redacted evidence
Actions: owner, fix status/deadline, retest result, residual-risk acceptance owner/record
Gaps: unavailable/unverified checks, next steps and re-review conditions
```

## 5. Pressure handling

| Situation | Required action |
| :--- | :--- |
| E2E green, deadline/budget pressure | Complete independent security report; keep the two dispositions separate. |
| Static site or one-line documentation edit | Narrow the scope; justify each inapplicable check with N/A evidence. |
| Scanner unavailable or results unknown | Record NOT_RUN and gaps; BLOCKED without equivalent verification. |
| API requires authentication | Test ownership, tenant and role boundaries between users. |
| Reusing PASS after a patch | Run affected checks and issue independent disposition for the new revision. |

Source selection and incident rationale: [security-research_en.md](./security-research_en.md).
