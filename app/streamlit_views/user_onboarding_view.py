import streamlit as st
from app.streamlit_components.progress_stepper import display_progress_stepper

# Define the steps for User Onboarding
ONBOARDING_STEPS = ["Search Devices", "Select Network", "Initialize Connection", "Confirm Setup", "Status Check"]


def display_user_onboarding_view():
    st.header("🚀 User Onboarding & Device Connection")

    # Manage current step in session state for this view
    if 'onboarding_current_step' not in st.session_state:
        st.session_state.onboarding_current_step = -1
    if 'onboarding_show_completion' not in st.session_state:
        st.session_state.onboarding_show_completion = False

    # Display the progress stepper
    display_progress_stepper(st.session_state.onboarding_current_step, ONBOARDING_STEPS)

    # Optional - add a small header with current step name for context
    valid_step = (0 <= st.session_state.onboarding_current_step < len(ONBOARDING_STEPS))
    if valid_step:
        current_step_name = ONBOARDING_STEPS[st.session_state.onboarding_current_step]
        st.markdown("--- ")
        st.subheader(f"Current Step: {current_step_name}")
    else:
        st.markdown("--- ")
        st.subheader(f"Current Step: Not Started")



if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("User Onboarding View Demo")
    display_user_onboarding_view()
