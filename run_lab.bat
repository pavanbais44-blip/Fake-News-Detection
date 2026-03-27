@echo off
setlocal
echo 🛡️  Starting TruthGuard Forensic Hub...
echo.

:: Check for uv (Python package manager)
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  UV not found. Please install uv for the backend.
    echo Visit: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

:: Check for npm (Node.js package manager)
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  NPM not found. Please install Node.js/NPM for the frontend.
    pause
    exit /b 1
)

echo 🧠  [1/2] Launching Neural Backend Cluster (Port 8000)...
:: Run backend in a separate persistent window
start "TruthGuard_Backend" cmd /k "cd backend && echo Backend starting... && uv run python app.py"

:: 🕧 Wait for Backend Startup
echo ⏳  Waiting for Neural weights to load...
timeout /t 5 /nobreak > nul

echo 🔬  [2/2] Spinning up Research Dashboard (Port 5173)...
:: Run frontend in a separate persistent window
start "TruthGuard_Frontend" cmd /k "cd frontend && echo Frontend starting... && npm run dev"

echo.
echo ✅  TruthGuard Lab is initializing!
echo.
echo 📜  Research Dashboard:  http://localhost:5173
echo 🧠  Forensic API Portal: http://localhost:8000
echo.
echo ⚠️   Keep BOTH terminal windows open during your investigation.
echo.
pause

