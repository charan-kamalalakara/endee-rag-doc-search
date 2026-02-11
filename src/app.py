import streamlit as st
import os
import subprocess
import sys

from rag_qa import answer_question

DOCUMENTS_DIR = "data/documents"

st.set_page_config(
    page_title="Endee RAG Document QA",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Endee RAG Document QA System")

st.markdown(
    """
Upload **PDF or TXT documents**, index them, and ask questions using  
**Endee Vector Database + RAG**.
"""
)

# -----------------------------
# 📤 Document Upload Section
# -----------------------------
st.subheader("📤 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = os.path.join(DOCUMENTS_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("Files uploaded successfully!")

# -----------------------------
# 🔁 Reindex Button
# -----------------------------
if st.button("🔁 Re-index Documents"):
    with st.spinner("Indexing documents..."):
        subprocess.run(
            [sys.executable, "src/index_documents.py"],
            check=True
        )
    st.success("Documents indexed successfully!")

st.divider()

# -----------------------------
# ❓ Question Answering Section
# -----------------------------
st.subheader("❓ Ask a Question")

question = st.text_input(
    "Enter your question",
    placeholder="e.g. What is Endee used for?"
)

if st.button("Get Answer"):
    if question.strip():
        with st.spinner("Retrieving information and generating answer..."):
            answer = answer_question(question)
        st.success("Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question.")
