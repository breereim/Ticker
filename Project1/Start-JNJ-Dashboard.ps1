# Starts the local JNJ valuation dashboard and opens it in the default browser.
# Keep this PowerShell window open while using the dashboard.
Set-Location -LiteralPath $PSScriptRoot
$candidates = @(
    (Join-Path $PSScriptRoot '.venv\Scripts\python.exe'),
    (Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe')
)
$python = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if ($python) {
    & $python .\jnj_valuation_app.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 .\jnj_valuation_app.py
} else {
    throw 'Python 3 was not found. Install Python 3, then rerun this launcher.'
}
