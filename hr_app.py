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

# Initialize variable to store extracted data
extracted_data = ""

# Set the page configuration to use a wide layout
st.set_page_config(layout="wide")

# Custom CSS to attempt to align the file uploader at the bottom left
st.markdown("""
    <style>
        .css-1l02zno {
            flex-direction: column;
            display: flex;
            justify-content: space-between;
        }
        .css-1l02zno > div:first-child {
            flex: 1 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Use columns to create a side-by-side layout
col1, col2 = st.columns([1, 3])

# Placeholder to push the uploader to the bottom of the left column
spacer = col1.empty()
uploaded_file = col1.file_uploader("Upload your file", type=["pdf", "png", "jpg", "jpeg", "docx"])
spacer.empty()  # This will remove the placeholder and push the uploader to the bottom

# Right column for displaying the uploaded file's content or message
with col2:
    st.write("Content or instructions will appear here.")

# Process the uploaded file and store the extracted text
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        extracted_data = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type.startswith("image/"):
        extracted_data = extract_text_from_image(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted_data = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type")

    # At this point, `extracted_data` contains the text extracted from the uploaded file
    # You can now insert this data into your Snowflake database
    # The actual insertion code will depend on your Snowflake setup and is not shown here

# The rest of your app logic would go here
