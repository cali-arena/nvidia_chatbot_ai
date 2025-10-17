# 📋 Project Overview

## NVIDIA AI Chatbot - Complete Documentation

This document provides a comprehensive overview of the entire project structure and components.

---

## 🎯 Project Goals

Create a production-ready chatbot application that:
- Integrates with NVIDIA AI endpoints
- Processes documents (PDF, TXT, DOCX)
- Analyzes images
- Provides a beautiful, user-friendly interface
- Supports multiple AI models
- Handles large documents efficiently

---

## 📁 Project Structure

```
CHAT_BOTS/
│
├── app.py                  # Main Streamlit application
├── utils.py                # Utility functions for processing
├── config.py               # Configuration settings
├── test_api.py             # API key testing script
│
├── requirements.txt        # Python dependencies
├── README.md              # Full documentation
├── QUICKSTART.md          # Quick start guide
├── PROJECT_OVERVIEW.md    # This file
│
├── examples.ipynb         # Jupyter notebook with examples
│
├── run.bat                # Windows launcher script
├── run.sh                 # Unix/Mac launcher script
│
└── .env                   # Environment variables (create this)
```

---

## 🔧 Core Components

### 1. Main Application (`app.py`)

**Purpose**: The primary Streamlit web interface

**Key Features**:
- Chat interface with message history
- Document upload and processing
- Image upload and display
- Model selection and configuration
- Real-time API interaction
- Beautiful dark-themed UI with NVIDIA branding

**Main Functions**:
- `extract_text_from_pdf()` - Extract text from PDF files
- `extract_text_from_docx()` - Extract text from Word documents
- `extract_text_from_txt()` - Read text files
- `process_document()` - Route documents to appropriate processor
- `encode_image_to_base64()` - Convert images for API
- `get_chat_response()` - Get AI response from NVIDIA models

**Technologies**:
- Streamlit for UI
- LangChain for AI orchestration
- NVIDIA AI Endpoints for models
- Custom CSS for styling

---

### 2. Utilities (`utils.py`)

**Purpose**: Helper functions for document and data processing

**Key Functions**:

| Function | Purpose |
|----------|---------|
| `chunk_text()` | Split large documents into manageable chunks |
| `summarize_document()` | Create document previews |
| `extract_text_from_image()` | OCR for image text extraction |
| `resize_image()` | Optimize image sizes |
| `format_chat_history()` | Format conversation context |
| `estimate_tokens()` | Calculate token usage |
| `validate_api_key()` | Check API key format |
| `get_model_info()` | Get model specifications |
| `format_file_size()` | Human-readable file sizes |

**Use Cases**:
- Processing large documents that exceed token limits
- Extracting text from scanned documents
- Managing chat context efficiently
- Validating user inputs

---

### 3. Configuration (`config.py`)

**Purpose**: Centralized configuration management

**Settings Include**:
- Available AI models
- Default parameters (temperature, tokens, etc.)
- File format support
- UI customization
- Model information database
- Error and success messages
- Use case templates

**Key Constants**:
```python
DEFAULT_MODEL = "meta/llama-3.1-405b-instruct"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024
MAX_FILE_SIZE_MB = 2048
CHUNK_SIZE = 4000
```

---

### 4. API Testing (`test_api.py`)

**Purpose**: Validate API key and connection

**Features**:
- Check if API key exists
- Test API connectivity
- Verify model access
- List available models
- Provide troubleshooting guidance

**Usage**:
```bash
python test_api.py
```

---

### 5. Examples Notebook (`examples.ipynb`)

**Purpose**: Demonstrate various API usage patterns

**Examples Include**:
1. Zero-shot classification with few-shot prompting
2. Direct API calls with requests
3. Simple chat with LangChain
4. Streaming responses
5. Chaining operations
6. Document Q&A
7. Multi-turn conversations
8. Batch processing

---

## 🚀 Available Models

| Model | Parameters | Context | Best For |
|-------|------------|---------|----------|
| Llama 3.1 405B | 405B | 128K | Complex reasoning, coding |
| Llama 3.1 70B | 70B | 128K | Balanced performance |
| Llama 3.1 8B | 8B | 128K | Quick responses |
| Mistral 7B | 7B | 32K | Instructions, classification |
| Mixtral 8x7B | 47B | 32K | Diverse tasks |
| Mixtral 8x22B | 141B | 32K | High-quality output |
| Phi-3 Medium | 14B | 128K | Long context |
| Llama 4 Maverick | 17B | 128K | Experimental features |

---

## 🎨 User Interface

### Layout

```
┌─────────────────────────────────────────────────────────┐
│  Sidebar                  │  Main Chat Area              │
│  ┌────────────────┐      │  ┌──────────────────────┐   │
│  │ API Key Input  │      │  │  Chat History        │   │
│  ├────────────────┤      │  │  [User Messages]     │   │
│  │ Model Settings │      │  │  [AI Responses]      │   │
│  │ - Temperature  │      │  └──────────────────────┘   │
│  │ - Max Tokens   │      │                               │
│  ├────────────────┤      │  ┌──────────────────────┐   │
│  │ System Prompt  │      │  │  Chat Input          │   │
│  ├────────────────┤      │  │  [Type message...]   │   │
│  │ File Uploads   │      │  └──────────────────────┘   │
│  │ - Documents    │      │                               │
│  │ - Images       │      │                               │
│  └────────────────┘      │                               │
└─────────────────────────────────────────────────────────┘
```

