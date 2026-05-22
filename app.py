import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import time

# 1. إعدادات الهوية والملكية لـ Argentiny@khedr
st.set_page_config(
    page_title="Khedr AI - صاحب الكل", 
    page_icon="🤖", 
    layout="centered"
)

# المحرك السري والبيانات (Gemini API Key الجديد)
# تم تحديث المفتاح هنا يا أرجنتيني لضمان التشغيل
API_KEY = "AIzaSyCxV_V5..." # حط المفتاح الجديد هنا أو استخدم اللي هبعتهولك في رسالة منفصلة
genai.configure(api_key=API_KEY)
MY_PHONE = "201099899711"

if "user_status" not in st.session_state:
    st.session_state.user_status = "Free"

# --- نظام التصميم ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #d4af37 !important; color: black !important; border-radius: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🤖 Khedr AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold;'>Official Property of:<br>Argentiny@khedr</p>", unsafe_allow_html=True)
    st.write("---")
    st.info("النسخة المجانية ذكية جداً!")

# 3. الواجهة الرئيسية
st.markdown("<h1 style='text-align: center;'>✨ KHEDR AI ✨</h1>", unsafe_allow_html=True)

# 4. التفاعل
file = st.file_uploader("ارفع صورة أو ملف:", type=["jpg", "png", "jpeg"])
prompt = st.chat_input("اسأل Khedr AI أي حاجة...")

if prompt or file:
    with st.chat_message("assistant"):
        with st.spinner("خضر بيفكر..."):
            inputs = []
            if prompt: inputs.append(prompt)
            if file: inputs.append(Image.open(file))
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                result = model.generate_content(inputs)
                response_text = result.text
                st.markdown(response_text)
                
                # صوت بسيط كهدية
                tts = gTTS(text=response_text[:100], lang='ar')
                tts.save("res.mp3")
                st.audio("res.mp3")
            except Exception as e:
                st.error("المفتاح محتاج تحديث، تواصل مع المطور!")

# 5. التوقيع
st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
    
