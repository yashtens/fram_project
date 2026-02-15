@echo off
REM FRAM - Farm Management System - Setup Script for Windows

echo.
echo ============================================
echo FRAM Farm Management System - Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo [1/5] Python found: Installing/Updating packages...
echo.

REM Check if venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/Update requirements
pip install -r requirements.txt

echo.
echo [2/5] Packages installed successfully!
echo.
echo [3/5] Checking MySQL setup...
echo.
echo IMPORTANT: Before proceeding, ensure MySQL is installed and running!
echo.
echo To set up MySQL:
echo 1. Download MySQL: https://dev.mysql.com/downloads/mysql/
echo 2. Install MySQL Server (default port 3306)
echo 3. During installation, set a root password
echo .
echo [4/5] Configuring database...
echo.

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo CREATED: .env file
    echo.
    echo ^^!^^! IMPORTANT: Edit .env file with your MySQL credentials ^^!^^!
    echo.
    echo Open .env file and update:
    echo   - MYSQL_HOST (default: localhost)
    echo   - MYSQL_USER (default: root)
    echo   - MYSQL_PASSWORD (enter your MySQL password)
    echo   - MYSQL_DB (default: fram_management)
    echo.
    echo Press any key to open .env file in notepad...
    pause
    notepad .env
) else (
    echo .env file already exists
)

echo.
echo [5/5] Setup complete!
echo.
echo ============================================
echo Next Steps:
echo ============================================
echo.
echo 1. Ensure MySQL Server is running
echo 2. Update .env with your MySQL credentials
echo 3. Create MySQL database:
echo    mysql -u root -p
echo    CREATE DATABASE fram_management;
echo    EXIT;
echo.
echo 4. Run the application:
echo    python run.py
echo.
echo 5. Open browser: http://localhost:5000
echo.
echo ============================================
echo.
pause
