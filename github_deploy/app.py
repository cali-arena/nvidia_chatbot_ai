import streamlit as st
import os
from dotenv import load_dotenv
import requests
from PIL import Image
import io
import base64
from typing import List, Optional
import tempfile
import pandas as pd
import asyncio
import warnings
import logging

# Suprimir warnings e logs desnecessários
warnings.filterwarnings("ignore")
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger("chromadb").setLevel(logging.ERROR)
logging.getLogger("langchain").setLevel(logging.ERROR)

# LangChain imports
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Document processing imports
from PyPDF2 import PdfReader
from docx import Document

# RAG System imports
try:
    from rag_system import AdvancedRAGSystem, RAGConfig
    RAG_AVAILABLE = True
except ImportError as e:
    st.warning(f"RAG system not available: {e}")
    RAG_AVAILABLE = False

# Free vision processing
import tempfile
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="NVIDIA AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI and hide 200MB text
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: white;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.assistant {
        background-color: #1e2130;
    }
    .chat-message .message {
        color: #ffffff;
        font-size: 1rem;
        line-height: 1.5;
    }
    .stButton > button {
        background-color: #76b900;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #5a8f00;
    }
    .upload-section {
        background-color: #1e2130;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Hide 200MB text from file uploaders */
    .stFileUploader > div > div > div > div > div {
        display: none !important;
    }
    
    /* Hide any element containing 200MB text */
    *:contains("200MB") {
        display: none !important;
    }
    
    /* Hide any element containing "MB per file" text */
    *:contains("MB per file") {
        display: none !important;
    }
    
    /* Hide any element containing "Limit" text */
    *:contains("Limit") {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []

if "document_context" not in st.session_state:
    st.session_state.document_context = ""

if "image_text_context" not in st.session_state:
    st.session_state.image_text_context = ""

if "image_context" not in st.session_state:
    st.session_state.image_context = []

if "api_key" not in st.session_state:
    # API key pré-configurada para o usuário
    st.session_state.api_key = "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"

# Initialize RAG system
if RAG_AVAILABLE and "rag_system" not in st.session_state:
    try:
        # Configure RAG for large files (up to 2GB)
        rag_config = RAGConfig(
            chunk_size=1000,
            chunk_overlap=200,
            max_file_size_gb=2.0,
            embedding_model="nvidia/parakeet-tdt-0.6b-v2",
            vector_store_type="chroma",
            retrieval_k=5,
            similarity_threshold=0.7
        )
        st.session_state.rag_system = AdvancedRAGSystem(st.session_state.api_key, rag_config)
        st.session_state.rag_enabled = True
    except Exception as e:
        st.session_state.rag_system = None
        st.session_state.rag_enabled = False
        st.warning(f"RAG system initialization failed: {e}")
else:
    st.session_state.rag_enabled = False

def select_best_model_and_params(user_input=""):
    """Automatically select the best model and parameters based on input type"""
    
    # Analyze input to determine best settings
    if any(word in user_input.lower() for word in ['image', 'photo', 'picture', 'ocr', 'text']):
        # For image-related queries - use most capable model
        return {
            "model": "meta/llama-3.1-405b-instruct",
            "temperature": 0.3,
            "max_tokens": 800,
            "system_prompt": "You are a helpful AI assistant that analyzes text extracted from images. Provide intelligent, conversational analysis and insights about the content."
        }
    elif any(word in user_input.lower() for word in ['financial', 'money', 'price', 'cost', 'budget', 'table']):
        # For financial data - use balanced model with lower temperature
        return {
            "model": "meta/llama-3.1-70b-instruct", 
            "temperature": 0.1,
            "max_tokens": 600,
            "system_prompt": "You are a financial analysis assistant. Analyze financial data, tables, and documents with precision. Focus on accuracy and clear explanations."
        }
    elif any(word in user_input.lower() for word in ['creative', 'write', 'story', 'poem', 'essay']):
        # For creative tasks - use balanced model with higher temperature
        return {
            "model": "meta/llama-3.1-70b-instruct",
            "temperature": 0.8,
            "max_tokens": 1200,
            "system_prompt": "You are a creative writing assistant. Help with stories, poems, essays, and creative content. Be imaginative and engaging."
        }
    elif len(user_input) > 200:
        # For long/complex queries - use most capable model
        return {
            "model": "meta/llama-3.1-405b-instruct",
            "temperature": 0.5,
            "max_tokens": 1500,
            "system_prompt": "You are a comprehensive AI assistant. Handle complex queries with detailed, well-structured responses."
        }
    else:
        # Default for general queries - use fast model
        return {
            "model": "meta/llama-3.1-8b-instruct",
            "temperature": 0.7,
            "max_tokens": 800,
            "system_prompt": "You are a helpful AI assistant. Provide clear, accurate, and conversational responses."
        }

# Helper functions
def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting DOCX text: {str(e)}"

def extract_text_from_txt(file) -> str:
    """Extract text from TXT file"""
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        return f"Error reading TXT file: {str(e)}"

def process_document(file) -> str:
    """Process uploaded document and extract text"""
    file_type = file.name.split(".")[-1].lower()
    
    if file_type == "pdf":
        return extract_text_from_pdf(file)
    elif file_type == "docx":
        return extract_text_from_docx(file)
    elif file_type == "txt":
        return extract_text_from_txt(file)
    else:
        return "Unsupported file type"

def encode_image_to_base64(image_file) -> str:
    """Encode image to base64 string"""
    try:
        image = Image.open(image_file)
        # Convert RGBA to RGB if necessary (remove transparency)
        if image.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        return f"Error encoding image: {str(e)}"

def extract_text_easyocr(image_file) -> str:
    """Extract text using EasyOCR (OTIMIZADO - sem loading messages)"""
    try:
        import easyocr
        
        # Initialize reader (only once) - SEM SPINNER
        if 'easyocr_reader' not in st.session_state:
            st.session_state.easyocr_reader = easyocr.Reader(['en', 'pt'], gpu=False)
        
        # Process image directly without saving to temp file
        image = Image.open(image_file)
        # Convert RGBA to RGB if necessary (remove transparency)
        if image.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert PIL image to numpy array for EasyOCR
        import numpy as np
        image_array = np.array(image)
        
        # Extract text directly from image array
        results = st.session_state.easyocr_reader.readtext(image_array)
        
        # Format results
        extracted_text = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # Only high-confidence text
                extracted_text.append(text)
        
        return "\n".join(extracted_text) if extracted_text else "No clear text detected"
            
    except ImportError:
        return "❌ EasyOCR not installed. Run: pip install easyocr"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def orchestrate_rag_chat_integration(user_message: str, context: str = "") -> dict:
    """Intelligent orchestration between RAG system and Chat for optimal responses"""
    try:
        result = {
            "success": False,
            "response": "",
            "method": "",
            "confidence": 0.0,
            "sources": 0
        }
        
        # Check if RAG is available and has documents
        rag_available = st.session_state.rag_enabled and st.session_state.rag_system
        has_docs = False
        
        if rag_available:
            try:
                stats = st.session_state.rag_system.get_system_stats()
                has_docs = stats.get("total_documents", 0) > 0
            except:
                has_docs = False
        
        # Strategy 1: Direct RAG Query (when documents available)
        if rag_available and has_docs:
            try:
                # Create enhanced query for RAG
                enhanced_query = f"""
Pergunta do usuário: {user_message}

CONTEXTO ADICIONAL DISPONÍVEL:
{context}

INSTRUÇÕES:
- Busque informações relevantes nos documentos processados
- Combine com o contexto adicional fornecido
- Forneça resposta completa e precisa
- Use informações específicas dos documentos quando disponível
"""
                
                rag_result = asyncio.run(st.session_state.rag_system.query(enhanced_query, use_memory=True))
                
                if rag_result["confidence"] > 0.15:  # Very low threshold for better coverage
                    result.update({
                        "success": True,
                        "response": rag_result["answer"],
                        "method": "RAG_DIRECT",
                        "confidence": rag_result["confidence"],
                        "sources": len(rag_result.get("source_documents", []))
                    })
                    return result
                    
            except Exception as e:
                print(f"RAG query failed: {e}")
        
        # Strategy 2: Enhanced Chat with Full Context
        result.update({
            "success": True,
            "response": "ENHANCED_CHAT",
            "method": "ENHANCED_CHAT",
            "confidence": 1.0,
            "sources": 0
        })
        return result
        
    except Exception as e:
        print(f"Orchestration failed: {e}")
        result["response"] = f"Error in orchestration: {e}"
        return result

def analyze_image_with_ai(image_file, ocr_text=None) -> str:
    """Analyze image using NVIDIA AI vision capabilities"""
    try:
        # If OCR text is provided, analyze it directly
        if ocr_text:
            prompt = f"""Analise este texto extraído de uma imagem via OCR e forneça uma análise inteligente e humanizada:

{ocr_text}

Por favor, explique o que significa este conteúdo, organize as informações de forma clara, e forneça insights úteis sobre o que foi encontrado na imagem. Seja conversacional e útil na sua análise."""
            
            # Get optimal configuration for image analysis
            config = select_best_model_and_params("image analysis")
            
            # Initialize AI model with optimal parameters
            llm = ChatNVIDIA(
                model=config["model"],
                temperature=config["temperature"],
                max_completion_tokens=config["max_tokens"],
                nvidia_api_key=st.session_state.api_key
            )
            
            # Create message for text analysis
            messages = [
                SystemMessage(content="You are a helpful AI assistant that analyzes text extracted from images. Provide intelligent, conversational analysis and insights about the content."),
                HumanMessage(content=prompt)
            ]
            
            # Get AI response
            response = llm.invoke(messages)
            return response.content.strip()
        
        # Original image analysis (fallback)
        # Encode image for AI analysis
        encoded_image = encode_image_to_base64(image_file)
        if encoded_image and not encoded_image.startswith("Error"):
            
            # Create AI prompt for image analysis
            prompt = """Please analyze this image and extract ALL text content in a clean, readable format. 

For tables or financial data:
- List each row clearly
- Separate values with proper formatting
- Include all numbers and labels

For documents:
- Transcribe text line by line
- Preserve formatting and structure
- Include all visible text

Provide only the extracted text content, formatted for easy reading. Do not include any technical details or image descriptions."""

            # Initialize AI model
            llm = ChatNVIDIA(
                model="meta/llama-3.1-405b-instruct",  # Use most capable model for vision
                temperature=0.1,  # Low temperature for accurate text extraction
                max_completion_tokens=1000,
                nvidia_api_key=st.session_state.api_key
            )
            
            # Create multimodal message
            messages = [
                SystemMessage(content="You are a professional document scanner and text extraction specialist. Your job is to read images and extract text content in a clean, human-readable format. Focus only on transcribing visible text accurately."),
                HumanMessage(content=[
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ])
            ]
            
            # Get AI response
            response = llm.invoke(messages)
            extracted_text = response.content.strip()
            
            # Clean up the response to ensure it's human-readable
            if len(extracted_text) > 50 and not extracted_text.startswith("IVfIXWG") and not extracted_text.startswith("/9j/"):
                return extracted_text
            else:
                return "Text extraction completed. The AI has analyzed the image and can answer questions about its content."
            
        else:
            return "Error: Could not process image"
            
    except Exception as e:
        return f"Analysis error: {str(e)}"

def get_chat_response(user_message: str, chat_history: List, context: str = "", images: List = None) -> str:
    """Get response from NVIDIA AI model with intelligent RAG orchestration"""
    try:
        if not st.session_state.api_key:
            return "⚠️ API key not configured."
        
        # INTELLIGENT ORCHESTRATION - Use the new orchestration function
        orchestration_result = orchestrate_rag_chat_integration(user_message, context)
        
        # If RAG provided a good response, use it
        if orchestration_result["success"] and orchestration_result["method"] == "RAG_DIRECT":
            response_parts = []
            response_parts.append(f"🤖 **Análise Inteligente Baseada em Documentos**")
            response_parts.append(f"**Confiança:** {orchestration_result['confidence']:.2f}")
            response_parts.append("")
            response_parts.append(orchestration_result["response"])
            
            if orchestration_result["sources"] > 0:
                response_parts.append(f"\n📚 **Fontes Consultadas:** {orchestration_result['sources']} documentos relevantes")
            
            return "\n".join(response_parts)
        
        # ENHANCED CONTEXT PROCESSING (Fallback or complementary)
        # Auto-select best model and parameters based on input
        config = select_best_model_and_params(user_message)
        
        # Initialize the chat model with auto-selected parameters
        llm = ChatNVIDIA(
            model=config["model"],
            temperature=config["temperature"],
            max_completion_tokens=config["max_tokens"],
            nvidia_api_key=st.session_state.api_key
        )
        
        # Build enhanced system prompt with RAG awareness
        enhanced_system_prompt = config["system_prompt"]
        
        # Check if we have documents processed
        rag_available = st.session_state.rag_enabled and st.session_state.rag_system
        has_docs = False
        if rag_available:
            try:
                stats = st.session_state.rag_system.get_system_stats()
                has_docs = stats.get("total_documents", 0) > 0
            except:
                has_docs = False
        
        # Add RAG context if available
        if rag_available and has_docs:
            enhanced_system_prompt += f"""

🤖 SISTEMA RAG ATIVO:
- Documentos processados e disponíveis para consulta
- Resumos automáticos gerados e integrados
- Use as informações dos documentos para responder perguntas
- Priorize informações dos documentos quando relevante"""
        
        messages = [SystemMessage(content=enhanced_system_prompt)]
        
        # Add context from documents if available
        if context:
            context_prompt = f"""📄 CONTEXTO DE DOCUMENTOS E ANÁLISES CARREGADOS:

{context}

🎯 INSTRUÇÕES CRÍTICAS:
- Use as informações acima para responder perguntas sobre os documentos carregados
- Base suas respostas nos resumos e análises automáticas fornecidos
- Seja preciso e contextualizado em suas respostas
- Cite informações específicas quando relevante
- Se perguntado sobre conteúdo dos documentos, use PRIMEIRO as informações do contexto acima"""
            
            messages.append(SystemMessage(content=context_prompt))
        
        # Add chat history
        for msg in chat_history[-10:]:  # Keep last 10 messages for context
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # Handle images if provided
        if images and len(images) > 0:
            # Create content list for multimodal message
            content = [{"type": "text", "text": user_message}]
            
            # Add images to content
            for image in images:
                if isinstance(image, str):  # Base64 encoded image
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                    })
            
            messages.append(HumanMessage(content=content))
        else:
            messages.append(HumanMessage(content=user_message))
        
        # Get response
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key and try again."

