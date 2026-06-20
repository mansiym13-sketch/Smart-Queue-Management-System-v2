import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer Entry",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Smart Customer Entry")
st.markdown("---")

# =========================
# CUSTOMER FORM
# =========================

with st.form("customer_form"):

    st.subheader("Customer Details")

    customer_name = st.text_input(
        "Customer Name",
        placeholder="Enter customer name"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter email"
    )

    queue_name = st.selectbox(
        "Queue Name",
        [
            "Hospital Queue",
            "Bank Queue",
            "Admissions Queue"
        ]
    )

    reason = st.text_area(
        "Reason For Visit",
        placeholder="Example: Emergency, OPD Consultation, Enquiry..."
    )

    submitted = st.form_submit_button("Generate Token")

# =========================
# SMART PRIORITY LOGIC
# =========================

priority = "Low"

if reason:

    reason_lower = reason.lower()

    if "emergency" in reason_lower:
        priority = "High"

    elif "senior" in reason_lower:
        priority = "High"

    elif "consultation" in reason_lower:
        priority = "Medium"

    elif "opd" in reason_lower:
        priority = "Medium"

    else:
        priority = "Low"

# =========================
# DISPLAY SMART RESULTS
# =========================

if reason:

    st.markdown("---")

    st.subheader("🤖 Smart Recommendation")

    if priority == "High":
        st.error(f"Suggested Priority: {priority}")

    elif priority == "Medium":
        st.warning(f"Suggested Priority: {priority}")

    else:
        st.success(f"Suggested Priority: {priority}")

# =========================
# ESTIMATED WAIT TIME
# =========================

waiting_people = 5
estimated_wait = waiting_people * 5

if reason:

    st.subheader("⏳ Estimated Wait Time")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Queue Position",
            waiting_people
        )

    with col2:
        st.metric(
            "Estimated Wait Time",
            f"{estimated_wait} min"
        )

# =========================
# TOKEN GENERATION
# =========================

if submitted:

    token_number = "A00" + str(waiting_people + 1)

    st.success("Token Generated Successfully!")

    st.subheader("🎟 Generated Token")

    st.info(
        f"""
        Token Number: {token_number}

        Customer: {customer_name}

        Queue: {queue_name}

        Priority: {priority}

        Estimated Wait Time: {estimated_wait} Minutes
        """
    )

# =========================
# TODAY'S ENTRIES
# =========================

st.markdown("---")

st.subheader("📋 Recent Entries")

sample_data = pd.DataFrame(
    {
        "Token": ["A001", "A002", "A003"],
        "Customer": ["Mansi", "Rahul", "Sneha"],
        "Queue": ["Hospital", "Hospital", "Bank"],
        "Priority": ["High", "Medium", "Low"],
        "Status": ["Waiting", "Called", "Serving"]
    }
)

st.dataframe(sample_data, use_container_width=True)