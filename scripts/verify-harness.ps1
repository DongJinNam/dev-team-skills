# Shell entry point; validation rules live in verify-harness.py.
$ErrorActionPreference = "Stop"
$Verifier = Join-Path $PSScriptRoot "verify-harness.py"

foreach ($Interpreter in @("python3", "python", "py")) {
    $Command = Get-Command $Interpreter -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($Command) {
        if ($Interpreter -eq "py") {
            & $Command.Source -3 $Verifier @args
        } else {
            & $Command.Source $Verifier @args
        }
        exit $LASTEXITCODE
    }
}
[Console]::Error.WriteLine("ERROR: Python 3.10+ is required to run the package verifier.")
exit 2
