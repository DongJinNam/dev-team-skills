# Deployment Verification Gate (Definition of Done)

Before declaring any deployment complete, you must pass all 7 verification gates below in order. Keep proof (logs, status codes, test outputs) for each gate.

---

## 7-Stage Comprehensive Verification Checklist

| Gate | Responsible Role | Verification Area | Example Command | Passing Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **Gate 1** | **Frontend / Backend** | **Build & Compile** | `npm run build` / `cargo build` / `go build` | Exit Code 0, 0 compile/type errors |
| **Gate 2** | **Backend / Data** | **Unit & Integration Tests** | `npm test` / `pytest` / `go test ./...` | 0 failing tests |
| **Gate 3** | **QA Engineer** | **E2E & Quality Gate** | `npx playwright test` / `cypress run` | 100% pass on core scenarios |
| **Gate 4** | **DevOps Engineer** | **Environment Variables Match** | Check missing keys: `.env.example` vs `.env` | 0 missing required environment variables |
| **Gate 5** | **DevOps Engineer** | **Container Startup** | `docker compose up -d --build` | Container state stays `Up (healthy)` |
| **Gate 6** | **DevOps Engineer** | **Runtime Health Check** | `powershell -File ./scripts/verify-health.ps1` | HTTP status code `200 OK` |
| **Gate 7** | **SRE Engineer** | **Reliability & Metrics Check** | `curl -f http://localhost:PORT/metrics` | Metrics endpoint responds & 0% error rate |

---

## Troubleshooting Guide for Health Checks & Failures

1. **Check Container Logs**:
   ```powershell
   docker compose logs --tail=100 <service-name>
   ```
2. **Check Port Conflicts**:
   ```powershell
   Get-NetTCPConnection -LocalPort <PORT> -ErrorAction SilentlyContinue
   ```
3. **Verify Injected Environment Variables**:
   Check if the necessary environment variables are properly set inside the running process or container.
4. **Report if Unresolved**:
   Do not hide errors (Karpathy Principle 1). Share the current error logs and situation immediately with the Squad Lead and user.
