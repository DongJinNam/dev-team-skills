<#
.SYNOPSIS
    로컬 서비스의 헬스체크 엔드포인트를 호출하여 정상 응답(HTTP 200)을 검증하는 스크립트입니다.

.PARAMETER Url
    점검할 헬스체크 URL (기본값: http://localhost:8080/health)

.PARAMETER MaxRetries
    최대 재시도 횟수 (기본값: 10)

.PARAMETER DelaySeconds
    재시도 간격(초) (기본값: 3)

.PARAMETER SkipCertificateCheck
    사설 인증서(Self-signed SSL) 사용 시 인증서 유효성 검증을 건너뜁니다.
#>

param(
    [string]$Url = "http://localhost:8080/health",
    [int]$MaxRetries = 10,
    [int]$DelaySeconds = 3,
    [switch]$SkipCertificateCheck
)

if ($SkipCertificateCheck) {
    Write-Host "[INFO] SSL certificate validation is bypassed (-SkipCertificateCheck)." -ForegroundColor Yellow
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
}

Write-Host "==> Checking health endpoint: $Url" -ForegroundColor Cyan

$attempt = 1
$success = $false

while ($attempt -le $MaxRetries) {
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "[SUCCESS] Service is healthy! (HTTP 200 OK)" -ForegroundColor Green
            Write-Host "Response: $($response.Content)"
            $success = $true
            break
        } else {
            Write-Host "[WARNING] Attempt $attempt: Received HTTP $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[WAIT] Attempt $attempt/$MaxRetries failed: $($_.Exception.Message)" -ForegroundColor Gray
    }

    $attempt++
    if ($attempt -le $MaxRetries) {
        Start-Sleep -Seconds $DelaySeconds
    }
}

if (-not $success) {
    Write-Host "[ERROR] Health check failed after $MaxRetries attempts." -ForegroundColor Red
    exit 1
}

exit 0
