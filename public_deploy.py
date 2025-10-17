"""
Deploy público do Chatbot com isolamento de sessões
Configurado para múltiplos usuários simultâneos
"""

import streamlit as st
import os
import uuid
from datetime import datetime, timedelta
import time
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

# Configurações de segurança para múltiplos usuários
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_session_config():
    """Configurações de sessão para múltiplos usuários"""
    return {
        "max_session_duration": 3600,  # 1 hora
        "max_uploads_per_session": 10,
        "max_file_size_mb": 50,
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

def check_session_validity():
    """Verifica se a sessão ainda é válida"""
    config = get_session_config()
    session_duration = datetime.now() - st.session_state.session_start_time
    
    if session_duration.total_seconds() > config["max_session_duration"]:
        st.warning("⚠️ Sua sessão expirou. Por favor, recarregue a página para continuar.")
        return False
    
    return True

def check_rate_limit():
    """Verifica rate limiting por usuário"""
    config = get_session_config()
    now = datetime.now()
    time_diff = now - st.session_state.user_last_request_time
    
    if time_diff.total_seconds() < 60:  # Dentro do último minuto
        if st.session_state.user_request_count >= config["rate_limit_per_minute"]:
            st.error("🚫 Muitas requisições. Aguarde um momento antes de tentar novamente.")
            return False
    
    # Reset counter se passou mais de 1 minuto
    if time_diff.total_seconds() >= 60:
        st.session_state.user_request_count = 0
    
    st.session_state.user_request_count += 1
    st.session_state.user_last_request_time = now
    return True

def main():
    """Função principal com isolamento de sessões"""
    
    # Inicializar sessão do usuário
    initialize_user_session()
    
    # Verificar validade da sessão
    if not check_session_validity():
        return
    
    # Header público
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🤖 Chatbot IA Avançado</h1>
        <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Desenvolvido por Lucas Cabral | Powered by NVIDIA AI</p>
        <p style='color: #e0e0e0; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Sessão: {}</p>
    </div>
    """.format(st.session_state.user_session_id[:8]), unsafe_allow_html=True)
    
    # Sidebar com informações da sessão e segurança
    with st.sidebar:
        st.markdown("### 📊 Sua Sessão")
        st.info(f"**ID da Sessão:** {st.session_state.user_session_id[:8]}...")
        
        # Tempo de sessão
        session_duration = datetime.now() - st.session_state.session_start_time
        st.metric("⏱️ Tempo de Sessão", f"{int(session_duration.total_seconds()/60)} min")
        
        # Contador de requisições
        st.metric("📨 Requisições", st.session_state.user_request_count)
        
        # Uploads do usuário
        st.metric("📁 Arquivos", len(st.session_state.user_uploads))
        
        st.markdown("---")
        
        # Exibir informações de segurança
        display_security_info()
        
        st.markdown("---")
        
        # Informações sobre privacidade
        st.markdown("### 🔒 Privacidade")
        st.success("✅ Sua sessão é completamente isolada")
        st.info("ℹ️ Seus dados não são compartilhados com outros usuários")
        st.warning("⚠️ Sessão expira em 1 hora")
        
        # Botão para limpar sessão
        if st.button("🗑️ Limpar Minha Sessão", use_container_width=True):
            # Limpar mensagens do chat
            st.session_state.user_messages = []
            
            # Limpar documentos e imagens carregados
            st.session_state.user_uploads = []
            
            # Limpar contextos de documentos e imagens
            st.session_state.user_context = ""
            st.session_state.user_image_context = ""
            
            # Resetar contador de requisições
            st.session_state.user_request_count = 0
            
            # Log do evento
            log_security_event("SESSION_CLEARED", "User manually cleared session")
            
            # Mostrar confirmação
            st.success("✅ Chat, documentos e imagens limpos com sucesso!")
            
            # Forçar rerun para atualizar a interface
            st.rerun()
    
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
        
        # Executar interface principal
        run_main_interface()
        
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

def run_main_interface():
    """Executa a interface principal do chatbot"""
    
    # Verificar segurança e rate limiting
    if not check_security_and_rate_limit():
        return
    
    # Log da atividade
    log_security_event("INTERFACE_ACCESS", "User accessed main interface")
    
    # Upload de documentos
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
        
        # Processar documentos
        if st.button("🔄 Processar Documentos"):
            with st.spinner("Processando documentos..."):
                try:
                    document_context = process_documents(uploaded_docs)
                    st.session_state.document_context = document_context
                    st.session_state.user_context = document_context
                    st.success("✅ Documentos processados com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao processar documentos: {str(e)}")
    
    # Upload de imagens otimizado
    st.markdown("### 🖼️ Upload de Imagens")
    uploaded_images = st.file_uploader(
        "Carregue suas imagens para análise",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        accept_multiple_files=True,
        help="Análise automática rápida com OCR e IA"
    )
    
    if uploaded_images:
        st.session_state.uploaded_images = uploaded_images
        
        # Processar imagens de forma rápida e silenciosa
        if st.button("🔄 Processar Imagens", use_container_width=True):
            try:
                # Processamento rápido sem spinners
                image_context = ""
                for image_file in uploaded_images:
                    # OCR rápido sem mensagens de loading
                    ocr_text = extract_text_easyocr(image_file)
                    if ocr_text and ocr_text != "No clear text detected":
                        image_context += f"\n\nImagem {image_file.name}:\n{ocr_text}"
                
                st.session_state.image_text_context = image_context
                st.session_state.user_image_context = image_context
                
                st.success("✅ Imagens processadas com sucesso!")
                
            except Exception as e:
                st.error(f"Erro ao processar imagens: {str(e)}")
    
    # Chat interface
    st.markdown("### 💬 Chat com IA")
    
    # Inicializar mensagens se necessário
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        # Verificar segurança antes de processar
        if not check_security_and_rate_limit():
            return
        
        # Log da mensagem
        log_security_event("CHAT_MESSAGE", f"Message length: {len(prompt)}")
            
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gerar resposta
        with st.chat_message("assistant"):
            with st.spinner("🤔 Pensando..."):
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
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"❌ Erro ao gerar resposta: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
