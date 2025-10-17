"""
Simplified LangServe Server for Final Assessment
Minimal implementation with working endpoints
"""

from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LangServe Assessment Server",
    version="1.0.0",
    description="Server for Final Assessment with RAG capabilities"
)

# Sample documents for RAG
sample_docs = [
    Document(page_content="Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans."),
    Document(page_content="Machine Learning is a subset of AI that focuses on algorithms that can learn from data."),
    Document(page_content="Deep Learning is a subset of machine learning that uses neural networks with multiple layers."),
    Document(page_content="Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language."),
    Document(page_content="Computer Vision is a field of AI that enables computers to interpret and understand visual information.")
]

# Simple LLM simulation
def simple_llm_response(input_data):
    """Simple LLM response simulation"""
    question = input_data.get("input", "") if isinstance(input_data, dict) else str(input_data)
    
    responses = {
        "hello": "Hello! I'm a simple AI assistant. How can I help you today?",
        "ai": "Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans.",
        "machine learning": "Machine Learning is a subset of AI that focuses on algorithms that can learn from data.",
        "deep learning": "Deep Learning is a subset of machine learning that uses neural networks with multiple layers.",
        "nlp": "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language.",
        "computer vision": "Computer Vision is a field of AI that enables computers to interpret and understand visual information."
    }
    
    question_lower = question.lower()
    for key, response in responses.items():
        if key in question_lower:
            return response
    
    return f"I received your question: '{question}'. This is a simulated AI response. In a real implementation, this would use a proper LLM model."

# Define chains
def basic_chat_chain():
    """Basic chat endpoint"""
    return RunnableLambda(simple_llm_response) | StrOutputParser()

def retriever_chain():
    """Retriever endpoint for RAG"""
    def retrieve_docs(input_data):
        query = input_data.get("input", "") if isinstance(input_data, dict) else str(input_data)
        query_lower = query.lower()
        
        # Simple keyword matching
        relevant_docs = []
        for doc in sample_docs:
            content_lower = doc.page_content.lower()
            if any(word in content_lower for word in query_lower.split()):
                relevant_docs.append(doc)
        
        # Return at least 2 documents
        if len(relevant_docs) < 2:
            relevant_docs = sample_docs[:2]
        
        return relevant_docs[:3]  # Return top 3
    
    return RunnableLambda(retrieve_docs)

def generator_chain():
    """Generator endpoint for RAG"""
    def generate_with_context(input_data):
        if isinstance(input_data, dict):
            question = input_data.get("input", "")
            context = input_data.get("context", "")
        else:
            question = str(input_data)
            context = ""
        
        if context:
            return f"Based on the context: '{context[:200]}...', here's my answer to '{question}': This is a simulated response that would use the provided context to generate a comprehensive answer."
        else:
            return simple_llm_response({"input": question})
    
    return RunnableLambda(generate_with_context) | StrOutputParser()

# Add routes
try:
    # Basic chat endpoint
    add_routes(app, basic_chat_chain(), path="/basic_chat")
    logger.info("Basic chat endpoint added")
    
    # Retriever endpoint
    add_routes(app, retriever_chain(), path="/retriever")
    logger.info("Retriever endpoint added")
    
    # Generator endpoint
    add_routes(app, generator_chain(), path="/generator")
    logger.info("Generator endpoint added")
    
except Exception as e:
    logger.error(f"Failed to add routes: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "LangServe Assessment Server is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LangServe Assessment Server",
        "endpoints": ["/basic_chat", "/retriever", "/generator", "/health"],
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Simplified LangServe Assessment Server on port 9012")
    uvicorn.run(app, host="0.0.0.0", port=9012)
