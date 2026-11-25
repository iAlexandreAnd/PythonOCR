import easyocr
import numpy as np
import streamlit as st
from PIL import Image

st.title("Simple OCR")
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image")

    if st.button("Scan text"):
        reader = get_reader()
        results = reader.readtext(np.array(image))
        text = "\n".join(item[1] for item in results)

        if text:
            st.text_area("Recognized text", text, height=200)
        else:
            st.info("No text was detected.")