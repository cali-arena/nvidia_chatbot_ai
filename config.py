"""
Configuration settings for NVIDIA AI Chatbot
"""

import os
from typing import Dict, List

# API Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
API_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Available Models
AVAILABLE_MODELS = [
    "meta/llama-3.1-405b-instruct",
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct-v0.2",
    "mistralai/mixtral-8x7b-instruct-v0.1",
    "mistralai/mixtral-8x22b-instruct-v0.1",
    "microsoft/phi-3-medium-128k-instruct",
    "meta/llama-4-maverick-17b-128e-instruct"
]

# Default Model Settings
DEFAULT_MODEL = "meta/llama-3.1-405b-instruct"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TOP_P = 1.0

# Document Processing Settings
MAX_FILE_SIZE_MB = 200
CHUNK_SIZE = 4000
CHUNK_OVERLAP = 200

SUPPORTED_DOC_FORMATS = ["pdf", "txt", "docx"]
SUPPORTED_IMAGE_FORMATS = ["png", "jpg", "jpeg"]

# Chat Settings
MAX_CHAT_HISTORY = 50
MAX_CONTEXT_MESSAGES = 10

# UI Settings
APP_TITLE = "NVIDIA AI Chatbot"
APP_ICON = "🤖"
PAGE_LAYOUT = "wide"

# Default System Prompt
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant powered by NVIDIA AI. You can analyze documents, images, and answer questions accurately and concisely. You provide detailed explanations when needed and can help with coding, writing, analysis, and creative tasks."""

# Model Information
MODEL_INFO: Dict[str, Dict] = {
    "meta/llama-3.1-405b-instruct": {
        "name": "Llama 3.1 405B",
        "description": "Most powerful Llama model, excellent for complex reasoning",
        "context_length": 128000,
        "best_for": "Complex analysis, coding, reasoning",
        "speed": "slower",
        "quality": "highest"
    },
    "meta/llama-3.1-70b-instruct": {
        "name": "Llama 3.1 70B",
        "description": "Balanced performance and speed",
        "context_length": 128000,
        "best_for": "General purpose, balanced tasks",
        "speed": "medium",
        "quality": "high"
    },
    "meta/llama-3.1-8b-instruct": {
        "name": "Llama 3.1 8B",
        "description": "Fast and efficient for simpler tasks",
        "context_length": 128000,
        "best_for": "Quick responses, simple queries",
        "speed": "fast",
        "quality": "good"
    },
    "mistralai/mistral-7b-instruct-v0.2": {
        "name": "Mistral 7B",
        "description": "Efficient instruction-following model",
        "context_length": 32000,
        "best_for": "Instructions, classification",
        "speed": "fast",
        "quality": "good"
    },
    "mistralai/mixtral-8x7b-instruct-v0.1": {
        "name": "Mixtral 8x7B",
        "description": "Mixture of experts model",
        "context_length": 32000,
        "best_for": "Diverse tasks, efficient processing",
        "speed": "medium",
        "quality": "high"
    },
    "mistralai/mixtral-8x22b-instruct-v0.1": {
        "name": "Mixtral 8x22B",
        "description": "Larger mixture of experts",
        "context_length": 32000,
        "best_for": "Complex tasks, high quality",
        "speed": "medium",
        "quality": "very high"
    },
    "microsoft/phi-3-medium-128k-instruct": {
        "name": "Phi-3 Medium",
        "description": "Microsoft's efficient model",
        "context_length": 128000,
        "best_for": "Long context, efficiency",
        "speed": "fast",
        "quality": "good"
    },
    "meta/llama-4-maverick-17b-128e-instruct": {
        "name": "Llama 4 Maverick",
        "description": "Latest experimental Llama model",
        "context_length": 128000,
        "best_for": "Cutting-edge capabilities",
        "speed": "medium",
        "quality": "experimental"
    }
}

# Temperature Presets
TEMPERATURE_PRESETS = {
    "precise": 0.1,
    "balanced": 0.7,
    "creative": 1.2
}

# Use Case Templates
USE_CASE_PROMPTS = {
    "code_assistant": """You are an expert programmer. Provide clean, well-documented code with explanations. Include error handling and best practices.""",
    
    "tutor": """You are a patient and knowledgeable tutor. Explain concepts clearly using simple language and examples. Break down complex topics into easy-to-understand parts.""",
    
    "writer": """You are a professional writer and editor. Create engaging, well-structured content. Use varied sentence structures and vivid language.""",
    
    "analyst": """You are a data analyst and researcher. Provide thorough analysis with insights and recommendations. Use data-driven reasoning.""",
    
    "creative": """You are a creative storyteller. Write engaging narratives with vivid descriptions and compelling characters. Use your imagination freely.""",
}

# Error Messages
ERROR_MESSAGES = {
    "no_api_key": "⚠️ Please enter your NVIDIA API key in the sidebar.",
    "invalid_api_key": "❌ Invalid API key. Please check and try again.",
    "api_error": "⚠️ API error: {error}. Please try again.",
    "file_too_large": "⚠️ File too large. Maximum size is {max_size}MB.",
    "unsupported_format": "⚠️ Unsupported file format. Supported formats: {formats}",
    "processing_error": "⚠️ Error processing file: {error}",
}

# Success Messages
SUCCESS_MESSAGES = {
    "api_key_set": "✅ API Key configured",
    "file_processed": "✅ Processed {filename}",
    "chat_cleared": "✅ Chat history cleared",
}

def get_model_info(model_name: str) -> Dict:
    """Get information about a specific model"""
    return MODEL_INFO.get(model_name, {
        "name": model_name,
        "description": "Model information not available",
        "context_length": 4096,
        "best_for": "General purpose",
        "speed": "unknown",
        "quality": "unknown"
    })

def validate_file_size(file_size: int) -> bool:
    """Check if file size is within limits"""
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    return file_size <= max_size_bytes

def get_supported_formats() -> Dict[str, List[str]]:
    """Get all supported file formats"""
    return {
        "documents": SUPPORTED_DOC_FORMATS,
        "images": SUPPORTED_IMAGE_FORMATS
    }

