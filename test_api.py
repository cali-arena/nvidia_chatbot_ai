"""
Test script to verify NVIDIA API key and connection
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if NVIDIA API key is configured and working"""
    
    print("=" * 80)
    print("NVIDIA API Key Test")
    print("=" * 80)
    print()
    
    # Check if API key exists
    api_key = os.getenv("NVIDIA_API_KEY")
    
    if not api_key:
        print("❌ No API key found!")
        print()
        print("Please set your NVIDIA API key:")
        print("1. Create a .env file in this directory")
        print("2. Add: NVIDIA_API_KEY=nvapi-your-key-here")
        print("3. Or set it as an environment variable")
        print()
        print("Get your API key at: https://build.nvidia.com/")
        sys.exit(1)
    
    print(f"✅ API key found: {api_key[:15]}...")
    print()
    
    # Test the API key with a simple request
    print("Testing API connection...")
    print()
    
    try:
        from langchain_nvidia_ai_endpoints import ChatNVIDIA
        from langchain_core.messages import HumanMessage
        
        # Try to initialize the model
        llm = ChatNVIDIA(
            model="meta/llama-3.1-8b-instruct",
            nvidia_api_key=api_key,
            max_tokens=50
        )
        
        print("✅ Model initialized successfully")
        print()
        
        # Test a simple query
        print("Sending test message...")
        response = llm.invoke([HumanMessage(content="Say 'Hello from NVIDIA AI!' if you can hear me.")])
        
        print("✅ API connection successful!")
        print()
        print("Response:")
        print("-" * 80)
        print(response.content)
        print("-" * 80)
        print()
        
        # List available models
        print("Fetching available models...")
        models = ChatNVIDIA.get_available_models()
        
        print(f"✅ Found {len(models)} available models")
        print()
        print("Available models:")
        print("-" * 80)
        for model in models[:10]:  # Show first 10
            print(f"  • {model.id}")
        if len(models) > 10:
            print(f"  ... and {len(models) - 10} more")
        print("-" * 80)
        print()
        
        print("=" * 80)
        print("✅ All tests passed! Your setup is ready.")
        print("=" * 80)
        print()
        print("You can now run the chatbot:")
        print("  streamlit run app.py")
        print()
        
        return True
        
    except ImportError as e:
        print("❌ Missing dependencies!")
        print()
        print(f"Error: {str(e)}")
        print()
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print("❌ API test failed!")
        print()
        print(f"Error: {str(e)}")
        print()
        print("Possible issues:")
        print("1. Invalid API key - get a new one at https://build.nvidia.com/")
        print("2. Network connection problem")
        print("3. API service temporarily unavailable")
        print()
        print("Please check your API key and try again.")
        sys.exit(1)

if __name__ == "__main__":
    test_api_key()

