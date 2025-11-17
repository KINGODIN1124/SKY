import streamlit as st
from modules.assistant import sky_reply
from modules.memory import load_memory, save_memory
from modules.file_handler import handle_file_upload
from modules.web_browse import browse_web
from modules.translation import translate_text
from modules.monitoring import get_stats
from config import CURRENT_PERSONA, AVAILABLE_MODELS, GROQ_MODEL

st.title("SKY AI Assistant")

# Sidebar for settings
st.sidebar.header("Settings")
persona = "default"
model = st.sidebar.selectbox("Model", AVAILABLE_MODELS, index=AVAILABLE_MODELS.index(GROQ_MODEL))

# Load history
if 'history' not in st.session_state:
    st.session_state.history = load_memory()

# Chat interface
user_input = st.text_input("Ask SKY:")

if st.button("Send") and user_input:
    reply = sky_reply(user_input, st.session_state.history)
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": reply})
    save_memory(st.session_state.history)
    st.write(f"SKY: {reply}")

# File upload
uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    with open(f"temp_{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    result = handle_file_upload(f"temp_{uploaded_file.name}")
    st.write(f"File content: {result}")

# Web browse
url = st.text_input("Browse URL:")
if st.button("Browse") and url:
    result = browse_web(url)
    st.write(f"Web content: {result}")

# Translation
text_to_translate = st.text_input("Translate text:")
target_lang = st.text_input("To language (e.g., es):")
if st.button("Translate") and text_to_translate and target_lang:
    result = translate_text(text_to_translate, target_lang)
    st.write(f"Translated: {result}")

# Monitoring
if st.button("View Stats"):
    stats = get_stats()
    st.json(stats)
