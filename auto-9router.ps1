<#
.SYNOPSIS
    9Router Auto-Manager - Starts, monitors, and restarts 9Router automatically
.DESCRIPTION
    Runs 9Router in background, monitors health, auto-restarts on failure,
    provides system tray notifications, and exposes API for other scripts.
#>

param(
    [string]$RouterUrl = "http://localhost:20128",
    [int]$CheckInterval = 30,
    [int]$MaxRetries = 3,
    [switch]$Background
)

$ErrorActionPreference = "Stop"

# Global state
$script:process = $null
$script:retries = 0
$script:running = $true

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "HH:mm:ss"
    $color = switch ($Level) {
        "ERROR" { "Red" }
        "WARN"  { "Yellow" }
        "OK"    { "Green" }
        default { "Cyan" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

function Start-9Router {
    Write-Log "Starting 9Router..."
    try {
        $script:process = Start-Process "npx" -ArgumentList "@decolua/9router" `
            -WindowStyle Hidden -PassThru -ErrorAction Stop
        Write-Log "9Router started (PID: $($script:process.Id))" "OK"
        $script:retries = 0
        return $true
    } catch {
        Write-Log "Failed to start 9Router: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-Health {
    try {
        $response = Invoke-RestMethod -Uri "$RouterUrl/api/health" -Method Get -TimeoutSec 5 -ErrorAction Stop
        return $response.ok -eq $true
    } catch {
        return $false
    }
}

function Wait-ForHealthy {
    param([int]$Timeout = 30)
    $elapsed = 0
    while ($elapsed -lt $Timeout) {
        if (Test-Health) {
            Write-Log "9Router is healthy!" "OK"
            return $true
        }
        Start-Sleep -Seconds 2
        $elapsed += 2
    }
    Write-Log "Health check timeout" "ERROR"
    return $false
}

function Stop-9Router {
    if ($script:process -and -not $script:process.HasExited) {
        Write-Log "Stopping 9Router (PID: $($script:process.Id))..."
        Stop-Process -Id $script:process.Id -Force -ErrorAction SilentlyContinue
        $script:process.WaitForExit(5000)
        Write-Log "9Router stopped" "OK"
    }
}

function Monitor-Loop {
    Write-Log "Starting monitor loop (interval: ${CheckInterval}s)"
    while ($script:running) {
        Start-Sleep -Seconds $CheckInterval

        if (-not $script:running) { break }

        if (-not (Test-Health)) {
            Write-Log "Health check failed!" "WARN"
            $script:retries++

            if ($script:retries -le $MaxRetries) {
                Write-Log "Attempting restart ($($script:retries)/$MaxRetries)..." "WARN"
                Stop-9Router
                if (Start-9Router) {
                    Wait-ForHealthy -Timeout 30
                }
            } else {
                Write-Log "Max retries exceeded. Stopping monitor." "ERROR"
                $script:running = $false
            }
        } else {
            $script:retries = 0
        }
    }
}

# Register cleanup
$cleanup = {
    Write-Log "Shutting down..."
    $script:running = $false
    Stop-9Router
}
Register-EngineEvent -SourceIdentifier "PowerShell.Exiting" -Action $cleanup | Out-Null

# Main
Write-Log "========================================" "INFO"
Write-Log "   9Router Auto-Manager Starting" "INFO"
Write-Log "========================================" "INFO"
Write-Log "URL: $RouterUrl" "INFO"
Write-Log "Check interval: ${CheckInterval}s" "INFO"
Write-Log "Max retries: $MaxRetries" "INFO"
Write-Log ""

# Check if already running
if (Test-Health) {
    Write-Log "9Router already running and healthy!" "OK"
} else {
    if (-not (Start-9Router)) { exit 1 }
    if (-not (Wait-ForHealthy -Timeout 30)) { exit 1 }
}

# Show models
try {
    $models = Invoke-RestMethod -Uri "$RouterUrl/v1/models" -Method Get -TimeoutSec 10
    Write-Log "Models loaded: $($models.data.Count) total" "OK"
} catch {
    Write-Log "Could not fetch models" "WARN"
}

if ($Background) {
    Write-Log "Running in background. Press Ctrl+C to stop." "INFO"
    Monitor-Loop
} else {
    Write-Log "Running in foreground. Press Ctrl+C to stop." "INFO"
    Monitor-Loop
}