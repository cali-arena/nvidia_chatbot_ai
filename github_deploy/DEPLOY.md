# 🚀 Guia de Deploy - NVIDIA Chatbot AI

## 📋 Pré-requisitos

- Conta no GitHub
- Conta no Streamlit Cloud
- API Key da NVIDIA AI

## 🔧 Configuração do Repositório

### 1. Preparar Arquivos Essenciais

Os seguintes arquivos são necessários para o deploy:

```
nvidia_chatbot_ai/
├── public_deploy.py          # ✅ Interface pública principal
├── security_config.py        # ✅ Configurações de segurança
├── requirements.txt          # ✅ Dependências otimizadas
├── .streamlit/
│   └── config.toml          # ✅ Configuração do Streamlit
├── README.md                 # ✅ Documentação principal
└── DEPLOY.md                 # ✅ Este guia
```

### 2. Arquivos de Configuração

#### `.streamlit/config.toml`
```toml
[theme]
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
maxUploadSize = 200

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"
serverPort = 8501
```

#### `requirements.txt`
```
streamlit>=1.28.0
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
```

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Preparar Repositório
```bash
# Clone seu repositório
git clone https://github.com/cali-arena/nvidia_chatbot_ai.git
cd nvidia_chatbot_ai

# Adicione os arquivos necessários
git add .
git commit -m "Deploy público configurado"
git push origin main
```

### Passo 2: Deploy no Streamlit Cloud
1. **Acesse**: https://share.streamlit.io/
2. **Conecte**: Seu repositório GitHub
3. **Configure**:
   - **Main file path**: `public_deploy.py`
   - **Requirements file**: `requirements.txt`
   - **Python version**: 3.9+
4. **Variáveis de ambiente**:
   ```
   NVIDIA_API_KEY=sua_chave_aqui
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_SERVER_ENABLE_CORS=false
   ```
5. **Deploy!** 🎉

### Passo 3: Obter API Key da NVIDIA
1. Acesse: https://build.nvidia.com/
2. Crie uma conta gratuita
3. Gere sua API key
4. Configure no Streamlit Cloud

## 🔒 Configurações de Segurança

### Rate Limiting
- **30 requisições por minuto** por usuário
- **500 requisições por hora** por usuário
- **1000 requisições por sessão**

### Isolamento de Sessões
- Cada usuário tem sessão única
- Dados não são compartilhados
- Timeout automático em 1 hora

### Limites de Upload
- **50MB por arquivo** máximo
- **10 arquivos por sessão** máximo
- Tipos: PDF, TXT, DOCX, PNG, JPG, JPEG, GIF, BMP

## 📊 Monitoramento

### Para Usuários
- ID de sessão único
- Contador de requisições
- Tempo de sessão
- Status de rate limiting

### Para Administradores
- Logs de segurança
- Estatísticas de uso
- Monitoramento de sessões
- Alertas de segurança

## 🧪 Teste Local

### Executar com configurações de cloud:
```bash
python run_cloud_local.py
```

### Ou usar o arquivo .bat:
```bash
run_cloud_local.bat
```

## 🔗 Link Público

Após o deploy, você receberá um link como:
```
https://seu-app.streamlit.app
```

**Este link pode ser compartilhado publicamente no LinkedIn!**

## ⚠️ Troubleshooting

### Problemas Comuns

1. **Erro de API Key**
   - Verifique se `NVIDIA_API_KEY` está configurada
   - Confirme se a key é válida

2. **Erro de Dependências**
   - Verifique se `requirements.txt` está correto
   - Confirme se Python 3.9+ está sendo usado

3. **Erro de Upload**
   - Verifique limites de tamanho
   - Confirme tipos de arquivo suportados

4. **Rate Limiting**
   - Aguarde 1 minuto entre requisições
   - Limite de 30 req/min por usuário

### Logs de Debug
- Acesse logs no Streamlit Cloud
- Verifique console do navegador
- Monitore eventos de segurança

## 🎯 Pronto para Produção

Seu chatbot está configurado com:
- ✅ Segurança robusta
- ✅ Escalabilidade
- ✅ Monitoramento
- ✅ Rate limiting
- ✅ Isolamento de sessões

**Pronto para ser compartilhado publicamente!** 🚀

---

**Desenvolvido por Lucas Cabral** | **Powered by NVIDIA AI**
