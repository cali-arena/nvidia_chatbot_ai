"""
Utility functions for NVIDIA AI Chatbot
"""

import io
import base64
from typing import List, Dict, Optional
from PIL import Image
import pytesseract

def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """
    Split text into chunks for processing large documents
    
    Args:
        text: Input text to split
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        # Find the last period or newline before chunk_size to avoid cutting sentences
        if end < text_length:
            last_period = text.rfind('.', start, end)
            last_newline = text.rfind('\n', start, end)
            split_point = max(last_period, last_newline)
            
            if split_point > start:
                end = split_point + 1
        
        chunks.append(text[start:end])
        start = end - overlap if end < text_length else end
    
    return chunks


def summarize_document(text: str, max_length: int = 1000) -> str:
    """
    Create a summary preview of a document
    
    Args:
        text: Full document text
        max_length: Maximum length of summary
        
    Returns:
        Summarized text
    """
    if len(text) <= max_length:
        return text
    
    # Try to break at a sentence
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > max_length * 0.7:  # If we found a period in the last 30%
        return truncated[:last_period + 1] + f"\n\n... ({len(text) - last_period} more characters)"
    
    return truncated + "..."


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract text from an image using OCR
    
    Args:
        image: PIL Image object
        
    Returns:
        Extracted text
    """
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"OCR failed: {str(e)}"


def resize_image(image: Image.Image, max_size: tuple = (1024, 1024)) -> Image.Image:
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: PIL Image object
        max_size: Maximum dimensions (width, height)
        
    Returns:
        Resized image
    """
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image


def format_chat_history(messages: List[Dict[str, str]], max_messages: int = 10) -> str:
    """
    Format chat history for context
    
    Args:
        messages: List of message dictionaries
        max_messages: Maximum number of messages to include
        
    Returns:
        Formatted chat history string
    """
    recent_messages = messages[-max_messages:]
    formatted = []
    
    for msg in recent_messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        formatted.append(f"{role}: {content}")
    
    return "\n\n".join(formatted)


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    # Rough estimate: ~4 characters per token for English
    return len(text) // 4


def validate_api_key(api_key: str) -> bool:
    """
    Validate NVIDIA API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if format is valid
    """
    if not api_key:
        return False
    
    # NVIDIA API keys typically start with 'nvapi-'
    return api_key.startswith('nvapi-') and len(api_key) > 20


def get_model_info(model_name: str) -> Dict[str, any]:
    """
    Get information about a specific model
    
    Args:
        model_name: Name of the model
        
    Returns:
        Dictionary with model information
    """
    model_info = {
        "meta/llama-3.1-405b-instruct": {
            "name": "Llama 3.1 405B",
            "description": "Most powerful Llama model, excellent for complex reasoning",
            "context_length": 128000,
            "best_for": "Complex analysis, coding, reasoning"
        },
        "meta/llama-3.1-70b-instruct": {
            "name": "Llama 3.1 70B",
            "description": "Balanced performance and speed",
            "context_length": 128000,
            "best_for": "General purpose, balanced tasks"
        },
        "meta/llama-3.1-8b-instruct": {
            "name": "Llama 3.1 8B",
            "description": "Fast and efficient for simpler tasks",
            "context_length": 128000,
            "best_for": "Quick responses, simple queries"
        },
        "mistralai/mistral-7b-instruct-v0.2": {
            "name": "Mistral 7B",
            "description": "Efficient instruction-following model",
            "context_length": 32000,
            "best_for": "Instructions, classification"
        },
        "mistralai/mixtral-8x7b-instruct-v0.1": {
            "name": "Mixtral 8x7B",
            "description": "Mixture of experts model",
            "context_length": 32000,
            "best_for": "Diverse tasks, efficient processing"
        },
        "mistralai/mixtral-8x22b-instruct-v0.1": {
            "name": "Mixtral 8x22B",
            "description": "Larger mixture of experts",
            "context_length": 32000,
            "best_for": "Complex tasks, high quality"
        },
        "microsoft/phi-3-medium-128k-instruct": {
            "name": "Phi-3 Medium",
            "description": "Microsoft's efficient model",
            "context_length": 128000,
            "best_for": "Long context, efficiency"
        },
        "meta/llama-4-maverick-17b-128e-instruct": {
            "name": "Llama 4 Maverick",
            "description": "Latest experimental Llama model",
            "context_length": 128000,
            "best_for": "Cutting-edge capabilities"
        }
    }
    
    return model_info.get(model_name, {
        "name": model_name,
        "description": "Model information not available",
        "context_length": 4096,
        "best_for": "General purpose"
    })


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def create_download_link(content: str, filename: str, link_text: str) -> str:
    """
    Create a download link for content
    
    Args:
        content: Content to download
        filename: Name of the file
        link_text: Text for the download link
        
    Returns:
        HTML download link
    """
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'

