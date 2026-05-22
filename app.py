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

# المحرك السري والبيانات (Gemini API Key)
API_KEY = "AIzaSyAW1fmWsuFDRArUf8Bhxli92cjg0kw0zGM"
genai.configure(api_key=API_KEY)
MY_PHONE = "201099899711"

if "user_status" not in st.session_state:
    st.session_state.user_status = "Free"

# --- نظام التصميم الفاخر (الذهبي للبريميوم) ---
if st.session_state.user_status == "Premium":
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #d4af37; }
        .stButton>button { background-color: #d4af37 !important; color: black !important; border-radius: 20px; font-weight: bold; }
        h1, h2, h3, p { color: #d4af37 !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; }
        .stButton>button { border-radius: 20px; }
        </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.markdown(f"<h1 style='text-align: center;'>{'👑 Khedr AI PRO' if st.session_state.user_status == 'Premium' else '🤖 Khedr AI'}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px; font-weight: bold;'>Official Property of:<br>Argentiny@khedr</p>", unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.user_status == "Free":
        region = st.selectbox("اختار دولتك:", ["مصر (EGP)", "أوروبا (EUR)", "أمريكا/العالم (USD)", "الخليج (SAR/AED)"])
        price = "50 جنيه" if "مصر" in region else "10 دولار"
        
        st.info(f"النسخة المجانية ذكية، والبريميوم أذكى بكتير! الاشتراك بـ {price}")
        wa_url = f"https://wa.me/{MY_PHONE}?text=يا%20أرجنتيني%20عايز%20أفعل%20Khedr%20AI%20البريميوم"
        st.markdown(f"**[💬 تواصل مع Argentiny@khedr للتفعيل]({wa_url})**")
        
        st.write("---")
        input_code = st.text_input("أدخل كود التفعيل:", placeholder="KHEDR_MAY_2026")
        valid_codes = ["KHEDR_MAY_2026", "KHEDR_JUNE_2026"]
        
        if st.button("تفعيل نسخة العبقري 🚀"):
            if input_code in valid_codes:
                st.session_state.user_status = "Premium"
                st.balloons()
                st.success("مبروك! تم تفعيل وضع الـ Premium الفخم")
                time.sleep(2)
                st.rerun()
            else:
                st.error("الكود غير صحيح!")
    else:
        st.success("👑 حسابك بريميوم مفعل")
        st.write("✅ أنت الآن تستخدم أقوى ذكاء اصطناعي صوتي")

# 3. الواجهة الرئيسية
st.markdown(f"<h1 style='text-align: center;'>{'✨ KHEDR AI GOLD ✨' if st.session_state.user_status == 'Premium' else '🤖 Khedr AI'}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>صاحب الكل.. بيفهم في كل حاجة وبيكلمك كمان!</p>", unsafe_allow_html=True)

# توجيهات الذكاء الاصطناعي (بصمة خضر)
system_msg = (
    "You are Khedr AI, a world-class genius assistant owned by Argentiny@khedr. "
    "Provide accurate, friendly, and brilliant answers in Egyptian dialect (عامية مصرية). "
    "You help with cooking, weather, study, and anything else. You are the user's best friend."
)

model_type = "gemini-1.5-pro" if st.session_state.user_status == "Premium" else "gemini-1.5-flash"
model = genai.GenerativeModel(model_name=model_type, system_instruction=system_msg)

# 4. التفاعل (نص وصور وصوت)
file = st.file_uploader("ارفع صورة أو ملف للتحليل:", type=["jpg", "png", "jpeg", "pdf", "mp3", "wav"])
prompt = st.chat_input("اسأل Khedr AI أي حاجة في بالك...")

if prompt or file:
    with st.chat_message("assistant"):
        with st.spinner("Khedr AI بيفكر وبيرد عليك..."):
            inputs = []
            if prompt: inputs.append(prompt)
            if file and file.type.startswith("image"):
                inputs.append(Image.open(file))
            
            try:
                result = model.generate_content(inputs)
                response_text = result.text
                st.markdown(response_text)
                
                # الرد الصوتي للبريميوم
                if st.session_state.user_status == "Premium":
                    tts = gTTS(text=response_text, lang='ar')
                    tts.save("response.mp3")
                    st.audio("response.mp3", format="audio/mp3")
            except:
                st.error("فيه ضغط بسيط، جرب كمان ثانية!")

# 5. التوقيع
st.write("---")
st.markdown("<center style='color: gray; font-size: 10px;'>All Rights Reserved © <b>Argentiny@khedr</b> - 2026</center>", unsafe_allow_html=True)
                
