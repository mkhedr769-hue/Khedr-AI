import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة والربط السري ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ المفتاح مش موجود في الخزنة (Secrets)")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# صورة أفاتار شيك وفخمة (مودرن AI)
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

# --- 3. قائمة الإضافات (+) في الجنب ---
with st.sidebar:
    st.markdown('<p style="font-size: 25px; font-weight: bold; color: #00ffcc;">Khedr Hub</p>', unsafe_allow_html=True)
    st.write("---")
    uploaded_file = st.file_uploader("➕ إضافة ملف أو صورة", type=["jpg", "jpeg", "png", "pdf", "txt"])
    if st.button("🗑️ مسح الشات"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.info("تطوير: Argentiny@khedr")

# --- 4. ذاكرة المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    avatar = AI_AVATAR if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 5. منطق "خضر الفرفوش" ---
if prompt := st.chat_input("Ask Khedr-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AI_AVATAR):
        try:
            # هنا بنفهمه الشخصية بتاعته (System Instruction)
            personality = "أنت اسمك 'خضر AI'. أنت مش روبوت ممل، أنت صديق فرفوش وجدع. اتكلم بالعامية المصرية بأسلوب شبابي. لما حد يقولك عامل ايه، قوله الحمد لله يا زميلي أنت اللي عامل ايه. خليك مرح ومساعد جداً."
            
            # بنجيب الموديل المتاح
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(available_models[0], system_instruction=personality)
            
            # تجهيز الطلب (نص + صورة)
            full_content = [prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                full_content.append(img)
            
            response = model.generate_content(full_content)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"حصل قفلة في السلك: {e}")

st.markdown("<br><hr><center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
