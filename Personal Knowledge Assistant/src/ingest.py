import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

def ingest_docs(file_path: str):
    # Load PDF
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  # updated model
        google_api_key=GOOGLE_API_KEY
    )

    # Build FAISS vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")

    st.success(f"Indexed {len(chunks)} chunks from {file_path}")