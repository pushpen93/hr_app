import streamlit as st

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "png", "jpg", "jpeg"])



st.set_page_config(layout="wide")
base="dark"
primaryColor="#BF2A7C" #PINK
backgroundColor="#FFFFFF" #MAIN WINDOW BACKGROUND COLOR (white)
secondaryBackgroundColor="#EBF3FC" #SIDEBAR COLOR (light blue)
textColor="#31333F"
secondaryColor="#F0F2F6" #dark_blue
tertiaryColor ="#0810A6"
light_pink = "#CDC9FA"
plot_blue_colour="#0810A6" #vibrant blue for plots


import fitz  # PyMuPDF

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

if uploaded_file is not None:
    # Check file type
    if uploaded_file.type == "application/pdf":
        extracted_text = extract_text_from_pdf(uploaded_file)
    else:  # Assuming image
        extracted_text = extract_text_from_image(uploaded_file)
    
    st.write(extracted_text)
