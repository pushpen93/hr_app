import streamlit as st
from pdfminer.high_level import extract_text
import spacy
import pytesseract
from PIL import Image
from io import BytesIO
import base64

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    return extract_text(pdf_file)

# Function to extract text from an image using OCR
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

# Function to extract entities using spaCy
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Streamlit interface
st.title("Document AI with Streamlit")

st.write("Upload a PDF or an image to extract information.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_details = {"filename":uploaded_file.name, "filetype":uploaded_file.type,
                    "filesize":uploaded_file.size}
    st.write(file_details)

    if file_details["filetype"] == "application/pdf":
        with st.spinner('Extracting text from PDF...'):
            text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted text", text, height=300)
            extracted_info = extract_entities(text)
            st.write(extracted_info)
    elif file_details["filetype"] in ["image/png", "image/jpeg", "image/jpg"]:
        with st.spinner('Extracting text from image...'):
            text = extract_text_from_image(uploaded_file)
            st.text_area("Extracted text", text, height=300)
            extracted_info = extract_entities(text)
            st.write(extracted_info)

