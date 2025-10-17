@echo off
echo ========================================
echo NVIDIA AI Chatbot - Quick Start
echo ========================================
echo.

set NVIDIA_API_KEY=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

echo Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install streamlit langchain langchain-nvidia-ai-endpoints langchain-core langchain-community python-dotenv requests pillow pypdf python-docx
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK!
echo.
echo Starting chatbot...
echo Your API key is configured automatically.
echo The app will open in your browser.
echo.
echo Press Ctrl+C to stop
echo.

streamlit run app.py

pause

