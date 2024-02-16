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
        .st-c9 {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            height: 100%;
        }
        .st-c9 .stFileUploader {
            margin-top: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Use columns to create a side-by-side layout
col1, col2 = st.columns([1, 3])

# Placeholder for the top of the left column
for _ in range(20):  # The range value may need to be adjusted
    col1.empty()

 uploaded_file = st.file_uploader("Upload your file", type=["pdf", "png", "jpg", "jpeg", "docx"])

# Right column for displaying the uploaded file's content or message
with col2:
    if uploaded_file is not None:
        st.success("File uploaded successfully!")

# Process the uploaded file and store the extracted text
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        extracted_data = extract_text_from_pdf(uploaded_file)
        st.write("Extracted Text from PDF:")
        st.write(extracted_data)
    elif uploaded_file.type.startswith("image/"):
        extracted_data = extract_text_from_image(uploaded_file)
        st.write("Extracted Text from Image:")
        st.write(extracted_data)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted_data = extract_text_from_docx(uploaded_file)
        st.write("Extracted Text from DOCX:")
        st.write(extracted_data)
    else:
        st.error("Unsupported file type")

# Placeholder for inserting data into a Snowflake database
# connect_to_snowflake()
# insert_data_into_snowflake(extracted_data)

# Remove the placeholder to collapse the space at the top of the left column
# top_placeholder.empty()
