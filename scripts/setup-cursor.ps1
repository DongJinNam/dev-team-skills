<#
.SYNOPSIS
    Cursor 환경에 dev-team-skills 규칙을 설정하는 셋업 스크립트.

.DESCRIPTION
    Cursor의 최신 규칙 디렉토리(.cursor/rules/)에 engineering-squad.mdc 규칙을 생성하고,
    루트에 .cursorrules 파일을 동기화합니다.
    주의: Cursor 환경은 현재 실험적(Experimental) 단계입니다.

.PARAMETER TargetDir
    규칙을 복사할 대상 프로젝트 루트 디렉토리 (기본값: 현재 저장소 루트).

.EXAMPLE
    .\scripts\setup-cursor.ps1
    .\scripts\setup-cursor.ps1 -TargetDir "C:\path\to\my-project"
#>

[CmdletBinding()]
param (
    [string]$TargetDir
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

if (-not $TargetDir) {
    $TargetDir = $RepoRoot
}

Write-Host "=== Cursor dev-team-skills Setup [EXPERIMENTAL] ===" -ForegroundColor Cyan
Write-Host "Target Directory: $TargetDir"

$CursorRulesDir = Join-Path $TargetDir ".cursor\rules"
if (-not (Test-Path $CursorRulesDir)) {
    New-Item -ItemType Directory -Path $CursorRulesDir -Force | Out-Null
}

$SourceMdc = Join-Path $RepoRoot ".cursor\rules\engineering-squad.mdc"
$DestMdc = Join-Path $CursorRulesDir "engineering-squad.mdc"
Copy-Item -Path $SourceMdc -Destination $DestMdc -Force
Write-Host "  [OK] Created $DestMdc" -ForegroundColor Green

$SourceLegacy = Join-Path $RepoRoot ".cursorrules"
$DestLegacy = Join-Path $TargetDir ".cursorrules"
Copy-Item -Path $SourceLegacy -Destination $DestLegacy -Force
Write-Host "  [OK] Created $DestLegacy" -ForegroundColor Green

Write-Host "`nCursor setup complete!" -ForegroundColor Green
Write-Host "NOTE: Cursor support is currently EXPERIMENTAL. Feedback is welcome!" -ForegroundColor Yellow
