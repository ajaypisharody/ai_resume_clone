from openai import OpenAI
import streamlit as st
from pathlib import Path

client = OpenAI(api_key=st.secrets["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"])

st.set_page_config(page_title="AI Resume Chatbot", page_icon="🤖")
st.title("🤖 Ask My AI Clone")
st.markdown("This bot answers questions based on my resume, projects, and skills.")

about_me_file = Path("knowledge_base/about_me.txt")
context = about_me_file.read_text() if about_me_file.exists() else ""

user_input = st.text_input("Ask a question:")

if user_input:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a helpful AI assistant that answers questions about Ajay's professional background. Here is some context:\n\n{context}"},
                {"role": "user", "content": user_input}
            ]
        )
        st.markdown(f"**AI Ajay:** {response.choices[0].message.content}")