@echo off
echo ===================================================
echo Starting AI-Powered Crop Yield Prediction Project
echo ===================================================

echo [1/2] Launching Backend Server on http://localhost:8000 ...
start "Backend Server (FastAPI)" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Launching Frontend Server on http://localhost:5173 ...
start "Frontend Server (Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ===================================================
echo Project started!
echo Frontend: http://localhost:5173
echo Backend API Docs: http://localhost:8000/docs
echo Backend Health: http://localhost:8000/api/health
echo ===================================================
pause
