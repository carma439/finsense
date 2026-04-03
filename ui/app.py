import streamlit as st
import requests

# API_URL = "http://localhost:8000/chat" # for local run
API_URL = "https://chirags439-finsense.hf.space/chat" # deployed url

st.title("Financial AI Assistant")

st.write("Hello! I am an agent that can help you with your financial queries and tax calculations.\nIf you get a JSON error, that might be because of free-tier limitations of HuggingFace Spaces, which is being used for backend. Please reactivate the backend here: https://huggingface.co/spaces/chirags439/finsense and then try again! Thank you!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Detect if this is first load (no messages yet)
is_first = len(st.session_state.messages) == 0

# Apply CSS conditionally
if is_first:
    st.markdown("""
    <style>
    div[data-testid="stChatInput"] {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 60%;
        max-width: 700px;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        max-width: 700px;
    }
    </style>
    """, unsafe_allow_html=True)



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