# Main app - UPDATED VERSION
st.title("🤖 NVIDIA AI Chatbot with Advanced RAG System - TEST VERSION")

# Chat input - MOVED TO TOP
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Simple response for testing - FORCE UPDATE
                response = f"🎯 TEST SUCCESS! You asked: {prompt}. This is a test response to make sure the chat works. Version: {hash(prompt) % 1000}"
                st.markdown(response)
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                response = "I apologize, but I encountered an error. Please try again."
                st.markdown(response)
    
    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat messages
st.divider()
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Initialize variables for context
document_context = ""
image_text_context = ""
image_context = []
uploaded_files = []
uploaded_images = []

# Upload sections integrated below chat input - more beautiful and integrated
st.markdown("---")

# Create a beautiful upload area that looks integrated with chat
with st.container():
    # Beautiful upload section with better visual integration
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 1rem; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h4 style='margin: 0 0 1rem 0; color: white; text-align: center; font-size: 1.1rem;'>📎 Anexar arquivos para análise inteligente</h4>
        <p style='margin: 0; color: rgba(255,255,255,0.9); text-align: center; font-size: 0.9rem;'>Upload documentos e imagens para análise automática com IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border: 2px dashed #dee2e6; margin: 0.5rem 0;'>
            <h5 style='margin: 0 0 0.5rem 0; color: #495057;'>📄 Documentos</h5>
            <p style='margin: 0; color: #6c757d; font-size: 0.85rem;'>PDF, TXT, DOCX - Até 2GB</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "📄 Documentos",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            key="doc_uploader",
            label_visibility="collapsed",
            help="PDF, TXT, DOCX - Limite: 2GB"
        )
    
    with col2:
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border: 2px dashed #dee2e6; margin: 0.5rem 0;'>
            <h5 style='margin: 0 0 0.5rem 0; color: #495057;'>🖼️ Imagens</h5>
            <p style='margin: 0; color: #6c757d; font-size: 0.85rem;'>PNG, JPG, JPEG - Até 2GB</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_images = st.file_uploader(
            "🖼️ Imagens",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="image_uploader",
            label_visibility="collapsed",
            help="PNG, JPG, JPEG - Limite: 2GB"
        )

