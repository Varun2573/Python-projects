import streamlit as st
from src.ingest import ingest_docs
from src.query import load_chain

st.set_page_config(page_title="📚 Personalized Knowledge Assistant")
st.title("🧠 Ask Your Docs")
st.markdown("Upload your PDF files, then ask questions about them.")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Session state
if "index_ready" not in st.session_state:
    st.session_state.index_ready = False
if "chain" not in st.session_state:
    st.session_state.chain = None

# Ingest documents
if uploaded_file and not st.session_state.index_ready:
    with open("temp_uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Building index..."):
        ingest_docs("temp_uploaded_file.pdf")
        st.session_state.index_ready = True

# Load the QA chain
if st.session_state.index_ready and st.session_state.chain is None:
    st.session_state.chain = load_chain()

# Ask questions
if st.session_state.chain:
    question = st.text_input("Ask a question:")
    if question:
        with st.spinner("Thinking..."):
            result = st.session_state.chain({"query": question})
            st.markdown("### ✅ Answer:")
            st.write(result["result"])

            with st.expander("📎 Sources"):
                for i, doc in enumerate(result["source_documents"]):
                    st.markdown(f"**Source {i+1}:** {doc.metadata.get('source', 'Unknown')}")
                    st.write(doc.page_content[:500] + "...")