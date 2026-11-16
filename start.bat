@echo off
setlocal enabledelayedexpansion
title JARVIS AI — Just A Rather Very Intelligent System
color 0B
echo.
echo ============================================================
echo   JARVIS AI — Just A Rather Very Intelligent System
echo   Intelligent Personal Assistant and AI Problem-Solving System
echo ============================================================
echo.

REM Set and change to project root directory
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM 1. Check Python installation
where python >nul 2>&1
if %errorlevel% neq 0 (
    where py >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python is not installed or not in your system PATH.
        echo Please install Python 3.9+ from https://www.python.org and ensure "Add Python to PATH" is checked.
        echo.
        pause
        exit /b 1
    )
    set "PY_CMD=py"
) else (
    set "PY_CMD=python"
)

echo [1/3] Python environment detected.

REM 2. Check if required packages are already available in current Python
%PY_CMD% -c "import fastapi, uvicorn, pydantic, numpy" >nul 2>&1
if %errorlevel% equ 0 (
    echo [2/3] Core dependencies verified.
    goto :run_server
)

REM If not in current environment, check/use virtual environment
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe -c "import fastapi, uvicorn, pydantic, numpy" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [2/3] Virtual environment with dependencies found. Activating...
        call venv\Scripts\activate.bat
        goto :run_server
    )
)

REM If dependencies missing, set up venv and install
echo [2/3] Setting up environment and installing dependencies...
if not exist "venv\Scripts\activate.bat" (
    echo       Creating virtual environment...
    %PY_CMD% -m venv venv
)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    set "PY_CMD=python"
)

echo       Installing packages from requirements.txt...
%PY_CMD% -m pip install -r requirements.txt

:run_server
echo [3/3] Starting JARVIS AI server...
echo.
echo ============================================================
echo   JARVIS AI is online!
echo   Open your browser and navigate to: http://127.0.0.1:8000
echo   Press Ctrl+C to stop the server
echo ============================================================
echo.

%PY_CMD% -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo Server process has stopped.
pause
