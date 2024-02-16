
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
col1, col2 = st.columns([1, 3])

with col1:
    # Add empty space to push the uploader to the bottom
    for _ in range(20):  # You might need to adjust this number
        st.empty()

    # Add the file uploader
    st.markdown("**Upload your file**")
    uploaded_file = st.file_uploader("", type=["pdf", "png", "jpg", "jpeg", "docx"])

with col2:
    st.markdown("**Uploaded File Preview**")
    # Placeholder for displaying the PDF or the content
    if uploaded_file is not None:
        # Assuming a PDF is uploaded, display its content
        # This is a placeholder, Streamlit does not have a built-in PDF viewer
        st.markdown("PDF content would be displayed here.")

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

        

