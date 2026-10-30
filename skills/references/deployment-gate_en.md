# Deployment Verification Gate (Definition of Done)

Before declaring any deployment complete, you must pass all 5 verification gates below in order. Keep proof (logs, status codes, test outputs) for each gate.

---

## 5-Stage Verification Checklist

| Gate | Verification Area | Example Command | Passing Criteria |
| :--- | :--- | :--- | :--- |
| **Gate 1** | **Build & Compile** | `npm run build` / `cargo build` / `go build` | Exit Code 0, 0 type errors |
| **Gate 2** | **Unit & Integration Tests** | `npm test` / `pytest` / `go test ./...` | 0 failing tests |
| **Gate 3** | **Environment Variables Match** | `diff <(cat .env.example \| cut -d= -f1) <(cat .env \| cut -d= -f1)` | No missing required variables |
| **Gate 4** | **Container Startup** | `docker compose up -d --build` | Container state stays `Up` |
| **Gate 5** | **Runtime Health Check** | `powershell -Command "Invoke-WebRequest -Uri http://localhost:PORT/health"` | HTTP status code `200 OK` |

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
