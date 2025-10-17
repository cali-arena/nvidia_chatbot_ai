#!/bin/bash

echo "========================================"
echo "NVIDIA AI Chatbot Launcher"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python is installed"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo "✓ Dependencies are installed"
echo ""

# Check for API key
if [ ! -f .env ]; then
    echo "⚠ WARNING: No .env file found"
    echo "You'll need to enter your API key in the app"
    echo ""
fi

echo "Starting the chatbot..."
echo "The app will open in your browser automatically"
echo "Press Ctrl+C to stop the server"
echo ""
echo "========================================"
echo ""

streamlit run app.py

