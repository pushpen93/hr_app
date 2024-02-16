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
    doc = Document(io.BytesIO(uploaded_file.read()))
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Set the page configuration to use a wide layout
st.set_page_config(layout="wide")

# Custom CSS to attempt to align the file uploader at the bottom left
# and to make the left column appear "frozen"
st.markdown("""
    <style>
        .css-1l02zno {
            flex-direction: column;
            display: flex;
            justify-content: space-between;
        }
        .css-1l02zno > div:first-child {
            flex: 1 !important;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }
        .css-1l02zno > div:first-child > div {
            margin-bottom: -1.5rem;  /* Adjust this value as needed */
        }
        .st-c9 {
            display: flex;
            flex-direction: column;
            height: 100vh;  /* Set the height of the left column to fill the screen height */
            overflow-y: auto;  /* Enable scrolling if content overflows */
        }
    </style>
""", unsafe_allow_html=True)

# Use columns to create a side-by-side layout
col1, col2 = st.columns([1, 3])

# Placeholder to push the uploader to the bottom of the left column
spacer = col1.empty()

# File uploader in the left column
uploaded_file = col1.file_uploader("Upload your file", type=["pdf", "png", "jpg", "jpeg", "docx"])

# Variable to check if a file is uploaded successfully
file_uploaded = False

# Right column for displaying the uploaded file's content or message
with col2:
    # This section will be scrollable due to the content size
    # Add your visualizations or any other elements here
    pass

# Process the uploaded file and store the extracted text
if uploaded_file is not None:
    file_uploaded = True
    # Process the uploaded file based on its type
    # ... (Processing logic goes here)

# Add a success message at the bottom if a file is uploaded
if file_uploaded:
    col1.success("File uploaded successfully!")

st.write(uploaded_file)

# This line removes the placeholder, pushing the file uploader to the bottom.
# Remove the comment if you want the uploader at the bottom from the start.
# spacer.empty()
