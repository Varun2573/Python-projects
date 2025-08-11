import streamlit as st
from src.ingest import ingest_docs
from src.query import load_chain
import os

st.set_page_config(page_title="📚 Personalized Knowledge Assistant")

st.title("🧠 Ask Your Docs")
st.markdown("Upload your files, then ask anything about them.")

# Upload file widget (only PDFs for now)
uploaded_file = st.file_uploader("Upload your document (PDF)", type=["pdf"])

# Session state to track if index is ready
if "index_ready" not in st.session_state:
    st.session_state.index_ready = False

# If a file is uploaded
if uploaded_file:
    # Save uploaded file to temp location
    temp_filepath = "temp_uploaded_file.pdf"
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processing document and building index..."):
        # Call your existing ingestion to build FAISS index
        ingest_docs(temp_filepath)

    st.success("Document indexed successfully!")
    st.session_state.index_ready = True

# Only load chain and ask question if index is ready
if st.session_state.index_ready:
    qa_chain = load_chain()

    question = st.text_input("Ask a question from your uploaded documents:")

    if question:
        with st.spinner("Thinking..."):
            result = qa_chain({"query": question})  # Pass dict with 'query'
            st.markdown("### ✅ Answer:")
            st.write(result['result'])

            with st.expander("📎 Sources"):
                for doc in result['source_documents']:
                    st.markdown(f"**Source:** {doc.metadata.get('source', 'Unknown')}")
                    st.write(doc.page_content[:500])  # Show snippet
else:
    st.info("Please upload a document to get started.")
