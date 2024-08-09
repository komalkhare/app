import streamlit as st
import os
from db_setup import init_db, create_session, add_document, generate_key, get_document
from cryptography.fernet import Fernet

# Load the encryption key from an environment variable
encryption_key = os.getenv("ENCRYPTION_KEY")
if not encryption_key:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

try:
    fernet = Fernet(encryption_key)
except ValueError:
    raise ValueError("Invalid ENCRYPTION_KEY. It must be a 32-byte URL-safe base64-encoded key.")

# Initialize database and session
engine = init_db()
session = create_session(engine)

# Streamlit UI
st.title("Document Query Application")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
if uploaded_file is not None:
    file_content = uploaded_file.read()
    file_type = uploaded_file.type
    file_name = uploaded_file.name

    # Add document to the database
    add_document(session, file_name, file_type, file_content, encryption_key)
    st.success(f"File '{file_name}' uploaded and stored securely!")

# Querying section (placeholder)
st.header("Query Documents")
query = st.text_input("Enter your query")
if st.button("Search"):
    # Placeholder for search functionality
    st.write("Searching documents...")

# Download chat history (placeholder)
st.header("Download Chat History")
if st.button("Download"):
    # Placeholder for downloading chat history
    st.write("Downloading chat history...")
