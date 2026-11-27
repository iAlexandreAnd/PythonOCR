import easyocr
import numpy as np
import streamlit as st
from PIL import Image

from ocr_visualization import annotate_results

st.title("Simple OCR")
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    if st.button("Scan text"):
        reader = get_reader()
        results = reader.readtext(np.array(image))

        original_column, annotated_column = st.columns(2)
        with original_column:
            st.image(image, caption="Original image", use_container_width=True)
        with annotated_column:
            st.image(
                annotate_results(image, results),
                caption="Detected text regions",
                use_container_width=True,
            )

        if results:
            st.subheader("Recognized regions")
            for index, (_, text, confidence) in enumerate(results, start=1):
                st.markdown(f"**Region {index}** — confidence: {confidence:.2f}")
                st.text(text)
        else:
            st.info("No text was detected.")
    else:
        st.image(image, caption="Uploaded image")