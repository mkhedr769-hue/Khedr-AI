import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. الربط بالمفتاح ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ضيف المفتاح في Secrets")

st.set_page_config(page_title="Khedr-AI | Official", page_icon="🤖", layout="wide")

# --- 2. العلامات المائية وحقوق الملكية ---
st.markdown("""
    <style>
    .main-title { font-size: 40px; text-align: center; color: #00ffcc; font-weight: bold; margin-bottom: 5px; }
    .watermark { position: fixed; bottom: 80px; right: 20px; opacity: 0.3; font-size: 20px; color: grey; z-index: 100; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: #555; padding: 10px; }
    /* ستايل الشات */
    .stChatFloatingInputContainer { bottom: 40px; }
    </style>
    <div class="watermark">© Developed by Khedr</div>
    <div class="footer">جميع الحقوق محفوظة لـ Khedr-AI 2026</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. القائمة الجانبية (الرفع + الأنظمة + الحقوق) ---
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=Khedr+AI", caption="Khedr-AI Official")
    st.title("⚙️ التحكم والحقوق")
    st.write("---")
    
    # اختيار النظام
    model_choice = st.selectbox(
        "نظام التشغيل:",
        ["Gemini 2.5 Flash", "Gemini 1.5 Pro", "Gemini Pro"]
    )
    
    model_map = {
        "Gemini 2.5 Flash": "gemini-2.5-flash",
        "Gemini 1.5 Pro": "gemini-1.5-pro",
        "Gemini Pro": "gemini-pro"
    }
    selected_model = model_map[model_choice]

    st.write("---")
    uploaded_file = st.file_uploader("📤 ارفع ملفاتك (حقوق Khedr محفوظة)", type=["jpg", "png", "jpeg"])
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)
st.caption("بوابة الذكاء الاصطناعي الخاصة بـ Khedr")

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. خانة الكتابة ---
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages
    
