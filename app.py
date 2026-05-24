import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- الربط السري ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ضيف المفتاح في Secrets")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖")

# --- ستايل تظبيط شكل الزائد (+) جنب الإرسال ---
st.markdown("""
    <style>
    .main-title { font-size: 35px; font-weight: bold; text-align: center; color: #00ffcc; }
    /* تصغير خانة الرفع عشان تبقى شيك */
    .stFileUploader { margin-bottom: -40px; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- منطقة الرفع (الزائد) ---
# خليتها فوق خانة الكتابة مباشرة عشان تبقى قريبة من إيدك
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# خانة الكتابة
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعليمات خضر الفرفوش
            instruction = "أنت خضر AI، صاحب الأرجنتيني. فرفوش وبتتكلم مصري وبتقول يا زميلي. لما يقولك عامل إيه قوله الحمد لله يا زميلي."
            
            # هنا حلينا الـ 404: بنستخدم الاسم المختصر للموديل
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            content = [instruction, prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                content.append(img)
            
            response = model.generate_content(content)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"حصلت قفلة: {e}")

# مسح الشات في الجنب
with st.sidebar:
    if st.button("🗑️ مسح الشات"):
        st.session_state.messages = []
        st.rerun()
        
