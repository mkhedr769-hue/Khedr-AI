import streamlit as st
import google.generativeai as genai

# حط مفتاحك هنا وتأكد إنه شغال
MY_KEY = "AIzaSyDi4_5LvrbzqXyiWmkwt5muPElGafreY3M" 

# إعداد المكتبة بأحدث طريقة
try:
    API_KEY = st.secrets.get("GOOGLE_API_KEY", MY_KEY)
    genai.configure(api_key=API_KEY)
except:
    st.error("Problem with API settings")

st.title("🤖 خضر AI")
st.caption("تطوير Argentiny@khedr")

prompt = st.chat_input("اسأل خضر...")

if prompt:
    with st.chat_message("assistant"):
        try:
            # الحل السحري: بنجرب الموديل المستقر (gemini-1.5-flash-latest)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            try:
                # لو الأول منفعش بنجرب الموديل البديل فوراً
                model = genai.GenerativeModel('gemini-1.0-pro')
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e2:
                st.error(f"جوجل بتقول: {str(e2)}")

st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
