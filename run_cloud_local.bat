@echo off
echo ========================================
echo Deploy Local - Configuração Cloud
echo ========================================
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

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
