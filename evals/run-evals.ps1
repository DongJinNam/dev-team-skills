$ErrorActionPreference = "Stop"
$Runner = Join-Path $PSScriptRoot "run_evals.py"
foreach ($Interpreter in @("python3", "python", "py")) {
    $Command = Get-Command $Interpreter -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($Command) {
        if ($Interpreter -eq "py") { & $Command.Source -3 $Runner @args }
        else { & $Command.Source $Runner @args }
        exit $LASTEXITCODE
    }
}
[Console]::Error.WriteLine("ERROR: Python 3.10+ is required.")
exit 2
