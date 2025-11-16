param(
    [int]$Port = 8000,
    [string]$PythonExe = 'C:\Users\HP\miniconda3\envs\venv1\python.exe'
)

$reportDir = "$PSScriptRoot\allure-report"

if (-not (Test-Path $reportDir)) {
    Write-Host "ERROR: allure-report directory not found at: $reportDir" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "$reportDir\index.html")) {
    Write-Host "ERROR: index.html not found in $reportDir" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonExe)) {
    Write-Host "ERROR: Python executable not found at: $PythonExe" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Allure Report Server..." -ForegroundColor Green
Write-Host "Report directory: $reportDir" -ForegroundColor Cyan
Write-Host "Server URL: http://localhost:$Port" -ForegroundColor Cyan

$serverProcess = Start-Process -FilePath $PythonExe -ArgumentList "-m", "http.server", $Port -WorkingDirectory $reportDir -PassThru -NoNewWindow
Start-Sleep -Seconds 2

if ($null -eq $serverProcess -or $serverProcess.HasExited) {
    Write-Host "ERROR: Failed to start HTTP server" -ForegroundColor Red
    exit 1
}

Write-Host "Server started successfully (PID: $($serverProcess.Id))" -ForegroundColor Green
Write-Host "Opening report in browser..." -ForegroundColor Cyan

Start-Process "http://localhost:$Port"

Write-Host "Server is running. Press Ctrl+C to stop." -ForegroundColor Yellow

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    if ($null -ne $serverProcess -and -not $serverProcess.HasExited) {
        Stop-Process -Id $serverProcess.Id -Force
    }
    Write-Host "Server stopped" -ForegroundColor Green
}
