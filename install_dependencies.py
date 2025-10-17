"""
Install all required dependencies for the Final Assessment
Run this before executing the notebook
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all required dependencies"""
    print("🚀 Installing Dependencies for Final Assessment")
    print("=" * 60)
    
    # Required packages
    packages = [
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "langserve>=0.3.0",
        "langchain>=0.1.0",
        "langchain-core>=0.1.0",
        "langchain-community>=0.0.20",
        "langchain-huggingface>=0.3.0",
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.4",
        "requests>=2.31.0",
        "pydantic>=2.0.0"
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"📊 Installation Summary: {success_count}/{total_packages} packages installed")
    
    if success_count == total_packages:
        print("🎉 All dependencies installed successfully!")
        print("✅ You can now run the assessment notebook")
        print("📝 Execute: jupyter notebook 08_evaluation.ipynb")
    else:
        print("⚠️ Some packages failed to install")
        print("🔧 Please check the error messages above")
        print("💡 You may need to install them manually")
    
    print("\n🚀 Ready for Final Assessment!")

if __name__ == "__main__":
    main()
