import streamlit as st
import google.generativeai as genai
from PIL import Image
import shelve
import time

# --- 1. إعدادات الصفحة والبراند ---
API_KEY = "AIzaSyC2-3pnFUCNmIk86fE3FWHeMktFS3FcNt8"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# رابط اللوجو بتاعك (تأكد من رفعه مع الملفات باسم logo.jpg أو استخدام رابط مباشر)
AI_AVATAR = "https://raw.githubusercontent.com/Argentiny/Khedr-AI/main/1000167319.jpg" # مثال لمسار الملف

# --- 2. ستايل الـ Premium والـ CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0E1117; }
    .stChatMessage { border-radius: 12px; }
    /* ستايل اللوجو عشان يظهر كامل */
    [data-testid="stChatMessageAvatarCustom"] img {
        object-fit: contain !important;
        border-radius: 8px !important;
        background: transparent;
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

# --- 3. الذاكرة والسجل ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. العنوان والواجهة ---
st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)
st.caption("<center>Powering your imagination - By Argentiny@khedr</center>", unsafe_allow_html=True)

# عرض المحادثة
for msg in st.session_state.messages:
    avatar = AI_AVATAR if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 5. منطق الرد الذكي (الحل النهائي للـ 404) ---
if prompt := st.chat_input("Ask Khedr-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AI_AVATAR):
        with st.spinner("Khedr is thinking..."):
            # بنجرب الموديلات بالترتيب لحد ما واحد يفتح
            success = False
            for model_name in ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except:
                    continue
            
            if not success:
                st.error("جوجل لسه بتحدث في السيرفرات، جرب كمان 5 دقايق.")

st.markdown("<br><hr><center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
            
