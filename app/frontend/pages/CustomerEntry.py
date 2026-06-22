import streamlit as st

from api import get_queues, get_tokens, get_users, join_queue_customer
from ui_helpers import build_token_dataframe, priority_value, queue_label, show_api_error


st.set_page_config(
    page_title="Customer Entry",
    page_icon="random",
    layout="wide"
)

st.title("Customer Entry")

queues = get_queues()
tokens = get_tokens()
users = get_users()


def suggest_priority(reason):
    reason_lower = reason.lower()

    if "emergency" in reason_lower or "senior" in reason_lower or "urgent" in reason_lower:
        return "High"

    if "consultation" in reason_lower or "opd" in reason_lower or "appointment" in reason_lower:
        return "Medium"

    return "Low"


st.markdown("---")

if not queues:
    st.warning("Create a queue before generating customer tokens.")
else:
    with st.form("customer_form"):
        st.subheader("Customer Details")

        customer_name = st.text_input(
            "Customer Name",
            placeholder="Enter customer name"
        )

        email = st.text_input(
            "Email",
            placeholder="customer@example.com"
        )

        selected_queue = st.selectbox(
            "Queue",
            queues,
            format_func=queue_label
        )

        reason = st.text_area(
            "Reason For Visit",
            placeholder="Example: Emergency, OPD consultation, enquiry"
        )

        suggested_priority = suggest_priority(reason) if reason else "Low"

        priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High"
            ],
            index=[
                "Low",
                "Medium",
                "High"
            ].index(suggested_priority)
        )

        submitted = st.form_submit_button(
            "Generate Token",
            type="primary"
        )

    if submitted:
        if not customer_name.strip() or not email.strip():
            st.error("Customer name and email are required")
        else:
            result = join_queue_customer(
                selected_queue["id"],
                customer_name.strip(),
                email.strip(),
                priority_value(priority)
            )

            if not show_api_error(st, result, "Token generation failed"):
                queue_tokens = [
                    token
                    for token in tokens
                    if token.get("queue_id") == selected_queue["id"]
                    and token.get("status") in ["WAITING", "CALLED", "SERVING"]
                ]

                estimated_wait = len(queue_tokens) * 5

                st.success("Token generated successfully")
                st.info(
                    f"Token {result.get('token_number')} for {customer_name.strip()} "
                    f"in {selected_queue.get('name')}. Estimated wait: {estimated_wait} minutes."
                )

st.markdown("---")

st.subheader("Recent Entries")

token_df = build_token_dataframe(
    tokens,
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
