"""
Script de Deploy para Streamlit Cloud
Configuração para múltiplos usuários simultâneos
"""

import subprocess
import os
import sys

def create_streamlit_cloud_config():
    """Cria configuração para Streamlit Cloud"""
    
    # Criar diretório .streamlit se não existir
    os.makedirs('.streamlit', exist_ok=True)
    
    # Configuração do Streamlit
    config_content = """[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 2048
maxMessageSize = 2048

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"
serverPort = 8501

[logger]
level = "info"
"""
    
    with open('.streamlit/config.toml', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ Configuração do Streamlit criada")

def create_requirements_for_cloud():
    """Cria requirements.txt otimizado para Streamlit Cloud"""
    
    requirements = """streamlit>=1.28.0
langchain>=0.1.0
langchain-nvidia-ai-endpoints>=0.0.1
langchain-community>=0.0.20
nvidia-ai-endpoints>=0.0.1
chromadb>=0.4.0
PyPDF2>=3.0.0
python-docx>=0.8.11
easyocr>=1.7.0
Pillow>=10.0.0
requests>=2.31.0
python-dotenv>=1.0.0
numpy>=1.24.0
pandas>=2.0.0
"""
    
    with open('requirements_cloud.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ Requirements para cloud criados")

def create_deploy_instructions():
    """Cria instruções de deploy"""
    
    instructions = """# 🚀 Deploy para Streamlit Cloud

## Passos para Deploy Público:

### 1. Preparar o Repositório
- Faça commit de todos os arquivos
- Certifique-se de que `public_deploy.py` está no repositório
- Verifique se `requirements_cloud.txt` está presente

### 2. Deploy no Streamlit Cloud
1. Acesse: https://share.streamlit.io/
2. Conecte seu repositório GitHub
3. Configure:
   - **Main file path**: `public_deploy.py`
   - **Requirements file**: `requirements_cloud.txt`
   - **Python version**: 3.9+

### 3. Configurações de Segurança
- ✅ Isolamento de sessões por usuário
- ✅ Rate limiting (30 req/min por usuário)
- ✅ Timeout de sessão (1 hora)
- ✅ Upload limitado (2GB por arquivo)
- ✅ Proteção XSRF habilitada

### 4. Variáveis de Ambiente
Configure no Streamlit Cloud:
- `NVIDIA_API_KEY`: Sua chave da NVIDIA AI
- `STREAMLIT_SERVER_HEADLESS`: `true`
- `STREAMLIT_SERVER_ENABLE_CORS`: `false`

### 5. Teste o Deploy
- Acesse o link público gerado
- Teste com múltiplos usuários simultâneos
- Verifique isolamento de sessões

## 🔒 Recursos de Segurança Implementados:

1. **Isolamento de Sessões**: Cada usuário tem sua própria sessão isolada
2. **Rate Limiting**: Máximo 30 requisições por minuto por usuário
3. **Timeout de Sessão**: Sessões expiram em 1 hora
4. **Limite de Upload**: Máximo 2GB por arquivo
5. **Proteção XSRF**: Proteção contra ataques cross-site
6. **Logs de Segurança**: Monitoramento de atividades suspeitas

## 📊 Monitoramento:
- Cada sessão tem ID único
- Contador de requisições por usuário
- Tempo de sessão monitorado
- Uploads isolados por usuário

## 🌐 Link Público:
Após o deploy, você receberá um link como:
`https://seu-app.streamlit.app`

Compartilhe este link no LinkedIn para que as pessoas testem!
"""
    
    with open('DEPLOY_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Instruções de deploy criadas")

def create_cloud_runner():
    """Cria script para executar localmente com configurações de cloud"""
    
    runner_content = """@echo off
echo ========================================
echo Deploy Local - Configuração Cloud
echo ========================================
echo.

REM Ativar ambiente virtual
call venv\\Scripts\\activate.bat

REM Configurar variáveis de ambiente para teste
set STREAMLIT_SERVER_HEADLESS=true
set STREAMLIT_SERVER_ENABLE_CORS=false
set STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200

echo Iniciando servidor com configurações de cloud...
echo.
echo Acesse: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar
echo.

streamlit run public_deploy.py --server.port 8501 --server.address 0.0.0.0

pause
"""
    
    with open('run_cloud_local.bat', 'w', encoding='utf-8') as f:
        f.write(runner_content)
    
    print("✅ Script de execução local criado")

def main():
    """Função principal"""
    print("🚀 Configurando deploy para Streamlit Cloud...")
    print()
    
    try:
        create_streamlit_cloud_config()
        create_requirements_for_cloud()
        create_deploy_instructions()
        create_cloud_runner()
        
        print()
        print("✅ Configuração completa!")
        print()
        print("📋 Próximos passos:")
        print("1. Faça commit dos arquivos no Git")
        print("2. Acesse https://share.streamlit.io/")
        print("3. Conecte seu repositório")
        print("4. Configure public_deploy.py como main file")
        print("5. Use requirements_cloud.txt")
        print("6. Configure suas variáveis de ambiente")
        print("7. Deploy!")
        print()
        print("🔗 Após o deploy, você terá um link público para compartilhar!")
        
    except Exception as e:
        print(f"❌ Erro na configuração: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
