import streamlit as st
import pandas as pd

def external_data_view():
    st.title("External Data Dashboard")

    # Weather Section
    st.header("Weather Information")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Temperature", "22°C", delta="1.5°C")
        st.metric("Humidity", "65%", delta="-5%")
    with col2:
        st.metric("Wind Speed", "12 km/h", delta="3 km/h")
        st.metric("Air Quality", "Good", delta="stable")

    # Energy Tariffs
    st.header("Current Energy Tariffs")
    tariff_data = {
        'Time Period': ['Peak', 'Off-Peak', 'Super Off-Peak'],
        'Hours': ['2PM - 8PM', '8AM - 2PM', '12AM - 8AM'],
        'Rate ($/kWh)': [0.25, 0.15, 0.10]
    }
    st.dataframe(pd.DataFrame(tariff_data), hide_index=True)

    # Grid Status
    st.header("Grid Status")
    col3, col4 = st.columns(2)

    with col3:
        st.metric("Grid Load", "75%", delta="-5%")
        st.metric("Renewable Mix", "35%", delta="10%")
    with col4:
        status = st.selectbox("Current Status",
                            ["Normal", "Peak Demand", "Low Demand"],
                            disabled=True)
        if status == "Normal":
            st.success("Grid operating normally")
        elif status == "Peak Demand":
            st.warning("High demand period")
        else:
            st.info("Low demand period")

    # Market Updates
    st.header("Energy Market Updates")
    with st.expander("Latest Updates"):
        st.write("""
        - Market prices showing stable trend
        - Renewable energy generation increasing
        - New energy policies announced for next quarter
        - Grid maintenance scheduled for next week
        """)