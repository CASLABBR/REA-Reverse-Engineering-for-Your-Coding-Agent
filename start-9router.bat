@echo off
echo Starting 9Router on http://localhost:20128
echo.
echo Make sure you have 9Router installed: https://github.com/decolua/9router
echo.
echo Set your NINEROUTER_KEY environment variable if using authentication:
echo   set NINEROUTER_KEY=sk-your-key-here
echo.
echo Checking if 9Router is already running...
curl -s http://localhost:20128/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo 9Router is already running!
    echo Health check: http://localhost:20128/api/health
) else (
    echo 9Router not running. Starting...
    echo Run: npx @decolua/9router
    echo Or if installed globally: 9router
)
echo.