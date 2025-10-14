import easyocr
import streamlit as st
from PIL import Image
import numpy as np
from st_copy import copy_button
import pandas as pd

st.markdown("""
<style>
.stApp{
    background:#000000;
    color:whitesmoke
}
</style>            
""",unsafe_allow_html=True)
st.set_page_config(
    page_title="Text Extractor",
    page_icon="📖"
)

st.title("Text Extraction from Image")

uploaded_image = st.file_uploader("Upload an Image",type=['jpeg','png','jpg','svg','webp'])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    image_np = np.array(image)
    reader = easyocr.Reader(['ja','en'])
    st.subheader("Detected text")
    
    texts = []
    
    
    with st.spinner("Extracting text..."):
        results = reader.readtext(image_np)

    st.success("Extraction complete!")
    
    st.subheader("Detected Text:")
    for _, text, _ in results:
        st.write(text)
        texts.append(text)
    
        
    st.text_area("Copy below:", value=texts, height=150)

    copy_button(
        texts,
        tooltip="Click to copy",
        icon="📋"
    )
    
    