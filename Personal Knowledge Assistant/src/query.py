
import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import GoogleGenerativeAI
from langchain.embeddings import GoogleGenerativeAIEmbeddings

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vectorstore = FAISS.load_local("faiss_index", embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = GoogleGenerativeAI(model="models/gemini-pro", google_api_key=GOOGLE_API_KEY)

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain
