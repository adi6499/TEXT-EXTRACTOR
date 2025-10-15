import easyocr
import streamlit as st
from PIL import Image
import numpy as np

st.markdown("""
<style>
.stApp{
    background:#000000;
    color:whitesmoke
}
</style>            
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Text Extractor",
    page_icon="📖"
)

# Initialize EasyOCR once
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

st.title("Text Extraction from Image")

uploaded_image = st.file_uploader("Upload an Image", type=['jpeg','png','jpg','svg','webp'])

if uploaded_image is not None:
    try:
        image = Image.open(uploaded_image)
        
        # Resize very large images
        if image.size[0] > 2000 or image.size[1] > 2000:
            image = image.resize((1500, 1500))
        
        st.image(image, caption="Uploaded Image", width=True)
        image_np = np.array(image)
        
        texts = []
        
        with st.spinner("Extracting text..."):
            results = reader.readtext(image_np)

        st.success("Extraction complete!")
        
        if results:
            # Extract just the text, no confidence scores
            for _, text, _ in results:
                texts.append(text)
            
            # Combine all text
            all_text = "\n".join(texts)
            
            st.subheader("Extracted Text:")
            st.text_area("Copy your text below:", value=all_text, height=200)

        else:
            st.warning("No text detected in the image!")
            
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
else:
    st.info("👆 Please upload an image file to extract text")