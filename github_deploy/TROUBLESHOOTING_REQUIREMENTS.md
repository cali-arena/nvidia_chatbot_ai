# 🔧 Solução para Erros de Requirements

## ❌ Problema: "Error installing requirements"

Se você está enfrentando erros de instalação de requirements no Streamlit Cloud, siga estas soluções:

## ✅ Soluções

### 1. Use o arquivo requirements_minimal.txt
Se o `requirements.txt` principal falhar, use o arquivo `requirements_minimal.txt` que contém apenas as dependências essenciais.

### 2. Instale dependências uma por vez
Se ainda houver problemas, instale as dependências mais importantes primeiro:

```txt
streamlit
langchain
langchain-nvidia-ai-endpoints
python-dotenv
requests
Pillow
```

### 3. Versões específicas (se necessário)
Se ainda houver conflitos, use versões específicas:

```txt
streamlit==1.28.0
langchain==0.1.0
langchain-nvidia-ai-endpoints==0.1.0
python-dotenv==1.0.0
requests==2.31.0
Pillow==10.0.0
PyPDF2==3.0.0
python-docx==1.1.0
easyocr==1.7.0
pandas==2.0.0
numpy==1.24.0
chromadb==0.4.0
```

## 🚀 Passos para Deploy

1. **Teste localmente primeiro:**
   ```bash
   pip install -r requirements.txt
   streamlit run public_deploy.py
   ```

2. **Se funcionar localmente, use no Streamlit Cloud:**
   - Main file: `public_deploy.py`
   - Requirements: `requirements.txt` (ou `requirements_minimal.txt`)
   - Python version: 3.9+

3. **Configure sua NVIDIA_API_KEY:**
   - Vá em "Secrets" no Streamlit Cloud
   - Adicione: `NVIDIA_API_KEY = "sua_chave_aqui"`

## 🔍 Troubleshooting

### Erro comum: "No module named 'easyocr'"
- Use `requirements_minimal.txt` primeiro
- Se ainda falhar, remova `easyocr` temporariamente

### Erro comum: "No module named 'chromadb'"
- Use `requirements_minimal.txt` primeiro
- Se ainda falhar, remova `chromadb` temporariamente

### Erro comum: "No module named 'langchain'"
- Verifique se a versão do Python é 3.9+
- Use versões específicas se necessário

## 📞 Suporte

Se ainda houver problemas:
1. Verifique os logs no Streamlit Cloud
2. Teste localmente primeiro
3. Use o arquivo `requirements_minimal.txt`
4. Abra uma issue no GitHub