# Process uploaded documents with RAG system - moved below uploads for better flow
document_context = ""

# Initialize document context in session state if not exists
if "document_context" not in st.session_state:
    st.session_state.document_context = ""

if uploaded_files:
    # Show processing status in a more integrated way
    st.markdown("**📄 Processando Documentos:**")
    with st.container():
        for file in uploaded_files:
            st.write(f"**{file.name}** ({file.size / 1024:.2f} KB)")
            
            if st.session_state.rag_enabled:
                # Use RAG system for large file processing
                with st.spinner(f"Processing {file.name} with RAG system..."):
                    try:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                            tmp_file.write(file.getvalue())
                            tmp_path = tmp_file.name
                        
                        # Process with RAG system
                        file_type = file.name.split('.')[-1].lower()
                        result = asyncio.run(st.session_state.rag_system.process_file(tmp_path, file_type))
                        
                        if result["status"] == "success":
                            st.success(f"✅ Processed {file.name} - {result['chunks']} chunks added to RAG system")
                            document_context += f"\n\n--- RAG Content from {file.name} ({result['chunks']} chunks) ---\n"
                            # Update session state
                            st.session_state.document_context += document_context
                            
                            # Gerar resumo automático do documento
                            with st.spinner(f"🤖 Gerando resumo automático de {file.name}..."):
                                try:
                                    # Fazer uma consulta RAG para gerar resumo
                                    summary_query = f"Faça um resumo detalhado e análise completa do documento {file.name}. Inclua os pontos principais, conceitos importantes, dados relevantes e insights sobre o conteúdo."
                                    
                                    # Use async wrapper for RAG query
                                    import asyncio
                                    summary_result = asyncio.run(st.session_state.rag_system.query(summary_query, use_memory=False))
                                    
                                    if summary_result["confidence"] > 0.3:
                                        # Adicionar resumo ao contexto do documento
                                        summary_text = f"\n\n--- RESUMO AUTOMÁTICO {file.name} ---\n{summary_result['answer']}\n\n--- CONSIDERAÇÕES PARA RESPOSTAS ---\nBase suas respostas neste resumo quando perguntado sobre {file.name}. Use as informações extraídas para fornecer respostas precisas e contextualizadas."
                                        document_context += summary_text
                                        st.session_state.document_context += summary_text
                                        st.success(f"📝 Resumo automático adicionado ao contexto para {file.name}")
                                        
                                        # AUTOMATICALLY ADD SUMMARY TO CHAT
                                        summary_chat_message = f"🤖 **Resumo Automático de {file.name}**\n\n{summary_result['answer']}"
                                        st.session_state.messages.append({"role": "assistant", "content": summary_chat_message})
                                        
                                        # Display the summary in chat immediately
                                        with st.chat_message("assistant"):
                                            st.markdown(summary_chat_message)
                                    else:
                                        # Fallback: generate summary using regular chat
                                        st.info(f"🔄 RAG resumo com baixa confiança, usando IA regular...")
                                        summary_prompt = f"""Analise o documento {file.name} que foi processado pelo sistema RAG e forneça um resumo detalhado e análise completa.

Por favor, forneça:
1. Resumo executivo dos pontos principais
2. Conceitos e temas centrais identificados
3. Dados e informações importantes
4. Insights e conclusões relevantes
5. Contexto e aplicações práticas

Seja detalhado e organizado na sua análise."""
                                        
                                        summary_response = get_chat_response(
                                            user_message=summary_prompt,
                                            chat_history=[],
                                            context=document_context,
                                            images=None
                                        )
                                        
                                        summary_text = f"\n\n--- RESUMO AUTOMÁTICO {file.name} ---\n{summary_response}\n\n--- CONSIDERAÇÕES PARA RESPOSTAS ---\nBase suas respostas neste resumo quando perguntado sobre {file.name}. Use as informações extraídas para fornecer respostas precisas e contextualizadas."
                                        document_context += summary_text
                                        st.session_state.document_context += summary_text
                                        st.success(f"📝 Resumo automático gerado e adicionado ao contexto para {file.name}")
                                        
                                        # AUTOMATICALLY ADD SUMMARY TO CHAT
                                        summary_chat_message = f"🤖 **Resumo Automático de {file.name}**\n\n{summary_response}"
                                        st.session_state.messages.append({"role": "assistant", "content": summary_chat_message})
                                        
                                        # Display the summary in chat immediately
                                        with st.chat_message("assistant"):
                                            st.markdown(summary_chat_message)
                                except Exception as e:
                                    st.warning(f"⚠️ Erro ao gerar resumo com RAG: {str(e)}")
                                    # Fallback: generate summary using regular chat
                                    try:
                                        st.info(f"🔄 Tentando gerar resumo com IA regular...")
                                        summary_prompt = f"""Analise o documento {file.name} e forneça um resumo detalhado:

Por favor, forneça:
1. Resumo executivo dos pontos principais
2. Conceitos e temas centrais
3. Dados e informações importantes
4. Insights e conclusões relevantes

Seja detalhado e organizado na sua análise."""

                                        summary_response = get_chat_response(
                                            user_message=summary_prompt,
                                            chat_history=[],
                                            context=document_context,
                                            images=None
                                        )
                                        
                                        summary_text = f"\n\n--- RESUMO AUTOMÁTICO {file.name} ---\n{summary_response}\n\n--- CONSIDERAÇÕES PARA RESPOSTAS ---\nBase suas respostas neste resumo quando perguntado sobre {file.name}. Use as informações extraídas para fornecer respostas precisas e contextualizadas."
                                        document_context += summary_text
                                        st.session_state.document_context += summary_text
                                        st.success(f"📝 Resumo automático gerado e adicionado ao contexto para {file.name}")
                                        
                                        # AUTOMATICALLY ADD SUMMARY TO CHAT
                                        summary_chat_message = f"🤖 **Resumo Automático de {file.name}**\n\n{summary_response}"
                                        st.session_state.messages.append({"role": "assistant", "content": summary_chat_message})
                                        
                                        # Display the summary in chat immediately
                                        with st.chat_message("assistant"):
                                            st.markdown(summary_chat_message)
                                    except Exception as e2:
                                        st.warning(f"⚠️ Erro ao gerar resumo: {str(e2)}")
                        else:
                            st.warning(f"⚠️ {result['message']}")
                            # Fallback to regular processing
                            text_content = process_document(file)
                            document_context += f"\n\n--- Content from {file.name} ---\n{text_content}\n"
                        
                        # Clean up temp file
                        os.unlink(tmp_path)
                        
                    except Exception as e:
                        st.error(f"❌ RAG processing failed: {e}")
                        # Fallback to regular processing
                        text_content = process_document(file)
                        document_context += f"\n\n--- Content from {file.name} ---\n{text_content}\n"
            else:
                # Regular processing without RAG
                with st.spinner(f"Processing {file.name}..."):
                    text_content = process_document(file)
                    document_context += f"\n\n--- Content from {file.name} ---\n{text_content}\n"
                    st.success(f"✅ Processed {file.name}")
                    
                    # Gerar resumo com IA regular
                    with st.spinner(f"🤖 Gerando resumo automático de {file.name}..."):
                        try:
                            # Usar IA regular para gerar resumo
                            summary_prompt = f"""Analise o seguinte conteúdo do documento {file.name} e forneça um resumo detalhado e análise completa:

{text_content[:3000]}

Por favor, forneça:
1. Resumo executivo dos pontos principais
2. Conceitos e temas centrais identificados
3. Dados e informações importantes
4. Insights e conclusões relevantes
5. Contexto e aplicações práticas

Seja detalhado e organizado na sua análise. Foque em extrair os insights mais importantes do documento."""

                            # Usar função de chat regular para resumo
                            summary_response = get_chat_response(
                                user_message=summary_prompt,
                                chat_history=[],
                                context="",
                                images=None
                            )
                            
                            # Adicionar resumo ao contexto do documento
                            summary_text = f"\n\n--- RESUMO AUTOMÁTICO {file.name} ---\n{summary_response}\n\n--- CONSIDERAÇÕES PARA RESPOSTAS ---\nBase suas respostas neste resumo quando perguntado sobre {file.name}. Use as informações extraídas para fornecer respostas precisas e contextualizadas."
                            document_context += summary_text
                            st.session_state.document_context += summary_text
                            st.success(f"📝 Resumo automático gerado e adicionado ao contexto para {file.name}")
                            
                            # AUTOMATICALLY ADD SUMMARY TO CHAT
                            summary_chat_message = f"🤖 **Resumo Automático de {file.name}**\n\n{summary_response}"
                            st.session_state.messages.append({"role": "assistant", "content": summary_chat_message})
                            
                            # Display the summary in chat immediately
                            with st.chat_message("assistant"):
                                st.markdown(summary_chat_message)
                        except Exception as e:
                            st.warning(f"⚠️ Erro ao gerar resumo: {str(e)}")
                            # Adicionar conteúdo básico mesmo sem resumo
                            document_context += f"\n\n--- RESUMO AUTOMÁTICO {file.name} ---\nDocumento processado com sucesso. Conteúdo disponível para consultas.\n\n--- CONSIDERAÇÕES PARA RESPOSTAS ---\nBase suas respostas no conteúdo do documento {file.name} quando perguntado sobre ele."
                            st.info(f"📄 Documento {file.name} processado (resumo não pôde ser gerado)")

