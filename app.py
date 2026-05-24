import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. الربط الأساسي ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ناقصك المفتاح في الـ Secrets!")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖")

# --- 2. ستايل الواجهة ---
st.markdown("""
    <style>
    .main-title { font-size: 30px; text-align: center; color: #00ffcc; font-weight: bold; }
    .stFileUploader { margin-bottom: -40px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. اختيار النظام (حل مشكلة الـ 404) ---
with st.sidebar:
    st.title("⚙️ نظام خضر")
    # غيرت الأسماء للأسماء الخام عشان نضمن إن جوجل تشوفهم
    model_id = st.selectbox(
        "اختار المحرك:",
        ["gemini-pro", "gemini-1.5-flash", "gemini-1.5-pro"]
    )
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. علامة الزائد (+) والرفع ---
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# --- 5. منطقة الرد الذكي ---
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام الموديل المختار
            model = genai.GenerativeModel(model_id)
            
            # شخصية خضر محطوطة جوه الـ prompt عشان نضمن إنها تشتغل
            personality = "أنت 'خضر AI' صاحب الأرجنتيني. فرفوش ومصري وبتقول يا زميلي. "
            
            payload = [personality + prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                payload.append(img)
            
            response = model.generate_content(payload)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"حصلت قفلة: {e}")
            st.info("جرب تختار 'gemini-pro' من القائمة اللي في الجنب، ده أضمن نظام شغال دلوقتي.")
            
