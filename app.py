import streamlit as st
import google.generativeai as genai

# حط مفتاحك الجديد هنا
MY_KEY = "AIzaSyAIzaSyDi4_5LvrbzqXyiWmkwt5muPElGafreY3M" 

# إعداد الربط
try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY", MY_KEY)
    genai.configure(api_key=API_KEY)
except:
    st.error("Error with API settings")

st.title("🤖 خضر AI")
st.caption("تطوير Argentiny@khedr")

prompt = st.chat_input("اسأل خضر...")

if prompt:
    with st.chat_message("assistant"):
        # مصفوفة بأسماء الموديلات المتاحة عند جوجل
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        success = False
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                st.write(response.text)
                success = True
                break # أول ما واحد يشتغل يخرج من اللفة
            except:
                continue # لو فشل يجرب اللي بعده
        
        if not success:
            st.error("جوجل لسه مش شايفة المفتاح بتاعك.. جرب حساب جيميل تاني.")

st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
            
