import streamlit as st
import requests
from auth import require_login

host = "http://databasephase1-e3daa06311f4.herokuapp.com/losprogramadores/chat"

st.title("Tarzan Chatbot")
st.header("For better understanding, please write down the courses either in this format 'CIIC 4060'/n or saying the name of the class the most exact way possible")
require_login()

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Send a message to Tarzan"):
    st.session_state["messages"].append({"role": "user", "content": prompt}) 
    
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    response = requests.post(host, json={"question": prompt}).json()
    message = response.get("answer")
    st.markdown(message)
    st.session_state["messages"].append({"role": "assistant", "content": message})
