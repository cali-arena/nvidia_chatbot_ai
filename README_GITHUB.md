# 🤖 NVIDIA Chatbot AI - Deploy Público

Sistema de chatbot inteligente com IA da NVIDIA, configurado para múltiplos usuários simultâneos com isolamento de sessões.

## 🚀 Deploy Rápido

### Streamlit Cloud (Recomendado)
[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

1. **Fork este repositório**
2. **Acesse [Streamlit Cloud](https://share.streamlit.io/)**
3. **Conecte seu repositório**
4. **Configure:**
   - Main file: `public_deploy.py`
   - Requirements: `requirements.txt`
5. **Adicione sua `NVIDIA_API_KEY`**
6. **Deploy!** 🎉

## 🔒 Recursos de Segurança

- ✅ **Isolamento de Sessões**: Cada usuário tem sessão única
- ✅ **Rate Limiting**: 30 req/min, 500 req/hora por usuário
- ✅ **Timeout Automático**: Sessões expiram em 1 hora
- ✅ **Limites de Upload**: 50MB por arquivo, 10 arquivos por sessão
- ✅ **Proteção XSRF**: Segurança contra ataques
- ✅ **Logs de Segurança**: Monitoramento de eventos

## 📁 Estrutura do Projeto

```
nvidia_chatbot_ai/
├── public_deploy.py          # Interface pública principal
├── security_config.py        # Configurações de segurança
├── requirements.txt          # Dependências
├── .streamlit/
│   └── config.toml          # Configuração do Streamlit
├── README.md                 # Este arquivo
└── DEPLOY.md                 # Instruções detalhadas
```

## 🛠️ Instalação Local

```bash
# Clone o repositório
git clone https://github.com/cali-arena/nvidia_chatbot_ai.git
cd nvidia_chatbot_ai

# Instale dependências
pip install -r requirements.txt

# Configure sua API key
export NVIDIA_API_KEY=sua_chave_aqui

# Execute localmente
streamlit run public_deploy.py
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
NVIDIA_API_KEY=sua_chave_da_nvidia
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
```

### Obter API Key da NVIDIA
1. Acesse: https://build.nvidia.com/
2. Crie uma conta
3. Gere sua API key
4. Configure no Streamlit Cloud ou localmente

## 📊 Funcionalidades

### 🤖 Chat Inteligente
- Conversação com IA da NVIDIA
- Contexto mantido por sessão
- Respostas personalizadas

### 📁 Upload de Documentos
- Suporte a PDF, TXT, DOCX
- Processamento RAG automático
- Análise inteligente de conteúdo

### 🖼️ Análise de Imagens
- OCR automático com EasyOCR
- Análise visual com IA
- Extração de texto de imagens

### 🔒 Segurança
- Sessões isoladas por usuário
- Rate limiting inteligente
- Timeout automático
- Logs de segurança

## 🌐 Deploy Público

Após o deploy no Streamlit Cloud, você receberá um link público como:
```
https://seu-app.streamlit.app
```

**Este link pode ser compartilhado publicamente!**

## 📈 Monitoramento

- **Sidebar**: Informações da sessão
- **Rate Limiting**: Controle automático
- **Logs**: Eventos de segurança
- **Estatísticas**: Uso por usuário

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvedor

**Lucas Cabral**
- Powered by NVIDIA AI
- Built with ❤️ using Streamlit

## 🆘 Suporte

Se encontrar problemas:
1. Verifique se sua `NVIDIA_API_KEY` está configurada
2. Confirme se todas as dependências estão instaladas
3. Abra uma issue no GitHub

---

**Pronto para ser compartilhado publicamente!** 🎯
