"""
Integrate free vision models into your NVIDIA chatbot
Replace expensive API calls with local processing
"""

import streamlit as st
from PIL import Image
import io
import base64
import tempfile
import os

class FreeVisionIntegration:
    """Integrate free vision models into Streamlit app"""
    
    def __init__(self):
        self.vision_processor = None
        self.ocr_processor = None
        
    def initialize_easyocr(self):
        """Initialize EasyOCR (recommended for most users)"""
        try:
            import easyocr
            self.ocr_processor = easyocr.Reader(['en', 'pt'], gpu=False)
            return True
        except ImportError:
            st.error("❌ EasyOCR not installed. Run: pip install easyocr")
            return False
        except Exception as e:
            st.error(f"❌ Error loading EasyOCR: {str(e)}")
            return False
    
    def extract_text_easyocr(self, image_file):
        """Extract text using EasyOCR"""
        if not self.ocr_processor:
            return "❌ EasyOCR not initialized"
        
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                image = Image.open(image_file)
                image.save(tmp_file.name, 'JPEG')
                
                # Extract text
                results = self.ocr_processor.readtext(tmp_file.name)
                
                # Clean up
                os.unlink(tmp_file.name)
                
                # Format results
                text_lines = []
                for (bbox, text, confidence) in results:
                    if confidence > 0.5:  # Only high-confidence text
                        text_lines.append(text)
                
                return "\n".join(text_lines) if text_lines else "No clear text detected"
                
        except Exception as e:
            return f"❌ OCR Error: {str(e)}"
    
    def initialize_llava(self):
        """Initialize LLaVA (requires GPU)"""
        try:
            import torch
            from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
            
            if not torch.cuda.is_available():
                st.warning("⚠️ GPU not available. LLaVA will be slow on CPU.")
            
            model_id = "llava-hf/llava-v1.5-7b-hf"
            
            self.processor = LlavaNextProcessor.from_pretrained(model_id)
            self.model = LlavaNextForConditionalGeneration.from_pretrained(
                model_id, 
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            st.success("✅ LLaVA model loaded")
            return True
            
        except ImportError:
            st.error("❌ transformers not installed. Run: pip install transformers torch")
            return False
        except Exception as e:
            st.error(f"❌ Error loading LLaVA: {str(e)}")
            return False
    
    def analyze_image_llava(self, image_file, prompt="Extract all text from this image"):
        """Analyze image with LLaVA"""
        if not self.model or not self.processor:
            return "❌ LLaVA not initialized"
        
        try:
            import torch
            
            # Load image
            image = Image.open(image_file)
            
            # Prepare conversation
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
            
            # Process inputs
            inputs = self.processor.apply_chat_template(
                conversation, 
                tokenize=True, 
                add_generation_prompt=True, 
                return_tensors="pt"
            )
            
            # Generate response
            with torch.no_grad():
                output = self.model.generate(
                    inputs,
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.1
                )
            
            # Decode response
            response = self.processor.decode(output[0], skip_special_tokens=True)
            
            # Extract only the model's response
            if "assistant" in response:
                response = response.split("assistant")[-1].strip()
            
            return response
            
        except Exception as e:
            return f"❌ LLaVA Error: {str(e)}"

# Streamlit integration function
def integrate_free_vision():
    """Add free vision processing to your Streamlit app"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🆓 Free Vision Processing")
    
    # Choose vision method
    vision_method = st.sidebar.selectbox(
        "Choose Vision Method",
        ["EasyOCR (Recommended)", "LLaVA (GPU Required)", "NVIDIA AI (Current)"],
        help="EasyOCR: Fast, no GPU needed. LLaVA: High quality, needs GPU."
    )
    
    # Initialize based on selection
    if vision_method == "EasyOCR (Recommended)":
        if 'easyocr_loaded' not in st.session_state:
            with st.spinner("Loading EasyOCR..."):
                vision = FreeVisionIntegration()
                if vision.initialize_easyocr():
                    st.session_state.easyocr_loaded = True
                    st.session_state.easyocr_processor = vision.ocr_processor
                    st.success("✅ EasyOCR ready!")
                else:
                    st.error("❌ Failed to load EasyOCR")
    
    elif vision_method == "LLaVA (GPU Required)":
        if 'llava_loaded' not in st.session_state:
            with st.spinner("Loading LLaVA (this may take a few minutes)..."):
                vision = FreeVisionIntegration()
                if vision.initialize_llava():
                    st.session_state.llava_loaded = True
                    st.session_state.llava_model = vision.model
                    st.session_state.llava_processor = vision.processor
                    st.success("✅ LLaVA ready!")
                else:
                    st.error("❌ Failed to load LLaVA")
    
    return vision_method

# Modified image processing function
def process_image_with_free_vision(image_file, vision_method):
    """Process image using selected free vision method"""
    
    if vision_method == "EasyOCR (Recommended)":
        if 'easyocr_processor' in st.session_state:
            vision = FreeVisionIntegration()
            vision.ocr_processor = st.session_state.easyocr_processor
            return vision.extract_text_easyocr(image_file)
    
    elif vision_method == "LLaVA (GPU Required)":
        if 'llava_model' in st.session_state:
            vision = FreeVisionIntegration()
            vision.model = st.session_state.llava_model
            vision.processor = st.session_state.llava_processor
            return vision.analyze_image_llava(image_file)
    
    return None

# Example usage in your main app.py:
"""
# Add this to your app.py imports:
from integrate_free_vision import integrate_free_vision, process_image_with_free_vision

# Add this to your sidebar section:
vision_method = integrate_free_vision()

# Modify your image processing section:
if uploaded_images:
    with st.expander("🖼️ Uploaded Images", expanded=True):
        for idx, image_file in enumerate(uploaded_images):
            # ... existing code ...
            
            # Use free vision processing
            if vision_method != "NVIDIA AI (Current)":
                with st.spinner(f"🔍 Analyzing {image_file.name} with {vision_method}..."):
                    free_text = process_image_with_free_vision(image_file, vision_method)
                    if free_text and not free_text.startswith("❌"):
                        st.success(f"📝 Text extracted: {len(free_text)} characters")
                        # Add to context
                        image_text_context += f"\n\nText from {image_file.name}:\n{free_text}"
"""
