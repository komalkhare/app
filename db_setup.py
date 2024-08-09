from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Generate a new encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypt data
def encrypt(data, key):
    f = Fernet(key)
    return f.encrypt(data)

# Decrypt data
def decrypt(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data)

# Database setup function
def init_db():
    engine = create_engine('sqlite:///documents.db')
    Base.metadata.create_all(engine)
    return engine

# Example table structure for documents
class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filetype = Column(String)
    content = Column(LargeBinary)  # Store encrypted content

# Example table structure for user history
class UserHistory(Base):
    __tablename__ = 'user_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    query = Column(String)
    response = Column(String)

# Create a session
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Insert a new document
def add_document(session, filename, filetype, content, key):
    encrypted_content = encrypt(content, key)
    new_doc = Document(filename=filename, filetype=filetype, content=encrypted_content)
    session.add(new_doc)
    session.commit()

# Retrieve and decrypt a document
def get_document(session, document_id, key):
    doc = session.query(Document).filter_by(id=document_id).first()
    if doc:
        return decrypt(doc.content, key)
    return None
