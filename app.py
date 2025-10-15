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

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

st.title("Text Extraction from Image")

uploaded_image = st.file_uploader("Upload an Image", type=['jpeg','png','jpg','webp'])

if uploaded_image is not None:
    try:
        # Check 1: File size
        if uploaded_image.size == 0:
            st.error("❌ File is empty! Please upload a valid image.")
            st.stop()
        
        # Check 2: File type validation
        valid_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
        if uploaded_image.type not in valid_types:
            st.error(f"❌ Invalid file type: {uploaded_image.type}")
            st.stop()
        
        # Try to open and validate image
        image = Image.open(uploaded_image)
        
        # Check 3: Image dimensions
        width, height = image.size
        if width <= 0 or height <= 0:
            st.error("❌ Corrupted image: Invalid dimensions")
            st.stop()
            
        # Check 4: Try to process image
        image.verify()  # This checks if image data is valid
        
        # If we get here, image is valid - reopen since verify() closes it
        image = Image.open(uploaded_image)
        
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Convert to RGB if needed (for PNG with transparency)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        image_np = np.array(image)
        
        with st.spinner("Extracting text..."):
            results = reader.readtext(image_np)

        st.success("Extraction complete!")
        
        if results:
            texts = [text for _, text, _ in results]
            all_text = "\n".join(texts)
            
            st.subheader("Extracted Text:")
            st.text_area("Copy your text below:", value=all_text, height=200)
        else:
            st.warning("No text detected in the image!")
            
    except Exception as e:
        st.error(f"❌ Invalid image file: {str(e)}")
        st.info("💡 Try uploading a different image file")
else:
    st.info("👆 Please upload an image file to extract text")