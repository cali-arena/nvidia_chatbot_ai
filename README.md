# 🤖 NVIDIA AI Chatbot with Document & Image Analysis

A powerful AI chatbot built with Streamlit that integrates NVIDIA AI Endpoints, featuring document processing, image analysis, and a beautiful modern UI.

![NVIDIA AI](https://img.shields.io/badge/NVIDIA-AI-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## ✨ Features

- 🤖 **Multiple NVIDIA AI Models**: Access to Llama 3.1, Mistral, Mixtral, Phi-3, and more
- 📄 **Document Processing**: Upload and analyze PDF, TXT, and DOCX files
- 🖼️ **Image Support**: Upload and reference images in your conversations
- 💬 **Chat History**: Maintains conversation context for natural dialogue
- 🎨 **Modern UI**: Beautiful dark-themed interface with NVIDIA branding
- ⚙️ **Customizable**: Adjust temperature, max tokens, and system prompts
- 📊 **Large Document Support**: Handle large documents and multiple files
- 🔒 **Secure**: API key management with environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NVIDIA API key (get one at [build.nvidia.com](https://build.nvidia.com/))

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd CHAT_BOTS
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your NVIDIA API key:**
   
   Create a `.env` file in the project root:
   ```env
   NVIDIA_API_KEY=nvapi-your-api-key-here
   ```
   
   Or enter it directly in the app sidebar when running.

### Running the App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🎯 Usage

### Getting Your NVIDIA API Key

1. Visit [build.nvidia.com](https://build.nvidia.com/)
2. Sign up or log in
3. Navigate to the API Keys section
4. Generate a new API key
5. Copy and paste it into the app sidebar or `.env` file

### Using the Chatbot

1. **Enter API Key**: Paste your NVIDIA API key in the sidebar
2. **Select Model**: Choose from available NVIDIA AI models
3. **Adjust Settings**: Configure temperature and max tokens
4. **Upload Documents** (optional): Add PDF, TXT, or DOCX files
5. **Upload Images** (optional): Add images for visual reference
6. **Start Chatting**: Ask questions and get AI-powered responses!

### Document Processing

The chatbot can analyze and answer questions about uploaded documents:

```
User: "Summarize the main points from the uploaded document"
AI: [Provides summary based on document content]
```

Supported formats:
- PDF (`.pdf`)
- Text (`.txt`)
- Word (`.docx`)

### Model Selection

Available models include:
- **Llama 3.1 405B**: Most powerful, best for complex tasks
- **Llama 3.1 70B**: Balanced performance and speed
- **Llama 3.1 8B**: Fast responses, good for simple tasks
- **Mistral 7B**: Efficient instruction following
- **Mixtral 8x7B/8x22B**: Mixture of experts models
- **Phi-3 Medium**: Microsoft's efficient model
- **Llama 4 Maverick**: Latest experimental model

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:
```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxx
```

### System Prompt

Customize the AI's behavior by editing the system prompt in the sidebar:
```
You are a helpful AI assistant powered by NVIDIA AI...
```

### Model Parameters

- **Temperature** (0.0-2.0): Controls randomness
  - Lower = More focused and deterministic
  - Higher = More creative and random
  
- **Max Tokens** (128-4096): Maximum response length
  - Higher = Longer responses
  - Lower = Shorter, more concise responses

## 🛠️ Technical Details

### Architecture

```
User Input
    ↓
Streamlit Interface
    ↓
Document/Image Processing
    ↓
LangChain + NVIDIA AI Endpoints
    ↓
Response Generation
    ↓
Display to User
```

### Dependencies

- **Streamlit**: Web interface
- **LangChain**: AI orchestration
- **langchain-nvidia-ai-endpoints**: NVIDIA model integration
- **PyPDF**: PDF processing
- **python-docx**: Word document processing
- **Pillow**: Image processing
- **python-dotenv**: Environment management

### Code Structure

```
CHAT_BOTS/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .env               # API keys (create this)
```

## 📚 Advanced Usage

### API Direct Access

You can also use the NVIDIA API directly:

```python
import requests

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}
payload = {
    "model": "meta/llama-3.1-405b-instruct",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 512,
    "temperature": 0.7
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

### LangChain Integration

Example zero-shot classification:

```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate

chat = ChatNVIDIA(model="mistralai/mistral-7b-instruct-v0.2")
prompt = ChatPromptTemplate.from_template("Classify: {text}")
chain = prompt | chat

result = chain.invoke({"text": "I love flying!"})
```

## 🐛 Troubleshooting

### Common Issues

1. **"Please enter your NVIDIA API key"**
   - Solution: Add your API key in the sidebar or `.env` file

2. **"Error: 401 Unauthorized"**
   - Solution: Check that your API key is valid and active

3. **"Module not found" errors**
   - Solution: Run `pip install -r requirements.txt`

4. **PDF processing fails**
   - Solution: Ensure the PDF is not encrypted or corrupted

5. **Slow responses**
   - Solution: Try a smaller model or reduce max_tokens

### System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB for dependencies
- **Internet**: Required for API calls

## 🔐 Security Notes

- Never commit `.env` files or API keys to version control
- Keep your API key private and secure
- API keys can be regenerated at build.nvidia.com if compromised

## 📝 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve this chatbot! Some ideas:
- Add more document formats (Excel, PowerPoint)
- Implement RAG (Retrieval Augmented Generation)
- Add voice input/output
- Create conversation export feature
- Add more visualization options

## 📞 Support

- NVIDIA AI Documentation: [docs.nvidia.com](https://docs.nvidia.com)
- LangChain Documentation: [python.langchain.com](https://python.langchain.com)
- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)

## 🎉 Acknowledgments

- NVIDIA for providing powerful AI endpoints
- LangChain for excellent AI orchestration tools
- Streamlit for the amazing web framework

---

**Made with ❤️ using NVIDIA AI, LangChain, and Streamlit**

