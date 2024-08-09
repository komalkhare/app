import streamlit as st
import os
from db_setup import init_db, create_session, add_document, get_document, Document
from cryptography.fernet import Fernet
from sqlalchemy import or_

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

# Querying section
st.header("Query Documents")
query = st.text_input("Enter your query")
if st.button("Search"):
    # Retrieve all documents from the database
    documents = session.query(Document).all()
    results = []
    
    # Search through each document's content
    for doc in documents:
        decrypted_content = get_document(session, doc.id, encryption_key)
        
        # Safely decode content with error handling
        try:
            content_str = decrypted_content.decode('utf-8')
        except UnicodeDecodeError:
            content_str = decrypted_content.decode('utf-8', errors='ignore')
        
        if query.lower() in content_str.lower():
            results.append(f"Found in {doc.filename}: {content_str[:200]}...")
    
    if results:
        for result in results:
            st.write(result)
    else:
        st.write("No results found.")

# Download chat history
st.header("Download Chat History")
if st.button("Download"):
    chat_history = "Chat history is a placeholder. Implement chat logging logic."
    
    # Create a downloadable text file
    st.download_button(label="Download", data=chat_history, file_name="chat_history.txt")
