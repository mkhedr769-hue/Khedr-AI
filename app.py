import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة والربط السري ---
# هنا بنسحب المفتاح من Secrets عشان ميتسرقش وجوجل تقفله
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
    else:
        st.error("⚠️ المفتاح مش موجود في الخزنة (Secrets)! ضيف GOOGLE_API_KEY هناك.")
except Exception as e:
    st.error(f"⚠️ حصلت مشكلة في سحب المفتاح: {e}")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# صورة أفاتار شيك وفخمة (الـ AI المودرن)
AI_AVATAR = "https://cdn-icons-png.flaticon.com/512/6298/6298377.png"

# --- 2. ستايل الواجهة والـ CSS ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #333; }
    [data-testid="stChatMessageAvatarCustom"] img {
        object-fit: contain !important;
        border-radius: 50% !important;
        border: 2px solid #00ffcc;
    }
    .main-title {
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        color: #00ffcc;
        font-family: 'Arial Black';
        margin-top: -50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. الـ Sidebar (الإضافات +) ---
with st.sidebar:
    st.markdown('<p style="font-size: 25px; font-weight: bold; color: #00ffcc;">Khedr Hub</p>', unsafe_allow_html=True)
    st.write("---")
    # زرار الـ (+) لرفع الصور والملفات
    uploaded_file = st.file_uploader("➕ إضافة ملف أو صورة", type=["jpg", "jpeg", "png", "pdf", "txt"])
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.info("تطوير: Argentiny@khedr")

# --- 4. ذاكرة الشات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)
st.caption("<center>Powering your imagination - By Argentiny@khedr</center>", unsafe_allow_html=True)

# عرض الرسائل القديمة عشان متختفيش
for msg in st.session_state.messages:
    avatar = AI_AVATAR if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 5. منطقة "خضر الفرفوش" الذكية ---
if prompt := st.chat_input("Ask Khedr-AI..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown
        
