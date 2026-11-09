
@echo off
title RecallBox Setup

echo ====================================
echo       RECALLBOX ENVIRONMENT SETUP
echo ====================================

cd /d "%~dp0"

echo.
echo Checking Python installation...

python --version

if errorlevel 1 (
    echo Python is not installed or not available in PATH.
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...

if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
)

echo.
echo Activating environment...

call .venv\Scripts\activate.bat

echo.
echo Upgrading pip...

python -m pip install --upgrade pip

echo.
echo Installing project dependencies...

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Package installation failed.
    pause
    exit /b 1
)

echo.
echo ====================================
echo       SETUP COMPLETED!
echo ====================================

pause
