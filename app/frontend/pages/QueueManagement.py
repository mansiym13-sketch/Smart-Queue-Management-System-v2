import streamlit as st
import pandas as pd
from api import get_queues, create_queue

st.set_page_config(
    page_title="Queue Management",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Queue Management")

st.markdown("---")

# =========================
# CREATE QUEUE
# =========================

st.subheader("➕ Create New Queue")

with st.form("create_queue"):

    queue_name = st.text_input(
        "Queue Name",
        placeholder="Hospital Queue"
    )

    description = st.text_area(
        "Description",
        placeholder="OPD Consultation Queue"
    )

    max_capacity = st.number_input(
        "Maximum Capacity",
        min_value=1,
        value=50
    )

    status = st.selectbox(
        "Status",
        ["Active", "Inactive"]
    )

    create_btn = st.form_submit_button("Create Queue")

if create_btn:

    payload = {
        "name": queue_name,
        "description": description
    }

    result = create_queue(payload)

    st.success("Queue created successfully")
    st.write(result)

st.markdown("---")

# =========================
# EXISTING QUEUES
# =========================

queues = get_queues()

if queues:
    st.dataframe(
        pd.DataFrame(queues),
        use_container_width=True
    )
else:
    st.info("No queues found")

st.markdown("---")

# =========================
# UPDATE QUEUE
# =========================

st.subheader("✏ Update Queue")

selected_queue = st.selectbox(
    "Select Queue",
    [
        "Hospital Queue",
        "Bank Queue",
        "Admissions Queue"
    ]
)

new_status = st.selectbox(
    "Update Status",
    [
        "Active",
        "Inactive"
    ]
)

if st.button("Update Queue"):
    st.success(
        f"{selected_queue} updated successfully"
    )

st.markdown("---")

# =========================
# DELETE QUEUE
# =========================

st.subheader("🗑 Delete Queue")

delete_queue = st.selectbox(
    "Select Queue To Delete",
    [
        "Hospital Queue",
        "Bank Queue",
        "Admissions Queue"
    ]
)

if st.button("Delete Queue"):
    st.error(
        f"{delete_queue} deleted successfully"
    )

st.markdown("---")

# =========================
# QUEUE LOAD MONITORING
# =========================

st.subheader("📊 Queue Load Monitoring")

load_data = pd.DataFrame({
    "Queue": [
        "Hospital",
        "Bank",
        "Admissions"
    ],
    "Customers": [
        20,
        8,
        5
    ]
})

st.bar_chart(
    load_data.set_index("Queue")
)

st.markdown("---")

# =========================
# SMART ALERTS
# =========================

st.subheader("🚨 Queue Alerts")

st.warning(
    "Hospital Queue is at 80% capacity."
)

st.info(
    "Bank Queue operating normally."
)

st.success(
    "Admissions Queue has available capacity."
)

st.markdown("---")

# =========================
# QUICK STATS
# =========================

st.subheader("📈 Queue Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Queues",
        3
    )

with col2:
    st.metric(
        "Active Queues",
        3
    )

with col3:
    st.metric(
        "Total Waiting",
        27
    )