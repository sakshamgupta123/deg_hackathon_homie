import streamlit as st
# from streamlit_views.control_panel import setup_view # Will be replaced by new views
# from streamlit_views.cost_dashboard import cost_analysis_view # Will be replaced by new views
# from streamlit_views.external_data_dashboard import external_data_view # Will be replaced by new views
from app.streamlit_components.chat_window import chat_window
from app.streamlit_components.log_viewer import display_log_viewer
from app.streamlit_views.home_view import display_home_view
from app.streamlit_views.user_onboarding_view import display_user_onboarding_view
from app.streamlit_views.solar_retail_view import display_solar_retail_view
from app.streamlit_views.solar_service_view import display_solar_service_view
from app.streamlit_views.subsidy_subscription_view import display_subsidy_subscription_view


# Placeholder functions (to be removed)
# def home_view(): ...
# def user_onboarding_view(): ...
# def solar_retail_view(): ...
# def solar_service_view(): ...
# def subsidy_subscription_view(): ...
# def log_viewer(): ...

st.set_page_config(
    page_title="Homie - Smart Home AI",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS for background, chat area wrapper, and to remove top padding
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    }
    .block-container, .main { padding-top: 0 !important; }
    .stMarkdown, .stAlert, p, h1, h2, h3 {
        color: white !important;
    }
    /* Invisible wrapper for chat area: only height and overflow control */
    .chat-area-wrapper {
        height: 50vh !important; /* Reduced from 65vh */
        max-height: 50vh !important; /* Reduced from 65vh */
        overflow-y: hidden !important;
        margin-top: -40vh !important; /* Adjusted to match new height */
        margin-bottom: 0;
        display: flex;
        flex-direction: column;
    }
    /* Shift main content headings down by 10% */
    .main-content-shift {
        margin-top: 10vh !important;
        padding-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for active tab
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Home'

# Initialize needs_rerun flag if not present
if 'needs_rerun' not in st.session_state:
    st.session_state.needs_rerun = False

# Define tabs and their content mapping
tabs = {
    'Home': {'icon': '🏠', 'view': display_home_view},
    'User Onboarding': {'icon': '🚀', 'view': display_user_onboarding_view},
    'Solar Retail': {'icon': '☀️', 'view': display_solar_retail_view},
    'Solar Service': {'icon': '🔧', 'view': display_solar_service_view},
    'Subsidy Subscription': {'icon': '📜', 'view': display_subsidy_subscription_view}
}

# Sidebar navigation
with st.sidebar:
    st.title("💡 Homie")
    st.markdown("---")
    for tab_name, tab_info in tabs.items():
        if st.button(
            f"{tab_info['icon']} {tab_name}",
            use_container_width=True,
            type="primary" if st.session_state.active_tab == tab_name else "secondary"
        ):
            st.session_state.active_tab = tab_name
            st.rerun()

# Main content and chat (side by side, chat fixed height and scrollable internally)
main_col, chat_col = st.columns([7, 3], gap="large")
with main_col:
    st.markdown('<div class="main-content-shift">', unsafe_allow_html=True)
    tabs[st.session_state.active_tab]['view']()
    st.markdown('</div>', unsafe_allow_html=True)
with chat_col:
    st.markdown('<div class="chat-area-wrapper">', unsafe_allow_html=True)
    chat_window()
    st.markdown('</div>', unsafe_allow_html=True)

# Logs at the bottom (integrated, no overlays)
with st.container():
    display_log_viewer()

# Check if we need to rerun the app (e.g., after an agent handler has switched tabs)
if st.session_state.needs_rerun:
    st.session_state.needs_rerun = False
    st.rerun()

# Removed old sidebar content:
# # Sidebar header
# st.sidebar.title("Smart Home Assistant")  # Can be repurposed if sidebar is used for status
# st.sidebar.markdown("---")

# # Navigation with custom styling (REMOVED)
# # tab_selected = st.sidebar.radio(...)

# # System status section (Can be kept or moved if sidebar is used)
# st.sidebar.markdown("---")
# st.sidebar.markdown("### System Status")
# col1, col2 = st.sidebar.columns(2)
# with col1:
#     st.success("🟢 System Online")
#     st.info("📡 Network Active")
# with col2:
#     st.success("✅ Devices Connected")
#     st.info("🔄 Last Update: Now")

# # Create two columns for main content and chat (REPLACED with new layout)
# # main_content, chat_section = st.columns([0.7, 0.3])
# # ... old content loading logic ...
