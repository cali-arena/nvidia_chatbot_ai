"""
Quick setup and run script for NVIDIA AI Chatbot
"""

import subprocess
import sys
import os

# Set the API key
API_KEY = "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"

print("=" * 80)
print("NVIDIA AI Chatbot - Quick Setup")
print("=" * 80)
print()

# Check if dependencies are installed
print("Checking dependencies...")
try:
    import streamlit
    import langchain
    from langchain_nvidia_ai_endpoints import ChatNVIDIA
    print("✅ All dependencies installed")
except ImportError as e:
    print(f"⚠ Missing dependencies: {e}")
    print()
    print("Installing dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-q",
        "streamlit", "langchain", "langchain-nvidia-ai-endpoints",
        "langchain-core", "langchain-community", "python-dotenv",
        "requests", "pillow", "pypdf", "python-docx"
    ])
    print("✅ Dependencies installed")

print()
print("=" * 80)
print("Launching NVIDIA AI Chatbot...")
print("=" * 80)
print()
print(f"✅ API Key configured: {API_KEY[:20]}...")
print()
print("The app will open in your browser automatically")
print("Press Ctrl+C to stop the server")
print()

# Set environment variable
os.environ["NVIDIA_API_KEY"] = API_KEY

# Run Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

