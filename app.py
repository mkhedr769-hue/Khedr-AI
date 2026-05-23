import streamlit as st
import google.generativeai as genai
from PIL import Image
import shelve
import time

# --- 1. إعدادات الصفحة والبراند ---
API_KEY = "AIzaSyC2-3pnFUCNmIk86fE3FWHeMktFS3FcNt8"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# رابط اللوجو الفخم
AI_AVATAR = "https://raw.githubusercontent.com/Argentiny/Khedr-AI/main/1000167319.jpg"

# --- 2. ستايل الواجهة واللوجو ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0E1117; }
    [data-testid="stChatMessageAvatarCustom"] img {
        object-fit: contain !important;
        border-radius: 8px !important;
    }
    .main-title {
        font-size: 55px;
        font-weight: bold;
        text-align: center;
        color: #00ffcc;
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام السجل والذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown('<p style="font-size: 22px; font-weight: bold; color: #00ffcc;">Khedr History</p>', unsafe_allow_html=True)
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.info("Developed by: Argentiny@khedr")
    uploaded_file = st.file_uploader("➕ Attachment", type=["jpg", "jpeg", "png"])

# --- 4. الواجهة الرئيسية ---
st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)
st.caption("<center>Powering your imagination - By Argentiny@khedr</center>", unsafe_allow_html=True)

# عرض الرسايل (مبتختفيش)
for msg in st.session_state.messages:
    avatar = AI_AVATAR if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 5. منطقة "السستم" التلقائي ---
if prompt := st.chat_input("Ask Khedr-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AI_AVATAR):
        try:
            # هنا السستم: بيدور على أي موديل شغال في حسابك ويستخدمه فوراً
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                model = genai.GenerativeModel(available_models[0])
                
                inputs = [prompt]
                if uploaded_file:
                    inputs.append(Image.open(uploaded_file))
                
                response = model.generate_content(inputs)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("جوجل لسه مفعلتش الموديلات على حسابك.")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("<br><hr><center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
                         
