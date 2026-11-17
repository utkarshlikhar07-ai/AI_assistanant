@echo off
setlocal enabledelayedexpansion
title JARVIS AI — Environment Setup
color 0A
echo.
echo ============================================================
echo   JARVIS AI — Initial Environment Setup & Dependency Installer
echo   Google Gemini LLM + Python Algorithms Laboratory
echo ============================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM 1. Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    where py >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python is not installed or not in PATH.
        echo Please install Python 3.9+ from https://www.python.org/
        pause
        exit /b 1
    )
    set "PY_CMD=py"
) else (
    set "PY_CMD=python"
)

echo [1/4] Python detected. Using: %PY_CMD%

REM 2. Create or verify venv
if not exist "venv\Scripts\activate.bat" (
    echo [2/4] Creating virtual environment (venv)...
    %PY_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo       Virtual environment created successfully.
) else (
    echo [2/4] Virtual environment (venv) already exists.
)

call venv\Scripts\activate.bat
set "PY_CMD=python"

REM 3. Upgrade pip and install requirements
echo [3/4] Installing dependencies from requirements.txt...
%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

REM 4. Setup .env file if missing
echo [4/4] Verifying environment configuration (.env)...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo       Created .env from .env.example.
        echo       Please edit .env to insert your GEMINI_API_KEY if desired.
    )
) else (
    echo       .env file detected.
)

echo.
echo ============================================================
echo   Setup Complete!
echo   Run 'start.bat' to launch the JARVIS AI assistant.
echo ============================================================
echo.
pause
