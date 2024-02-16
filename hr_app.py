'''
import streamlit as st

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "png", "jpg", "jpeg"])


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
    
    st.write(extracted_text) '''

import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


# Function to inject custom CSS
def local_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from an image using OCR
def extract_text_from_image(uploaded_file):
    image = Image.open(io.BytesIO(uploaded_file.read()))
    text = pytesseract.image_to_string(image)
    return text


# Custom CSS to inject
custom_css = """
    <style>
        html, body, [class*="st-"] {
            font-family: 'sans-serif';
        }
        .stFileUploader {
            font-Papyrus: bold;
        }
        .stButton>button {
            color: orange;
            border: none;
            padding: 20px 15px ;
            margin: 2px;
            border-radius: 1px;
            background-color: #FDF5E6;
        }
        .stTextArea {
            border: 1px solid #F63366;
        }
    </style>


st.markdown(custom_css, unsafe_allow_html=True)

st.set_page_config(layout="wide")

# Use columns to create a side-by-side layout
col1, col2 = st.columns([1, 3], gap="small")  # Adjust the ratio as needed

with col1:
    # File uploader in the left column
    st.markdown("**Upload your resume**")  # Bold text
    uploaded_file = st.file_uploader("", type=["pdf", "png", "jpg", "jpeg"])

with col2:
    # Display extracted text in the right column
    if uploaded_file is not None:
        # Check file type
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        else:  # Assuming image
            extracted_text = extract_text_from_image(uploaded_file)
        
        # Use a text area with a scrollbar
        st.text_area("", extracted_text, height=400)"""

import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from docx import Document  # For DOCX file handling

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from an image using OCR
def extract_text_from_image(uploaded_file):
    image = Image.open(io.BytesIO(uploaded_file.read()))
    text = pytesseract.image_to_string(image)
    return text

# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Initialize variable to store extracted data
extracted_data = ""

st.set_page_config(layout="wide")

# Use columns to create a side-by-side layout
col1, col2 = st.columns([1, 3], gap="small")

with col1:
    st.markdown("**Upload your file**")
    uploaded_file = st.file_uploader("", type=["pdf", "png", "jpg", "jpeg", "docx"])

# Process the uploaded file and store the extracted text
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        extracted_data = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type.startswith("image/"):
        extracted_data = extract_text_from_image(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted_data = extract_text_from_docx(uploaded_file)
    else:
        st.write("Unsupported file type")

    # Placeholder for the data processing or display section
    # You can choose to display a confirmation message or some metadata about the extracted content
    st.success("Data extracted successfully. Ready for the next steps.")

    # Here you would add the code to insert `extracted_data` into your Snowflake database
    # This is a placeholder for Snowflake database insertion logic
    # connect_to_snowflake()
    # insert_data_into_snowflake(extracted_data)

# Note: This code snippet does not include the actual Snowflake connection and insertion logic.
# You will need to use the Snowflake connector for Python (`snowflake-connector-python`) for database operations.

        

