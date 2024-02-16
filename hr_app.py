import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import spacy  # NLP library
from spacy import displacy

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

# Function to display the candidate's passport-size photo
def display_passport_size_photo(image):
    # Define the size of a passport photo: 2x2 inches with 300 DPI
    passport_size = (600, 600)  # (Width, Height) in pixels
    image = image.resize(passport_size)
    st.image(image, caption="Candidate Photo", use_column_width=False)

# NLP-based information extraction
def extract_information_nlp(text):
    doc = nlp(text)
    # Assuming that the first PERSON entity in the document is the candidate's name
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "Not found")
    email = next((ent.text for ent in doc.ents if ent.label_ == "EMAIL"), "Not found")
    phone = next((ent.text for ent in doc.ents if ent.label_ == "PHONE"), "Not found")
    # Address extraction is more complex, not directly available in spaCy
    address = "Not found"
    return name, email, phone, address

# Main application
def main():
    st.title("Resume Analyzer")
    
    # File uploader in the left column
    uploaded_file = st.file_uploader("Upload your file", type=["pdf", "png", "jpg", "jpeg", "docx"])
    
    # Process the uploaded file and store the extracted text
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            text, images = extract_text_from_pdf(uploaded_file)
            if images:
                # Display the first image as the candidate photo
                display_passport_size_photo(images[0])
            else:
                st.write("No photo found in the PDF.")
        elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
            text = extract_text_from_image(uploaded_file)
        # More conditions for docx or other file types...
        
        # Extract information using NLP
        if text:
            name, email, phone, address = extract_information_nlp(text)
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Mobile Number:** {phone}")
            st.write(f"**Address:** {address}")
        else:
            st.error("Could not extract any information from the file.")
    
    # Visualize the named entities (optional)
    #if text:
    #    doc = nlp(text)
    #    html = displacy.render(doc, style="ent")
    #    st.write(html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
