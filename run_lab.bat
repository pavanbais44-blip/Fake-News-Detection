@echo off
setlocal
echo 🛡️  Starting TruthGuard Forensic Hub...
echo.

:: 1. Launch Agentic Backend
echo 🧠  [1/2] Launching Neural Backend Cluster (Port 8000)...
start /B "TruthGuard_Backend" cmd /c "cd backend && uv run python app.py"

:: 🕧 Wait for Backend Startup
echo ⏳  Waiting for Neural weights to load...
timeout /t 5 /nobreak > nul

:: 2. Launch Forensic Dashboard
echo 🔬  [2/2] Spinning up Research Dashboard (Port 5173)...
start "TruthGuard_Frontend" cmd /c "cd frontend && npx vite"

echo.
echo ✅  TruthGuard Lab is initializing!
echo.
echo 📜  Research Dashboard: http://localhost:5173
echo 🧠  Forensic API:      http://localhost:8000
echo.
echo ⚠️   Keep BOTH terminal windows open during your investigation.
echo.
pause
