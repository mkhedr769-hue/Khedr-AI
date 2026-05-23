import streamlit as st
import google.generativeai as genai
from PIL import Image
import shelve
import time

# --- 1. إعدادات الصفحة والبراند ---
API_KEY = "AIzaSyC2-3pnFUCNmIk86fE3FWHeMktFS3FcNt8"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Khedr-AI", page_icon="🤖", layout="wide")

# رابط الصورة الفخمة اللي بعتها (تم استخدامها كـ Avatar)
# ملاحظة: استبدل الرابط أدناه برابط الصورة المباشر بعد رفعها أو تأكد من وجودها في نفس مجلد الكود
AI_AVATAR = "https://lh3.googleusercontent.com/d/1000167319.jpg" # رابط تخيلي للصورة المرفوعة

# --- 2. ستايل الـ Premium ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0E1117; border-right: 1px solid #333; }
    .stChatFloatingInputContainer { background-color: rgba(0,0,0,0); }
    .stChatMessage { border-radius: 12px; }
    
    /* ستايل لجعل صورة الـ AI تظهر بالكامل وبشكل احترافي */
    [data-testid="stChatMessageAvatarCustom"] img {
        object-fit: contain !important;
        border-radius: 5px !important;
    }

    .main-title {
        font-size: 55px;
        font-weight: bold;
        text-align: center;
        color: #00ffcc;
        text-shadow: 2px 2px 10px rgba(0,255,204,0.3);
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. قاعدة بيانات المحادثات (Shelve) ---
def get_db():
    return shelve.open("khedr_history_db")

if "all_chats" not in st.session_state:
    with get_db() as db:
        st.session_state.all_chats = db.get("chats", {})

# --- 4. القائمة الجانبية (السجل والإضافات) ---
with st.sidebar:
    st.markdown('<p style="font-size: 22px; font-weight: bold; color: #00ffcc;">Khedr History</p>', unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_chat_id = str(time.time())
        st.session_state.messages = []
        st.rerun()
    
    st.write("---")
    for cid, cdata in st.session_state.all_chats.items():
        if st.button(f"💬 {cdata['title']}", key=cid, use_container_width=True):
            st.session_state.current_chat_id = cid
            st.session_state.messages = cdata["messages"]
            st.rerun()
    
    st.write("---")
    uploaded_file = st.file_uploader("➕ Attachment", type=["jpg", "jpeg", "png"])

# --- 5. منطق المحادثة ---
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(time.time())

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-title">Khedr-AI</p>', unsafe_allow_html=True)
st.caption("<center>Powering your imagination - By Argentiny@khedr</center>", unsafe_allow_html=True)

# عرض الشات بالصورة الجديدة
for msg in st.session_state.messages:
    avatar = AI_AVATAR if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("Ask Khedr-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AI_AVATAR):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            inputs = [prompt]
            if uploaded_file:
                inputs.append(Image.open(uploaded_file))
            
            response = model.generate_content(inputs)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # حفظ في السجل
            chat_title = st.session_state.messages[0]["content"][:25]
            st.session_state.all_chats[st.session_state.current_chat_id] = {
                "title": chat_title, "messages": st.session_state.messages
            }
            with get_db() as db:
                db["chats"] = st.session_state.all_chats
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("<br><hr><center>All Rights Reserved © Argentiny@khedr</center>", unsafe_allow_html=True)
    
