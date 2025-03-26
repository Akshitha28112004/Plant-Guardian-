import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Plant Guardian", page_icon="🌱") 

# Replace with your actual Google Cloud API key
GOOGLE_API_KEY = "API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the chatbot session
if "chat" not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')  # Use the latest version
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Set page title and header
st.markdown(
    """
    <h1 style="text-align: center; color: #2E8B57;">Plant Guardian 🌱</h1>
    <p style="text-align: center; font-size: 18px;">Your personal plant care assistant. Ask me anything about plant care!🌿</p>
    <hr>
    """,
    unsafe_allow_html=True,
)

# Initial chatbot introduction and prompt setup
initial_query = (
    "Act as a plant care assistant chatbot called 'Plant Guardian AI'. "
    "Users will ask about plant-related queries such as watering, sunlight needs, soil, diseases, and fertilizers. "
    "You should ONLY respond to plant-related queries. If a question is unrelated, politely ask the user to focus on plant care. "
    "Introduce yourself as 'Plant Guardian AI' and be interactive in your responses."
)
st.session_state.chat.send_message(initial_query)

# Display chatbot introduction message
with st.chat_message("assistant", avatar="🌱"):
    st.markdown("Hello! I am **Plant Guardian AI**. Ask me anything about plant care, and I'll provide the best advice to help your plants thrive! 🌿")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🌿" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# User input field
if prompt := st.chat_input("Ask about plant care..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(response.text)

        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown("I can't help with that. Please ask only plant-related questions! 🌱")
