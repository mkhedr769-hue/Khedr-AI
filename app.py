import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات المفتاح ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ناقصك المفتاح في الـ Secrets باسم GOOGLE_API_KEY")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖")

# --- 2. ستايل تظبيط شكل الزائد (+) ---
st.markdown("""
    <style>
    .main-title { font-size: 35px; text-align: center; color: #00ffcc; font-weight: bold; }
    .stFileUploader { margin-bottom: -45px; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. اختيار النظام من الجنب (ضفنا 2.5 فلاش) ---
with st.sidebar:
    st.title("⚙️ غرفة التحكم")
    model_choice = st.selectbox(
        "اختار المحرك (النظام):",
        ["Gemini 2.5 Flash (الأحدث)", "Gemini 1.5 Pro (العبقري)", "Gemini Pro (المستقر)"]
    )
    
    # ربط الاختيارات بالأسماء التقنية
    model_map = {
        "Gemini 2.5 Flash (الأحدث)": "gemini-2.5-flash",
        "Gemini 1.5 Pro (العبقري)": "gemini-1.5-pro",
        "Gemini Pro (المستقر)": "gemini-pro"
    }
    selected_model = model_map[model_choice]
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. علامة الزائد (+) للصور ---
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# --- 5. منطق الرد (خضر الفرفوش) ---
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تشغيل الموديل اللي اخترته (اللي هو غالباً 2.5 دلوقتي)
            model = genai.GenerativeModel(selected_model)
            
            # السيستم (شخصية خضر)
            personality = "أنت 'خضر AI' صاحب الأرجنتيني. فرفوش ومصري وبتقول يا زميلي. "
            
            payload = [personality + prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                payload.append(img)
            
            response = model.generate_content(payload)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            if "429" in str(e):
                st.error("جوجل بتقولك الموديل ده جاب جاز النهاردة، غير النظام من الجنب لـ 'المستقر'.")
            else:
                st.error(f"حصلت قفلة: {e}")
                
