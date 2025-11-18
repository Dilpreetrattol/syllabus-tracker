[CmdletBinding()]
param(
    [int]$Port = 5000,
    [switch]$Debug,
    [string]$DatabaseUrl
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Warning ".venv Python not found at $venvPython. Falling back to system 'python' in PATH."
    $venvPython = "python"
}

# Env vars
$env:FLASK_APP = "app"
$env:FLASK_ENV = if ($Debug) { "development" } else { "production" }

if ($DatabaseUrl) {
    $env:DATABASE_URL = $DatabaseUrl
    Write-Host "Using DATABASE_URL from parameter." -ForegroundColor Cyan
}

# Print summary
Write-Host "Starting Flask with:" -ForegroundColor Green
Write-Host "  FLASK_APP=$($env:FLASK_APP)" -ForegroundColor Green
Write-Host "  FLASK_ENV=$($env:FLASK_ENV)" -ForegroundColor Green
if ($env:DATABASE_URL) { Write-Host "  DATABASE_URL set" -ForegroundColor Green } else { Write-Host "  DATABASE_URL not set (local MySQL/Config fallback)" -ForegroundColor Yellow }
Write-Host "  Port=$Port" -ForegroundColor Green

# Run server
& $venvPython -m flask run --port $Port
