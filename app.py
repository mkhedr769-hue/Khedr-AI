import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS

# --- 1. اكتشاف لغة المستخدم تلقائياً ---
# بنجرب نجيب لغة المتصفح، لو فشلنا بنخليها English كافتراض
user_lang = st.query_params.get("lang", ["ar"])[0][:2] 

# قاموس اللغات لترجمة الواجهة
translations = {
    "ar": {"title": "خضر AI", "sub": "تطوير Argentiny@khedr", "input": "اسأل Khedr AI...", "upload": "ارفع ملف", "options": ["كاميرا", "صور", "ملفات", "مستندات"]},
    "en": {"title": "Khedr AI", "sub": "Developed by Argentiny@khedr", "input": "Ask Khedr AI...", "upload": "Upload", "options": ["Camera", "Photos", "Files", "Docs"]},
    "de": {"title": "Khedr AI", "sub": "Entwickelt von Argentiny@khedr", "input": "Fragen Sie Khedr AI...", "upload": "Hochladen", "options": ["Kamera", "Fotos", "Dateien", "Dokumente"]},
    "fr": {"title": "Khedr AI", "sub": "Développé par Argentiny@khedr", "input": "Demandez à Khedr AI...", "upload": "Télécharger", "options": ["Caméra", "Photos", "Fichiers", "Documents"]}
}

lang = translations.get(user_lang, translations["en"])

st.set_page_config(page_title=lang["title"], layout="centered")

# --- 2. إعدادات المفتاح السري ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Missing API Key in Secrets!")

# --- 3. تصميم الواجهة الروشة (CSS) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    /* تصميم منطقة الإدخال لتشبه تطبيقات الشات */
    .chat-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        background: #1e1e1e;
        padding: 10px;
        border-radius: 30px;
    }}
    .plus-btn {{
        background: #333;
        color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        font-size: 24px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title(f"🤖 {lang['title']}")
st.caption(lang["sub"])

# --- 4. نظام الرفع المتقدم (علامة الزائد) ---
# بنستخدم الـ Sidebar أو Expander لمحاكاة قائمة الزائد
with st.sidebar:
    st.markdown("### ➕ " + lang["upload"])
    choice = st.radio("", lang["options"])
    
    if choice:
        uploaded_file = st.file_uploader(f"Select {choice}", type=["jpg", "png", "pdf", "docx", "mp4"])

# --- 5. منطقة الدردشة ---
prompt = st.chat_input(lang["input"])

if prompt or (locals().get('uploaded_file')):
    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                parts = []
                if prompt: parts.append(prompt)
                if locals().get('uploaded_file'):
                    img = Image.open(uploaded_file)
                    parts.append(img)
                
                # إرسال الطلب مع توجيه الذكاء الاصطناعي للرد بنفس لغة المستخدم
                response = model.generate_content(parts + [f"Reply in the language: {user_lang}"])
                st.markdown(response.text)
                
                # صوت الرد
                tts = gTTS(text=response.text[:100], lang=user_lang)
                tts.save("res.mp3")
                st.audio("res.mp3")
            except Exception as e:
                st.error("Error! Check API Key.")

st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
