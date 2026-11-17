@echo off
setlocal enabledelayedexpansion
title JARVIS AI - Just A Rather Very Intelligent System
color 0B
echo.
echo ============================================================
echo   JARVIS AI - Just A Rather Very Intelligent System
echo   Intelligent Personal Assistant and AI Problem-Solving System
echo ============================================================
echo.
cd /d "%~dp0"

REM ============================================================
REM  STEP 1: Detect Python
REM ============================================================
echo [STEP 1/3]  Detecting Python installation...
echo.
set "PY_CMD="

python --version >nul 2>&1
if !errorlevel! equ 0 ( set "PY_CMD=python" & goto :python_found )

py --version >nul 2>&1
if !errorlevel! equ 0 ( set "PY_CMD=py" & goto :python_found )

echo.
echo  [ERROR]  Python was NOT found on your system.
echo.
echo  Please download and install Python 3.9 or later from:
echo  https://www.python.org/downloads/
echo.
echo  IMPORTANT: During installation, tick the box "Add Python to PATH".
echo.
pause
exit /b 1

:python_found
for /f "tokens=*" %%v in ('!PY_CMD! --version 2^>^&1') do set "PY_VER=%%v"
echo  [OK]  Found: !PY_VER!
echo.

REM ============================================================
REM  STEP 2: Install All Dependencies Directly to System Python
REM ============================================================
echo [STEP 2/3]  Installing all required libraries to your computer...
echo             This may take a few minutes on first run.
echo.

echo  - Upgrading pip...
!PY_CMD! -m pip install --upgrade pip --quiet
echo.

echo  - Installing fastapi...
!PY_CMD! -m pip install "fastapi>=0.104.1" --quiet
echo  - Installing uvicorn...
!PY_CMD! -m pip install "uvicorn[standard]>=0.24.0" --quiet
echo  - Installing pydantic...
!PY_CMD! -m pip install "pydantic>=2.5.0" --quiet
echo  - Installing numpy...
!PY_CMD! -m pip install "numpy>=1.26.0" --quiet
echo  - Installing scikit-learn...
!PY_CMD! -m pip install "scikit-learn>=1.3.0" --quiet
echo  - Installing networkx...
!PY_CMD! -m pip install "networkx>=3.2.0" --quiet
echo  - Installing scipy...
!PY_CMD! -m pip install "scipy>=1.11.0" --quiet
echo  - Installing python-multipart...
!PY_CMD! -m pip install "python-multipart>=0.0.6" --quiet
echo  - Installing python-dotenv...
!PY_CMD! -m pip install "python-dotenv>=1.0.0" --quiet
echo  - Installing pytest...
!PY_CMD! -m pip install "pytest>=7.4.0" --quiet
echo  - Installing pytest-asyncio...
!PY_CMD! -m pip install "pytest-asyncio>=0.21.0" --quiet
echo  - Installing httpx...
!PY_CMD! -m pip install "httpx>=0.25.0" --quiet
echo  - Installing aiofiles...
!PY_CMD! -m pip install "aiofiles>=23.2.0" --quiet
echo  - Installing google-genai...
!PY_CMD! -m pip install "google-genai>=3.0.0" --quiet
echo.

echo  Verifying installation...
!PY_CMD! -c "import fastapi, uvicorn, pydantic, numpy, google.genai" >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo  [ERROR]  One or more required libraries failed to install.
    echo  Please check your internet connection and try again.
    echo  Or run manually:  !PY_CMD! -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo  [OK]  All libraries installed and verified successfully!
echo.

REM  Create .env from template if not present
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo  [INFO]  Created .env configuration file from template.
        echo.
    )
)

REM ============================================================
REM  STEP 3: Launch JARVIS AI
REM ============================================================
echo [STEP 3/3]  Launching JARVIS AI server...
echo.
echo ============================================================
echo   JARVIS AI is now ONLINE!
echo   Open your browser and navigate to:  http://127.0.0.1:8000
echo   Press Ctrl+C in this window to stop the server.
echo ============================================================
echo.

!PY_CMD! -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo ============================================================
echo   JARVIS AI server has stopped.
echo ============================================================
echo.
pause
