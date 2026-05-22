import streamlit as st
import google.generativeai as genai

# --- 1. المفتاح السحري ---
# حط مفتاحك الجديد مكان النجوم هنا
MY_KEY = "AIzaSyAIzaSyCUkgFQp-XJ_xiZRgZuVXexeSIWZGl2YuE" 

# محاولة الربط بالمفتاح
try:
    # جرب يلقط من Secrets الأول، لو منفعش ياخد اللي فوق
    API_KEY = st.secrets.get("GOOGLE_API_KEY", MY_KEY)
    genai.configure(api_key=API_KEY)
except:
    st.error("Problem with API Key")

# --- 2. إعدادات الواجهة ---
st.set_page_config(page_title="Khedr AI", page_icon="🤖")
st.title("🤖 خضر AI")
st.caption("تطوير Argentiny@khedr")

# --- 3. الدردشة ---
prompt = st.chat_input("اسأل خضر...")

if prompt:
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            # لو المفتاح غلط هيظهرلك الرسالة دي عشان نتأكد
            st.error(f"المفتاح غير صالح أو محظور. تأكد من نسخه صح.")

st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
