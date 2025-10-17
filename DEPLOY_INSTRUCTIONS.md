# 🚀 Deploy para Streamlit Cloud

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
- ✅ Upload limitado (50MB por arquivo)
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
4. **Limite de Upload**: Máximo 50MB por arquivo
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
