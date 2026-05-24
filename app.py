import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. الربط بالمفتاح ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ضيف المفتاح في Secrets باسم GOOGLE_API_KEY")

st.set_page_config(page_title="Khedr-AI | Official", page_icon="🤖", layout="wide")

# --- 2. ستايل الحقوق والعلامة المائية (Argentiny@khedr) ---
st.markdown(f"""
    <style>
    .main-title {{ font-size: 38px; text-align: center; color: #00ffcc; font-weight: bold; margin-bottom: 0px; }}
    .watermark {{ position: fixed; bottom: 100px; left: 20px; opacity: 0.4; font-size: 18px; color: #00ffcc; z-index: 100; transform: rotate(-15deg); font-family: sans-serif; pointer-events: none; }}
    .footer {{ position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; font-size: 14px; color: #777; padding: 10px; background: rgba(0,0,0,0.5); z-index: 1000; }}
    .stChatFloatingInputContainer {{ bottom: 50px; }}
    </style>
    <div class="watermark">Argentiny@khedr</div>
    <div class="footer">© Copyright Argentiny@khedr | All Rights Reserved 2026</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. القائمة الجانبية (التحكم الكامل) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>Argentiny@khedr</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # إضافة نظام 2.0/2.5 كأول خيار
    model_choice = st.selectbox(
        "اختار نظام التشغيل:",
        ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"]
    )
    
    st.write("---")
    uploaded_file = st.file_uploader("📤 ارفع ملفاتك (حقوق Argentiny محفوظة)", type=["jpg", "png", "jpeg"])
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>بوابة الذكاء الاصطناعي - تطوير Argentiny@khedr</p>", unsafe_allow_html=True)

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. خانة الكتابة ---
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(model_choice)
            
            # شخصية خضر الزيتونة (بدون رغي الأرجنتين)
            instruction = (
                "أنت خضر AI، المساعد الذكي الخاص بـ Argentiny@khedr. "
                "ردك مصري، جدع، ومختصر جداً جداً. "
                "لو حد قالك إزيك، رد بكلمة: 'زي الفل يا زميلي'. "
                "ممنوع تذكر كلمة 'الأرجنتين' في كلامك نهائياً."
            )
            
            content = [instruction + "\n\n" + prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                content.append(img)
            
            response = model.generate_content(content)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"حصلت قفلة فنية: {e}")
            st.info("نصيحة: لو الموديل الجديد معلق، قلب من الجنب على 'gemini-pro' المستقر.")
            
