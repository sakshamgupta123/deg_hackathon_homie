import streamlit as st
from streamlit_views.control_panel import setup_view
from streamlit_views.cost_dashboard import cost_analysis_view
from streamlit_views.external_data_dashboard import external_data_view
from streamlit_components.chat_window import chat_window

st.set_page_config(
    page_title="Smart Home LLM Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Layout styling
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a;
        min-width: 300px;
        max-width: 300px;
    }
    section[data-testid="stSidebar"] .sidebar-content {
        padding: 1rem;
    }
    section[data-testid="stSidebar"] hr {
        margin: 20px 0;
        border-color: #333;
    }
    section[data-testid="stSidebar"] .stRadio > label {
        background: #2d2d2d;
        padding: 15px;
        border-radius: 5px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.2s;
    }
    section[data-testid="stSidebar"] .stRadio > label:hover {
        background: #3d3d3d;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] > h1 {
        padding: 0;
        margin-bottom: 1rem;
    }
    /* Main content layout */
    .main-content {
        width: 70%;
        float: left;
        padding-right: 20px;
    }
    .chat-content {
        width: 30%;
        float: right;
        position: fixed;
        right: 0;
        top: 0;
        height: 100vh;
        padding: 20px;
        background-color: #0e1117;
        border-left: 1px solid #333;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar header
st.sidebar.title("Smart Home Assistant")
st.sidebar.markdown("---")

# Navigation with custom styling
tab_selected = st.sidebar.radio(
    "Navigation",
    ["🎛️ Control Panel", "💰 Cost Dashboard", "🌍 External Data"],
    format_func=lambda x: x.split(" ", 1)[1],
    key="nav"
)

# System status section
st.sidebar.markdown("---")
st.sidebar.markdown("### System Status")

# Status indicators with custom styling
col1, col2 = st.sidebar.columns(2)
with col1:
    st.success("🟢 System Online")
    st.info("📡 Network Active")
with col2:
    st.success("✅ Devices Connected")
    st.info("🔄 Last Update: Now")

# Create two columns for main content and chat
main_content, chat_section = st.columns([0.7, 0.3])

# Main content
with main_content:
    if "Control Panel" in tab_selected:
        setup_view()
    elif "Cost Dashboard" in tab_selected:
        cost_analysis_view()
    else:
        external_data_view()

# Chat window
with chat_section:
    chat_window()
