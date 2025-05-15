import streamlit as st
from app.streamlit_components.progress_stepper import display_progress_stepper


# Define the steps for Solar Retail
SOLAR_RETAIL_STEPS = ["Search Providers", "Select Plan", "Initialize Agreement",
                      "Confirm Purchase", "Activation Status"]


def display_solar_retail_view():
    st.header("☀️ Solar Retail Marketplace")

    if 'retail_current_step' not in st.session_state:
        st.session_state.retail_current_step = -1
    if 'retail_show_completion' not in st.session_state:
        st.session_state.retail_show_completion = False

    # Display only the progress stepper
    display_progress_stepper(st.session_state.retail_current_step, SOLAR_RETAIL_STEPS)

    # Optional - add a small header with current step name for context
    if st.session_state.retail_current_step >= 0 and st.session_state.retail_current_step < len(SOLAR_RETAIL_STEPS):
        current_step_name = SOLAR_RETAIL_STEPS[st.session_state.retail_current_step]
        st.markdown("--- ")
        st.subheader(f"Current Step: {current_step_name}")
    else:
        st.markdown("--- ")
        st.subheader(f"Current Step: Not Started")




if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Solar Retail View Demo")
    display_solar_retail_view()