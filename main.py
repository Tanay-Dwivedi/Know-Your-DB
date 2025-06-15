# main.py

import streamlit as st
from json_chat_bot import handle_json_chat

# Set page config
st.set_page_config(page_title="🧠 Know Your DB", layout="wide")
st.title("🧠 Chat with Know Your DB Bot")

# Center title
st.markdown("<h1 style='text-align: center;'>Know Your DB</h1>", unsafe_allow_html=True)
st.markdown("###")

# Layout for dropdown and uploader
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    file_type = st.selectbox("Select File Type", ["Excel", "CSV", "JSON"])

file_extensions = {
    "Excel": ["xls", "xlsx"],
    "CSV": ["csv"],
    "JSON": ["json"]
}

with col2:
    uploaded_file = st.file_uploader(
        f"Upload your {file_type} file",
        type=file_extensions[file_type],
        key="file_uploader"  # consistent key
    )

# Sidebar API key input
together_api_key = st.sidebar.text_input("🔑 Enter your Together API Key", type="password")

# Call appropriate handler
if file_type == "JSON" and uploaded_file and together_api_key:
    handle_json_chat(uploaded_file, together_api_key)
elif uploaded_file and not together_api_key:
    st.warning("⚠️ Please enter your Together API Key.")
