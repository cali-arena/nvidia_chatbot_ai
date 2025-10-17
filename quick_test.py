"""
Quick Test Script for Assessment
Test all endpoints and run a simple assessment
"""

import requests
import time
import json

# Server configuration
SERVER_URL = "http://localhost:9012"

def test_endpoints():
    """Test all endpoints quickly"""
    print("🧪 Testing All Endpoints...")
    print("=" * 50)
    
    # Test Basic Chat
    try:
        response = requests.post(
            f"{SERVER_URL}/basic_chat",
            json={"input": "What is artificial intelligence?"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ /basic_chat - Working")
        else:
            print(f"❌ /basic_chat - Error: {response.status_code}")
    except Exception as e:
        print(f"❌ /basic_chat - Error: {e}")
    
    # Test Retriever
    try:
        response = requests.post(
            f"{SERVER_URL}/retriever",
            json={"input": "machine learning"},
            timeout=10
        )
        if response.status_code == 200:
            print("✅ /retriever - Working")
        else:
            print(f"❌ /retriever - Error: {response.status_code}")
    except Exception as e:
        print(f"❌ /retriever - Error: {e}")
    
    # Test Generator
    try:
        response = requests.post(
            f"{SERVER_URL}/generator",
            json={
                "input": "What is deep learning?",
                "context": "Deep Learning is a subset of machine learning that uses neural networks with multiple layers."
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ /generator - Working")
        else:
            print(f"❌ /generator - Error: {response.status_code}")
    except Exception as e:
        print(f"❌ /generator - Error: {e}")
    
    # Test Health
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ /health - Working")
        else:
            print(f"❌ /health - Error: {response.status_code}")
    except Exception as e:
        print(f"❌ /health - Error: {e}")

def run_quick_assessment():
    """Run a quick assessment with 3 questions"""
    print("\n🎯 Running Quick Assessment (3 questions)...")
    print("=" * 50)
    
    questions = [
        "What is artificial intelligence?",
        "What is machine learning?", 
        "What is deep learning?"
    ]
    
    expected_answers = [
        "Artificial Intelligence (AI) is intelligence demonstrated by machines",
        "Machine Learning is a subset of AI that focuses on algorithms",
        "Deep Learning is a subset of machine learning that uses neural networks"
    ]
    
    score = 0
    
    for i, question in enumerate(questions):
        print(f"\n📝 Question {i+1}: {question}")
        
        # Get RAG response
        try:
            # Retrieve documents
            retriever_response = requests.post(
                f"{SERVER_URL}/retriever",
                json={"input": question},
                timeout=10
            )
            
            if retriever_response.status_code == 200:
                docs = retriever_response.json()["output"]
                context = " ".join([doc["page_content"] for doc in docs[:2]])
                
                # Generate response
                generator_response = requests.post(
                    f"{SERVER_URL}/generator",
                    json={"input": question, "context": context},
                    timeout=10
                )
                
                if generator_response.status_code == 200:
                    rag_response = generator_response.json()["output"]
                    
                    # Simple evaluation
                    expected = expected_answers[i].lower()
                    response_lower = rag_response.lower()
                    
                    if any(word in response_lower for word in expected.split()):
                        score += 1
                        print(f"✅ CORRECT! (+1 point)")
                    else:
                        print(f"❌ INCORRECT")
                    
                    print(f"Response: {rag_response[:100]}...")
                else:
                    print(f"❌ Generator error: {generator_response.status_code}")
            else:
                print(f"❌ Retriever error: {retriever_response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Final results
    success_rate = score / len(questions)
    print(f"\n🎯 QUICK ASSESSMENT RESULTS:")
    print(f"📊 Score: {score}/{len(questions)}")
    print(f"📈 Success Rate: {success_rate:.1%}")
    
    if success_rate > 0.60:
        print("🎉 CONGRATULATIONS! You would pass the assessment!")
    else:
        print("❌ Assessment would fail. Success rate below 60%.")
    
    return success_rate > 0.60

def main():
    """Main function"""
    print("🚀 Quick Assessment Test")
    print("=" * 60)
    
    # Check server status
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("❌ Server not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("🔧 Make sure the server is running: python simple_assessment_server.py")
        return
    
    # Test endpoints
    test_endpoints()
    
    # Run quick assessment
    passed = run_quick_assessment()
    
    print("\n" + "=" * 60)
    if passed:
        print("🎉 READY FOR FINAL ASSESSMENT!")
        print("✅ All systems working correctly")
        print("📝 You can now run the full notebook")
    else:
        print("🔧 Please check the implementation")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
