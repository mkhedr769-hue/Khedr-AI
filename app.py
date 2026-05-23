import streamlit as st
import google.generativeai as genai

# --- 1. إعداد المفتاح (تم وضع المفتاح الجديد هنا) ---
MY_KEY = "AIzaSyC2-3pnFUCNmIk86fE3FWHeMktFS3FcNt8" 

try:
    genai.configure(api_key=MY_KEY)
except:
    st.error("مشكلة في إعدادات الربط")

# --- 2. واجهة التطبيق ---
st.set_page_config(page_title="خضر AI", page_icon="🤖")
st.title("🤖 خضر AI")
st.caption("تطوير Argentiny@khedr")

# --- 3. الدردشة الذكية ---
prompt = st.chat_input("اسأل خضر أي حاجة...")

if prompt:
    with st.chat_message("assistant"):
        # الكود ده بيدور تلقائياً على الموديل اللي شغال في الحساب
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                # بيختار أول موديل متاح (زي gemini-1.5-flash أو gemini-pro)
                model = genai.GenerativeModel(available_models[0])
                response = model.generate_content(prompt)
                st.write(response.text)
            else:
                st.error("جوجل لسه مفعلتش الموديلات على الحساب ده، جرب تبعت رسالة في AI Studio الأول.")
        except Exception as e:
            # لو الموديلات التلقائية منفعش، بنجرب الموديل الأساسي كحل أخير
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e2:
                st.error(f"خطأ من جوجل: {str(e2)}")

st.write("---")
st.markdown("<center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
