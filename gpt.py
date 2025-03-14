import os
import streamlit as st
import google.generativeai as gen_ai

# Load environment variables

# Configure Streamlit page settings
st.set_page_config(
    page_title="Trav bot",
    page_icon=":alien:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Sidebar to input Google API Key
st.sidebar.title("TRIP SUGGEST")
GOOGLE_API_KEY = "AIzaSyDiF3G98dWgoXvOo0FIGI4OgVxVxhpFU7U"

# Check if API key is provided
if not GOOGLE_API_KEY:
    st.error("no api key")
    st.stop()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("ð¤ Trav bot ")

# Add small text below the header


# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask â¨...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)