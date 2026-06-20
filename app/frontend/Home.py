import streamlit as st

st.set_page_config(
    page_title="Smart Queue Management System",
    page_icon="🎟",
    layout="wide"
)

st.title("🎟 Smart Queue Management System")

st.markdown("""
### Welcome to Smart Queue Management System

A real-time queue management platform for:

- 🏥 Hospitals
- 🏦 Banks
- 🎓 Colleges
- 🍽 Canteens

Manage customers, tokens, queues, analytics and reports from one dashboard.
""")

st.markdown("---")

st.subheader("🚀 Features")

col1, col2 = st.columns(2)

with col1:
    st.success("Dashboard Monitoring")
    st.success("Customer Entry")
    st.success("Token Management")
    st.success("Queue Management")

with col2:
    st.success("Analytics Dashboard")
    st.success("Reports & Export")
    st.success("Priority Handling")
    st.success("Estimated Wait Time")

st.markdown("---")

st.subheader("📊 System Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Queues", 5)

with col2:
    st.metric("Customers Today", 124)

with col3:
    st.metric("Average Wait Time", "12 min")

st.markdown("---")

st.info(
    """
    Use the sidebar to navigate between modules:
    
    🏠 Home
    
    📊 Dashboard
    
    📝 Customer Entry
    
    🎟 Token Management
    
    📈 Analytics
    
    🏢 Queue Management
    
    📑 Reports
    """
)

st.markdown("---")

st.success("System Status: Online ✅")