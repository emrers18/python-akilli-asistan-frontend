import streamlit as st
import requests


BACKEND_URL = "https://python-akilli-asistan.onrender.com"

st.set_page_config(
    page_title = "Akıllı Asistan",
    page_icon = "🤖",
    layout = "centered"
)

st.title("Akıllı Asistan")
st.write("Mesajınızı yazın, asistan cevaplasın!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 

def load_messages():
    try:
        response = requests.get(f"{BACKEND_URL}/messages")
        if response.status_code == 200:
            data = response.json()
            return data.get("messages", [])
        else:
            st.warning("Mesajlar yüklenirken hata oluştu")
            return []
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")
        return []


def send_message(user_message):
    try:
        response = requests.post(f"{BACKEND_URL}/chat", json = {"user_message":user_message})
        if response.status_code == 200:
            return response.json()
        return {"assistant_response":"Bir hata oluştu"}
    
    except:
        st.error("Mesaj gönderilirken hata oluştu")
        return {"assistant_response":"Mesaj gönderilirken hata oluştu"}


if not st.session_state.chat_history:
    old_messages = load_messages()

    for item in old_messages:
        st.session_state.chat_history.append({
            "role": "user",
            "content": item["user_message"]
        })

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": item["assistant_response"]
        })
        

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Mesajınızı yazın")

if user_input:
    st.session_state.chat_history.append({
        "role":"user",
        "content":user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    result = send_message(user_input)
    assistant_response = result.get("assistant_response")

    st.session_state.chat_history.append({
        "role":"assistant",
        "content":assistant_response
    })
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

