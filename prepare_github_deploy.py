#!/usr/bin/env python3
"""
Script para preparar deploy no GitHub
Cria estrutura limpa e organizada para o repositório
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_github_structure():
    """Cria estrutura limpa para o GitHub"""
    
    print("🚀 Preparando estrutura para GitHub...")
    
    # Arquivos essenciais para o GitHub
    essential_files = [
        "public_deploy.py",
        "security_config.py", 
        "requirements_github.txt",
        "README_GITHUB.md",
        "DEPLOY_GITHUB.md",
        ".streamlit/config.toml",
        "run_cloud_local.py"
    ]
    
    # Criar diretório para GitHub
    github_dir = Path("github_deploy")
    github_dir.mkdir(exist_ok=True)
    
    # Copiar arquivos essenciais
    for file_path in essential_files:
        source = Path(file_path)
        if source.exists():
            dest = github_dir / source.name
            if source.is_file():
                shutil.copy2(source, dest)
                print(f"✅ Copiado: {file_path}")
            elif source.is_dir():
                dest.mkdir(exist_ok=True)
                for subfile in source.iterdir():
                    shutil.copy2(subfile, dest / subfile.name)
                print(f"✅ Copiado diretório: {file_path}")
        else:
            print(f"⚠️ Arquivo não encontrado: {file_path}")
    
    # Renomear requirements
    requirements_source = github_dir / "requirements_github.txt"
    requirements_dest = github_dir / "requirements.txt"
    if requirements_source.exists():
        requirements_source.rename(requirements_dest)
        print("✅ Renomeado requirements.txt")
    
    # Renomear README
    readme_source = github_dir / "README_GITHUB.md"
    readme_dest = github_dir / "README.md"
    if readme_source.exists():
        readme_source.rename(readme_dest)
        print("✅ Renomeado README.md")
    
    # Renomear DEPLOY
    deploy_source = github_dir / "DEPLOY_GITHUB.md"
    deploy_dest = github_dir / "DEPLOY.md"
    if deploy_source.exists():
        deploy_source.rename(deploy_dest)
        print("✅ Renomeado DEPLOY.md")
    
    # Criar .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Logs
*.log

# Temporary files
*.tmp
*.temp

# ChromaDB
chroma_db/

# Uploads (se houver)
uploads/
temp_uploads/

# Environment variables
.env
.env.local
.env.production

# API Keys (não commitar)
api_keys.txt
secrets.txt
"""
    
    with open(github_dir / ".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print("✅ Criado .gitignore")
    
    # Criar LICENSE
    license_content = """MIT License

Copyright (c) 2025 Lucas Cabral

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open(github_dir / "LICENSE", "w", encoding="utf-8") as f:
        f.write(license_content)
    print("✅ Criado LICENSE")
    
    print(f"\n📁 Estrutura criada em: {github_dir.absolute()}")
    return github_dir

def show_deploy_instructions(github_dir):
    """Mostra instruções de deploy"""
    
    print("\n" + "="*60)
    print("🎯 INSTRUÇÕES PARA DEPLOY NO GITHUB")
    print("="*60)
    
    print(f"\n📁 Diretório preparado: {github_dir.absolute()}")
    
    print("\n📋 Arquivos incluídos:")
    for file in github_dir.iterdir():
        if file.is_file():
            print(f"  ✅ {file.name}")
        elif file.is_dir():
            print(f"  📁 {file.name}/")
            for subfile in file.iterdir():
                print(f"    ✅ {subfile.name}")
    
    print("\n🚀 Próximos passos:")
    print("1. Copie o conteúdo do diretório 'github_deploy' para seu repositório")
    print("2. Faça commit e push:")
    print("   git add .")
    print("   git commit -m 'Deploy público configurado'")
    print("   git push origin main")
    print("3. Acesse https://share.streamlit.io/")
    print("4. Conecte seu repositório")
    print("5. Configure:")
    print("   - Main file: public_deploy.py")
    print("   - Requirements: requirements.txt")
    print("6. Adicione sua NVIDIA_API_KEY")
    print("7. Deploy! 🎉")
    
    print("\n🔗 Após o deploy, você terá um link público para compartilhar!")
    
    print("\n📊 Recursos implementados:")
    print("  ✅ Isolamento de sessões")
    print("  ✅ Rate limiting (30 req/min)")
    print("  ✅ Timeout automático (1 hora)")
    print("  ✅ Limites de upload (50MB)")
    print("  ✅ Proteção XSRF")
    print("  ✅ Logs de segurança")
    print("  ✅ Monitoramento de uso")

def main():
    """Função principal"""
    try:
        github_dir = create_github_structure()
        show_deploy_instructions(github_dir)
        
        print("\n✅ Preparação concluída com sucesso!")
        print("🎯 Pronto para deploy no GitHub!")
        
    except Exception as e:
        print(f"❌ Erro na preparação: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
