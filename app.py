import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة واللغة التلقائية ---
# بيحاول يلقط لغة المتصفح، لو معرفش بيخليها عربي كافتراض
user_lang = st.query_params.get("lang", ["ar"])[0][:2]

texts = {
    "ar": {"title": "خضر AI", "sub": "تطوير Argentiny@khedr", "input": "اسأل خضر AI أي حاجة...", "side": "➕ الإضافات", "up": "ارفع صورة أو ملف"},
    "en": {"title": "Khedr AI", "sub": "Developed by Argentiny@khedr", "input": "Ask Khedr AI anything...", "side": "➕ Add-ons", "up": "Upload image or file"},
    "de": {"title": "Khedr AI", "sub": "Entwickelt von Argentiny@khedr", "input": "Frag Khedr AI etwas...", "side": "➕ Extras", "up": "Bild oder Datei hochladen"}
}

# اختيار اللغة بناءً على لغة المتصفح أو العربي كافتراض
content = texts.get(user_lang, texts["ar"])

st.set_page_config(page_title=content["title"], page_icon="🤖")

# --- 2. إدارة المفتاح (API KEY) ---
# الكود بيدور في الـ Secrets الأول، لو ملقاش بياخد المفتاح اللي هتحطه هنا كاحتياط
try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY", "حط_مفتاحك_هنا_بين_العلامات")
    if API_KEY and API_KEY != "AIzaSyCUkgFQp-XJ_xiZRgZuVXexeSIWZGl2YuE":
        genai.configure(api_key=API_KEY)
    else:
        st.warning("⚠️ محتاجين المفتاح (API Key) عشان نشتغل")
except Exception as e:
    st.error("مشكلة في إعدادات المفتاح")

# --- 3. تصميم الواجهة ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #161b22; }}
    </style>
""", unsafe_allow_html=True)

st.title(f"🤖 {content['title']}")
st.caption(content["sub"])

# --- 4. علامة الزائد (في القائمة الجانبية) ---
with st.sidebar:
    st.header(content["side"])
    uploaded_file = st.file_uploader(content["up"], type=["jpg", "png", "jpeg", "pdf", "txt"])
    if uploaded_file:
        st.success("✅ تم رفع الملف")

# --- 5. منطقة الدردشة ---
prompt = st.chat_input(content["input"])

if prompt:
    with st.chat_message("assistant"):
        try:
            # استخدام موديل فلاش السريع
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            inputs = [prompt]
            if uploaded_file:
                if uploaded_file.type.startswith("image"):
                    img = Image.open(uploaded_file)
                    inputs.append(img)
            
            # توجيه الموديل للرد بلغة المستخدم
            inputs.append(f"Please respond in {user_lang} language.")
            
            response = model.generate_content(inputs)
            st.markdown(response.text)
            
        except Exception as e:
            st.error("المفتاح محتاج تحديث، تواصل مع المطور!")

# --- 6. التوقيع النهائي ---
st.markdown("<br><hr><center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
