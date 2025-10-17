#!/usr/bin/env python3
"""
Script final para deploy no GitHub
Copia arquivos para o repositório e prepara para commit
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def copy_to_github_repo():
    """Copia arquivos para o repositório GitHub"""
    
    print("🚀 Preparando arquivos para o repositório GitHub...")
    
    # Diretório de origem
    source_dir = Path("github_deploy")
    
    # Verificar se o diretório existe
    if not source_dir.exists():
        print("❌ Diretório github_deploy não encontrado!")
        print("Execute primeiro: python prepare_github_deploy.py")
        return False
    
    # Listar arquivos que serão copiados
    print("\n📋 Arquivos para deploy:")
    for file_path in source_dir.rglob("*"):
        if file_path.is_file():
            print(f"  ✅ {file_path.relative_to(source_dir)}")
    
    print(f"\n📁 Diretório preparado: {source_dir.absolute()}")
    
    return True

def show_github_instructions():
    """Mostra instruções específicas para o GitHub"""
    
    print("\n" + "="*70)
    print("🎯 INSTRUÇÕES PARA DEPLOY NO GITHUB")
    print("="*70)
    
    print("\n📋 Passo a passo:")
    
    print("\n1️⃣ PREPARAR REPOSITÓRIO:")
    print("   - Acesse: https://github.com/cali-arena/nvidia_chatbot_ai")
    print("   - Clone o repositório:")
    print("     git clone https://github.com/cali-arena/nvidia_chatbot_ai.git")
    print("     cd nvidia_chatbot_ai")
    
    print("\n2️⃣ COPIAR ARQUIVOS:")
    print("   - Copie TODOS os arquivos do diretório 'github_deploy'")
    print("   - Para o diretório do seu repositório")
    print("   - Mantenha a estrutura de pastas")
    
    print("\n3️⃣ COMMIT E PUSH:")
    print("   git add .")
    print("   git commit -m 'Deploy público configurado com segurança'")
    print("   git push origin main")
    
    print("\n4️⃣ DEPLOY NO STREAMLIT CLOUD:")
    print("   - Acesse: https://share.streamlit.io/")
    print("   - Conecte seu repositório GitHub")
    print("   - Configure:")
    print("     • Main file path: public_deploy.py")
    print("     • Requirements file: requirements.txt")
    print("     • Python version: 3.9+")
    
    print("\n5️⃣ CONFIGURAR VARIÁVEIS:")
    print("   - NVIDIA_API_KEY: sua_chave_da_nvidia")
    print("   - STREAMLIT_SERVER_HEADLESS: true")
    print("   - STREAMLIT_SERVER_ENABLE_CORS: false")
    
    print("\n6️⃣ OBTER API KEY DA NVIDIA:")
    print("   - Acesse: https://build.nvidia.com/")
    print("   - Crie uma conta gratuita")
    print("   - Gere sua API key")
    print("   - Configure no Streamlit Cloud")
    
    print("\n7️⃣ DEPLOY! 🎉")
    print("   - Clique em 'Deploy'")
    print("   - Aguarde o build")
    print("   - Receba seu link público!")
    
    print("\n🔗 LINK PÚBLICO:")
    print("   Após o deploy, você terá um link como:")
    print("   https://seu-app.streamlit.app")
    print("   Este link pode ser compartilhado no LinkedIn!")

def show_security_features():
    """Mostra recursos de segurança implementados"""
    
    print("\n" + "="*70)
    print("🔒 RECURSOS DE SEGURANÇA IMPLEMENTADOS")
    print("="*70)
    
    print("\n✅ ISOLAMENTO DE SESSÕES:")
    print("   • Cada usuário tem sessão única e isolada")
    print("   • Dados não são compartilhados entre usuários")
    print("   • Uploads e conversas são privados por sessão")
    
    print("\n✅ RATE LIMITING:")
    print("   • 30 requisições por minuto por usuário")
    print("   • 500 requisições por hora por usuário")
    print("   • 1000 requisições por sessão")
    
    print("\n✅ TIMEOUT AUTOMÁTICO:")
    print("   • Sessões expiram em 1 hora")
    print("   • Renovação automática com atividade")
    print("   • Limpeza automática de sessões inativas")
    
    print("\n✅ LIMITES DE UPLOAD:")
    print("   • 2GB por arquivo máximo")
    print("   • 10 arquivos por sessão máximo")
    print("   • Tipos: PDF, TXT, DOCX, PNG, JPG, JPEG, GIF, BMP")
    
    print("\n✅ PROTEÇÕES ADICIONAIS:")
    print("   • Proteção XSRF habilitada")
    print("   • Logs de segurança para monitoramento")
    print("   • IDs de sessão únicos e seguros")
    print("   • Limpeza automática de dados expirados")

def show_monitoring():
    """Mostra recursos de monitoramento"""
    
    print("\n" + "="*70)
    print("📊 RECURSOS DE MONITORAMENTO")
    print("="*70)
    
    print("\n👤 PARA USUÁRIOS:")
    print("   • ID de sessão único na sidebar")
    print("   • Contador de requisições em tempo real")
    print("   • Tempo de sessão atual")
    print("   • Status de rate limiting")
    print("   • Botão para limpar sessão")
    
    print("\n🔧 PARA ADMINISTRADORES:")
    print("   • Logs de segurança detalhados")
    print("   • Estatísticas de uso por usuário")
    print("   • Monitoramento de sessões ativas")
    print("   • Alertas de segurança")
    print("   • Limpeza automática de dados")

def main():
    """Função principal"""
    
    print("🤖 NVIDIA Chatbot AI - Deploy para GitHub")
    print("="*50)
    
    # Verificar se os arquivos estão prontos
    if not copy_to_github_repo():
        return 1
    
    # Mostrar instruções
    show_github_instructions()
    show_security_features()
    show_monitoring()
    
    print("\n" + "="*70)
    print("🎯 RESUMO FINAL")
    print("="*70)
    
    print("\n✅ Sistema configurado com:")
    print("   • Interface pública segura")
    print("   • Isolamento de sessões")
    print("   • Rate limiting inteligente")
    print("   • Monitoramento completo")
    print("   • Deploy automático")
    
    print("\n🚀 Pronto para:")
    print("   • Deploy no GitHub")
    print("   • Deploy no Streamlit Cloud")
    print("   • Compartilhamento público")
    print("   • Múltiplos usuários simultâneos")
    
    print("\n🎉 Sucesso! Seu chatbot está pronto para o LinkedIn!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
