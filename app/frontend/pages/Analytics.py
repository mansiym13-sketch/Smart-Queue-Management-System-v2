import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Queue Analytics Dashboard")

st.markdown("---")

# =========================
# KPI CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", 250)

with col2:
    st.metric("Completed", 180)

with col3:
    st.metric("Waiting", 45)

with col4:
    st.metric("Avg Wait Time", "12 min")

st.markdown("---")

# =========================
# QUEUE LOAD DISTRIBUTION
# =========================

st.subheader("📊 Queue Load Distribution")

queue_load = pd.DataFrame({
    "Queue": ["Hospital", "Bank", "Admissions"],
    "Customers": [25, 10, 8]
})

fig = px.bar(
    queue_load,
    x="Queue",
    y="Customers",
    title="Customers Waiting Per Queue"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# COMPLETION RATE
# =========================

st.subheader("✅ Completion Rate")

completion_data = pd.DataFrame({
    "Status": ["Completed", "Waiting", "Serving"],
    "Count": [180, 45, 25]
})

fig2 = px.pie(
    completion_data,
    values="Count",
    names="Status",
    title="Customer Status Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# QUEUE PERFORMANCE
# =========================

st.subheader("🏆 Queue Performance")

performance = pd.DataFrame({
    "Queue": ["Hospital", "Bank", "Admissions"],
    "Completed Customers": [120, 80, 50]
})

fig3 = px.bar(
    performance,
    x="Queue",
    y="Completed Customers",
    title="Queue-wise Completed Customers"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# PEAK HOURS
# =========================

st.subheader("⏰ Peak Hours")

hour_data = pd.DataFrame({
    "Hour": [
        "9 AM", "10 AM", "11 AM",
        "12 PM", "1 PM", "2 PM",
        "3 PM", "4 PM"
    ],
    "Visitors": [12, 18, 25, 30, 28, 22, 15, 10]
})

fig4 = px.line(
    hour_data,
    x="Hour",
    y="Visitors",
    markers=True,
    title="Customer Traffic Throughout The Day"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# HIGH PRIORITY ANALYSIS
# =========================

st.subheader("🔥 High Priority Customers")

priority_data = pd.DataFrame({
    "Priority": ["High", "Medium", "Low"],
    "Count": [20, 70, 160]
})

fig5 = px.pie(
    priority_data,
    values="Count",
    names="Priority",
    title="Priority Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# =========================
# TABLE
# =========================

st.subheader("📋 Queue Summary")

summary = pd.DataFrame({
    "Queue": ["Hospital", "Bank", "Admissions"],
    "Waiting": [25, 10, 8],
    "Serving": [3, 2, 1],
    "Completed": [120, 80, 50],
    "Average Wait": ["15 min", "8 min", "5 min"]
})

st.dataframe(summary, use_container_width=True)

# =========================
# SMART INSIGHTS
# =========================

st.subheader("🤖 Smart Insights")

st.warning(
    "Hospital Queue has the highest waiting count. Consider opening another counter."
)

st.info(
    "Admissions Queue has the lowest average waiting time."
)

st.success(
    "Overall completion rate is above 80%."
)