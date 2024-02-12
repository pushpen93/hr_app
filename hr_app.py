import fitz
import streamlit as st

def extract_text_from_pdf_with_fitz(pdf_file):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()
    return text
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
            text = extract_text_from_pdf_with_fitz(uploaded_file)
            st.text_area("Extracted text", text, height=300)
            extracted_info = extract_entities(text)
            st.write(extracted_info)
    elif file_details["filetype"] in ["image/png", "image/jpeg", "image/jpg"]:
        with st.spinner('Extracting text from image...'):
            text = extract_text_from_image(uploaded_file)
            st.text_area("Extracted text", text, height=300)
            extracted_info = extract_entities(text)
            st.write(extracted_info)
