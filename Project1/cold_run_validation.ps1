# Isolated cold run: stages only the standard-library model files in a fresh
# temporary folder, executes Python in isolated mode, then writes a dated log.
$project = $PSScriptRoot
$staging = Join-Path ([System.IO.Path]::GetTempPath()) ("jnj-cold-run-" + [guid]::NewGuid().ToString())
$log = Join-Path $project 'docs\cold-run-log.md'
New-Item -ItemType Directory -Path $staging -ErrorAction Stop | Out-Null
try {
    Copy-Item (Join-Path $project 'jnj_project1_fcff.py') $staging -ErrorAction Stop
    Copy-Item (Join-Path $project 'jnj_peer_multiples.py') $staging -ErrorAction Stop
    Copy-Item (Join-Path $project 'validation_suite.py') $staging -ErrorAction Stop
    $output = Push-Location $staging; try {
        & (Join-Path $project '..\.venv\Scripts\python.exe') -I .\validation_suite.py 2>&1
    } finally { Pop-Location }
    if ($LASTEXITCODE -ne 0) { throw "Cold-run validation failed: $output" }
    @(
        '# Cold-run validation log',
        '',
        "- Run timestamp: $(Get-Date -Format 'o')",
        '- Environment: fresh temporary working directory; Python isolated mode (`-I`); standard-library model only.',
        '- Result: PASS',
        '',
        '```text',
        $output,
        '```'
    ) | Set-Content -LiteralPath $log -Encoding utf8
    Write-Output "PASS: cold-run log written to $log"
} finally {
    if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }
}
