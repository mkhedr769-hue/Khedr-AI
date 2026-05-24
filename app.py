import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- الربط السري بمفتاح جوجل ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ضيف المفتاح في Secrets")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖")

# --- ستايل لتقريب المسافات وتظبيط الشكل ---
st.markdown("""
    <style>
    .main-title { font-size: 40px; font-weight: bold; text-align: center; color: #00ffcc; margin-top: -30px; }
    /* تصغير مساحة الرفع عشان متخدش مكان كبير */
    .stFileUploader { padding: 0px 10px; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- منطقة الإدخال (الزائد + والرفع تحت) ---
# عملنا حاجة اسمها container عشان الرفع يظهر فوق الكتابة علطول
input_container = st.container()
with input_container:
    # علامة الزائد والرفع هنا بدل الـ Sidebar
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# شريط الكتابة الأساسي
if prompt := st.chat_input("قول يا حب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام الموديل المستقر
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # شخصية خضر الفرفوش
            sys_msg = "أنت خضر AI، صاحب الأرجنتيني. فرفوش وبتتكلم مصري وبتقول يا زميلي. ردك سريع ومختصر."
            
            content = [sys_msg, prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                content.append(img)
            
            response = model.generate_content(content)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            if "404" in str(e):
                st.error("جوجل بتهزر.. لحظة وبظبطلك الموديل!")
                model = genai.GenerativeModel('gemini-pro') # حل احتياطي
            else:
                st.error(f"حصل قفلة: {e}")

# زرار مسح الشات خليته في الجنب عشان ميزحمش الدنيا
with st.sidebar:
    if st.button("🗑️ مسح الشات"):
        st.session_state.messages = []
        st.rerun()
        
