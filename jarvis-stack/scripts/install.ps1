Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Set-Location (Join-Path $PSScriptRoot '..')

$dockerFound = Get-Command docker -ErrorAction SilentlyContinue
if ($dockerFound) {
  try {
    docker compose version | Out-Null
    Write-Host '[JARVIS] Starting with Docker Compose...'
    docker compose up -d --build
    Write-Host '[JARVIS] Ready at http://localhost:8787'
    exit 0
  } catch {}
}

Write-Host '[JARVIS] Docker not found. Falling back to Python local install...'
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
uvicorn server:app --app-dir app --host 0.0.0.0 --port 8787
