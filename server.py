import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client with Hugging Face router and HF_TOKEN from .env
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

# Streamlit app config
st.set_page_config(page_title="PlanIt Chatbot", layout="centered")
st.title("🤖 PLANIT - Career Guidance Bot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are PlanIt, a helpful AI assistant."}
    ]

# Display existing messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything about careers..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:fireworks-ai",
            messages=st.session_state.messages
        )
        bot_reply = response.choices[0].message["content"]

        # Append bot message
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

    except Exception as e:
        error_text = f"⚠️ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_text})
        with st.chat_message("assistant"):
            st.markdown(error_text)
