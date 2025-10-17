@echo off
echo ========================================
echo NVIDIA AI Chatbot Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python is installed
echo.

REM Check if requirements are installed
echo Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies are installed
echo.

REM Check for API key
if not exist .env (
    echo WARNING: No .env file found
    echo You'll need to enter your API key in the app
    echo.
)

echo Starting the chatbot...
echo The app will open in your browser automatically
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

streamlit run app.py

pause

