# 🎯 Final Assessment - LangServe RAG System

Este projeto implementa um sistema completo de RAG (Retrieval-Augmented Generation) usando LangServe para avaliação final.

## 🚀 Funcionalidades

### Endpoints Implementados
- **`/basic_chat`** - Chat básico com LLM
- **`/retriever`** - Sistema de recuperação de documentos
- **`/generator`** - Geração de respostas com contexto
- **`/health`** - Verificação de saúde do servidor

### Interface Gradio
- **Basic Chat** - Teste direto do LLM
- **Document Retrieval** - Busca de documentos relevantes
- **Response Generation** - Geração com contexto
- **Complete RAG Chain** - Pipeline completo RAG

## 📁 Estrutura do Projeto

```
CHAT_BOTS/
├── server_app.py              # Servidor LangServe principal
├── frontend_block.py          # Interface Gradio
├── frontend_server.py         # Servidor FastAPI + Gradio
├── start_assessment.py        # Script de inicialização
├── requirements_assessment.txt # Dependências
└── README_ASSESSMENT.md       # Este arquivo
```

## 🛠️ Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements_assessment.txt
```

2. **Configurar variáveis de ambiente (opcional):**
```bash
export NVIDIA_API_KEY="sua_chave_nvidia"
```

## 🚀 Execução

### Opção 1: Inicialização Automática
```bash
python start_assessment.py
```

### Opção 2: Inicialização Manual

**Terminal 1 - LangServe Server:**
```bash
python server_app.py
```

**Terminal 2 - Frontend Server:**
```bash
python frontend_server.py
```

## 🌐 URLs de Acesso

- **Frontend Interface:** http://localhost:8000
- **LangServe Server:** http://localhost:9012
- **Health Check:** http://localhost:9012/health
- **API Docs:** http://localhost:9012/docs

## 🧪 Testando o Sistema

### 1. Verificar Status do Servidor
- Acesse http://localhost:8000
- Clique em "🔍 Check Server Status"

### 2. Testar Basic Chat
- Vá para a aba "💬 Basic Chat"
- Digite uma pergunta
- Clique em "🚀 Send"

### 3. Testar Document Retrieval
- Vá para a aba "📚 Document Retrieval"
- Digite uma consulta de busca
- Clique em "🔍 Search"

### 4. Testar Response Generation
- Vá para a aba "🤖 Response Generation"
- Digite uma pergunta e contexto opcional
- Clique em "✨ Generate"

### 5. Testar RAG Chain Completo
- Vá para a aba "🔗 Complete RAG Chain"
- Digite uma pergunta complexa
- Clique em "🚀 Run RAG Chain"

## 📊 Exemplos de Teste

### Perguntas para Basic Chat
- "What is artificial intelligence?"
- "Explain machine learning in simple terms"

### Consultas para Retrieval
- "AI and machine learning"
- "neural networks"
- "computer vision"

### Perguntas para RAG Chain
- "What is the difference between AI, machine learning, and deep learning?"
- "How does natural language processing work?"
- "Explain the relationship between computer vision and AI"

## 🔧 Configuração Avançada

### Modelos NVIDIA
O sistema tenta usar modelos NVIDIA primeiro:
- **Embeddings:** `nvidia/parakeet-tdt-0.6b-v2`
- **LLM:** `meta/llama3-8b-instruct`

### Fallback Models
Se os modelos NVIDIA falharem, usa modelos HuggingFace:
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **LLM:** `microsoft/DialoGPT-medium`

## 🐛 Solução de Problemas

### Servidor não inicia
1. Verifique se as dependências estão instaladas
2. Verifique se as portas 8000 e 9012 estão livres
3. Verifique os logs de erro

### Erro de API Key
1. Configure `NVIDIA_API_KEY` se usando modelos NVIDIA
2. O sistema usará modelos HuggingFace como fallback

### Erro de conexão
1. Verifique se ambos os servidores estão rodando
2. Teste a URL de health check: http://localhost:9012/health

## 📝 Logs e Debugging

### Logs do LangServe Server
```bash
python server_app.py
```

### Logs do Frontend Server
```bash
python frontend_server.py
```

### Logs Combinados
```bash
python start_assessment.py
```

## 🎯 Critérios de Avaliação

### ✅ Funcionalidades Implementadas
- [x] Endpoint `/basic_chat` funcionando
- [x] Endpoint `/retriever` funcionando
- [x] Endpoint `/generator` funcionando
- [x] Interface Gradio completa
- [x] Sistema RAG funcional
- [x] Health check endpoint
- [x] Documentação completa

### 🔍 Pontos de Avaliação
1. **Funcionalidade dos Endpoints**
2. **Interface do Usuário**
3. **Integração RAG**
4. **Tratamento de Erros**
5. **Documentação**

## 🚀 Deploy em Produção

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements_assessment.txt .
RUN pip install -r requirements_assessment.txt

COPY . .
EXPOSE 8000 9012

CMD ["python", "start_assessment.py"]
```

### Variáveis de Ambiente
```bash
export NVIDIA_API_KEY="sua_chave"
export APP_ROOT_PATH="/"
export PORT=8000
export LANG_SERVE_PORT=9012
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs de erro
2. Teste os endpoints individualmente
3. Verifique a documentação da API em `/docs`

---

**Desenvolvido por Lucas Cabral** 🚀
**Powered by NVIDIA AI Endpoints & LangServe**
