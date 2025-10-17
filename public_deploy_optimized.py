"""
Deploy público do Chatbot com isolamento de sessões - VERSÃO OTIMIZADA
Configurado para múltiplos usuários simultâneos com performance melhorada
"""

import streamlit as st
import os
import uuid
from datetime import datetime, timedelta
import time
import asyncio
from security_config import (
    check_security_and_rate_limit, 
    display_security_info, 
    log_security_event,
    get_secure_user_id
)

# Configurações para deploy público
st.set_page_config(
    page_title="🤖 Chatbot IA - Lucas Cabral",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache para melhor performance
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_session_config():
    """Configurações de sessão para múltiplos usuários"""
    return {
        "max_session_duration": 3600,  # 1 hora
        "max_uploads_per_session": 10,
        "max_file_size_mb": 2048,  # 2GB
        "rate_limit_per_minute": 30
    }

def initialize_user_session():
    """Inicializa uma nova sessão de usuário isolada"""
    if "user_session_id" not in st.session_state:
        st.session_state.user_session_id = str(uuid.uuid4())
        st.session_state.session_start_time = datetime.now()
        st.session_state.user_uploads = []
        st.session_state.user_messages = []
        st.session_state.user_context = ""
        st.session_state.user_image_context = ""
        st.session_state.user_request_count = 0
        st.session_state.user_last_request_time = datetime.now()
        st.session_state.clear_chat_requested = False

def check_session_validity():
    """Verifica se a sessão ainda é válida"""
    config = get_session_config()
    session_duration = datetime.now() - st.session_state.session_start_time
    
    if session_duration.total_seconds() > config["max_session_duration"]:
        st.warning("⚠️ Sua sessão expirou. Por favor, recarregue a página para continuar.")
        return False
    
    return True

def clear_user_session_fast():
    """Limpa a sessão do usuário de forma rápida e eficiente"""
    # Limpar apenas os dados essenciais
    st.session_state.user_messages = []
    st.session_state.user_uploads = []
    st.session_state.user_context = ""
    st.session_state.user_image_context = ""
    st.session_state.user_request_count = 0
    st.session_state.clear_chat_requested = True
    
    # Log do evento
    log_security_event("SESSION_CLEARED_FAST", "User cleared session with fast method")
    
    # Forçar rerun imediato
    st.rerun()

def main():
    """Função principal com isolamento de sessões"""
    
    # Inicializar sessão do usuário
    initialize_user_session()
    
    # Verificar validade da sessão
    if not check_session_validity():
        return
    
    # Verificar se foi solicitada limpeza rápida
    if st.session_state.get("clear_chat_requested", False):
        st.session_state.clear_chat_requested = False
        st.success("✅ Chat limpo com sucesso!")
        time.sleep(0.5)  # Pequena pausa para mostrar a mensagem
    
    # Header público otimizado
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 1.5rem;'>
        <h1 style='color: white; margin: 0; font-size: 2.2rem;'>🤖 Chatbot IA Avançado</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.1rem;'>Desenvolvido por Lucas Cabral | Powered by NVIDIA AI</p>
        <p style='color: #e0e0e0; margin: 0.5rem 0 0 0; font-size: 0.8rem;'>Sessão: {}</p>
    </div>
    """.format(st.session_state.user_session_id[:8]), unsafe_allow_html=True)
    
    # Sidebar otimizada
    with st.sidebar:
        st.markdown("### 📊 Sua Sessão")
        st.info(f"**ID:** {st.session_state.user_session_id[:8]}...")
        
        # Métricas rápidas
        col1, col2 = st.columns(2)
        with col1:
            session_duration = datetime.now() - st.session_state.session_start_time
            st.metric("⏱️ Tempo", f"{int(session_duration.total_seconds()/60)}m")
        with col2:
            st.metric("📨 Reqs", st.session_state.user_request_count)
        
        st.metric("📁 Arquivos", len(st.session_state.user_uploads))
        
        st.markdown("---")
        
        # Exibir informações de segurança
        display_security_info()
        
        st.markdown("---")
        
        # Botão de limpeza rápida
        if st.button("🗑️ Limpar Chat", use_container_width=True, type="primary"):
            clear_user_session_fast()
        
        # Informações sobre privacidade (compactas)
        st.markdown("### 🔒 Privacidade")
        st.success("✅ Sessão isolada")
        st.warning("⚠️ Expira em 1h")
    
    # Importar e executar o app principal com contexto isolado
    try:
        # Importar funções do app principal
        from app import (
            get_chat_response, 
            extract_text_easyocr, 
            encode_image_to_base64,
            process_documents,
            initialize_rag_system
        )
        
        # Usar contexto isolado do usuário
        original_messages = st.session_state.get("messages", [])
        original_uploaded_docs = st.session_state.get("uploaded_docs", [])
        original_uploaded_images = st.session_state.get("uploaded_images", [])
        original_document_context = st.session_state.get("document_context", "")
        original_image_text_context = st.session_state.get("image_text_context", "")
        
        # Substituir por contexto do usuário
        st.session_state.messages = st.session_state.user_messages
        st.session_state.uploaded_docs = st.session_state.user_uploads
        st.session_state.uploaded_images = []
        st.session_state.document_context = st.session_state.user_context
        st.session_state.image_text_context = st.session_state.user_image_context
        
        # Executar interface principal otimizada
        run_optimized_interface()
        
        # Salvar contexto de volta
        st.session_state.user_messages = st.session_state.messages
        st.session_state.user_uploads = st.session_state.uploaded_docs
        st.session_state.user_context = st.session_state.document_context
        st.session_state.user_image_context = st.session_state.image_text_context
        
        # Restaurar contexto original
        st.session_state.messages = original_messages
        st.session_state.uploaded_docs = original_uploaded_docs
        st.session_state.uploaded_images = original_uploaded_images
        st.session_state.document_context = original_document_context
        st.session_state.image_text_context = original_image_text_context
        
    except Exception as e:
        st.error(f"Erro ao carregar o sistema: {str(e)}")
        st.info("Por favor, recarregue a página e tente novamente.")

def run_optimized_interface():
    """Executa a interface principal otimizada do chatbot"""
    
    # Verificar segurança e rate limiting
    if not check_security_and_rate_limit():
        return
    
    # Log da atividade
    log_security_event("INTERFACE_ACCESS", "User accessed optimized interface")
    
    # Upload de documentos com progress bar
    st.markdown("### 📁 Upload de Documentos")
    uploaded_docs = st.file_uploader(
        "Carregue seus documentos (PDF, TXT, DOCX)",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True,
        help="Cada usuário tem sua própria sessão isolada"
    )
    
    if uploaded_docs:
        st.session_state.uploaded_docs = uploaded_docs
        st.session_state.user_uploads = uploaded_docs
        
        # Processar documentos com progress bar
        if st.button("🔄 Processar Documentos", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔄 Iniciando processamento...")
                progress_bar.progress(10)
                
                status_text.text("📄 Processando documentos...")
                progress_bar.progress(50)
                
                document_context = process_documents(uploaded_docs)
                progress_bar.progress(80)
                
                st.session_state.document_context = document_context
                st.session_state.user_context = document_context
                
                progress_bar.progress(100)
                status_text.text("✅ Processamento concluído!")
                
                st.success("✅ Documentos processados com sucesso!")
                
                # Limpar progress bar após 2 segundos
                time.sleep(2)
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.error(f"Erro ao processar documentos: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    # Upload de imagens otimizado
    st.markdown("### 🖼️ Upload de Imagens")
    uploaded_images = st.file_uploader(
        "Carregue suas imagens para análise",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        accept_multiple_files=True,
        help="Análise automática com OCR e IA"
    )
    
    if uploaded_images:
        st.session_state.uploaded_images = uploaded_images
        
        # Processar imagens com progress bar
        if st.button("🔄 Processar Imagens", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔄 Iniciando análise de imagens...")
                progress_bar.progress(20)
                
                image_context = ""
                total_images = len(uploaded_images)
                
                for i, image_file in enumerate(uploaded_images):
                    status_text.text(f"🖼️ Processando imagem {i+1}/{total_images}...")
                    progress_bar.progress(20 + (i * 60 // total_images))
                    
                    # OCR rápido
                    ocr_text = extract_text_easyocr(image_file)
                    if ocr_text:
                        image_context += f"\n\nImagem {image_file.name}:\n{ocr_text}"
                
                progress_bar.progress(90)
                status_text.text("💾 Salvando contexto...")
                
                st.session_state.image_text_context = image_context
                st.session_state.user_image_context = image_context
                
                progress_bar.progress(100)
                status_text.text("✅ Análise concluída!")
                
                st.success("✅ Imagens processadas com sucesso!")
                
                # Limpar progress bar após 2 segundos
                time.sleep(2)
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.error(f"Erro ao processar imagens: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    # Chat interface otimizada
    st.markdown("### 💬 Chat com IA")
    
    # Inicializar mensagens se necessário
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar histórico de mensagens (limitado para performance)
    max_messages = 20  # Limitar mensagens exibidas
    recent_messages = st.session_state.messages[-max_messages:] if len(st.session_state.messages) > max_messages else st.session_state.messages
    
    for message in recent_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário otimizado
    if prompt := st.chat_input("Digite sua mensagem aqui...", key="chat_input"):
        # Verificar segurança antes de processar
        if not check_security_and_rate_limit():
            return
        
        # Log da mensagem
        log_security_event("CHAT_MESSAGE", f"Message length: {len(prompt)}")
        
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gerar resposta com loading otimizado
        with st.chat_message("assistant"):
            # Container para resposta
            response_container = st.empty()
            
            # Loading spinner personalizado
            with response_container.container():
                st.markdown("🤔 **IA está pensando...**")
                progress_dots = st.empty()
                
                # Animação de loading
                for i in range(3):
                    dots = "." * (i + 1)
                    progress_dots.markdown(f"Processando{dots}")
                    time.sleep(0.5)
            
            try:
                # Combinar contextos
                full_context = ""
                if st.session_state.document_context:
                    full_context += st.session_state.document_context
                if st.session_state.image_text_context:
                    full_context += st.session_state.image_text_context
                
                # Gerar resposta
                response = get_chat_response(
                    user_message=prompt,
                    chat_history=st.session_state.messages[:-1],
                    context=full_context,
                    images=None
                )
                
                # Limpar loading e mostrar resposta
                response_container.empty()
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                # Limpar loading e mostrar erro
                response_container.empty()
                error_msg = f"❌ Erro ao gerar resposta: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
