import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. الربط والمفتاح ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ ناقصك المفتاح في الـ Secrets!")

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="centered")

# --- 2. ستايل "شات جي بي تي" السري ---
st.markdown("""
    <style>
    /* إخفاء النصوص الزائدة في زر الرفع */
    .stFileUploader section { padding: 0; min-height: 0; border: none; }
    .stFileUploader label { display: none; }
    .stFileUploader [data-testid="stFileUploaderFileName"] { display: none; }
    
    /* تظبيط المسافات بين الأعمدة */
    [data-testid="column"] { display: flex; align-items: flex-end; }
    .main-title { font-size: 30px; text-align: center; color: #00ffcc; font-weight: bold; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# اختيار المحرك من الجنب (خليته 2.5 كاختيار أول)
with st.sidebar:
    st.title("⚙️ التحكم")
    model_id = st.selectbox("النظام:", ["gemini-1.5-flash", "gemini-pro"])
    if st.button("🗑️ مسح"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 3. حركة "الزائد" الاحترافية جنب الإرسال ---
# بنقسم السطر لعمودين: واحد صغير جداً للزائد والتاني للكتابة
col1, col2 = st.columns([0.15, 0.85])

with col1:
    # زر الرفع بقى عبارة عن علامة (+) فقط ومكانه جنب الإرسال
    uploaded_file = st.file_uploader("➕", type=["jpg", "png", "jpeg"], key="plus_btn")

with col2:
    prompt = st.chat_input("قول يا حب...")

# --- 4. معالجة الرد ---
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(model_id)
            personality = "أنت 'خضر AI' صاحب الأرجنتيني. فرفوش ومصري. "
            
            payload = [personality + prompt]
            if uploaded_file:
                img = Image.open(uploaded_file)
                payload.append(img)
            
            response = model.generate_content(payload)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"حصلت قفلة: {e}")
    
