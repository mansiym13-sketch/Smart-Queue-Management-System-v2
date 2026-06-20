import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Smart Queue Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Smart Queue Management Dashboard")
st.markdown("---")

# =========================
# KPI CARDS
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Customers Today", 124)

with col2:
    st.metric("🏢 Active Queues", 5)

with col3:
    st.metric("⏳ Waiting Customers", 18)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("✅ Completed Customers", 96)

with col5:
    st.metric("🕒 Average Wait Time", "12 min")

with col6:
    st.metric("🔥 High Priority Customers", 4)

st.markdown("---")

# =========================
# LIVE QUEUE MONITOR
# =========================

st.subheader("📡 Live Queue Monitor")

queue_data = pd.DataFrame({
    "Queue": ["Hospital", "Bank", "Admissions"],
    "Now Serving": ["A012", "B005", "C003"],
    "Waiting Customers": [15, 8, 4]
})

st.dataframe(queue_data, use_container_width=True)

st.markdown("---")

# =========================
# QUEUE LOAD MONITORING
# =========================

st.subheader("📈 Queue Load Distribution")

chart_data = pd.DataFrame({
    "Queue": ["Hospital", "Bank", "Admissions"],
    "Customers": [20, 8, 5]
})

st.bar_chart(
    chart_data.set_index("Queue")
)

st.markdown("---")

# =========================
# TOKEN MANAGEMENT PREVIEW
# =========================

st.subheader("🎟 Token Management")

token_data = pd.DataFrame({
    "Token": ["A001", "A002", "B001", "C001"],
    "Customer": ["Mansi", "Rahul", "Amit", "Sneha"],
    "Queue": ["Hospital", "Hospital", "Bank", "Admissions"],
    "Priority": ["High", "Medium", "Low", "Medium"],
    "Status": ["Waiting", "Called", "Waiting", "Serving"]
})

st.dataframe(token_data, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.button("📢 Call Next")

with col2:
    st.button("🩺 Mark Serving")

with col3:
    st.button("✅ Mark Completed")

st.markdown("---")

# =========================
# SMART ALERTS
# =========================

st.subheader("🚨 Smart Alerts")

st.warning(
    "⚠ Hospital Queue overloaded. Current waiting count: 25"
)

st.error(
    "⚠ High Priority Customer waiting for more than 20 minutes"
)

st.info(
    "ℹ Admissions Queue performing normally"
)

st.markdown("---")

# =========================
# PERFORMANCE ANALYTICS
# =========================

st.subheader("📋 Queue Performance")

performance_data = pd.DataFrame({
    "Queue": ["Hospital", "Bank", "Admissions"],
    "Completed Customers": [120, 80, 40]
})

st.dataframe(performance_data, use_container_width=True)

st.markdown("---")

# =========================
# FOOTER
# =========================

st.success("✅ Smart Queue Management System Running Successfully")