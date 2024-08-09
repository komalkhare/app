from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet

Base = declarative_base()

# Model for storing documents
class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filetype = Column(String)
    content = Column(LargeBinary)

# Model for storing user history
class UserHistory(Base):
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    query = Column(Text)
    response = Column(Text)

def init_db():
    engine = create_engine('sqlite:///secure_data.db')
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Encryption setup
def generate_key():
    return Fernet.generate_key()

def encrypt(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt(data, key):
    f = Fernet(key)
    return f.decrypt(data).decode()

