import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configuring the Streamlit page
st.set_page_config(
    page_title="Talk with Gemini",
    page_icon=":🌐:",
    layout="centered"
)

# Setting up Google Gemini AI models
gen_ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def translate_role_for_streamlit(user_role):
    """Translate Gemini role to Streamlit terminology."""
    return "model" if user_role == "assistant" else "user"

def get_gemini_response(input_text, model_id):
    """Get response from Gemini AI model."""
    chat_session = st.session_state.chat_sessions[model_id]
    response = chat_session.send_message(input_text)
    return response.text

# Initialize chat sessions and history if not already present
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
    st.session_state.chat_history = []
    st.session_state.selected_model_id = None

# Sidebar content
st.sidebar.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <h1 style="font-size: 24px;">Gemini GPT</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("f1eda4768df8d8135c779772f2833e88 (1).gif", use_column_width=True)

# Sidebar for model selection
model_choice = st.sidebar.selectbox("Choose the model:", ("Fast", "Pro", "Normal"))

# Map the model choice to the respective model ID
model_id_map = {
    "Fast": "gemini-1.5-flash-latest",
    "Pro": "gemini-1.5-pro-latest",
    "Normal": "gemini-1.0-pro"
}
selected_model_id = model_id_map[model_choice]

# Initialize or switch chat session based on selected model
if selected_model_id not in st.session_state.chat_sessions:
    # Ensure history is in the correct format
    formatted_history = [{"role": "model" if msg["role"] == "assistant" else "user", "parts": [{"text": msg["text"]}]} for msg in st.session_state.chat_history]
    model = gen_ai.GenerativeModel(selected_model_id)
    st.session_state.chat_sessions[selected_model_id] = model.start_chat(history=formatted_history)

# Display the chatbot on webpage
st.title("Gemini GPT - Unleash The Beast")

# Display the chat history for the selected model
chat_session = st.session_state.chat_sessions[selected_model_id]
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Input field for user's message
user_prompt = st.chat_input("Ask me...")

if user_prompt:
    # Add user message to chat history and display it
    user_message = {"role": "user", "text": user_prompt}
    st.session_state.chat_history.append(user_message)
    st.chat_message("user").markdown(user_prompt)

    # Get Gemini-Pro's response
    gemini_response_text = get_gemini_response(user_prompt, selected_model_id)
    gemini_response = {"role": "model", "text": gemini_response_text}

    # Add Gemini-Pro's response to chat history and display it
    st.session_state.chat_history.append(gemini_response)
    with st.chat_message("model"):
        st.markdown(gemini_response_text)

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 10px;
        bottom: 10px;
        color: gray;
        font-size: 12px;
    }
    </style>
    """
    , unsafe_allow_html=True)

st.sidebar.header('Made by Ayush Kumar')