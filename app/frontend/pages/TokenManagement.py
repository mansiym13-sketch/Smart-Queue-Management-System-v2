import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Token Management",
    page_icon="🎟",
    layout="wide"
)

st.title("🎟 Token Management")
st.markdown("---")

# =========================
# FILTERS
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    queue_filter = st.selectbox(
        "Queue",
        ["All", "Hospital", "Bank", "Admissions"]
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        ["All", "Waiting", "Serving", "Completed"]
    )

with col3:
    search = st.text_input(
        "Search Customer"
    )

st.markdown("---")

# =========================
# TOKEN TABLE
# =========================

token_data = pd.DataFrame({
    "Token": ["A001", "A002", "A003", "B001", "C001"],
    "Customer": ["Mansi", "Rahul", "Sneha", "Amit", "Priya"],
    "Queue": ["Hospital", "Hospital", "Hospital", "Bank", "Admissions"],
    "Priority": ["High", "Medium", "Low", "Medium", "High"],
    "Status": ["Waiting", "Serving", "Completed", "Waiting", "Waiting"]
})

st.subheader("📋 Active Tokens")

st.dataframe(
    token_data,
    use_container_width=True
)

st.markdown("---")

# =========================
# TOKEN ACTIONS
# =========================

st.subheader("⚙ Queue Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📢 Call Next"):
        st.success("Next customer called successfully")

with col2:
    if st.button("🩺 Mark Serving"):
        st.info("Customer status changed to Serving")

with col3:
    if st.button("✅ Mark Completed"):
        st.success("Customer marked as Completed")

st.markdown("---")

# =========================
# CURRENT SERVING
# =========================

st.subheader("🔔 Currently Serving")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Hospital",
        "A002"
    )

with col2:
    st.metric(
        "Bank",
        "B001"
    )

with col3:
    st.metric(
        "Admissions",
        "C001"
    )

st.markdown("---")

# =========================
# QUEUE SUMMARY
# =========================

st.subheader("📊 Queue Summary")

summary = pd.DataFrame({
    "Queue": ["Hospital", "Bank", "Admissions"],
    "Waiting": [12, 5, 3],
    "Serving": [1, 1, 1],
    "Completed": [45, 20, 15]
})

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

# =========================
# HIGH PRIORITY ALERTS
# =========================

st.subheader("🚨 Priority Alerts")

st.error(
    "High Priority Customer A001 waiting for 18 minutes"
)

st.warning(
    "Hospital Queue nearing overload capacity"
)

st.success(
    "Bank Queue operating normally"
)