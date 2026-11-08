<#
.SYNOPSIS
    Antigravity(AGY) 환경에 dev-team-skills를 한 번에 적용하는 셋업 스크립트.

.DESCRIPTION
    Antigravity는 프로젝트의 .agents/skills/ 또는 사용자 홈의 ~/.gemini/config/skills/ 경로에서
    스킬을 자동으로 검색(Discovery)합니다.
    이 스크립트는 스킬들을 올바른 디스커버리 위치에 배치하고, 헌법 규칙(GEMINI.md)을 연동합니다.

.PARAMETER Target
    "workspace" (기본값): 현재 프로젝트의 .agents/skills 및 GEMINI.md에 연동합니다.
    "global": 사용자 홈 디렉토리(~/.gemini/config/skills)에 설치하여 모든 프로젝트에서 사용합니다.

.EXAMPLE
    .\scripts\setup-antigravity.ps1 -Target workspace
    .\scripts\setup-antigravity.ps1 -Target global
#>

[CmdletBinding()]
param (
    [ValidateSet("workspace", "global")]
    [string]$Target = "workspace"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SkillsSourceDir = Join-Path $RepoRoot "skills"
$GeminiRuleSource = Join-Path $RepoRoot "GEMINI.md"

Write-Host "=== Antigravity (AGY) dev-team-skills Setup ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot"

if (-not (Test-Path $SkillsSourceDir)) {
    Write-Error "Skills directory not found at $SkillsSourceDir"
    exit 1
}

function Link-Or-Copy {
    param (
        [string]$Source,
        [string]$Destination
    )
    if (Test-Path $Destination) {
        Write-Host "  [Exists] $Destination" -ForegroundColor DarkGray
        return
    }
    try {
        # 심볼릭 링크 또는 Junction 시도
        New-Item -ItemType SymbolicLink -Path $Destination -Target $Source -ErrorAction Stop | Out-Null
        Write-Host "  [Linked] $Destination -> $Source" -ForegroundColor Green
    }
    catch {
        # 권한 부족 시 복사로 Fallback
        Copy-Item -Path $Source -Destination $Destination -Recurse -Force
        Write-Host "  [Copied] $Destination (fallback from symlink)" -ForegroundColor Yellow
    }
}

if ($Target -eq "workspace") {
    $AgentsDir = Join-Path $RepoRoot ".agents"
    $AgentsSkillsDir = Join-Path $AgentsDir "skills"
    
    if (-not (Test-Path $AgentsSkillsDir)) {
        New-Item -ItemType Directory -Path $AgentsSkillsDir -Force | Out-Null
    }

    Write-Host "[1/2] Linking workspace skills to .agents/skills/..." -ForegroundColor Cyan
    Get-ChildItem -Path $SkillsSourceDir -Directory | ForEach-Object {
        $skillName = $_.Name
        if ($skillName -ne "references" -and $skillName -ne "scripts") {
            $dest = Join-Path $AgentsSkillsDir $skillName
            Link-Or-Copy -Source $_.FullName -Destination $dest
        }
    }

    Write-Host "[2/2] Ensuring GEMINI.md rule exists at repository root..." -ForegroundColor Cyan
    if (Test-Path $GeminiRuleSource) {
        Write-Host "  [Ready] GEMINI.md is present at repository root." -ForegroundColor Green
    }
    
    Write-Host "`nWorkspace setup complete!" -ForegroundColor Green
    Write-Host "Antigravity CLI/IDE will now automatically discover workspace skills in .agents/skills/"
}
elseif ($Target -eq "global") {
    $UserHome = [Environment]::GetFolderPath("UserProfile")
    $GlobalSkillsDir = Join-Path $UserHome ".gemini\config\skills"

    if (-not (Test-Path $GlobalSkillsDir)) {
        New-Item -ItemType Directory -Path $GlobalSkillsDir -Force | Out-Null
    }

    Write-Host "[1/1] Installing skills to Global config (~/.gemini/config/skills)..." -ForegroundColor Cyan
    Get-ChildItem -Path $SkillsSourceDir -Directory | ForEach-Object {
        $skillName = $_.Name
        if ($skillName -ne "references" -and $skillName -ne "scripts") {
            $dest = Join-Path $GlobalSkillsDir $skillName
            Link-Or-Copy -Source $_.FullName -Destination $dest
        }
    }

    Write-Host "`nGlobal setup complete!" -ForegroundColor Green
    Write-Host "All Antigravity sessions on this machine will now have access to these skills."
}
