import streamlit as st
from llm_service.ollama_service import OllamaService

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Smart Home Assistant. How can I help you today?"}
        ]
    if "ollama_service" not in st.session_state:
        st.session_state.ollama_service = OllamaService()

def process_message(prompt: str):
    """Process a new message and get response from Ollama."""
    if prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Get response from Ollama
        response = st.session_state.ollama_service.chat(prompt)
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

def handle_quick_action(action_type: str):
    """Handle quick action button clicks."""
    prompts = {
        "energy_report": "Generate an energy usage report for today",
        "temperature": "What's the current temperature and what do you recommend?",
        "smart_tips": "Give me some energy saving tips",
        "device_status": "Show me the status of all connected devices"
    }
    if action_type in prompts:
        process_message(prompts[action_type])

def chat_window():
    """Main chat window UI component."""
    # Custom CSS for chat window
    st.markdown("""
        <style>
        .chat-container {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            height: 60vh;
            overflow-y: auto;
        }
        .user-message {
            background-color: #2d2d2d;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            text-align: right;
        }
        .assistant-message {
            background-color: #0e4166;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            text-align: left;
        }
        .stTextInput input {
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #444;
        }
        .quick-actions {
            margin-top: 10px;
            padding: 10px;
            background-color: #1e1e1e;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    initialize_chat_history()

    # Chat messages container
    with st.container():
        st.markdown("### 🤖 Smart Home Assistant")

        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="user-message">
                        👤 {message["content"]}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="assistant-message">
                        🤖 {message["content"]}
                    </div>
                """, unsafe_allow_html=True)

        # Chat input using callback
        if "chat_input_key" not in st.session_state:
            st.session_state.chat_input_key = 0

        # Use a unique key for the text input each time we want to clear it
        prompt = st.text_input(
            "Ask me anything...",
            key=f"chat_input_{st.session_state.chat_input_key}"
        )

        if prompt:
            process_message(prompt)
            # Increment the key to create a new input widget
            st.session_state.chat_input_key += 1
            st.rerun()

        # Quick actions
        with st.expander("Quick Actions"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Energy Report", key="energy_report"):
                    handle_quick_action("energy_report")
                    st.session_state.chat_input_key += 1
                    st.rerun()
                if st.button("🌡️ Temperature", key="temp_control"):
                    handle_quick_action("temperature")
                    st.session_state.chat_input_key += 1
                    st.rerun()
            with col2:
                if st.button("💡 Smart Tips", key="smart_tips"):
                    handle_quick_action("smart_tips")
                    st.session_state.chat_input_key += 1
                    st.rerun()
                if st.button("🏠 Device Status", key="device_status"):
                    handle_quick_action("device_status")
                    st.session_state.chat_input_key += 1
                    st.rerun()