@echo off
title Secure Enterprise RAG System
color 0B

echo.
echo  ================================================
echo   Secure Enterprise RAG System - Startup
echo  ================================================
echo.

set "PYTHON_CMD=python"
if exist "%USERPROFILE%\.venv\Scripts\python.exe" (
    set "PYTHON_CMD=%USERPROFILE%\.venv\Scripts\python.exe"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
)

:: Start backend in new window
echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "RAG Backend" cmd /k "cd /d %~dp0 && "%PYTHON_CMD%" -m uvicorn backend.main:app --reload --port 8000"

:: Wait 8 seconds for backend initialization
echo Waiting for backend to load AI security models...
timeout /t 8 /nobreak >nul

:: Start frontend in new window
echo [2/2] Starting React Frontend on http://localhost:5173 ...
start "RAG Frontend" cmd /k "cd /d %~dp0frontend && npm.cmd run dev -- --port 5173"

:: Wait 3 seconds then open browser
timeout /t 3 /nobreak >nul
echo Opening browser...
start http://localhost:5173

echo.
echo  ================================================
echo   Both servers running!
echo   Frontend : http://localhost:5173
echo   Backend  : http://localhost:8000
echo   API Docs : http://localhost:8000/docs
echo  ================================================
echo.
echo  Test Accounts:
echo    admin_user  / adminpassword  (Full Access)
echo    hr_user     / hrpassword     (HR Docs)
echo    emp_user    / emppassword    (Employee Docs)
echo    intern_user / internpassword (Onboarding Only)
echo.
pause
