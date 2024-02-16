import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import spacy  # NLP library
import re  # For regex

# Load the pre-trained NLP model
nlp = spacy.load('en_core_web_sm')

# Set the page configuration to use a wide layout
st.set_page_config(layout="wide")

def extract_text_from_pdf(uploaded_file):
    text = ""
    images = []
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                images.append(Image.open(io.BytesIO(image_bytes)))
    return text, images

# Function to display the candidate's photo with a smaller size
def display_candidate_photo(image):
    # Define the size of a passport photo: 2x2 inches at 300 DPI
    passport_size = (150, 150)  # Resize to 150x150 pixels
    image = image.resize(passport_size, Image.ANTIALIAS)
    st.image(image, caption="Candidate Photo")

def extract_text_from_image(uploaded_file):
    image = Image.open(io.BytesIO(uploaded_file.read()))
    text = pytesseract.image_to_string(image)
    return text

# NLP-based information extraction with regex for email and phone
def extract_information_nlp(text):
    doc = nlp(text)
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "Not found")
    
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'\b\d{10}\b|\(\d{3}\)\s*\d{3}[-\s]*\d{4}')
    
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    
    email = email.group(0) if email else "Not found"
    phone = phone.group(0) if phone else "Not found"
    address = "Not found"  # Address extraction remains complex
    
    return name, email, phone, address

# Main application
def main():
    st.title("Resume Analyzer")
    
    uploaded_file = st.file_uploader("Upload your file", type=["pdf", "png", "jpg", "jpeg", "docx"])
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            text, images = extract_text_from_pdf(uploaded_file)
            if images:
                display_candidate_photo(images[0])
            else:
                st.write("No photo found in the PDF.")
        elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
            uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            text = extract_text_from_image(uploaded_file)
            display_candidate_photo(image)
        
        if text:
            name, email, phone, address = extract_information_nlp(text)
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Mobile Number:** {phone}")
            st.write(f"**Address:** {address}")
        else:
            st.error("Could not extract any information from the file.")

if __name__ == "__main__":
    main()
