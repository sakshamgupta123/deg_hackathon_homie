import streamlit as st
from app.streamlit_components.progress_stepper import display_progress_stepper


# Define the steps for Subsidy Subscription
SUBSIDY_STEPS = ["Explore Subsidies", "Apply for Subsidy", "Application Status"]


def display_subsidy_subscription_view():
    st.header("📜 Subsidy & Grant Applications")

    if 'subsidy_current_step' not in st.session_state:
        st.session_state.subsidy_current_step = -1
    if 'subsidy_show_completion' not in st.session_state:
        st.session_state.subsidy_show_completion = False

    # Display only the progress stepper
    display_progress_stepper(st.session_state.subsidy_current_step, SUBSIDY_STEPS)

    # Optional - add a small header with current step name for context
    valid_step = (0 <= st.session_state.subsidy_current_step < len(SUBSIDY_STEPS))
    if valid_step:
        current_step_name = SUBSIDY_STEPS[st.session_state.subsidy_current_step]
        st.markdown("--- ")
        st.subheader(f"Current Step: {current_step_name}")
    else:
        st.markdown("--- ")
        st.subheader("Current Step: Not Started")


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Subsidy Subscription View Demo")
    display_subsidy_subscription_view()