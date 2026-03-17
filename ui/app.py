import streamlit as st
import requests

# API_URL = "http://localhost:8000/chat" # for local run
API_URL = "https://chirags439-finsense.hf.space/chat" # deployed url

st.title("Financial AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# user input
prompt = st.chat_input("Ask a question")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    res = requests.post(
        API_URL,
        json={"messages": st.session_state.messages[-3:]}
    )

    st.write(res.text)
    answer = res.json()["answer"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    
    st.rerun()
