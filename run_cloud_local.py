#!/usr/bin/env python3
"""
Script para executar o deploy local com configurações de cloud
"""

import os
import sys
import subprocess
import time

def main():
    print("=" * 50)
    print("Deploy Local - Configuração Cloud")
    print("=" * 50)
    print()
    
    # Configurar variáveis de ambiente
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "200"
    
    print("Configurações de ambiente definidas:")
    print("- STREAMLIT_SERVER_HEADLESS=true")
    print("- STREAMLIT_SERVER_ENABLE_CORS=false")
    print("- STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200")
    print()
    
    print("Iniciando servidor com configurações de cloud...")
    print()
    print("Acesse: http://localhost:8501")
    print()
    print("Pressione Ctrl+C para parar")
    print()
    
    try:
        # Executar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "public_deploy.py", 
            "--server.port", "8501", 
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro ao executar servidor: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
