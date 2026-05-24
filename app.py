import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. الربط بمفتاح جوجل (Secrets) ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ناقصك المفتاح في الـ Secrets!")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖")

# --- 2. ستايل تظبيط الواجهة ---
st.markdown("""
    <style>
    .stFileUploader { margin-bottom: -45px; }
    .main-title { font-size: 30px; text-align: center; color: #00ffcc; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. القائمة الجانبية (اختيار النظام) ---
with st.sidebar:
    st.title("⚙️ إعدادات خضر")
    # هنا الميزة اللي طلبتها: اختيار النظام
    model_choice = st.selectbox(
        "اختار نظام الـ AI:",
        ("Gemini 1.5 Flash (سريع)", "Gemini 1.5 Pro (ذكي جداً)", "Gemini Pro (مستقر)")
    )
    
    # تحويل الاختيار لاسم الموديل التقني
    model_map = {
        "Gemini 1.5 Flash (سريع)": "gemini-1.5-flash",
        "Gemini 1.5 Pro (ذكي جداً)": "gemini-1.5-pro",
        "Gemini Pro (مستقر)": "gemini-pro"
    }
    selected_model = model_map[model_choice]
    
    st.write("---")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# علامة الزائد (+) للصور فوق خانة الكتابة
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# --- 4. منطق الإرسال والرد ---
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تشغيل الموديل اللي تم اختياره من القائمة
            model = genai.GenerativeModel(selected_model)
            
            # شخصية خضر الفرفوش
            personality = "أنت 'خضر AI' صاحب الأرجنتيني. فرفوش وبتتكلم مصري جدع وبتقول يا زميلي. "
            full_prompt = personality + prompt
            
            # تجهيز المحتوى (نص + صورة)
            parts = [full_prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                parts.append(img)
            
            # طلب الرد
            response = model.generate_content(parts)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"النظام ده فيه مشكلة حالياً: {e}")
            st.info("نصيحة: جرب تختار 'Gemini Pro (مستقر)' من القائمة اللي في الجنب.")
                
