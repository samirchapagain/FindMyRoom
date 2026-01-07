@echo off
title LuxeRooms - Django Website
color 0A

echo ========================================
echo    LuxeRooms - Room Finder Platform
echo ========================================
echo.

REM Change to project directory
cd /d "C:\myproject"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Running database migrations...
python manage.py migrate

echo.
echo [3/3] Starting Django development server...
echo.
echo ========================================
echo   Website URLs:
echo   Main Site: http://127.0.0.1:8000
echo   Admin Panel: http://127.0.0.1:8000/admin
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo ========================================

python manage.py runserver