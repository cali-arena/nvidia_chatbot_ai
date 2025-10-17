# 🚀 Quick Start Guide

Get your NVIDIA AI Chatbot running in 5 minutes!

## Step 1: Get Your NVIDIA API Key

1. Go to [build.nvidia.com](https://build.nvidia.com/)
2. Sign up or log in with your NVIDIA account
3. Navigate to the **API Keys** section
4. Click **Generate API Key**
5. Copy your API key (starts with `nvapi-`)

## Step 2: Install Dependencies

Open your terminal and run:

```bash
cd CHAT_BOTS
pip install -r requirements.txt
```

**Note**: This will install all necessary packages including:
- Streamlit (for the web interface)
- LangChain (for AI orchestration)
- NVIDIA AI Endpoints (for model access)
- Document processing libraries (PDF, DOCX)
- Image processing tools

## Step 3: Run the App

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Step 4: Configure Your API Key

Once the app opens:

1. Look at the **left sidebar**
2. Find the **"NVIDIA API Key"** text input
3. Paste your API key (from Step 1)
4. You should see a green ✅ "API Key configured" message

## Step 5: Start Chatting!

You're ready! Try these example prompts:

### Basic Chat
```
What is machine learning?
```

### With Documents
1. Click **"Upload documents"** in the sidebar
2. Upload a PDF, TXT, or DOCX file
3. Ask: "Summarize the main points from this document"

### With Images
1. Click **"Upload images"** in the sidebar
2. Upload an image (PNG, JPG, JPEG)
3. Ask: "What can you tell me about the uploaded image?"

### Code Help
```
Write a Python function to sort a list of dictionaries by a specific key
```

### Creative Tasks
```
Write a short story about a robot learning to paint
```

## Tips for Best Results

### 1. Choose the Right Model

Different models excel at different tasks:

| Model | Best For | Speed |
|-------|----------|-------|
| Llama 3.1 405B | Complex reasoning, coding | Slower |
| Llama 3.1 70B | General purpose, balanced | Medium |
| Llama 3.1 8B | Quick questions, simple tasks | Fast |
| Mistral 7B | Classification, instructions | Fast |
| Mixtral 8x22B | Complex multi-step tasks | Medium |

### 2. Adjust Temperature

- **Low (0.0-0.3)**: Focused, deterministic, good for factual questions
- **Medium (0.4-0.8)**: Balanced, good for most tasks
- **High (0.9-2.0)**: Creative, random, good for storytelling

### 3. Use System Prompts

Customize the AI's behavior:

```
You are an expert Python programmer. Provide code examples with explanations.
```

```
You are a friendly tutor. Explain concepts in simple terms suitable for beginners.
```

```
You are a professional editor. Review text for grammar, clarity, and style.
```

## Common Use Cases

### 📄 Document Analysis

```python
1. Upload your PDF/DOCX
2. Ask: "What are the key takeaways from this document?"
3. Follow up: "Can you create a bullet-point summary?"
```

### 💻 Code Assistant

```
1. Ask: "Write a Python function to validate email addresses"
2. Follow up: "Add error handling and unit tests"
3. Follow up: "Explain how the regex pattern works"
```

### 📊 Data Processing

```
1. Ask: "Generate Python code to analyze a CSV file"
2. Follow up: "Add data visualization with matplotlib"
3. Follow up: "Export results to Excel"
```

### ✍️ Content Creation

```
1. Ask: "Write a blog post about renewable energy"
2. Follow up: "Make it more engaging with statistics"
3. Follow up: "Add a compelling introduction"
```

### 🔍 Research Assistant

```
1. Upload multiple research papers (PDF)
2. Ask: "Compare the methodologies used in these papers"
3. Follow up: "What are the common findings?"
```

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line in message
- **Ctrl/Cmd + K**: Focus on chat input

## Troubleshooting

### "Please enter your NVIDIA API key"
→ Make sure you've pasted your API key in the sidebar

### "Error: 401 Unauthorized"
→ Your API key is invalid. Get a new one from build.nvidia.com

### "ModuleNotFoundError"
→ Run: `pip install -r requirements.txt`

### App won't start
→ Make sure you're in the correct directory: `cd CHAT_BOTS`

### Slow responses
→ Try a smaller model (Llama 3.1 8B or Mistral 7B)

### Document won't upload
→ Check file format (PDF, TXT, DOCX) and size (< 2GB)

## Advanced Features

### Environment Variables

Create a `.env` file for permanent configuration:

```env
NVIDIA_API_KEY=nvapi-your-key-here
```

### Using Jupyter Notebooks

Check out `examples.ipynb` for code examples:

```bash
jupyter notebook examples.ipynb
```

### Programmatic Access

Use the utilities in `utils.py`:

```python
from utils import chunk_text, get_model_info

# Chunk large documents
chunks = chunk_text(large_text, chunk_size=4000)

# Get model details
info = get_model_info("meta/llama-3.1-405b-instruct")
print(info['best_for'])  # "Complex analysis, coding, reasoning"
```

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 📓 Explore [examples.ipynb](examples.ipynb) for code samples
- 🛠️ Check out [utils.py](utils.py) for helper functions
- 🌐 Visit [build.nvidia.com](https://build.nvidia.com/) for API documentation

## Need Help?

- **NVIDIA AI Docs**: [docs.nvidia.com/ai](https://docs.nvidia.com)
- **LangChain Docs**: [python.langchain.com](https://python.langchain.com)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)

---

**Happy chatting! 🤖**

