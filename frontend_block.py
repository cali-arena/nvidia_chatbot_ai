"""
Gradio Frontend for Final Assessment
Interface for testing RAG endpoints
"""

import gradio as gr
import requests
import json
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
SERVER_URL = "http://localhost:9012"

class AssessmentClient:
    """Client for interacting with LangServe endpoints"""
    
    def __init__(self, base_url: str = SERVER_URL):
        self.base_url = base_url
        self.endpoints = {
            'basic': f"{base_url}/basic_chat",
            'retriever': f"{base_url}/retriever", 
            'generator': f"{base_url}/generator"
        }
    
    def basic_chat(self, question: str) -> str:
        """Call basic chat endpoint"""
        try:
            response = requests.post(
                self.endpoints['basic'],
                json={"input": question},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("output", "No response received")
        except Exception as e:
            logger.error(f"Basic chat error: {e}")
            return f"Error: {str(e)}"
    
    def retrieve_documents(self, query: str) -> List[Dict]:
        """Call retriever endpoint"""
        try:
            response = requests.post(
                self.endpoints['retriever'],
                json={"input": query},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            # Handle different response formats
            if isinstance(result, dict) and "output" in result:
                return result["output"]
            elif isinstance(result, list):
                return result
            else:
                return [{"page_content": str(result)}]
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return [{"page_content": f"Error: {str(e)}"}]
    
    def generate_response(self, question: str, context: str = "") -> str:
        """Call generator endpoint"""
        try:
            payload = {
                "input": question,
                "context": context
            }
            response = requests.post(
                self.endpoints['generator'],
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("output", "No response received")
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"Error: {str(e)}"
    
    def rag_chain(self, question: str) -> Dict[str, Any]:
        """Complete RAG chain: retrieve + generate"""
        try:
            # Step 1: Retrieve relevant documents
            retrieved_docs = self.retrieve_documents(question)
            
            # Step 2: Format context
            context = "\n\n".join([
                doc.get("page_content", str(doc)) 
                for doc in retrieved_docs
            ])
            
            # Step 3: Generate response
            response = self.generate_response(question, context)
            
            return {
                "question": question,
                "retrieved_docs": retrieved_docs,
                "context": context,
                "response": response,
                "success": True
            }
        except Exception as e:
            logger.error(f"RAG chain error: {e}")
            return {
                "question": question,
                "retrieved_docs": [],
                "context": "",
                "response": f"Error: {str(e)}",
                "success": False
            }

# Initialize client
client = AssessmentClient()

def test_basic_chat(question: str) -> str:
    """Test basic chat functionality"""
    if not question.strip():
        return "Please enter a question to test basic chat."
    return client.basic_chat(question)

def test_retriever(query: str) -> str:
    """Test document retrieval"""
    if not query.strip():
        return "Please enter a query to test retrieval."
    
    docs = client.retrieve_documents(query)
    
    result = "**Retrieved Documents:**\n\n"
    for i, doc in enumerate(docs, 1):
        content = doc.get("page_content", str(doc))
        result += f"**Document {i}:**\n{content}\n\n"
    
    return result

def test_generator(question: str, context: str) -> str:
    """Test response generation"""
    if not question.strip():
        return "Please enter a question to test generation."
    
    return client.generate_response(question, context)

def test_rag_chain(question: str) -> str:
    """Test complete RAG chain"""
    if not question.strip():
        return "Please enter a question to test RAG chain."
    
    result = client.rag_chain(question)
    
    output = f"**Question:** {result['question']}\n\n"
    
    if result['success']:
        output += f"**Retrieved Documents:** {len(result['retrieved_docs'])}\n\n"
        output += f"**Context:**\n{result['context'][:500]}{'...' if len(result['context']) > 500 else ''}\n\n"
        output += f"**Generated Response:**\n{result['response']}"
    else:
        output += f"**Error:** {result['response']}"
    
    return output

def check_server_status() -> str:
    """Check if server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            return "✅ Server is running and healthy!"
        else:
            return f"⚠️ Server responded with status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "❌ Server is not running. Please start server_app.py first."
    except Exception as e:
        return f"❌ Error checking server: {str(e)}"

def get_demo():
    """Create Gradio demo interface"""
    
    with gr.Blocks(
        title="Final Assessment - LangServe RAG System",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as demo:
        
        gr.Markdown("""
        # 🚀 Final Assessment - LangServe RAG System
        
        This interface tests the LangServe endpoints for the final assessment:
        - **Basic Chat** (`/basic_chat`): Direct LLM interaction
        - **Retriever** (`/retriever`): Document retrieval system  
        - **Generator** (`/generator`): Response generation with context
        - **RAG Chain**: Complete Retrieval-Augmented Generation pipeline
        
        **Server Status:** Check if the LangServe server is running on port 9012
        """)
        
        # Server status
        with gr.Row():
            status_btn = gr.Button("🔍 Check Server Status", variant="secondary")
            status_output = gr.Textbox(label="Server Status", interactive=False)
        
        status_btn.click(
            fn=check_server_status,
            outputs=status_output
        )
        
        # Basic Chat Tab
        with gr.Tab("💬 Basic Chat"):
            gr.Markdown("Test the `/basic_chat` endpoint - direct LLM interaction")
            
            with gr.Row():
                with gr.Column():
                    basic_question = gr.Textbox(
                        label="Question",
                        placeholder="Ask me anything...",
                        lines=2
                    )
                    basic_btn = gr.Button("🚀 Send", variant="primary")
                
                with gr.Column():
                    basic_output = gr.Textbox(
                        label="Response",
                        lines=8,
                        interactive=False
                    )
            
            basic_btn.click(
                fn=test_basic_chat,
                inputs=basic_question,
                outputs=basic_output
            )
        
        # Retriever Tab
        with gr.Tab("📚 Document Retrieval"):
            gr.Markdown("Test the `/retriever` endpoint - find relevant documents")
            
            with gr.Row():
                with gr.Column():
                    retriever_query = gr.Textbox(
                        label="Search Query",
                        placeholder="What would you like to find?",
                        lines=2
                    )
                    retriever_btn = gr.Button("🔍 Search", variant="primary")
                
                with gr.Column():
                    retriever_output = gr.Textbox(
                        label="Retrieved Documents",
                        lines=10,
                        interactive=False
                    )
            
            retriever_btn.click(
                fn=test_retriever,
                inputs=retriever_query,
                outputs=retriever_output
            )
        
        # Generator Tab
        with gr.Tab("🤖 Response Generation"):
            gr.Markdown("Test the `/generator` endpoint - generate responses with context")
            
            with gr.Row():
                with gr.Column():
                    generator_question = gr.Textbox(
                        label="Question",
                        placeholder="What would you like to know?",
                        lines=2
                    )
                    generator_context = gr.Textbox(
                        label="Context (optional)",
                        placeholder="Provide context for the question...",
                        lines=4
                    )
                    generator_btn = gr.Button("✨ Generate", variant="primary")
                
                with gr.Column():
                    generator_output = gr.Textbox(
                        label="Generated Response",
                        lines=8,
                        interactive=False
                    )
            
            generator_btn.click(
                fn=test_generator,
                inputs=[generator_question, generator_context],
                outputs=generator_output
            )
        
        # RAG Chain Tab
        with gr.Tab("🔗 Complete RAG Chain"):
            gr.Markdown("Test the complete RAG pipeline - retrieve documents and generate responses")
            
            with gr.Row():
                with gr.Column():
                    rag_question = gr.Textbox(
                        label="Question",
                        placeholder="Ask a complex question that requires document retrieval...",
                        lines=3
                    )
                    rag_btn = gr.Button("🚀 Run RAG Chain", variant="primary")
                
                with gr.Column():
                    rag_output = gr.Textbox(
                        label="RAG Response",
                        lines=12,
                        interactive=False
                    )
            
            rag_btn.click(
                fn=test_rag_chain,
                inputs=rag_question,
                outputs=rag_output
            )
        
        # Examples
        with gr.Tab("📝 Examples"):
            gr.Markdown("""
            ## Example Questions to Test:
            
            **Basic Chat:**
            - "What is artificial intelligence?"
            - "Explain machine learning in simple terms"
            
            **Document Retrieval:**
            - "AI and machine learning"
            - "neural networks"
            - "computer vision"
            
            **RAG Chain:**
            - "What is the difference between AI, machine learning, and deep learning?"
            - "How does natural language processing work?"
            - "Explain the relationship between computer vision and AI"
            """)
    
    return demo

if __name__ == "__main__":
    demo = get_demo()
    demo.launch(server_port=8000, share=False)
