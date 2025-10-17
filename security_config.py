"""
Configurações de Segurança para Deploy Público
Rate Limiting e Proteções Adicionais
"""

import streamlit as st
import time
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityManager:
    """Gerenciador de segurança para múltiplos usuários"""
    
    def __init__(self):
        self.user_sessions = {}
        self.rate_limits = defaultdict(list)
        self.blocked_ips = set()
        self.max_requests_per_minute = 30
        self.max_requests_per_hour = 500
        self.session_timeout = 3600  # 1 hora
        
    def get_user_ip(self):
        """Obtém IP do usuário"""
        try:
            # Para Streamlit Cloud, usar session_id como identificador único
            return st.session_state.get("user_session_id", "unknown")
        except:
            return "unknown"
    
    def is_rate_limited(self, user_id):
        """Verifica se usuário está sendo rate limited"""
        now = datetime.now()
        user_requests = self.rate_limits[user_id]
        
        # Limpar requisições antigas (mais de 1 hora)
        user_requests[:] = [req_time for req_time in user_requests 
                          if now - req_time < timedelta(hours=1)]
        
        # Verificar limite por minuto
        recent_requests = [req_time for req_time in user_requests 
                          if now - req_time < timedelta(minutes=1)]
        
        if len(recent_requests) >= self.max_requests_per_minute:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return True
        
        # Verificar limite por hora
        if len(user_requests) >= self.max_requests_per_hour:
            logger.warning(f"Hourly rate limit exceeded for user {user_id}")
            return True
        
        # Adicionar requisição atual
        user_requests.append(now)
        return False
    
    def create_secure_session(self, user_id):
        """Cria sessão segura para usuário"""
        session_data = {
            "id": user_id,
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "request_count": 0,
            "uploads": [],
            "messages": [],
            "context": "",
            "image_context": ""
        }
        
        self.user_sessions[user_id] = session_data
        logger.info(f"Secure session created for user {user_id}")
        return session_data
    
    def get_session(self, user_id):
        """Obtém sessão do usuário"""
        if user_id not in self.user_sessions:
            return self.create_secure_session(user_id)
        
        session = self.user_sessions[user_id]
        
        # Verificar timeout
        if datetime.now() - session["last_activity"] > timedelta(seconds=self.session_timeout):
            logger.info(f"Session expired for user {user_id}")
            del self.user_sessions[user_id]
            return self.create_secure_session(user_id)
        
        # Atualizar última atividade
        session["last_activity"] = datetime.now()
        return session
    
    def cleanup_expired_sessions(self):
        """Limpa sessões expiradas"""
        now = datetime.now()
        expired_users = []
        
        for user_id, session in self.user_sessions.items():
            if now - session["last_activity"] > timedelta(seconds=self.session_timeout):
                expired_users.append(user_id)
        
        for user_id in expired_users:
            del self.user_sessions[user_id]
            logger.info(f"Cleaned up expired session for user {user_id}")

# Instância global do gerenciador de segurança
security_manager = SecurityManager()

def get_secure_user_id():
    """Gera ID único e seguro para usuário"""
    if "secure_user_id" not in st.session_state:
        # Usar timestamp + session_id para criar ID único
        timestamp = str(int(time.time()))
        session_id = st.session_state.get("user_session_id", "unknown")
        unique_string = f"{timestamp}_{session_id}"
        
        # Criar hash seguro
        secure_id = hashlib.md5(unique_string.encode()).hexdigest()[:16]
        st.session_state.secure_user_id = secure_id
    
    return st.session_state.secure_user_id

def check_security_and_rate_limit():
    """Verifica segurança e rate limiting"""
    user_id = get_secure_user_id()
    
    # Verificar rate limiting
    if security_manager.is_rate_limited(user_id):
        st.error("🚫 Muitas requisições. Aguarde um momento antes de tentar novamente.")
        st.info("💡 Dica: Aguarde 1 minuto para fazer novas requisições.")
        return False
    
    # Obter sessão segura
    session = security_manager.get_session(user_id)
    
    # Verificar limite de requisições da sessão
    if session["request_count"] >= 1000:  # Limite por sessão
        st.error("🚫 Limite de requisições da sessão atingido.")
        st.info("💡 Dica: Recarregue a página para iniciar uma nova sessão.")
        return False
    
    # Incrementar contador
    session["request_count"] += 1
    
    return True

def log_security_event(event_type, details=""):
    """Registra eventos de segurança"""
    user_id = get_secure_user_id()
    timestamp = datetime.now().isoformat()
    
    logger.info(f"SECURITY_EVENT: {event_type} | User: {user_id} | Time: {timestamp} | Details: {details}")

def display_security_info():
    """Exibe informações de segurança na sidebar"""
    with st.sidebar:
        st.markdown("### 🔒 Segurança")
        
        user_id = get_secure_user_id()
        session = security_manager.get_session(user_id)
        
        # Informações da sessão
        st.metric("🆔 ID Seguro", user_id[:8] + "...")
        st.metric("📊 Requisições", session["request_count"])
        
        # Tempo de sessão
        session_duration = datetime.now() - session["created_at"]
        st.metric("⏱️ Sessão", f"{int(session_duration.total_seconds()/60)} min")
        
        # Rate limiting info
        st.info("📈 Limite: 30 req/min, 500 req/hora")
        
        # Botão de emergência
        if st.button("🚨 Limpar Sessão", help="Limpa sua sessão em caso de problemas"):
            if "secure_user_id" in st.session_state:
                del st.session_state.secure_user_id
            st.rerun()

def cleanup_background():
    """Limpeza em background (executar periodicamente)"""
    security_manager.cleanup_expired_sessions()
    
    # Limpar rate limits antigos
    now = datetime.now()
    for user_id in list(security_manager.rate_limits.keys()):
        user_requests = security_manager.rate_limits[user_id]
        user_requests[:] = [req_time for req_time in user_requests 
                           if now - req_time < timedelta(hours=1)]
        
        if not user_requests:
            del security_manager.rate_limits[user_id]

# Executar limpeza em background
if st.session_state.get("last_cleanup", 0) < time.time() - 300:  # A cada 5 minutos
    cleanup_background()
    st.session_state.last_cleanup = time.time()
