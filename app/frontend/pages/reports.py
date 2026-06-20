import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Reports",
    page_icon="📑",
    layout="wide"
)

st.title("📑 Reports & Export Center")

st.markdown("---")

# =========================
# FILTERS
# =========================

st.subheader("🔍 Report Filters")

col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input(
        "Start Date",
        date(2026, 1, 1)
    )

with col2:
    end_date = st.date_input(
        "End Date",
        date.today()
    )

with col3:
    queue_filter = st.selectbox(
        "Queue",
        [
            "All",
            "Hospital",
            "Bank",
            "Admissions"
        ]
    )

status_filter = st.selectbox(
    "Status",
    [
        "All",
        "Waiting",
        "Serving",
        "Completed"
    ]
)

st.markdown("---")

# =========================
# REPORT DATA
# =========================

report_df = pd.DataFrame({
    "Token": ["A001", "A002", "B001", "C001"],
    "Customer": ["Mansi", "Rahul", "Amit", "Sneha"],
    "Queue": ["Hospital", "Hospital", "Bank", "Admissions"],
    "Priority": ["High", "Medium", "Low", "Medium"],
    "Status": ["Completed", "Serving", "Waiting", "Completed"],
    "Wait Time (min)": [10, 15, 5, 8]
})

st.subheader("📋 Report Results")

st.dataframe(
    report_df,
    use_container_width=True
)

st.markdown("---")

# =========================
# SUMMARY CARDS
# =========================

st.subheader("📊 Report Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        len(report_df)
    )

with col2:
    st.metric(
        "Completed",
        2
    )

with col3:
    st.metric(
        "Waiting",
        1
    )

with col4:
    st.metric(
        "Avg Wait",
        "9 min"
    )

st.markdown("---")

# =========================
# EXPORT SECTION
# =========================

st.subheader("📥 Export Reports")

csv = report_df.to_csv(index=False)

st.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name="queue_report.csv",
    mime="text/csv"
)

st.info(
    "Excel and PDF export can be added later."
)

st.markdown("---")

# =========================
# SMART INSIGHTS
# =========================

st.subheader("🤖 Smart Report Insights")

st.success(
    "Overall average waiting time is under 10 minutes."
)

st.warning(
    "Hospital Queue contributes 60% of today's traffic."
)

st.info(
    "Admissions Queue has the highest completion rate."
)
