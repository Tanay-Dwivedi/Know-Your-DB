import streamlit as st
from chat_engine import load_json_context_from_file, get_chat_chain

# Set page config
st.set_page_config(page_title="Know Your DB", layout="wide")

# Center the title using HTML and CSS
st.markdown(
    """
    <h1 style='text-align: center;'>Know Your DB</h1>
    """,
    unsafe_allow_html=True
)

# Add vertical space
st.markdown("###")

# Centered dropdown and uploader
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
        label_visibility="visible"
    )

    if uploaded_file is not None:
        st.markdown(
            f"<div style='text-align: center; color: green; font-weight: bold;'>Uploaded file: {uploaded_file.name}</div>",
            unsafe_allow_html=True
        )

# Initialize chat state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Activate chatbot only if JSON file is uploaded
if file_type == "JSON" and uploaded_file is not None:
    try:
        json_context = load_json_context_from_file(uploaded_file)
        chat_chain = get_chat_chain(json_context)

        user_input = st.chat_input("Ask me anything about the JSON data...")

        if user_input:
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            response = chat_chain.invoke({"json_context": json_context, "question": user_input})
            st.session_state.chat_history.append({"role": "assistant", "text": response})

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["text"])

    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
elif file_type == "JSON":
    st.info("Upload a valid classroom JSON file to begin chatting.")
