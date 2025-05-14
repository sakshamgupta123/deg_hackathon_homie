import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def generate_sample_data():
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    usage = np.random.normal(loc=30, scale=5, size=len(dates))
    cost = usage * 0.15  # Sample rate
    return pd.DataFrame({
        'Date': dates,
        'Usage (kWh)': usage,
        'Cost ($)': cost
    })


def usage_trends():
    st.subheader("Energy Usage Trends")
    df = generate_sample_data()

    fig = px.line(df, x='Date', y=['Usage (kWh)', 'Cost ($)'],
                  title='Energy Usage and Cost Over Time')
    st.plotly_chart(fig, use_container_width=True)


def cost_prediction():
    st.subheader("Cost Predictions")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Predicted Monthly Cost", "$145.30", delta="-$12.50")
        st.metric("Potential Savings", "$25.80", delta="15%")

    with col2:
        # Sample donut chart for cost breakdown
        fig = go.Figure(data=[go.Pie(
            labels=['Heating', 'Cooling', 'Lighting', 'Appliances'],
            values=[35, 25, 15, 25],
            hole=.3
        )])
        st.plotly_chart(fig, use_container_width=True)


def savings_opportunities():
    st.subheader("Savings Opportunities")
    opportunities = [
        {"title": "Switch to LED Lighting", "savings": "$15/month"},
        {"title": "Optimize AC Schedule", "savings": "$25/month"},
        {"title": "Smart Power Strip Usage", "savings": "$10/month"}
    ]

    for opp in opportunities:
        with st.expander(f"{opp['title']} - Save {opp['savings']}"):
            st.write("Implementation steps and details would go here.")


def cost_analysis_view():
    st.title("Energy Cost Dashboard")

    # Sample data for demonstration
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    usage = np.random.normal(loc=30, scale=5, size=len(dates))
    cost = usage * 0.15

    df = pd.DataFrame({
        'Date': dates,
        'Usage (kWh)': usage,
        'Cost ($)': cost
    })

    # Usage Trends
    st.header("Energy Usage Trends")
    fig = px.line(df, x='Date', y=['Usage (kWh)', 'Cost ($)'])
    st.plotly_chart(fig, use_container_width=True)

    # Cost Summary
    st.header("Cost Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Today's Usage", f"{usage[-1]:.1f} kWh",
                 delta=f"{usage[-1] - usage[-2]:.1f} kWh")
    with col2:
        st.metric("Today's Cost", f"${cost[-1]:.2f}",
                 delta=f"${cost[-1] - cost[-2]:.2f}")
    with col3:
        st.metric("Monthly Average", f"${cost.mean():.2f}",
                 delta=f"${cost.mean() - cost[:-30].mean():.2f}")

    # Savings Tips
    st.header("Savings Opportunities")
    with st.expander("View Tips"):
        st.write("""
        - 💡 Switch to LED bulbs to save up to 15% on lighting costs
        - 🌡️ Adjust thermostat by 1°C to save up to 10% on heating/cooling
        - ⏰ Use appliances during off-peak hours
        - 🔌 Unplug devices when not in use
        """)