# Process uploaded images - moved below uploads for better flow
image_context = []
image_text_context = ""

# Initialize image context in session state if not exists
if "image_text_context" not in st.session_state:
    st.session_state.image_text_context = ""

if uploaded_images:
    # Show processing status in a more integrated way
    st.markdown("**🖼️ Processando Imagens:**")
    with st.container():
        cols = st.columns(3)
        for idx, image_file in enumerate(uploaded_images):
            with cols[idx % 3]:
                image = Image.open(image_file)
                st.image(image, caption=image_file.name, use_container_width=True)
                
                # Store image for chat context
                image_context.append(encode_image_to_base64(image_file))
                
                # Extract text using EasyOCR
                ocr_text = extract_text_easyocr(image_file)
                
                if ocr_text and ocr_text != "No clear text detected":
                    try:
                        # Analyze with AI
                        analysis_prompt = f"""Analise este texto extraído de uma imagem e forneça uma análise inteligente e humanizada:

{ocr_text}

Por favor, forneça:
1. Resumo do conteúdo textual
2. Análise do conteúdo textual
3. Contexto e significado
4. Insights e observações relevantes
5. Possíveis aplicações ou interpretações

Seja detalhado e forneça insights úteis sobre a imagem."""

                        ai_analysis = get_chat_response(
                            user_message=analysis_prompt,
                            chat_history=[],
                            context="",
                            images=None
                        )
                        
                        # Store analysis for chat context
                        image_text_context += f"\n\n--- ANÁLISE AUTOMÁTICA {image_file.name} ---\nText from {image_file.name} (OCR):\n{ocr_text}\n\nAI Analysis:\n{ai_analysis}\n\n--- CONSIDERAÇÕES PARA RESPOSTAS ---\nBase suas respostas nesta análise quando perguntado sobre {image_file.name}. Use as informações extraídas para fornecer respostas precisas e contextualizadas."
                        st.session_state.image_text_context += image_text_context
                        st.success(f"📝 Análise automática gerada e adicionada ao contexto para {image_file.name}")
                        
                        # AUTOMATICALLY ADD IMAGE ANALYSIS TO CHAT
                        analysis_chat_message = f"🖼️ **Análise Automática de {image_file.name}**\n\n**Texto extraído (OCR):**\n{ocr_text}\n\n**Análise IA:**\n{ai_analysis}"
                        st.session_state.messages.append({"role": "assistant", "content": analysis_chat_message})
                        
                        # Display the analysis in chat immediately
                        with st.chat_message("assistant"):
                            st.markdown(analysis_chat_message)
                    except Exception as e:
                        # Fallback: just store OCR text
                        image_text_context += f"\n\nText from {image_file.name}:\n{ocr_text}"
                        st.warning(f"⚠️ Análise IA falhou: {str(e)}, mas texto OCR está disponível para chat")
                else:
                    # Try to analyze image without OCR text
                    try:
                        st.info("🔄 Tentando análise visual direta...")
                        analysis_prompt = f"""Analise a imagem {image_file.name} visualmente e forneça uma análise detalhada:

Por favor, forneça:
1. Descrição visual detalhada
2. Elementos identificados na imagem
3. Contexto e significado possível
4. Insights e observações relevantes

Seja detalhado na sua análise visual."""

                        encoded_image = encode_image_to_base64(image_file)
                        ai_analysis = get_chat_response(
                            user_message=analysis_prompt,
                            chat_history=[],
                            context="",
                            images=[encoded_image]  # Pass the image directly
                        )
                        
                        # Store analysis for chat context
                        image_text_context += f"\n\n--- ANÁLISE AUTOMÁTICA {image_file.name} ---\nAnálise visual direta:\n{ai_analysis}\n\n--- CONSIDERAÇÕES PARA RESPOSTAS ---\nBase suas respostas nesta análise quando perguntado sobre {image_file.name}. Use as informações extraídas para fornecer respostas precisas e contextualizadas."
                        st.session_state.image_text_context += image_text_context
                        st.success(f"📝 Análise visual automática gerada e adicionada ao contexto para {image_file.name}")
                        
                        # AUTOMATICALLY ADD IMAGE ANALYSIS TO CHAT
                        analysis_chat_message = f"🖼️ **Análise Visual Automática de {image_file.name}**\n\n{ai_analysis}"
                        st.session_state.messages.append({"role": "assistant", "content": analysis_chat_message})
                        
                        # Display the analysis in chat immediately
                        with st.chat_message("assistant"):
                            st.markdown(analysis_chat_message)
                    except Exception as e2:
                        st.error(f"❌ Falha na análise: {str(e2)}")
                        image_text_context += f"\n\n--- IMAGEM {image_file.name} ---\nImagem processada e disponível para análise visual no chat."

# Clear chat button - moved to be closer to uploads and processing
if st.button("🗑️ Limpar Histórico do Chat", use_container_width=True):
    # Limpar mensagens do chat
    st.session_state.messages = []
    
    # Limpar documentos e imagens carregados
    st.session_state.uploaded_docs = []
    st.session_state.uploaded_images = []
    
    # Limpar contextos de documentos e imagens
    if "document_context" in st.session_state:
        st.session_state.document_context = ""
    if "image_text_context" in st.session_state:
        st.session_state.image_text_context = ""
    
    # Limpar variáveis locais também
    uploaded_files = []
    uploaded_images = []
    document_context = ""
    image_text_context = ""
    image_context = []
    
    # Mostrar confirmação
    st.success("✅ Chat, documentos e imagens limpos com sucesso!")
    
    # Forçar rerun para atualizar a interface
    st.rerun()

# Add authorship and credits below uploads
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <p style='font-size: 0.9rem; font-weight: bold; color: #4CAF50;'>🤖 IA desenvolvida por Lucas Cabral</p>
    <p style='font-size: 0.8rem; color: #666; margin-top: 0.5rem;'>Powered by <strong>NVIDIA AI Endpoints</strong> | Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
