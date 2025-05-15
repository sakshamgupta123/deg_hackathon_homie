import streamlit as st


def display_progress_stepper(current_step_index: int, steps: list):
    """
    Displays a 5-step progress bar.
    current_step_index: 0-indexed integer for the current active step.
    steps: A list of 5 strings representing the step names.
    """
    if not (0 <= current_step_index < len(steps)) and current_step_index != -1:
        st.error("Invalid current_step_index for progress stepper.")
        return

    st.markdown("""
    <style>
    .progress-stepper-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    .step-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex-grow: 1; /* Each step takes equal space */
        position: relative; /* For lines */
        margin: 0 10px; /* Add horizontal spacing between steps */
        padding: 10px 5px; /* Add padding around each step */
    }
    .step-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #4A4A4A; /* Dark grey for default */
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        margin-bottom: 15px; /* Increased space between circle and label */
        border: 2px solid #666;
        transition: background-color 0.3s, border-color 0.3s;
        font-size: 1.2rem; /* Increased font size for numbers */
    }
    .step-label {
        font-size: 1.1rem; /* Increased font size for labels */
        color: #D0D0D0; /* Light grey for labels */
        transition: color 0.3s;
        font-weight: normal;
        padding: 0 5px; /* Add padding around text */
        line-height: 1.4; /* Improve line spacing for readability */
    }
    .step-item.completed .step-circle, .step-item.active .step-circle {
        background-color: #e6683c; /* Theme color for active/completed */
        border-color: #f09433;
    }
    .step-item.completed .step-label {
        color: #FFFFFF; /* White for completed label */
        font-weight: bold;
    }
    .step-item.active .step-label {
        color: #FFFFFF; /* White for active label */
        font-weight: bold;
    }
    /* Line between steps */
    .step-item:not(:last-child)::after {
        content: '';
        position: absolute;
        top: 16px; /* Align with center of circle */
        left: 50%;
        width: calc(100% - 40px); /* Reduced width to account for spacing */
        height: 2px;
        background-color: #666; /* Line color */
        transform: translateX(20px); /* Adjusted to account for spacing */
        z-index: -1; /* Behind the circles */
    }
    .step-item.completed::after {
        background-color: #e6683c; /* Theme color for completed line */
    }

    /* Add pulsing animation for active step */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.5); }
        100% { transform: scale(1); }
    }

    .step-item.active .step-circle {
        animation: pulse 2s infinite ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add spacing before the stepper
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    cols = st.columns(len(steps))
    for i, step_name in enumerate(steps):
        with cols[i]:
            status_class = ""
            # Only apply active/completed classes if current_step_index is valid
            if current_step_index >= 0:
                if i < current_step_index:
                    status_class = "completed"
                elif i == current_step_index:
                    status_class = "active"

            # Using markdown to apply custom classes for styling individual parts
            st.markdown(f'''
            <div class="step-item {status_class}">
                <div class="step-circle">{i+1}</div>
                <div class="step-label">{step_name}</div>
            </div>
            ''', unsafe_allow_html=True)

    # Add spacing after the stepper
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Placeholder for completion animation - can be expanded
    if current_step_index == len(steps) - 1:  # If on the last step and it's considered active/done
        # This could be a state where the user just completed the last step.
        # A more complex animation might be triggered here if the last step is "Status" and it shows success.
        # For now, a simple message.
        if st.session_state.get("show_completion_animation", False):
            st.success(f"Process completed through all {len(steps)} steps!")
            st.session_state.show_completion_animation = False  # Reset after showing


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Progress Stepper Demo")

    defined_steps = ["Search", "Select", "Initialize", "Confirm Action", "Final Status"]

    if 'current_step_idx' not in st.session_state:
        st.session_state.current_step_idx = -1  # Initialize with -1 to show no active steps
    if 'show_completion_animation' not in st.session_state:
        st.session_state.show_completion_animation = False

    display_progress_stepper(st.session_state.current_step_idx, defined_steps)

    st.markdown("--- ")
    # Display current step information
    current_idx = st.session_state.current_step_idx
    if current_idx >= 0 and current_idx < len(defined_steps):
        current_step = defined_steps[current_idx]
        st.write(f"Current Step: {current_step} (Index: {current_idx})")
    else:
        st.write("No step currently active")