import os
import streamlit as st
import google.generativeai as gen_ai

# Load environment variables

# Configure Streamlit page settings
st.set_page_config(
    page_title="Trav Bot",
    page_icon="🛸",  # Favicon emoji
    layout="centered",
)

# Custom CSS for styling
def set_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #ffffff;
            color: #333333;
        }
        .stApp {
            background: linear-gradient(to right, #ff5f6d, #ffc371);
        }
        .stChatMessage {
            border-radius: 20px;
            padding: 10px;
        }
        .stChatMessage.user {
            background-color: #ff5f6d;
            color: white;
        }
        .stChatMessage.assistant {
            background-color: #ffc371;
            color: black;
        }
        .sidebar .sidebar-content {
            background-color: #ff5f6d;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

set_custom_css()

# Sidebar for API Key input
st.sidebar.title("🚀 Trip Suggest")
GOOGLE_API_KEY = "AIzaSyDiF3G98dWgoXvOo0FIGI4OgVxVxhpFU7U"

# Check if API key is provided
if not GOOGLE_API_KEY:
    st.error("No API key provided.")
    st.stop()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot title
st.markdown("<h1 style='text-align: center; color: #ff5f6d;'>🤖 Trav Bot</h1>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# User input field
user_prompt = st.chat_input("Ask me anything ✨...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
