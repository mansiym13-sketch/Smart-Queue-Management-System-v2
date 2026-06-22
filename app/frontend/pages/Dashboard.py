import streamlit as st

from api import call_next_token, get_dashboard_stats, get_queues, get_tokens, get_users
from ui_helpers import build_token_dataframe, queue_label, queue_summary_dataframe, show_api_error


st.set_page_config(
    page_title="Smart Queue Dashboard",
    page_icon="random",
    layout="wide"
)

st.title("Smart Queue Management Dashboard")

stats = get_dashboard_stats()
queues = get_queues()
tokens = get_tokens()
users = get_users()

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", stats.get("total_users", 0) if isinstance(stats, dict) else 0)

with col2:
    st.metric("Active Queues", sum(1 for queue in queues if queue.get("status") == "ACTIVE"))

with col3:
    st.metric("Waiting Tokens", sum(1 for token in tokens if token.get("status") == "WAITING"))

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Completed Tokens", stats.get("completed_tokens", 0) if isinstance(stats, dict) else 0)

with col5:
    st.metric("Active Tokens", stats.get("active_tokens", 0) if isinstance(stats, dict) else 0)

with col6:
    st.metric("High Priority Waiting", sum(
        1
        for token in tokens
        if token.get("priority_level") == 3 and token.get("status") == "WAITING"
    ))

st.markdown("---")

st.subheader("Live Queue Monitor")

summary = queue_summary_dataframe(
    tokens,
    queues
)

if not summary.empty:
    st.dataframe(
        summary,
        use_container_width=True
    )

    st.bar_chart(
        summary.set_index("Queue")[["Waiting", "Called", "Serving"]]
    )
else:
    st.info("No queues or tokens available yet.")

st.markdown("---")

st.subheader("Token Preview")

token_df = build_token_dataframe(
    tokens[:10],
    queues,
    users
)

if not token_df.empty:
    st.dataframe(
        token_df,
        use_container_width=True
    )
else:
    st.info("No tokens generated yet.")

st.markdown("---")

st.subheader("Quick Action")

if queues:
    selected_queue = st.selectbox(
        "Queue",
        queues,
        format_func=queue_label
    )

    if st.button("Call Next Token", type="primary"):
        result = call_next_token(selected_queue["id"])

        if not show_api_error(st, result, "Unable to call next token"):
            st.success(f"Called token {result.get('token_number')}")
            st.rerun()
else:
    st.info("Create a queue before calling tokens.")

st.markdown("---")

if tokens:
    high_priority_waiting = sum(
        1
        for token in tokens
        if token.get("priority_level") == 3 and token.get("status") == "WAITING"
    )

    if high_priority_waiting:
        st.warning(f"{high_priority_waiting} high priority token(s) are waiting.")
    else:
        st.success("No high priority tokens are waiting.")
else:
    st.info("No token activity yet.")
