import streamlit as st
from groq_copilot import get_coding_response
import os

# Streamlit app configuration
st.set_page_config(page_title="Rogers Coding Copilot", page_icon="💻", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTextArea textarea { border-radius: 10px; padding: 10px; }
    .stButton button { background-color: #1e90ff; color: white; border-radius: 5px; }
    .stMarkdown { font-family: 'Arial', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("Rogers Coding Copilot")
st.markdown("Your AI-powered coding assistant for code generation, debugging, and explanations, powered by Groq's ultra-fast inference.")

# Input form
with st.form("coding_form"):
    user_prompt = st.text_area("Enter your coding query:", height=150, placeholder="E.g., 'Write a Python function to sort a list' or 'Debug this code...'")
    context_file = st.text_input("Optional: Path to context file (e.g., sample.py)", "")
    submit_button = st.form_submit_button("Get Response")

# Display response
if submit_button and user_prompt:
    with st.spinner("Generating response..."):
        context_file_path = os.path.normpath(context_file) if context_file else None
        response = get_coding_response(user_prompt, context_file=context_file_path)
        st.markdown("### Response")
        st.markdown(response)