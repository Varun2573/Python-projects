import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA  # still in langchain main package

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

def load_chain():
    try:
        # Load embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

        # Load FAISS index
        vectorstore = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.0-flash",
            google_api_key=GOOGLE_API_KEY
        )

        # RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )
        return qa_chain
    except Exception as e:
        st.error(f"❌ Failed to load chain: {e}")
        return None