import streamlit as st

# Step names from the views
SOLAR_RETAIL_STEPS = [
    "Search Providers", "Select Plan", "Initialize Agreement",
    "Confirm Purchase", "Activation Status"
]
SOLAR_SERVICE_STEPS = [
    "Request Service", "Schedule Visit", "Technician Dispatch",
    "Confirm Service", "Service Status"
]
ONBOARDING_STEPS = [
    "Search Devices", "Select Network", "Initialize Connection",
    "Confirm Setup", "Status Check"
]
SUBSIDY_STEPS = [
    "Explore Subsidies", "Apply for Subsidy", "Application Status"
]

# Mapping between agent handlers and step indices
HANDLER_TO_STEP_MAPPING = {
    # Solar Retail Agent
    "solar_retail_search": 0,
    "solar_retail_select": 1,
    "solar_retail_init": 2,
    "solar_retail_confirm": 3,
    "solar_retail_status": 4,

    # Solar Service Agent
    "solar_service_search": 0,
    "solar_service_select": 1,
    "solar_service_init": 2,
    "solar_service_confirm": 3,
    "solar_service_status": 4,

    # Connection Agent (for user onboarding)
    "connection_search": 0,
    "connection_select": 1,
    "connection_init": 2,
    "connection_confirm": 3,
    "connection_status": 4,

    # Subsidy Agent
    "subsidy_search": 0,
    "subsidy_confirm": 1,
    "subsidy_status": 2
}

# Mapping agent types to corresponding tab names
AGENT_TO_TAB_MAPPING = {
    "solar_retail": "Solar Retail",
    "solar_service": "Solar Service",
    "connection": "User Onboarding",
    "subsidy": "Subsidy Subscription"
}

def update_progress_by_handler(agent_type: str, handler_name: str):
    """
    Update the progress stepper in the corresponding view based on the handler being called
    and switch to the appropriate tab.

    Args:
        agent_type: The type of agent ('solar_retail', 'solar_service', or 'connection')
        handler_name: The handler function name without the '_handle_' prefix
    """
    handler_key = f"{agent_type}_{handler_name}"
    step_index = HANDLER_TO_STEP_MAPPING.get(handler_key)

    if step_index is None:
        return  # Handler not mapped to any step

    # Switch to the appropriate tab based on agent type
    tab_name = AGENT_TO_TAB_MAPPING.get(agent_type)
    if tab_name and 'active_tab' in st.session_state:
        # Only trigger rerun if we're actually changing tabs
        tab_changed = st.session_state.active_tab != tab_name
        st.session_state.active_tab = tab_name

        # Store that we need to rerun after this handler completes
        if tab_changed:
            st.session_state.needs_rerun = True

    if agent_type == "solar_retail":
        if 'retail_current_step' in st.session_state:
            # Only advance one step at a time
            current_step = st.session_state.retail_current_step
            if current_step == -1 or current_step + 1 == step_index:
                st.session_state.retail_current_step = step_index
            elif current_step < step_index:
                # If trying to skip steps, just move one step forward
                st.session_state.retail_current_step = current_step + 1

            if step_index == 4:  # Last step
                st.session_state.retail_show_completion = True

    elif agent_type == "solar_service":
        if 'service_current_step' in st.session_state:
            # Only advance one step at a time
            current_step = st.session_state.service_current_step
            if current_step == -1 or current_step + 1 == step_index:
                st.session_state.service_current_step = step_index
            elif current_step < step_index:
                # If trying to skip steps, just move one step forward
                st.session_state.service_current_step = current_step + 1

            if step_index == 4:  # Last step
                st.session_state.service_show_completion = True

    elif agent_type == "connection":  # For user onboarding
        if 'onboarding_current_step' in st.session_state:
            # Only advance one step at a time
            current_step = st.session_state.onboarding_current_step
            if current_step == -1 or current_step + 1 == step_index:
                st.session_state.onboarding_current_step = step_index
            elif current_step < step_index:
                # If trying to skip steps, just move one step forward
                st.session_state.onboarding_current_step = current_step + 1

            if step_index == 4:  # Last step
                st.session_state.onboarding_show_completion = True

    elif agent_type == "subsidy":  # For subsidy subscription
        if 'subsidy_current_step' in st.session_state:
            # Only advance one step at a time
            current_step = st.session_state.subsidy_current_step
            if current_step == -1 or current_step + 1 == step_index:
                st.session_state.subsidy_current_step = step_index
            elif current_step < step_index:
                # If trying to skip steps, just move one step forward
                st.session_state.subsidy_current_step = current_step + 1

            if step_index == 2:  # Last step (subsidy has only 3 steps)
                st.session_state.subsidy_show_completion = True


def get_progress_step_name(agent_type: str, step_index: int) -> str:
    """
    Get the name of a specific step for an agent type.

    Args:
        agent_type: The type of agent ('solar_retail', 'solar_service', or 'connection')
        step_index: The 0-based index of the step

    Returns:
        The name of the step or an empty string if not found
    """
    steps = []

    if agent_type == "solar_retail":
        steps = SOLAR_RETAIL_STEPS
    elif agent_type == "solar_service":
        steps = SOLAR_SERVICE_STEPS
    elif agent_type == "connection":
        steps = ONBOARDING_STEPS
    elif agent_type == "subsidy":
        steps = SUBSIDY_STEPS

    if 0 <= step_index < len(steps):
        return steps[step_index]
    return ""