### Color Scheme

- **Background**: Dark theme (#0e1117)
- **Accent**: NVIDIA Green (#76b900)
- **User Messages**: #2b313e
- **AI Messages**: #1e2130
- **Text**: White (#ffffff)

---

## 🔄 Data Flow

```
User Input
    ↓
Validate API Key
    ↓
Process Documents/Images (if uploaded)
    ↓
Build Context
    ├─ System Prompt
    ├─ Document Content
    ├─ Chat History
    └─ User Message
    ↓
Send to NVIDIA AI Endpoint
    ↓
Receive Response
    ↓
Display in Chat
    ↓
Update Chat History
```

---

## 📊 Supported File Types

### Documents
- **PDF** (.pdf) - Portable Document Format
- **Text** (.txt) - Plain text files
- **Word** (.docx) - Microsoft Word documents

### Images
- **PNG** (.png) - Portable Network Graphics
- **JPEG** (.jpg, .jpeg) - Joint Photographic Experts Group

### Processing Capabilities
- Extract text from PDFs
- Read formatted Word documents
- Display uploaded images
- OCR text extraction (with pytesseract)
- Handle large files (up to 2GB)

---

## 🔐 Security

### API Key Management
- Stored in environment variables
- Input via sidebar (session-based)
- Never logged or displayed fully
- Can be rotated at build.nvidia.com

### Best Practices
1. Never commit `.env` files
2. Use `.gitignore` for sensitive files
3. Regenerate keys if compromised
4. Use environment-specific keys

---

## 🛠️ Installation & Setup

### Quick Install
```bash
# Navigate to project
cd CHAT_BOTS

# Install dependencies
pip install -r requirements.txt

# Set API key
echo "NVIDIA_API_KEY=nvapi-your-key" > .env

# Test setup
python test_api.py

# Run app
streamlit run app.py
```

### Using Launcher Scripts

**Windows**:
```bash
run.bat
```

**Mac/Linux**:
```bash
chmod +x run.sh
./run.sh
```

---

## 📚 Dependencies

### Core
- `streamlit` - Web framework
- `langchain` - AI orchestration
- `langchain-nvidia-ai-endpoints` - NVIDIA integration
- `python-dotenv` - Environment management

### Document Processing
- `pypdf` - PDF reading
- `python-docx` - Word documents
- `pytesseract` - OCR

### Data Processing
- `pillow` - Image processing
- `pandas` - Data manipulation
- `numpy` - Numerical operations

### AI/ML
- `faiss-cpu` - Vector search
- `tiktoken` - Token counting
- `openai` - Compatible interfaces

---

## 🎓 Usage Examples

### Basic Chat
```python
User: "What is machine learning?"
AI: [Provides detailed explanation]
```

### Document Analysis
```python
1. Upload document.pdf
2. User: "Summarize this document"
3. AI: [Provides summary of document content]
```

### Code Generation
```python
User: "Write a Python function to sort a list"
AI: [Provides code with explanation]
```

### Creative Writing
```python
User: "Write a short story about AI"
AI: [Generates creative story]
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| No API key | Add key in sidebar or `.env` file |
| 401 Error | Invalid API key, regenerate |
| Module not found | Run `pip install -r requirements.txt` |
| Slow responses | Use smaller model (8B or 7B) |
| File won't upload | Check format and size |
| App won't start | Check you're in correct directory |

---

## 📈 Performance Tips

### For Faster Responses
- Use smaller models (Llama 8B, Mistral 7B)
- Reduce `max_tokens`
- Lower `temperature` for more focused output

### For Better Quality
- Use larger models (Llama 405B, Mixtral 8x22B)
- Increase `max_tokens`
- Fine-tune `temperature` for task

### For Large Documents
- Documents are automatically chunked
- Use context-aware prompts
- Ask specific questions

---

## 🚀 Future Enhancements

### Potential Features
- [ ] RAG (Retrieval Augmented Generation)
- [ ] Vector database integration
- [ ] Conversation export (JSON, PDF)
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Custom fine-tuning
- [ ] Analytics dashboard
- [ ] Collaborative sessions

---

## 📞 Support Resources

- **NVIDIA AI**: https://build.nvidia.com/
- **LangChain**: https://python.langchain.com/
- **Streamlit**: https://docs.streamlit.io/

---

## 📝 Version History

### v1.0.0 (Current)
- Initial release
- Full chatbot functionality
- Document and image support
- Multiple model support
- Beautiful UI

---

## 👥 Contributing

To extend this project:
1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

---

## 📄 License

This project is provided as-is for educational and development purposes.

---

**Built with ❤️ using NVIDIA AI, LangChain, and Streamlit**

