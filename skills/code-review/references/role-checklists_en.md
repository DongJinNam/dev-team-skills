# Role-Tailored Review Checklists

Use these focused checklists during code reviews based on the engineering roles involved.

---

## 1. Product Planner Review Checklist
- [ ] **Problem-Solution Fit**: Does this PR directly solve the user problem and test the hypothesis outlined in the PRD?
- [ ] **Acceptance Criteria (AC)**: Are all Given-When-Then acceptance criteria in the user story fully satisfied?
- [ ] **KPI & Event Tracking**: Are product analytics metrics or event logs in place to measure the impact after release?
- [ ] **No Scope Creep**: Did the PR stay strictly within the MVP scope without unrequested extra features (YAGNI)?

---

## 2. AI Agent Engineer Review Checklist
- [ ] **Harness Coverage**: Are there repeatable eval tests or scripts to automatically test new features, tools, or rules?
- [ ] **Deterministic Guardrails**: Does the workflow use deterministic checkers (linters, schema validators, test runners) rather than relying only on LLM judgment?
- [ ] **Marketplace & Schema Integrity**: Do plugin manifests (`plugin.json`, `SKILL.md` frontmatter) and tool JSON schemas follow official specs?
- [ ] **Token Efficiency & Prompt Safety**: Are prompts concise without token waste, and is prompt injection guarded against?

---

## 3. Frontend Review Checklist
- [ ] **Rendering Performance**: Are there unnecessary re-renders? Are heavy calculations properly placed?
- [ ] **State Management**: Is state kept local whenever possible instead of polluting global state?
- [ ] **User Experience (UX)**: Are loading spinners/skeletons shown during async calls? Are network errors clearly shown to the user?
- [ ] **Responsive & Accessible**: Does the layout look good and work properly on both mobile and desktop screens?

---

## 4. Backend Review Checklist
- [ ] **Atomic Transactions**: Are multiple database writes wrapped in a transaction (`@Transactional`) to prevent partial failures?
- [ ] **No N+1 Queries**: Are database relations loaded efficiently using batching or joins instead of query-per-row?
- [ ] **Auth & Permissions**: Are endpoints guarded with proper role checks? Is direct object reference (IDOR) prevented?
- [ ] **Idempotency**: Does re-sending a network request avoid creating duplicate records or charges?

---

## 5. Data Engineer Review Checklist
- [ ] **Two-Way Migrations**: Is a rollback (`Down`) migration script included and verified?
- [ ] **Lock Safety**: Does applying DDL on large tables avoid locking the whole table and blocking live traffic?
- [ ] **Index Design**: Do WHERE, JOIN, and ORDER BY queries use effective compound indexes?
- [ ] **Proper Data Types**: Are money, quantities, and dates using appropriate types (e.g., DECIMAL, TIMESTAMP with timezone)?

---

## 6. QA Engineer Review Checklist
- [ ] **Boundary Conditions**: Are edge cases (0, negative numbers, null, empty strings, max length) tested?
- [ ] **Negative Paths**: Are failure scenarios and invalid inputs covered by automated tests, not just the happy path?
- [ ] **Test Independence**: Are tests completely isolated without shared DB state to prevent flaky runs?

---

## 7. DevOps & SRE Review Checklist
- [ ] **No Hardcoded Secrets**: Are API keys, DB passwords, and secrets strictly loaded from environment variables?
- [ ] **Resource Limits**: Are CPU and memory limits set on containers?
- [ ] **Graceful Shutdown**: Does the service handle `SIGTERM` cleanly by completing in-flight requests before exiting?
- [ ] **Observability**: Are structured JSON logs (with trace IDs and request IDs) generated for debugging?

## 9. Product Marketing Review Checklist
- [ ] Can the intended reader quickly identify value and next action?
- [ ] Are demo claims linked to verification, with unimplemented features and projections labeled?
- [ ] Is comprehension review labeled as real-user testing or internal review?
- [ ] Is external publishing or ad spending explicitly authorized?

## 10. Finance / FinOps Review Checklist
- [ ] Are measured/estimated/unknown data, rate sources, dates, currencies, and periods distinguished?
- [ ] Are input/output/cache charges and communication subsets counted without duplication?
- [ ] Are telemetry proxies kept distinct from exact tokens or billed costs?
- [ ] Are extra discussion/delegation justified and staffing minimized?
- [ ] Are overruns reported while required quality and security checks remain intact?
