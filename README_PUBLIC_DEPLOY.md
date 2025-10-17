# 🤖 Chatbot IA - Deploy Público

## 🚀 Sistema Configurado para Múltiplos Usuários Simultâneos

Este sistema foi especialmente configurado para permitir que várias pessoas acessem simultaneamente sem interferir nos dados uns dos outros.

### 🔒 Recursos de Segurança Implementados

#### ✅ Isolamento Completo de Sessões
- Cada usuário recebe uma sessão única e isolada
- Dados não são compartilhados entre usuários
- Uploads e conversas são privados por sessão

#### ✅ Rate Limiting Inteligente
- **30 requisições por minuto** por usuário
- **500 requisições por hora** por usuário
- **1000 requisições por sessão** (renovação automática)

#### ✅ Timeout de Sessão
- Sessões expiram automaticamente em **1 hora**
- Renovação automática com atividade do usuário
- Limpeza automática de sessões inativas

#### ✅ Limites de Upload
- **50MB por arquivo** máximo
- **10 arquivos por sessão** máximo
- Tipos suportados: PDF, TXT, DOCX, PNG, JPG, JPEG, GIF, BMP

#### ✅ Proteções Adicionais
- Proteção XSRF habilitada
- Logs de segurança para monitoramento
- IDs de sessão únicos e seguros
- Limpeza automática de dados expirados

### 🌐 Como Deployar Publicamente

#### Opção 1: Streamlit Cloud (Recomendado)
1. **Preparar repositório:**
   ```bash
   git add .
   git commit -m "Deploy público configurado"
   git push origin main
   ```

2. **Deploy no Streamlit Cloud:**
   - Acesse: https://share.streamlit.io/
   - Conecte seu repositório GitHub
   - Configure:
     - **Main file path**: `public_deploy.py`
     - **Requirements file**: `requirements_cloud.txt`
     - **Python version**: 3.9+

3. **Configurar variáveis de ambiente:**
   ```
   NVIDIA_API_KEY=sua_chave_aqui
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_SERVER_ENABLE_CORS=false
   ```

4. **Deploy!** 🎉

#### Opção 2: Execução Local Pública
```bash
# Executar com configurações de cloud
python run_cloud_local.bat
```

### 📊 Monitoramento e Estatísticas

#### Para Cada Usuário:
- **ID de Sessão Único**: Identificação segura
- **Contador de Requisições**: Acompanhamento de uso
- **Tempo de Sessão**: Duração da sessão atual
- **Arquivos Uploaded**: Quantidade de documentos

#### Para Administradores:
- **Logs de Segurança**: Eventos importantes registrados
- **Rate Limiting**: Controle automático de uso
- **Limpeza Automática**: Sessões expiradas removidas
- **Estatísticas de Uso**: Monitoramento geral

### 🔧 Configurações Técnicas

#### Arquivos Principais:
- `public_deploy.py` - Interface pública principal
- `security_config.py` - Configurações de segurança
- `requirements_cloud.txt` - Dependências otimizadas
- `.streamlit/config.toml` - Configuração do Streamlit

#### Recursos Implementados:
- **Sessões Isoladas**: UUID único por usuário
- **Rate Limiting**: Controle de requisições
- **Timeout Automático**: Limpeza de sessões
- **Logs de Segurança**: Monitoramento de eventos
- **Proteção XSRF**: Segurança contra ataques

### 📱 Interface do Usuário

#### Header Público:
- Título do sistema
- Créditos do desenvolvedor
- ID da sessão atual

#### Sidebar Informativa:
- **Sua Sessão**: Informações pessoais
- **Segurança**: Status de rate limiting
- **Privacidade**: Garantias de isolamento
- **Controles**: Botões de ação

#### Área Principal:
- **Upload de Documentos**: Processamento RAG
- **Upload de Imagens**: Análise com OCR
- **Chat Interface**: Conversação com IA
- **Estatísticas**: Informações do sistema

### 🚨 Recursos de Emergência

#### Botão "Limpar Sessão":
- Remove todos os dados da sessão atual
- Reinicia contadores
- Gera nova sessão limpa

#### Botão "Limpar Sessão" (Segurança):
- Limpa dados de segurança
- Reinicia rate limiting
- Força nova autenticação

#### Timeout Automático:
- Sessões expiram em 1 hora
- Renovação com atividade
- Limpeza automática de dados

### 📈 Escalabilidade

#### Suporta:
- **Múltiplos usuários simultâneos**
- **Sessões ilimitadas**
- **Rate limiting por usuário**
- **Limpeza automática**

#### Otimizações:
- Cache de configurações (5 min)
- Limpeza em background (5 min)
- Rate limits eficientes
- Sessões leves em memória

### 🔗 Link Público

Após o deploy no Streamlit Cloud, você receberá um link como:
```
https://seu-app.streamlit.app
```

**Este link pode ser compartilhado publicamente no LinkedIn!**

### ⚠️ Importante

- ✅ **Seguro**: Cada usuário tem sessão isolada
- ✅ **Escalável**: Suporta múltiplos usuários
- ✅ **Monitorado**: Logs de segurança ativos
- ✅ **Limitado**: Rate limiting protege o sistema
- ✅ **Automático**: Limpeza e timeout automáticos

### 🎯 Pronto para LinkedIn!

Seu chatbot está configurado e pronto para ser compartilhado publicamente. Cada pessoa que acessar terá sua própria experiência isolada e segura!

---

**Desenvolvido por Lucas Cabral** | **Powered by NVIDIA AI** | **Built with ❤️ using Streamlit**
