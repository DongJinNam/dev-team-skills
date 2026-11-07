# Research and selection rationale for the security role

Access date: 2026-10-31. Planner investigates technical fit and incident lessons; Marketing cross-checks adoption signals, claim scope and sources. This compares researched candidates, not a global ranking. Recheck metrics and source changes on reuse.

## Public skill candidates and composition

| Candidate / source | Observed adoption signal | Referenced capability | Selection limit |
| :--- | :--- | :--- | :--- |
| [Sentry security-review](https://github.com/getsentry/skills/blob/main/skills/security-review/SKILL.md) | [skills.sh](https://www.skills.sh/getsentry/skills/security-review): 21.8K installs; repository about 1.1K stars | Attacker input, framework defenses and evidence confidence | Reject exclusion of authenticated paths; review cross-user IDOR as well. |
| [Trail of Bits differential-review](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md) | [skills.sh](https://www.skills.sh/trailofbits/skills/differential-review): 9.3K installs | Diff, callers, history and impact review | Inspect affected personal-data boundaries beyond changed lines. |
| [Trail of Bits insecure-defaults](https://www.skills.sh/trailofbits/skills/insecure-defaults) | Catalog: 6.5K installs; [repository](https://github.com/trailofbits/skills): about 7.9K stars | Fail-open configuration and weak defaults | Verify actual configuration and execution paths rather than classifying from patterns alone. |

Catalog installs are cumulative display metrics, not unique users, effectiveness or safety measurements. Repository stars do not measure an individual skill. Audit badges may conflict and are not approval evidence: Sentry showed Socket Fail and insecure-defaults showed Snyk Fail. These are not proof of malice; they support reviewing rather than automatically installing popular skills.

Use [OWASP ASVS 5.0.0](https://asvs.owasp.org/) (published 2025-05-30) as a coverage reference. Combine review perspectives in our own [security-review_en.md](./security-review_en.md) contract. Do not copy or automatically install external files/scripts; no runtime dependency is added. Before future copying, verify revision, per-file license and notice requirements. Observed repository licenses: [Sentry Apache-2.0](https://github.com/getsentry/skills/blob/main/LICENSE), [Trail of Bits CC-BY-SA-4.0](https://github.com/trailofbits/skills/blob/main/LICENSE).

## General review rationale

Functional tests alone cannot establish personal-data protection. Review login abuse controls, authorization, input handling, retention/deletion and processor data flows. This is a general design rationale; company-specific incident accounts and identifying incident links are excluded. Security PASS is scoped evidence, not proof of zero vulnerabilities or legal certification.
