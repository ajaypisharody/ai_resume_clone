from openai import OpenAI
import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import glob

# Initialize OpenAI client from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Ajay's AI Resume Clone", layout="wide")

# Sidebar — Profile & Links
st.sidebar.image("profile.jpg", use_column_width=True)
st.sidebar.markdown("### Ajay Pisharody")
st.sidebar.markdown("**Data Analytics & BI Leader**")
st.sidebar.markdown("[LinkedIn](https://linkedin.com/in/ajaypisharody)")
st.sidebar.markdown("[GitHub](https://github.com/ajaypisharody)")

# Resume download
if os.path.exists("resume.pdf"):
    with open("resume.pdf", "rb") as pdf_file:
        st.sidebar.download_button(
            label="📄 Download Resume",
            data=pdf_file,
            file_name="Ajay_Pisharody_Resume.pdf",
            mime="application/pdf"
        )

# Load knowledge base files
kb_files = glob.glob("knowledge_base/*.txt")
knowledge_text = ""
for kb_file in kb_files:
    try:
        with open(kb_file, "r", encoding="utf-8", errors="ignore") as f:
            knowledge_text += f.read() + "\n"
    except Exception as e:
        st.error(f"Error loading {kb_file}: {e}")

st.title("💼 Ajay's AI Resume Clone")
st.write("Interactive AI-powered version of my professional resume.")

# Prebuilt recruiter questions
questions = [
    "Tell me about your career highlights",
    "What are your top technical skills?",
    "Describe a challenging project you worked on",
    "Why should we hire you?",
    "Tell me about your education",
    "What are your future career goals?"
]

st.subheader("Quick Questions")
col1, col2 = st.columns(2)
for idx, q in enumerate(questions):
    if col1.button(q) if idx % 2 == 0 else col2.button(q):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are Ajay Pisharody. Use this context from my resume:\n{knowledge_text}"},
                    {"role": "user", "content": q}
                ]
            )
            st.write(response.choices[0].message.content)

# Custom question mode
st.subheader("Ask Your Own Question")
user_input = st.text_input("Type your question here...")
if st.button("Submit Custom Question"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are Ajay Pisharody. Use this context from my resume:\n{knowledge_text}"},
                    {"role": "user", "content": user_input}
                ]
            )
            st.write(response.choices[0].message.content)
