import streamlit as st
import google.generativeai as genai

# حط مفتاحك هنا
MY_KEY = "AIzaSyDi4_5LvrbzqXyiWmkwt5muPElGafreY3M" 

try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY", MY_KEY)
    genai.configure(api_key=API_KEY)
except:
    st.error("Error setting up API")

st.title("🤖 خضر AI")
st.caption("تطوير Argentiny@khedr")

prompt = st.chat_input("اسأل خضر...")

if prompt:
    with st.chat_message("assistant"):
        try:
            # جربنا نغير الموديل لـ gemini-pro لأنه مضمون أكتر في النسخ دي
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"جوجل بتقول: {str(e)}")

st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
