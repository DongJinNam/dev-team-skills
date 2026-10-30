<#
.SYNOPSIS
  Cross-platform verification harness script for Windows (PowerShell).
  Verifies plugin manifest, SKILL.md frontmatter, and rule files synchronization.
#>

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔍 AI Agent Harness Verification (Windows)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $RepoRoot

$Failed = $false

# 1. Verify plugin.json
Write-Host "`n[1/3] Checking plugin.json manifest..." -ForegroundColor Yellow
$PluginPath = Join-Path $RepoRoot "plugin.json"
if (-not (Test-Path $PluginPath)) {
    Write-Host "❌ Error: plugin.json not found at repo root!" -ForegroundColor Red
    $Failed = $true
} else {
    try {
        $PluginContent = Get-Content -Raw -Path $PluginPath | ConvertFrom-Json
        if (-not $PluginContent.name -or -not $PluginContent.description) {
            Write-Host "❌ Error: plugin.json missing required 'name' or 'description'!" -ForegroundColor Red
            $Failed = $true
        } else {
            Write-Host "  ✅ plugin.json is valid (Name: $($PluginContent.name), Version: $($PluginContent.version))" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Error: Failed to parse plugin.json as valid JSON: $_" -ForegroundColor Red
        $Failed = $true
    }
}

# 2. Verify all SKILL.md frontmatter
Write-Host "`n[2/3] Checking SKILL.md frontmatters in skills/..." -ForegroundColor Yellow
$SkillFiles = Get-ChildItem -Path (Join-Path $RepoRoot "skills") -Filter "SKILL.md" -Recurse
if ($SkillFiles.Count -eq 0) {
    Write-Host "❌ Error: No SKILL.md files found in skills/!" -ForegroundColor Red
    $Failed = $true
} else {
    foreach ($file in $SkillFiles) {
        $relPath = Resolve-Path -Relative $file.FullName
        $content = Get-Content -Raw -Path $file.FullName
        $hasName = $content -match "(?m)^name:\s*[a-zA-Z0-9_\-]+"
        $hasDesc = $content -match "(?m)^description:\s*"
        if ($hasName -and $hasDesc) {
            Write-Host "  ✅ $relPath (valid frontmatter)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $relPath (invalid frontmatter: name or description missing)" -ForegroundColor Red
            $Failed = $true
        }
    }
}

# 3. Verify rule files synchronization (GEMINI, CLAUDE, CODEX, AGENTS)
Write-Host "`n[3/3] Checking Constitution rule files sync..." -ForegroundColor Yellow
$RuleFiles = @("GEMINI.md", "CLAUDE.md", "CODEX.md", "AGENTS.md")
$Hashes = @{}
foreach ($rf in $RuleFiles) {
    $rfPath = Join-Path $RepoRoot $rf
    if (Test-Path $rfPath) {
        $Hashes[$rf] = (Get-FileHash -Algorithm SHA256 -Path $rfPath).Hash
        Write-Host "  $rf : $($Hashes[$rf])" -ForegroundColor DarkGray
    } else {
        Write-Host "❌ Error: Missing rule file $rf" -ForegroundColor Red
        $Failed = $true
    }
}

$BaseHash = $Hashes["GEMINI.md"]
foreach ($rf in $RuleFiles) {
    if ($Hashes[$rf] -ne $BaseHash) {
        Write-Host "❌ Error: $rf is out of sync with GEMINI.md!" -ForegroundColor Red
        $Failed = $true
    }
}

if (-not $Failed) {
    Write-Host "  ✅ All 4 rule files are strictly synchronized!" -ForegroundColor Green
}

Pop-Location

Write-Host "`n========================================" -ForegroundColor Cyan
if ($Failed) {
    Write-Host "❌ Harness verification FAILED." -ForegroundColor Red
    exit 1
} else {
    Write-Host "🎉 Harness verification PASSED successfully!" -ForegroundColor Green
    exit 0
}
