
import streamlit as st
from src.query import load_chain

st.set_page_config(page_title="📚 Personalized Knowledge Assistant")

st.title("🧠 Ask Your Docs")
st.markdown("Upload your files, then ask anything about them.")

qa_chain = load_chain()

question = st.text_input("Ask a question from your uploaded documents:")

if question:
    with st.spinner("Thinking..."):
        result = qa_chain(question)
        st.markdown("### ✅ Answer:")
        st.write(result['result'])

        with st.expander("📎 Sources"):
            for doc in result['source_documents']:
                st.markdown(f"**Source:** {doc.metadata.get('source', 'Unknown')}")
                st.write(doc.page_content[:500])  # Show a snippet
