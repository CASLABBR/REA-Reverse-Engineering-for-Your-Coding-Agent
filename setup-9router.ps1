# 9Router Setup & Integration Script
# Run with: powershell -ExecutionPolicy Bypass -File setup-9router.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   9Router Setup & Auto-Integration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check if 9Router is installed
Write-Host "[1/6] Checking 9Router installation..." -ForegroundColor Yellow
$hasNpx = Get-Command npx -ErrorAction SilentlyContinue
if (-not $hasNpx) {
    Write-Host "  npx not found. Install Node.js first: https://nodejs.org" -ForegroundColor Red
    exit 1
}
Write-Host "  npx found: $($hasNpx.Source)" -ForegroundColor Green

# 2. Install 9Router globally
Write-Host "[2/6] Installing 9Router..." -ForegroundColor Yellow
try {
    npx @decolua/9router --version 2>&1 | Out-Null
    Write-Host "  9Router already available via npx" -ForegroundColor Green
} catch {
    Write-Host "  9Router will run via npx on demand" -ForegroundColor Yellow
}

# 3. Check environment variables
Write-Host "[3/6] Checking environment variables..." -ForegroundColor Yellow
$routerUrl = $env:NINEROUTER_URL ?? "http://localhost:20128"
$routerKey = $env:NINEROUTER_KEY

Write-Host "  NINEROUTER_URL = $routerUrl" -ForegroundColor Gray
if ($routerKey) {
    Write-Host "  NINEROUTER_KEY = **** (set)" -ForegroundColor Green
} else {
    Write-Host "  NINEROUTER_KEY = NOT SET (optional if auth disabled)" -ForegroundColor Yellow
}

# 4. Create .env file for persistence
Write-Host "[4/6] Creating .env file..." -ForegroundColor Yellow
$envContent = @"
# 9Router Configuration
NINEROUTER_URL=$routerUrl
NINEROUTER_KEY=$routerKey
"@
$envPath = "E:\INTELIGENCIA_ARTIFICIAL\SKILL\.env"
$envContent | Out-File -FilePath $envPath -Encoding utf8
Write-Host "  Created: $envPath" -ForegroundColor Green

# 5. Test health endpoint
Write-Host "[5/6] Testing 9Router health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$routerUrl/api/health" -Method Get -TimeoutSec 5 -ErrorAction Stop
    if ($response.ok) {
        Write-Host "  9Router is RUNNING and healthy!" -ForegroundColor Green
    }
} catch {
    Write-Host "  9Router NOT running. Start it with:" -ForegroundColor Red
    Write-Host "    npx @decolua/9router" -ForegroundColor Cyan
}

# 6. List available models
Write-Host "[6/6] Fetching available models..." -ForegroundColor Yellow
try {
    $models = Invoke-RestMethod -Uri "$routerUrl/v1/models" -Method Get -TimeoutSec 10 -ErrorAction Stop
    Write-Host "  Chat models:" -ForegroundColor Cyan
    $models.data | Where-Object { $_.owned_by -ne 'combo' } | Select-Object -First 10 | ForEach-Object {
        Write-Host "    - $($_.id) ($($_.owned_by))" -ForegroundColor Gray
    }
    $combos = $models.data | Where-Object { $_.owned_by -eq 'combo' }
    if ($combos) {
        Write-Host "  Combo models (auto-fallback):" -ForegroundColor Cyan
        $combos | ForEach-Object {
            Write-Host "    - $($_.id)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "  Could not fetch models (is 9Router running?)" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Start 9Router: npx @decolua/9router" -ForegroundColor White
Write-Host "  2. Get API key from Dashboard (if auth enabled)" -ForegroundColor White
Write-Host "  3. Use in your code: \$env:NINEROUTER_URL + \$env:NINEROUTER_KEY" -ForegroundColor White
Write-Host ""
Write-Host "Integration ready for auto-communication!" -ForegroundColor Green