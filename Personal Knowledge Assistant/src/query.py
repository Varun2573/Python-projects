from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
GOOGLE_API_KEY ="AIzaSyDkTqFKkphvtqD4rmmFiEaSrPSNp7-tws4"
def load_chain():
    # Load embeddings (no recomputation, just needed for loading index)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    
    # Load existing FAISS index from disk
    vectorstore = FAISS.load_local(
        "faiss_index", 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Initialize LLM once
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY
    )

    # Create RetrievalQA chain with sources returned
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    
    return qa_chain
