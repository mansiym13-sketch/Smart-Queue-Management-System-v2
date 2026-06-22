import streamlit as st

from api import get_queues, get_tokens, get_users
from ui_helpers import STATUS_OPTIONS, build_token_dataframe


st.set_page_config(
    page_title="Reports",
    page_icon="random",
    layout="wide"
)

st.title("Reports & Export")

queues = get_queues()
tokens = get_tokens()
users = get_users()

token_df = build_token_dataframe(
    tokens,
    queues,
    users
)

st.markdown("---")

st.subheader("Report Filters")

col1, col2 = st.columns(2)

queue_names = ["All"] + [
    queue.get("name")
    for queue in queues
]

with col1:
    queue_filter = st.selectbox(
        "Queue",
        queue_names
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        ["All"] + STATUS_OPTIONS
    )

report_df = token_df.copy()

if not report_df.empty and queue_filter != "All":
    report_df = report_df[
        report_df["Queue"] == queue_filter
    ]

if not report_df.empty and status_filter != "All":
    report_df = report_df[
        report_df["Status"] == status_filter
    ]

st.markdown("---")

st.subheader("Report Results")

if not report_df.empty:
    st.dataframe(
        report_df,
        use_container_width=True
    )
else:
    st.info("No records match the selected filters.")

st.markdown("---")

st.subheader("Report Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(report_df))

with col2:
    st.metric("Completed", len(report_df[report_df["Status"] == "COMPLETED"]) if not report_df.empty else 0)

with col3:
    st.metric("Waiting", len(report_df[report_df["Status"] == "WAITING"]) if not report_df.empty else 0)

with col4:
    st.metric("High Priority", len(report_df[report_df["Priority"] == "High"]) if not report_df.empty else 0)

st.markdown("---")

st.subheader("Export")

csv = report_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="queue_report.csv",
    mime="text/csv",
    disabled=report_df.empty
)
