import streamlit as st
from db_setup import init_db, get_session, Document, UserHistory, encrypt, decrypt
from utils import process_document
import os

# Initialize database
engine = init_db()
session = get_session(engine)
encryption_key = os.getenv("ENCRYPTION_KEY", b'mysecretkey')  # Replace with a secure key

# Streamlit Application
st.title("Document Query App")

# Document Upload Section
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    file_content = process_document(uploaded_file, file_type)
    encrypted_content = encrypt(file_content, encryption_key)
    
    # Store in the database
    new_doc = Document(filename=uploaded_file.name, filetype=file_type, content=encrypted_content)
    session.add(new_doc)
    session.commit()
    st.success("File uploaded successfully!")

# Query Section
query = st.text_input("Enter your query")
if query:
    # Search and retrieve relevant info (dummy logic for simplicity)
    documents = session.query(Document).all()
    response = ""
    for doc in documents:
        decrypted_content = decrypt(doc.content, encryption_key)
        if query.lower() in decrypted_content.lower():
            response += f"Found in {doc.filename}: {query}\n"
    
    st.write("Response:", response)

    # Store user history
    user_history = UserHistory(user_id="user1", query=query, response=response)  # Replace with dynamic user ID
    session.add(user_history)
    session.commit()

# Download Chat History
if st.button("Download Chat History"):
    history = session.query(UserHistory).filter_by(user_id="user1").all()  # Replace with dynamic user ID
    history_text = "\n".join([f"Query: {h.query}\nResponse: {h.response}" for h in history])
    
    st.download_button("Download", history_text, file_name="chat_history.txt")

