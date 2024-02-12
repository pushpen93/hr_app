import streamlit as st

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "png", "jpg", "jpeg"])
