# PowerShell script para iniciar o NVIDIA AI Chatbot
Write-Host "========================================" -ForegroundColor Green
Write-Host "NVIDIA AI Chatbot - Iniciando..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instale Python 3.8+ primeiro." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# Verificar se Streamlit está instalado
try {
    python -c "import streamlit" 2>$null
    Write-Host "✓ Streamlit encontrado" -ForegroundColor Green
} catch {
    Write-Host "⚠ Instalando dependências..." -ForegroundColor Yellow
    pip install streamlit langchain langchain-nvidia-ai-endpoints langchain-core langchain-community python-dotenv requests pillow pypdf python-docx
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erro ao instalar dependências" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Iniciando Chatbot..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "✓ API Key configurada automaticamente" -ForegroundColor Green
Write-Host "✓ O app abrirá no seu navegador" -ForegroundColor Green
Write-Host ""
Write-Host "Para parar o servidor, pressione Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Iniciar o Streamlit
streamlit run app.py
