@echo off
REM Allure Report Server Launcher (Batch version)
REM This script starts a local HTTP server and opens the Allure report

setlocal enabledelayexpand

set PORT=8000
set PYTHON_EXE=C:\Users\HP\miniconda3\envs\venv1\python.exe
set REPORT_DIR=%~dp0allure-report

REM Check if report directory exists
if not exist "!REPORT_DIR!" (
    echo.
    echo ERROR: allure-report directory not found at: !REPORT_DIR!
    echo.
    echo First, run tests to generate the report:
    echo   "!PYTHON_EXE!" -m pytest --alluredir=allure-results
    echo   allure generate allure-results -o allure-report --clean
    echo.
    pause
    exit /b 1
)

REM Check if index.html exists
if not exist "!REPORT_DIR!\index.html" (
    echo ERROR: index.html not found in !REPORT_DIR!
    pause
    exit /b 1
)

REM Check if Python exists
if not exist "!PYTHON_EXE!" (
    echo ERROR: Python executable not found at: !PYTHON_EXE!
    echo Update the PYTHON_EXE path in this script.
    pause
    exit /b 1
)

cls
echo.
echo ========================================
echo   Allure Report Server Launcher
echo ========================================
echo.
echo Report Directory: !REPORT_DIR!
echo Server URL: http://localhost:!PORT!
echo.
echo Starting server...
echo.

REM Start server and open browser
cd /d "!REPORT_DIR!"
"!PYTHON_EXE!" -m http.server !PORT!

REM This line won't be reached until server stops (Ctrl+C)
echo.
echo Server stopped.
pause
