import streamlit as st
import google.generativeai as genai

# --- 1. المفتاح الجديد ---
# حط المفتاح اللي صاحبك هيبعتهولك هنا بين علامتين التنصيص
MY_KEY = "AIzaSyC2-3pnFUCNmIk86fE3FWHeMktFS3FcNt8" 

# إعدادات الربط
try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY", MY_KEY)
    if API_KEY and API_KEY != "AIzaSy...":
        genai.configure(api_key=API_KEY)
    else:
        st.warning("⚠️ في انتظار وضع المفتاح الجديد (API Key)")
except:
    st.error("مشكلة في إعدادات الربط")

# --- 2. واجهة التطبيق ---
st.set_page_config(page_title="خضر AI", page_icon="🤖")
st.title("🤖 خضر AI")
st.caption("تطوير Argentiny@khedr")

# --- 3. الدردشة والذكاء الاصطناعي ---
prompt = st.chat_input("اسأل خضر أي حاجة...")

if prompt:
    with st.chat_message("assistant"):
        # مصفوفة بأسماء الموديلات عشان لو واحد منفعش التاني يشتغل
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        success = False
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                st.write(response.text)
                success = True
                break # أول ما يشتغل يخرج من اللفة
            except:
                continue # لو فشل يجرب الموديل اللي بعده
        
        if not success:
            st.error("جوجل لسه مش شايفة المفتاح.. تأكد إن المفتاح من حساب جديد وشغال.")

# --- 4. التوقيع ---
st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
