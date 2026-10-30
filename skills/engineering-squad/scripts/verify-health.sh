#!/usr/bin/env bash
# verify-health.sh: Cross-platform health check script for macOS & Linux
set -euo pipefail

URL="${1:-http://localhost:8080/health}"
MAX_RETRIES="${2:-10}"
DELAY_SECONDS="${3:-3}"
INSECURE_FLAG="${4:-}"

CURL_EXTRA=""
if [ "$INSECURE_FLAG" = "-k" ] || [ "$INSECURE_FLAG" = "--insecure" ]; then
    echo "==> [INFO] SSL certificate validation is bypassed ($INSECURE_FLAG)"
    CURL_EXTRA="-k"
fi

echo "==> [macOS/Linux] Checking health endpoint: $URL"

attempt=1
success=false

while [ "$attempt" -le "$MAX_RETRIES" ]; do
    HTTP_CODE=$(curl -s $CURL_EXTRA -o /dev/null -w "%{http_code}" --connect-timeout 5 "$URL" || true)

    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "\033[0;32m[SUCCESS] Service is healthy! (HTTP 200 OK)\033[0m"
        curl -s $CURL_EXTRA "$URL"
        echo ""
        success=true
        break
    else
        echo -e "\033[0;33m[WAIT] Attempt $attempt/$MAX_RETRIES: Received HTTP status $HTTP_CODE\033[0m"
    fi

    attempt=$((attempt + 1))
    if [ "$attempt" -le "$MAX_RETRIES" ]; then
        sleep "$DELAY_SECONDS"
    fi
done

if [ "$success" = false ]; then
    echo -e "\033[0;31m[ERROR] Health check failed after $MAX_RETRIES attempts.\033[0m"
    exit 1
fi

exit 0
