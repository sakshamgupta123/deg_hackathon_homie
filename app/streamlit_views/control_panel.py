import streamlit as st
from typing import Dict

def device_control_section():
    st.subheader("Device Control")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.toggle("Living Room Lights", key="lr_lights")
        st.toggle("Kitchen Lights", key="k_lights")
    with col2:
        st.toggle("AC", key="ac")
        st.toggle("Heater", key="heater")
    with col3:
        st.toggle("Security System", key="security")
        st.toggle("Smart Irrigation", key="irrigation")

def monitoring_section():
    st.subheader("Real-time Monitoring")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Temperature", value="22°C", delta="1.2°C")
        st.metric(label="Humidity", value="45%", delta="-5%")
    with col2:
        st.metric(label="Energy Usage", value="3.2 kW", delta="-0.5 kW")
        st.metric(label="Water Usage", value="120L", delta="10L")

def automation_section():
    st.subheader("Automation Setup")
    with st.expander("Create New Automation"):
        st.selectbox("Trigger Device", ["Living Room Lights", "AC", "Heater"])
        st.selectbox("Condition", ["Time", "Temperature", "Motion", "Light Level"])
        st.time_input("Time")
        st.button("Save Automation")

def setup_view():
    st.title("Smart Home Control Panel")

    # Device Control Section
    st.header("Device Control")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Living Room")
        st.toggle("Main Light", value=False, key="lr_main_light")
        st.slider("Brightness", 0, 100, 50, key="lr_brightness")

        st.subheader("Temperature")
        st.number_input("Set Temperature (°C)", 16, 30, 22, key="temperature")

    with col2:
        st.subheader("Kitchen")
        st.toggle("Kitchen Light", value=False, key="kitchen_light")
        st.toggle("Smart Plug", value=False, key="kitchen_plug")

        st.subheader("Security")
        st.toggle("Main Door Lock", value=True, key="main_door")

    # Quick Actions
    st.header("Quick Actions")
    col3, col4, col5 = st.columns(3)

    with col3:
        if st.button("All Lights Off"):
            st.toast("Turning off all lights...")
    with col4:
        if st.button("Night Mode"):
            st.toast("Activating night mode...")
    with col5:
        if st.button("Away Mode"):
            st.toast("Setting up away mode...")