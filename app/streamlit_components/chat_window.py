import streamlit as st
import asyncio
from google.genai import types
from app.runner_setup import runner, USER_ID, SESSION_ID


def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm Homie, your Smart Home Assistant. How can I help you today?"}
        ]

    # Limit message history to last 10 messages to prevent overflow
    if len(st.session_state.messages) > 10:
        st.session_state.messages = st.session_state.messages[-10:]


async def process_message(prompt: str):
    """Process a new message and get response from the ADK agent."""
    if prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            # Prepare the user's message in ADK format
            content = types.Content(role='user', parts=[types.Part(text=prompt)])

            # Default response in case no final response is received
            final_response_text = "Agent did not produce a final response."

            # Process events from the agent
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=content
            ):
                # Process intermediate responses
                if event.content and event.content.parts and event.content.parts[0].text:
                    # Add intermediate responses to chat
                    intermediate_text = event.content.parts[0].text
                    if intermediate_text.strip() and not event.is_final_response():  # Only add non-empty, non-final responses
                        # Store intermediate response but don't rerun to avoid infinite loop
                        st.session_state.messages.append({"role": "assistant", "content": f"{intermediate_text}"})
                        # Display the message without rerunning
                        st.chat_message("assistant").write(f"{intermediate_text}")

                # Process final response
                if event.is_final_response():
                    if event.content and event.content.parts:
                        # Get text from the first part
                        final_response_text = event.content.parts[0].text
                    elif event.actions and event.actions.escalate:
                        final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                    break  # Stop processing events once we have the final response

        except Exception as e:
            error_msg = f"Error interacting with ADK agent: {e}"
            st.error(error_msg)
            final_response_text = "Sorry, I encountered an error trying to process your request."

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": final_response_text})

        # Limit message history to last 10 messages
        if len(st.session_state.messages) > 10:
            st.session_state.messages = st.session_state.messages[-10:]


def chat_window():
    """Main chat window UI component."""
    initialize_chat_history()

    st.markdown("""
    <style>
    .custom-chat-area .stTextArea textarea {
        background-color: rgba(10, 10, 20, 0.8) !important;
        color: #FFFFFF !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        border: 1px solid #505050 !important;
        height: 600px !important;
        width: 200% !important;
        padding: 12px !important;
        line-height: 1.4 !important;
    }

    .custom-chat-input .stTextInput input {
        background-color: rgba(10, 10, 20, 0.8) !important;
        color: #FFFFFF !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        border: 1px solid #505050 !important;
        padding: 12px 10px !important;
        width: 200% !important;
        line-height: 1.4 !important;
    }

    /* Hide the "Chat History" and empty labels */
    .custom-chat-area label, .custom-chat-input label {
        display: none !important;
    }

    /* Placeholder text color */
    .custom-chat-input .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Focus states */
    .custom-chat-area .stTextArea textarea:focus,
    .custom-chat-input .stTextInput input:focus {
        border-color: #7C4DFF !important;
        box-shadow: 0 0 0 1px #7C4DFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Format messages like logs
    chat_content = []
    for message in st.session_state.messages:
        if message["role"] == "user":
            prefix = 'User: '
        else:
            prefix = 'Homie: '
        chat_content.append(f"{prefix} {message['content']}")

    # Display chat history with emoji header
    st.markdown('<div class="chat-header">💬 Chat History</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-chat-area">', unsafe_allow_html=True)
    st.text_area(
        "",
        value="\n".join(chat_content),
        height=450,
        key="chat_history_area",
        disabled=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input with emoji header
    st.markdown('<div class="chat-header">⌨️ Message Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-chat-input">', unsafe_allow_html=True)
    if "chat_input_key" not in st.session_state:
        st.session_state.chat_input_key = 0

    prompt = st.text_input(
        "",
        placeholder="Type your message...",
        key=f"chat_input_{st.session_state.chat_input_key}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if prompt:
        asyncio.run(process_message(prompt))
        st.session_state.chat_input_key += 1
        st.rerun()
