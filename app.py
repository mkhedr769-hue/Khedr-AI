import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات المفتاح (Secrets) ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("⚠️ ضيف المفتاح في الـ Secrets باسم GOOGLE_API_KEY")
except Exception as e:
    st.error(f"⚠️ مشكلة في الربط: {e}")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# --- 2. ستايل الواجهة ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .main-title {
        font-size: 50px; font-weight: bold; text-align: center;
        color: #00ffcc; font-family: 'Arial'; margin-top: -40px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. القائمة الجانبية (+) ---
with st.sidebar:
    st.title("Khedr Hub")
    uploaded_file = st.file_uploader("➕ ارفع صورة أو ملف", type=["jpg", "png", "jpeg", "txt"])
    if st.button("🗑️ مسح الشات"):
        st.session_state.messages = []
        st.rerun()

# --- 4. ذاكرة المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. منطق الرد (خضر الفرفوش) ---
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # الشخصية اللي طلبتها
            instruction = "أنت خضر AI، صاحب الأرجنتيني. خليك فرفوش ودردش بالعامية المصرية. لو قالك عامل إيه قوله الحمد لله يا زميلي."
            
            # الموديل المستقر
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)
            
            payload = [prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                payload.append(img)
            
            response = model.generate_content(payload)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"حصلت قفلة: {e}")
        
