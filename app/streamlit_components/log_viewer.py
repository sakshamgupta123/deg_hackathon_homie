import streamlit as st
import os
import time


def display_log_viewer():
    st.markdown("""
    <style>
    .custom-log-area .stTextArea textarea {
        background-color: rgba(10, 10, 20, 0.7) !important; /* Darker background for log area */
        color: #A0A0A0 !important; /* Lighter grey text */
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 0.85rem !important;
        border: 1px solid #303030 !important;
        height: 100% !important; /* Fill the .log-panel height */
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("📋 Agent Activity Logs")

    # Read the latest logs from progress.log file
    log_content = "No logs found."
    log_file_path = "app/logs/progress.log"

    if os.path.exists(log_file_path):
        try:
            # Read the file and get the last 20 lines
            with open(log_file_path, 'r') as file:
                lines = file.readlines()
                log_content = ''.join(lines[-40:]) if lines else "Log file is empty."
        except Exception as e:
            log_content = f"Error reading log file: {str(e)}"
    else:
        # Create the log file if it doesn't exist
        try:
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            with open(log_file_path, 'w') as file:
                file.write("Log file created.\n")
            log_content = "Log file created: logs/progress.log"
        except Exception as e:
            log_content = f"Error creating log file: {str(e)}"

    # The key for the text_area should be unique if multiple text_areas are used.
    # Using a class for styling instead of direct key for text_area style to avoid conflicts with main.py CSS
    st.markdown('<div class="custom-log-area">', unsafe_allow_html=True)
    st.text_area("", value=log_content, height=180, key="agent_log_area_content", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Auto-refresh the logs every second
    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = time.time()

    current_time = time.time()
    if current_time - st.session_state.last_refresh_time >= 1.0:
        st.session_state.last_refresh_time = current_time
        st.rerun()


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Log Viewer Component Demo")
    display_log_viewer()
