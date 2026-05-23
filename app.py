import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. سحب المفتاح من الخزنة (Secrets) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ المفتاح مش موجود في الخزنة (Secrets)")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# رابط اللوجو الفخم
AI_AVATAR = "https://raw.githubusercontent.com/Argentiny/Khedr-AI/main/1000167319.jpg"

st.markdown("""
    <style>
    [data-testid="stChatMessageAvatarCustom"] img { object-fit: contain !important; border-radius: 8px !important; }
    .main-title { font-size: 55px; font-weight: bold; text-align: center; color: #00ffcc; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    avatar = AI_AVATAR if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask Khedr-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AI_AVATAR):
        try:
            # "السستم" التلقائي عشان ميحصلش 404
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(available_models[0])
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
    
