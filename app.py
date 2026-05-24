import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. الربط بالمفتاح ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ضيف المفتاح في Secrets")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# --- 2. ستايل الواجهة (تثبيت الكتابة تحت) ---
st.markdown("""
    <style>
    .main-title { font-size: 35px; text-align: center; color: #00ffcc; font-weight: bold; margin-bottom: 30px; }
    /* جعل منطقة الشات تأخذ المساحة المتاحة وتترك الإدخال في الأسفل */
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. القائمة الجانبية (الرفع + الأنظمة) ---
with st.sidebar:
    st.title("⚙️ إعدادات خضر")
    
    # اختيار النظام - ضفنا 2.5 وكل اللي قلبك يحبه
    model_choice = st.selectbox(
        "اختار نظام التشغيل:",
        ["Gemini 2.5 Flash (الأحدث)", "Gemini 1.5 Pro", "Gemini 1.5 Flash", "Gemini Pro"]
    )
    
    model_map = {
        "Gemini 2.5 Flash (الأحدث)": "gemini-2.5-flash",
        "Gemini 1.5 Pro": "gemini-1.5-pro",
        "Gemini 1.5 Flash": "gemini-1.5-flash",
        "Gemini Pro": "gemini-pro"
    }
    selected_model = model_map[model_choice]

    st.write("---")
    # مكان الرفع الجديد (بعيد عن الوش)
    st.markdown("### 📤 رفع الملفات")
    uploaded_file = st.file_uploader("ارفع صورك هنا يا برنس", type=["jpg", "png", "jpeg"])
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. خانة الكتابة (تحت خالص) ---
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(selected_model)
            personality = "أنت 'خضر AI' صاحب الأرجنتيني. فرفوش ومصري وبتقول يا زميلي. "
            
            payload = [personality + prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                payload.append(img)
            
            response = model.generate_content(payload)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"النظام ده معلق: {e}")
    
