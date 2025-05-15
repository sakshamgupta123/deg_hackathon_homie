import streamlit as st
from app.streamlit_components.progress_stepper import display_progress_stepper


# Define the steps for Solar Service
SOLAR_SERVICE_STEPS = ["Request Service", "Schedule Visit", "Technician Dispatch",
                       "Confirm Service", "Service Status"]


def display_solar_service_view():
    st.header("🔧 Solar Panel Servicing")

    if 'service_current_step' not in st.session_state:
        st.session_state.service_current_step = -1
    if 'service_show_completion' not in st.session_state:
        st.session_state.service_show_completion = False

    # Display only the progress stepper
    display_progress_stepper(st.session_state.service_current_step, SOLAR_SERVICE_STEPS)

    # Optional - add a small header with current step name for context
    if st.session_state.service_current_step >= 0 and st.session_state.service_current_step < len(SOLAR_SERVICE_STEPS):
        current_step_name = SOLAR_SERVICE_STEPS[st.session_state.service_current_step]
        st.markdown("--- ")
        st.subheader(f"Current Step: {current_step_name}")
    else:
        st.markdown("--- ")
        st.subheader(f"Current Step: Not Started")


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Solar Service View Demo")
    display_solar_service_view()