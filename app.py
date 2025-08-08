from openai import OpenAI
import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load OpenAI key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Resume Chatbot", page_icon="🤖")
st.title("🤖 Ask My AI Resume Clone")
st.markdown("Ask me anything about my professional or educational background.")

# === Load documents from knowledge_base/ ===
def load_documents():
    documents = []

    # Load resume.pdf
    resume_path = Path("knowledge_base/resume.pdf")
    if resume_path.exists():
        loader = PyPDFLoader(str(resume_path))
        documents.extend(loader.load())

    # Load supporting text files
    for fname in ["about_me.txt", "faq.txt"]:
        path = Path(f"knowledge_base/{fname}")
        if path.exists():
            loader = TextLoader(str(path))
            documents.extend(loader.load())

    return documents

# Load & split documents into chunks
documents = load_documents()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
context = "\n\n".join([chunk.page_content for chunk in chunks[:10]])  # Limit to avoid overload

# === Chat UI ===
user_input = st.text_input("💬 Ask a question:")

if user_input:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are Ajay's AI assistant. Use the following resume and background context to answer like Ajay:\n\n{context}"
                },
                {"role": "user", "content": user_input}
            ]
        )
        st.markdown(f"**AI Ajay:** {response.choices[0].message.content}")
