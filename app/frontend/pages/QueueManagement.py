import pandas as pd
import streamlit as st

from api import create_queue, delete_queue, get_queues, get_tokens, update_queue
from ui_helpers import QUEUE_STATUS_OPTIONS, queue_label, queue_summary_dataframe, show_api_error


st.set_page_config(
    page_title="Queue Management",
    page_icon="random",
    layout="wide"
)

st.title("Queue Management")

queues = get_queues()
tokens = get_tokens()

st.markdown("---")

st.subheader("Create New Queue")

with st.form("create_queue"):
    queue_name = st.text_input(
        "Queue Name",
        placeholder="Hospital Queue"
    )

    description = st.text_area(
        "Description",
        placeholder="OPD Consultation Queue"
    )

    status = st.selectbox(
        "Status",
        QUEUE_STATUS_OPTIONS
    )

    create_btn = st.form_submit_button(
        "Create Queue",
        type="primary"
    )

if create_btn:
    if not queue_name.strip() or not description.strip():
        st.error("Queue name and description are required")
    else:
        result = create_queue(
            queue_name.strip(),
            description.strip(),
            status
        )

        if not show_api_error(st, result, "Queue creation failed"):
            st.success("Queue created successfully")
            st.rerun()

st.markdown("---")

st.subheader("Existing Queues")

if queues:
    st.dataframe(
        pd.DataFrame(queues),
        use_container_width=True
    )
else:
    st.info("No queues found")

st.markdown("---")

st.subheader("Update Queue")

if queues:
    selected_update_queue = st.selectbox(
        "Select Queue To Update",
        queues,
        format_func=queue_label
    )

    with st.form("update_queue"):
        updated_name = st.text_input(
            "Queue Name",
            value=selected_update_queue.get("name", "")
        )

        updated_description = st.text_area(
            "Description",
            value=selected_update_queue.get("description", "")
        )

        current_status = selected_update_queue.get("status", "ACTIVE")
        status_index = QUEUE_STATUS_OPTIONS.index(current_status) if current_status in QUEUE_STATUS_OPTIONS else 0

        updated_status = st.selectbox(
            "Status",
            QUEUE_STATUS_OPTIONS,
            index=status_index
        )

        update_btn = st.form_submit_button("Update Queue")

    if update_btn:
        result = update_queue(
            selected_update_queue["id"],
            name=updated_name.strip(),
            description=updated_description.strip(),
            status=updated_status
        )

        if not show_api_error(st, result, "Queue update failed"):
            st.success("Queue updated successfully")
            st.rerun()
else:
    st.info("Create a queue before updating.")

st.markdown("---")

st.subheader("Delete Queue")

if queues:
    selected_delete_queue = st.selectbox(
        "Select Queue To Delete",
        queues,
        format_func=queue_label
    )

    confirm_delete = st.checkbox(
        f"Confirm delete {selected_delete_queue.get('name')}"
    )

    if st.button("Delete Queue", disabled=not confirm_delete):
        result = delete_queue(selected_delete_queue["id"])

        if not show_api_error(st, result, "Queue delete failed"):
            st.success("Queue deleted successfully")
            st.rerun()
else:
    st.info("No queues are available to delete.")

st.markdown("---")

st.subheader("Queue Load Monitoring")

summary = queue_summary_dataframe(tokens, queues)

if not summary.empty:
    st.bar_chart(
        summary.set_index("Queue")[["Waiting", "Called", "Serving", "Completed"]]
    )

    st.dataframe(
        summary,
        use_container_width=True
    )
else:
    st.info("No queue activity yet.")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Queues", len(queues))

with col2:
    st.metric("Active Queues", sum(1 for queue in queues if queue.get("status") == "ACTIVE"))

with col3:
    st.metric("Waiting Tokens", sum(1 for token in tokens if token.get("status") == "WAITING"))
