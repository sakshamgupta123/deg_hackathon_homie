import streamlit as st


def display_home_view():
    st.header("🏠 Welcome to Homie's Home!")
    st.markdown("""
    <style>
    .home-content {
        font-size: 1.2rem;
        line-height: 1.6;
    }
    .home-content ul {
        margin-left: 1.5rem;
    }
    </style>
    <div class="home-content">
    Hello, I am <strong>Homie</strong>, your intelligent home assistant, ready to illuminate your world!

    I can help you:
    *   Navigate your smart home setup.
    *   Understand and optimize your solar energy usage.
    *   Explore potential subsidies and services.

    Let's get started! Use the tabs above to explore different sections.
    </div>
    """, unsafe_allow_html=True)  # unsafe_allow_html just in case, though not strictly needed here


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Home View Demo")
    display_home_view()
