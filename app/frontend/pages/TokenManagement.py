import streamlit as st

from api import call_next_token, get_queues, get_tokens, get_users, update_token_status
from ui_helpers import (
    STATUS_OPTIONS,
    build_token_dataframe,
    queue_label,
    queue_summary_dataframe,
    show_api_error,
    token_label,
)


st.set_page_config(
    page_title="Token Management",
    page_icon="random",
    layout="wide"
)

st.title("Token Management")

queues = get_queues()
tokens = get_tokens()
users = get_users()

queue_options = [
    {
        "id": None,
        "name": "All Queues"
    }
] + queues

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    queue_filter = st.selectbox(
        "Queue",
        queue_options,
        format_func=queue_label
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        ["ALL"] + STATUS_OPTIONS
    )

with col3:
    search = st.text_input("Search Customer")

filtered_tokens = tokens

if queue_filter.get("id") is not None:
    filtered_tokens = [
        token
        for token in filtered_tokens
        if token.get("queue_id") == queue_filter.get("id")
    ]

if status_filter != "ALL":
    filtered_tokens = [
        token
        for token in filtered_tokens
        if token.get("status") == status_filter
    ]

token_df = build_token_dataframe(
    filtered_tokens,
    queues,
    users
)

if search.strip() and not token_df.empty:
    token_df = token_df[
        token_df["Customer"].astype(str).str.contains(
            search.strip(),
            case=False,
            na=False
        )
    ]

st.markdown("---")

st.subheader("Active Tokens")

if not token_df.empty:
    st.dataframe(
        token_df,
        use_container_width=True
    )
else:
    st.info("No tokens match the current filters.")

st.markdown("---")

st.subheader("Queue Actions")

action_col1, action_col2 = st.columns(2)

with action_col1:
    if queues:
        action_queue = st.selectbox(
            "Queue For Call Next",
            queues,
            format_func=queue_label
        )

        if st.button("Call Next Token", type="primary"):
            result = call_next_token(action_queue["id"])

            if not show_api_error(st, result, "Unable to call next token"):
                st.success(f"Called token {result.get('token_number')}")
                st.rerun()
    else:
        st.info("Create a queue before calling tokens.")

with action_col2:
    if tokens:
        selected_token = st.selectbox(
            "Token To Update",
            tokens,
            format_func=token_label
        )

        new_status = st.selectbox(
            "New Status",
            STATUS_OPTIONS,
            index=STATUS_OPTIONS.index(selected_token.get("status"))
            if selected_token.get("status") in STATUS_OPTIONS
            else 0
        )

        if st.button("Update Token Status"):
            result = update_token_status(
                selected_token["id"],
                new_status
            )

            if not show_api_error(st, result, "Unable to update token"):
                st.success("Token status updated")
                st.rerun()
    else:
        st.info("No tokens are available to update.")

st.markdown("---")

st.subheader("Queue Summary")

summary = queue_summary_dataframe(
    tokens,
    queues
)

if not summary.empty:
    st.dataframe(
        summary,
        use_container_width=True
    )
else:
    st.info("No queue summary available yet.")

high_priority_waiting = [
    token
    for token in tokens
    if token.get("priority_level") == 3 and token.get("status") == "WAITING"
]

if high_priority_waiting:
    st.warning(f"{len(high_priority_waiting)} high priority token(s) are waiting.")
