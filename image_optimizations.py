def extract_text_easyocr_fast(image_file) -> str:
    """Extract text using EasyOCR (OTIMIZADO - sem loading messages)"""
    try:
        import easyocr
        
        # Initialize reader (only once) - SEM SPINNER
        if 'easyocr_reader' not in st.session_state:
            st.session_state.easyocr_reader = easyocr.Reader(['en', 'pt'], gpu=False)
        
        # Process image directly without saving to temp file
        image = Image.open(image_file)
        
        # Convert RGBA to RGB if necessary (remove transparency)
        if image.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert PIL image to numpy array for EasyOCR
        import numpy as np
        image_array = np.array(image)
        
        # Extract text directly from image array
        results = st.session_state.easyocr_reader.readtext(image_array)
        
        # Format results
        extracted_text = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # Only high-confidence text
                extracted_text.append(text)
        
        return "\n".join(extracted_text) if extracted_text else "No clear text detected"
            
    except ImportError:
        return "❌ EasyOCR not installed. Run: pip install easyocr"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def process_images_fast(uploaded_images):
    """Processa imagens de forma rápida e silenciosa"""
    image_context = ""
    
    for image_file in uploaded_images:
        # OCR rápido sem mensagens
        ocr_text = extract_text_easyocr_fast(image_file)
        
        if ocr_text and ocr_text != "No clear text detected":
            # Análise rápida com IA
            try:
                analysis_prompt = f"""Analise rapidamente este texto extraído de uma imagem:

{ocr_text}

Forneça uma análise concisa e útil do conteúdo encontrado na imagem."""
                
                # Usar configuração rápida
                config = {
                    "model": "meta/llama-3.1-8b-instruct",  # Modelo mais rápido
                    "temperature": 0.3,
                    "max_tokens": 300,  # Resposta mais curta
                    "system_prompt": "Seja conciso e direto na análise."
                }
                
                # Gerar análise rápida
                from app import get_chat_response
                ai_analysis = get_chat_response(
                    user_message=analysis_prompt,
                    chat_history=[],
                    context="",
                    images=None
                )
                
                # Armazenar contexto
                image_context += f"\n\n--- ANÁLISE RÁPIDA {image_file.name} ---\nTexto: {ocr_text}\nAnálise: {ai_analysis}"
                
            except Exception as e:
                # Fallback: apenas OCR
                image_context += f"\n\nImagem {image_file.name}: {ocr_text}"
    
    return image_context

def optimize_image_processing():
    """Otimizações para processamento de imagens"""
    
    # Configurações otimizadas
    optimized_settings = {
        "max_image_size": (800, 800),  # Redimensionar para processamento mais rápido
        "compression_quality": 75,  # Qualidade reduzida para velocidade
        "skip_low_confidence": True,  # Pular texto com baixa confiança
        "parallel_processing": False,  # Processamento sequencial mais estável
        "cache_results": True,  # Cache de resultados OCR
        "fast_model": "meta/llama-3.1-8b-instruct"  # Modelo mais rápido para análise
    }
    
    return optimized_settings
