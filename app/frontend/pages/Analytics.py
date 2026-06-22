import pandas as pd
import plotly.express as px
import streamlit as st

from api import get_dashboard_stats, get_queues, get_tokens
from ui_helpers import priority_label, queue_summary_dataframe


st.set_page_config(
    page_title="Analytics",
    page_icon="random",
    layout="wide"
)

st.title("Queue Analytics")

stats = get_dashboard_stats()
queues = get_queues()
tokens = get_tokens()

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tokens", stats.get("total_tokens", len(tokens)) if isinstance(stats, dict) else len(tokens))

with col2:
    st.metric("Completed", stats.get("completed_tokens", 0) if isinstance(stats, dict) else 0)

with col3:
    st.metric("Waiting", sum(1 for token in tokens if token.get("status") == "WAITING"))

with col4:
    st.metric("Queues", stats.get("total_queues", len(queues)) if isinstance(stats, dict) else len(queues))

st.markdown("---")

summary = queue_summary_dataframe(
    tokens,
    queues
)

if not summary.empty:
    st.subheader("Queue Load Distribution")

    fig = px.bar(
        summary,
        x="Queue",
        y=["Waiting", "Called", "Serving", "Completed"],
        title="Token Status By Queue",
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
else:
    st.info("No queue data available yet.")

status_counts = pd.DataFrame(
    [
        {
            "Status": status,
            "Count": sum(1 for token in tokens if token.get("status") == status)
        }
        for status in ["WAITING", "CALLED", "SERVING", "COMPLETED"]
    ]
)

if status_counts["Count"].sum() > 0:
    st.subheader("Status Distribution")

    fig2 = px.pie(
        status_counts,
        values="Count",
        names="Status",
        title="Token Status Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

priority_counts = pd.DataFrame(
    [
        {
            "Priority": label,
            "Count": sum(
                1
                for token in tokens
                if priority_label(token.get("priority_level")) == label
            )
        }
        for label in ["High", "Medium", "Low"]
    ]
)

if priority_counts["Count"].sum() > 0:
    st.subheader("Priority Distribution")

    fig3 = px.bar(
        priority_counts,
        x="Priority",
        y="Count",
        title="Tokens By Priority"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

st.markdown("---")

st.subheader("Queue Summary")

if not summary.empty:
    st.dataframe(
        summary,
        use_container_width=True
    )

    busiest = summary.sort_values(
        "Total",
        ascending=False
    ).iloc[0]

    st.info(f"{busiest['Queue']} currently has the highest token volume.")
else:
    st.info("Create queues and tokens to see insights.")
