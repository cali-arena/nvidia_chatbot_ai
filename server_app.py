"""
LangServe Server for Final Assessment
Endpoints: /basic_chat, /retriever, /generator
"""

from fastapi import FastAPI
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langserve import add_routes
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.vectorstores import FAISS
from langchain_community.document_transformers import LongContextReorder
from langchain_core.documents import Document
from langchain_core.runnables import RunnableAssign
from operator import itemgetter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize models - Use HuggingFace directly for better compatibility
try:
    from langchain_huggingface import HuggingFaceEmbeddings, ChatHuggingFace
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    instruct_llm = ChatHuggingFace.from_model_id(
        model_id="microsoft/DialoGPT-medium",
        task="text-generation",
        model_kwargs={"temperature": 0.7, "max_length": 512}
    )
    logger.info("HuggingFace models initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize HuggingFace models: {e}")
    # Try NVIDIA as fallback
    try:
        embedder = NVIDIAEmbeddings(model="nvidia/parakeet-tdt-0.6b-v2")
        instruct_llm = ChatNVIDIA(
            model="meta/llama3-8b-instruct",
            temperature=0.7,
            max_completion_tokens=512
        )
        logger.info("NVIDIA models initialized as fallback")
    except Exception as e2:
        logger.error(f"Failed to initialize NVIDIA models: {e2}")
        raise Exception("No models available")

# Create FastAPI app
app = FastAPI(
    title="LangServe Assessment Server",
    version="1.0.0",
    description="Server for Final Assessment with RAG capabilities"
)

# Helper functions
def docs2str(docs):
    """Convert documents to string"""
    return "\n\n".join([doc.page_content for doc in docs])

def output_puller(inputs):
    """Pull output from inputs"""
    return inputs["output"]

# Create sample documents for RAG
sample_docs = [
    Document(page_content="Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans."),
    Document(page_content="Machine Learning is a subset of AI that focuses on algorithms that can learn from data."),
    Document(page_content="Deep Learning is a subset of machine learning that uses neural networks with multiple layers."),
    Document(page_content="Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language."),
    Document(page_content="Computer Vision is a field of AI that enables computers to interpret and understand visual information.")
]

# Create vector store with HuggingFace embeddings
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    hf_embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(sample_docs, hf_embedder)
    logger.info("Vector store created successfully with HuggingFace embeddings")
except Exception as e:
    logger.error(f"Failed to create vector store: {e}")
    vectorstore = None

# Define chains
def basic_chat_chain():
    """Basic chat endpoint"""
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful AI assistant. Answer the following question: {question}"
    )
    return prompt | instruct_llm | StrOutputParser()

def retriever_chain():
    """Retriever endpoint for RAG"""
    def retrieve_docs(query):
        if vectorstore is None:
            return sample_docs[:2]  # Fallback
        try:
            docs = vectorstore.similarity_search(query, k=3)
            return docs
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return sample_docs[:2]
    
    return RunnableLambda(retrieve_docs)

def generator_chain():
    """Generator endpoint for RAG"""
    prompt = ChatPromptTemplate.from_template(
        """Based on the following context, answer the question:

Context: {context}

Question: {input}

Provide a comprehensive answer based on the context provided."""
    )
    return prompt | instruct_llm | StrOutputParser()

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
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting LangServe Assessment Server on port 9012")
    uvicorn.run(app, host="0.0.0.0", port=9012)
