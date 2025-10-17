"""
Otimizações de Performance para o Chatbot
Estratégias para carregar outputs da IA mais rapidamente
"""

import streamlit as st
import asyncio
import time
from typing import Dict, Any
import threading
from concurrent.futures import ThreadPoolExecutor

# Cache para respostas da IA
@st.cache_data(ttl=600)  # Cache por 10 minutos
def cache_ai_response(prompt_hash: str, context_hash: str) -> str:
    """Cache para respostas da IA baseado no hash da pergunta e contexto"""
    return None

def get_prompt_hash(prompt: str, context: str) -> str:
    """Gera hash único para prompt e contexto"""
    import hashlib
    combined = f"{prompt}_{context}"
    return hashlib.md5(combined.encode()).hexdigest()

def optimize_ai_response_generation():
    """Otimizações para geração de respostas da IA"""
    
    # Configurações otimizadas
    optimized_config = {
        "temperature": 0.7,
        "max_tokens": 512,  # Reduzido para respostas mais rápidas
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    
    return optimized_config

def generate_response_streaming(prompt: str, context: str = "", chat_history: list = None):
    """Gera resposta da IA com streaming para melhor UX"""
    
    # Verificar cache primeiro
    prompt_hash = get_prompt_hash(prompt, context)
    cached_response = cache_ai_response(prompt_hash, context)
    
    if cached_response:
        return cached_response
    
    # Configurações otimizadas
    config = optimize_ai_response_generation()
    
    # Simular streaming (se a API suportar)
    try:
        # Aqui você implementaria o streaming real da API
        # Por enquanto, vamos simular com chunks
        response_chunks = []
        
        # Primeiro chunk rápido
        response_chunks.append("🤖 **Resposta da IA:**\n\n")
        
        # Simular processamento em chunks
        full_response = f"Baseado na sua pergunta: '{prompt}'\n\n"
        if context:
            full_response += f"Considerando o contexto fornecido, aqui está minha resposta:\n\n"
        
        # Dividir resposta em chunks para simular streaming
        chunk_size = 50
        words = full_response.split()
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            response_chunks.append(chunk)
            time.sleep(0.1)  # Simular delay de rede
        
        return "".join(response_chunks)
        
    except Exception as e:
        return f"❌ Erro na geração de resposta: {str(e)}"

def optimize_document_processing():
    """Otimizações para processamento de documentos"""
    
    # Configurações otimizadas
    optimized_settings = {
        "chunk_size": 1000,  # Chunks menores para processamento mais rápido
        "chunk_overlap": 100,
        "max_file_size": 10 * 1024 * 1024,  # 10MB máximo
        "parallel_processing": True,
        "cache_processed_docs": True
    }
    
    return optimized_settings

def optimize_image_processing():
    """Otimizações para processamento de imagens"""
    
    # Configurações otimizadas
    optimized_settings = {
        "max_image_size": (1024, 1024),  # Redimensionar imagens grandes
        "compression_quality": 85,
        "parallel_ocr": True,
        "cache_ocr_results": True,
        "skip_duplicate_images": True
    }
    
    return optimized_settings

def create_loading_animation():
    """Cria animação de loading mais eficiente"""
    
    loading_styles = """
    <style>
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        color: #666;
        font-style: italic;
        margin-left: 10px;
    }
    </style>
    """
    
    return loading_styles

def show_optimized_loading(message: str = "Processando..."):
    """Mostra loading otimizado"""
    
    loading_html = f"""
    <div style="display: flex; align-items: center; padding: 10px;">
        <div class="loading-spinner"></div>
        <span class="loading-text">{message}</span>
    </div>
    """
    
    return loading_html

def optimize_session_management():
    """Otimizações para gerenciamento de sessão"""
    
    # Limpar dados desnecessários periodicamente
    if "last_cleanup" not in st.session_state:
        st.session_state.last_cleanup = time.time()
    
    # Limpeza a cada 5 minutos
    if time.time() - st.session_state.last_cleanup > 300:
        cleanup_session_data()
        st.session_state.last_cleanup = time.time()

def cleanup_session_data():
    """Limpa dados desnecessários da sessão"""
    
    # Limitar histórico de mensagens
    if "messages" in st.session_state and len(st.session_state.messages) > 50:
        st.session_state.messages = st.session_state.messages[-30:]  # Manter apenas últimas 30
    
    # Limpar cache antigo
    if "document_cache" in st.session_state:
        # Manter apenas cache dos últimos 10 documentos
        if len(st.session_state.document_cache) > 10:
            st.session_state.document_cache = list(st.session_state.document_cache.items())[-10:]

def create_fast_clear_button():
    """Cria botão de limpeza rápida"""
    
    if st.button("🗑️ Limpar Chat", key="fast_clear", type="primary"):
        # Limpeza instantânea
        st.session_state.messages = []
        st.session_state.uploaded_docs = []
        st.session_state.uploaded_images = []
        st.session_state.document_context = ""
        st.session_state.image_text_context = ""
        
        # Forçar rerun imediato
        st.rerun()

def optimize_ui_rendering():
    """Otimizações para renderização da UI"""
    
    # CSS otimizado
    optimized_css = """
    <style>
    /* Otimizações de performance */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Reduzir animações para melhor performance */
    * {
        animation-duration: 0.1s !important;
        transition-duration: 0.1s !important;
    }
    
    /* Otimizar scroll */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Loading otimizado */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    </style>
    """
    
    st.markdown(optimized_css, unsafe_allow_html=True)

def implement_response_caching():
    """Implementa cache de respostas para melhor performance"""
    
    if "response_cache" not in st.session_state:
        st.session_state.response_cache = {}
    
    # Limitar tamanho do cache
    if len(st.session_state.response_cache) > 100:
        # Manter apenas as 50 respostas mais recentes
        st.session_state.response_cache = dict(list(st.session_state.response_cache.items())[-50:])

def get_cached_response(prompt: str, context: str) -> str:
    """Obtém resposta do cache se disponível"""
    
    cache_key = f"{prompt}_{context}"
    return st.session_state.response_cache.get(cache_key)

def cache_response(prompt: str, context: str, response: str):
    """Armazena resposta no cache"""
    
    cache_key = f"{prompt}_{context}"
    st.session_state.response_cache[cache_key] = response

# Função principal de otimização
def apply_all_optimizations():
    """Aplica todas as otimizações"""
    
    # Otimizar UI
    optimize_ui_rendering()
    
    # Otimizar sessão
    optimize_session_management()
    
    # Implementar cache
    implement_response_caching()
    
    # Mostrar loading otimizado
    st.markdown(create_loading_animation(), unsafe_allow_html=True)
