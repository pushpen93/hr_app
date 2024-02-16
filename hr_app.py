import streamlit as st
import fitz  # PyMuPDF for PDF handling
import pytesseract
from PIL import Image
import io
from docx import Document  # For DOCX file handling
import re  # Regular expressions for text processing

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    images = []
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
            # Extract images
            image_list = page.get_images(full=True)
            for image_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                # Convert bytes to PIL Image
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)
    return text, images

# Function to extract basic information from text
def extract_basic_info(text):
    # Regular expressions for finding names, emails, mobile numbers, and addresses could be improved based on your data
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone = re.search(r'\b\d{10}\b', text)  # Adjust pattern according to the expected format
    # Placeholder for name and address extraction, could use NLP or more specific regex
    name = "John Doe"  # Placeholder, extracting names accurately may require NLP techniques
    address = "123 Main St, City, Country"  # Placeholder, extracting addresses accurately is complex
    return name, email.group(0) if email else "Not found", phone.group(0) if phone else "Not found", address

# Function to display the candidate's photo
def display_candidate_photo(images):
    if images:
        for image in images:
            st.image(image, caption="Candidate Photo", use_column_width=True)
    else:
        st.write("No photo found in the PDF.")

# Set the page configuration to use a wide layout
st.set_page_config(layout="wide")

# Use columns to create a side-by-side layout
col1, col2 = st.columns([1, 3])

# File uploader in the left column
uploaded_file = col1.file_uploader("Upload your file", type=["pdf", "png", "jpg", "jpeg", "docx"])

# Process the uploaded file and store the extracted text
if uploaded_file is not None:
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        extracted_text, images = extract_text_from_pdf(uploaded_file)
        display_candidate_photo(images)
    elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
        extracted_text = extract_text_from_image(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type")
        extracted_text = ""
    
    if extracted_text:
        name, email, phone, address = extract_basic_info(extracted_text)
        with col2:
            st.header("Candidate Basic Information")
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Mobile Number:** {phone}")
            st.write(f"**Address:** {address}")
        col1.success("File uploaded and processed successfully!")
    else:
        col1.error("Failed to extract information. Please try again with a different file.")
else:
    col1.write("Please upload a file to begin.")
