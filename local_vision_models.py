"""
Local Vision Models for Image Analysis
Free alternatives to expensive cloud APIs
"""

import torch
from PIL import Image
import requests
from io import BytesIO
import base64

class LocalVisionProcessor:
    """Free local vision model processor"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        
    def load_llava_model(self):
        """Load LLaVA model (free, open-source)"""
        try:
            from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
            
            model_id = "llava-hf/llava-v1.6-mistral-7b-hf"  # Free model
            
            self.processor = LlavaNextProcessor.from_pretrained(model_id)
            self.model = LlavaNextForConditionalGeneration.from_pretrained(
                model_id, 
                torch_dtype=torch.float16, 
                low_cpu_mem_usage=True,
                device_map="auto"
            )
            
            print(f"✅ LLaVA model loaded on {self.device}")
            return True
            
        except ImportError:
            print("❌ transformers library not installed")
            return False
        except Exception as e:
            print(f"❌ Error loading LLaVA: {str(e)}")
            return False
    
    def load_llava_light(self):
        """Load lighter LLaVA model"""
        try:
            from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
            
            model_id = "llava-hf/llava-v1.5-7b-hf"  # Smaller model
            
            self.processor = LlavaNextProcessor.from_pretrained(model_id)
            self.model = LlavaNextForConditionalGeneration.from_pretrained(
                model_id, 
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            print(f"✅ LLaVA Light model loaded on {self.device}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading LLaVA Light: {str(e)}")
            return False
    
    def analyze_image(self, image_path_or_url, prompt="Describe this image in detail"):
        """Analyze image with local model"""
        if not self.model or not self.processor:
            return "❌ Model not loaded"
        
        try:
            # Load image
            if image_path_or_url.startswith('http'):
                response = requests.get(image_path_or_url)
                image = Image.open(BytesIO(response.content))
            else:
                image = Image.open(image_path_or_url)
            
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
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                output = self.model.generate(
                    inputs,
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.1,
                    use_cache=True
                )
            
            # Decode response
            response = self.processor.decode(output[0], skip_special_tokens=True)
            
            # Extract only the model's response
            if "assistant" in response:
                response = response.split("assistant")[-1].strip()
            
            return response
            
        except Exception as e:
            return f"❌ Analysis error: {str(e)}"

# Alternative: Use Qwen-VL (Free, very good for text extraction)
class QwenVisionProcessor:
    """Qwen-VL for text extraction from images"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        
    def load_qwen_model(self):
        """Load Qwen-VL model"""
        try:
            from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer
            
            model_id = "Qwen/Qwen2-VL-2B-Instruct"  # Free, lightweight
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            print("✅ Qwen-VL model loaded")
            return True
            
        except Exception as e:
            print(f"❌ Error loading Qwen-VL: {str(e)}")
            return False
    
    def extract_text_from_image(self, image_path):
        """Extract text from image"""
        if not self.model:
            return "❌ Model not loaded"
        
        try:
            from PIL import Image
            
            image = Image.open(image_path)
            
            # Create prompt for text extraction
            prompt = "Extract all text from this image. Include numbers, tables, and any written content."
            
            # Prepare inputs
            query = self.tokenizer.from_list_format([
                {'image': image},
                {'text': prompt}
            ])
            
            # Generate response
            response, history = self.model.chat(
                self.tokenizer, 
                query=query, 
                history=None
            )
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Simple OCR alternative using EasyOCR (Free, no GPU required)
class EasyOCRProcessor:
    """EasyOCR for simple text extraction"""
    
    def __init__(self):
        self.reader = None
        
    def load_easyocr(self):
        """Load EasyOCR"""
        try:
            import easyocr
            self.reader = easyocr.Reader(['en', 'pt'])  # English and Portuguese
            print("✅ EasyOCR loaded")
            return True
        except ImportError:
            print("❌ EasyOCR not installed. Run: pip install easyocr")
            return False
        except Exception as e:
            print(f"❌ Error loading EasyOCR: {str(e)}")
            return False
    
    def extract_text(self, image_path):
        """Extract text using EasyOCR"""
        if not self.reader:
            return "❌ EasyOCR not loaded"
        
        try:
            results = self.reader.readtext(image_path)
            
            # Format results
            text_lines = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Only high-confidence text
                    text_lines.append(text)
            
            return "\n".join(text_lines)
            
        except Exception as e:
            return f"❌ OCR Error: {str(e)}"

# Usage examples
if __name__ == "__main__":
    print("=== Local Vision Models Demo ===")
    
    # Option 1: LLaVA (Best quality, needs GPU)
    print("\n1. Loading LLaVA...")
    llava = LocalVisionProcessor()
    if llava.load_llava_light():
        result = llava.analyze_image("test_image.jpg", "Read all text in this image")
        print(f"LLaVA Result: {result}")
    
    # Option 2: EasyOCR (Simple, no GPU needed)
    print("\n2. Loading EasyOCR...")
    ocr = EasyOCRProcessor()
    if ocr.load_easyocr():
        result = ocr.extract_text("test_image.jpg")
        print(f"EasyOCR Result: {result}")
    
    # Option 3: Qwen-VL (Good balance)
    print("\n3. Loading Qwen-VL...")
    qwen = QwenVisionProcessor()
    if qwen.load_qwen_model():
        result = qwen.extract_text_from_image("test_image.jpg")
        print(f"Qwen Result: {result}")
