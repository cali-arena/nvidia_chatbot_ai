"""
Simple Free Vision Integration for NVIDIA Chatbot
Easy to add to your existing app
"""

import streamlit as st
from PIL import Image
import tempfile
import os

def setup_free_vision():
    """Setup free vision processing options"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🆓 Free Vision Options")
    
    # Vision method selection
    vision_method = st.sidebar.radio(
        "Choose Vision Method:",
        ["EasyOCR (Free, No GPU)", "NVIDIA AI (Current)"],
        help="EasyOCR: Free text extraction. NVIDIA AI: Full image analysis."
    )
    
    return vision_method

def extract_text_easyocr(image_file):
    """Extract text using EasyOCR (free, no GPU needed)"""
    try:
        import easyocr
        
        # Initialize reader (only once)
        if 'easyocr_reader' not in st.session_state:
            with st.spinner("Loading EasyOCR (first time only)..."):
                st.session_state.easyocr_reader = easyocr.Reader(['en', 'pt'], gpu=False)
        
        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            image = Image.open(image_file)
            image.save(tmp_file.name, 'JPEG')
            
            # Extract text
            results = st.session_state.easyocr_reader.readtext(tmp_file.name)
            
            # Clean up
            os.unlink(tmp_file.name)
            
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

# How to integrate into your existing app.py:

"""
STEP 1: Add to your imports at the top of app.py:
from simple_free_vision import setup_free_vision, extract_text_easyocr

STEP 2: Add this line in your sidebar section (around line 100):
vision_method = setup_free_vision()

STEP 3: Replace your image processing section with this:

# Process uploaded images
image_context = []
image_text_context = ""
if uploaded_images:
    with st.expander("🖼️ Uploaded Images", expanded=True):
        cols = st.columns(3)
        for idx, image_file in enumerate(uploaded_images):
            with cols[idx % 3]:
                image = Image.open(image_file)
                st.image(image, caption=image_file.name, use_container_width=True)
                st.write(f"**{image_file.name}**")
                st.write(f"Size: {image.size[0]}x{image.size[1]}")
                
                # Process based on selected method
                if vision_method == "EasyOCR (Free, No GPU)":
                    # Use free EasyOCR
                    with st.spinner(f"🔍 Extracting text with EasyOCR..."):
                        ocr_text = extract_text_easyocr(image_file)
                        if ocr_text and not ocr_text.startswith("❌"):
                            image_text_context += f"\n\nText from {image_file.name}:\n{ocr_text}"
                            st.success(f"📝 Text extracted: {len(ocr_text)} characters")
                            
                            # Show extracted text
                            with st.expander(f"📄 Extracted text"):
                                st.text_area("OCR Result", ocr_text, height=150, disabled=True)
                        else:
                            st.error(ocr_text)
                
                else:  # NVIDIA AI method
                    # Your existing NVIDIA AI code here
                    encoded_image = encode_image_to_base64(image_file)
                    if encoded_image and not encoded_image.startswith("Error"):
                        image_context.append(encoded_image)
                        st.success(f"✅ {image_file.name} ready for AI analysis")
                        
                        # AI analysis code...
"""

if __name__ == "__main__":
    print("""
    🆓 Free Vision Integration for NVIDIA Chatbot
    
    Benefits:
    ✅ EasyOCR: Free, no GPU needed, fast text extraction
    ✅ Works offline
    ✅ No API costs
    ✅ Supports multiple languages
    
    Installation:
    pip install easyocr
    
    Integration:
    Just copy the code above into your app.py!
    """)
