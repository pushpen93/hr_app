import streamlit as st

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "png", "jpg", "jpeg"])


import PyMuPDF  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


import pytesseract
from PIL import Image
import io

def extract_text_from_image(uploaded_file):
    image = Image.open(io.BytesIO(uploaded_file.read()))
    text = pytesseract.image_to_string(image)
    return text
