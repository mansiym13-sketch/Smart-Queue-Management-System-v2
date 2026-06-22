import streamlit as st

from api import get_dashboard_stats, get_queues, get_tokens, is_backend_running


st.set_page_config(
    page_title="Smart Queue Management System",
    page_icon="random",
    layout="wide"
)

st.title("Smart Queue Management System")

backend_online = is_backend_running()

if backend_online:
    st.success("Backend connected")
else:
    st.error("Backend is not reachable. Check BACKEND_URL or the Render backend service.")

stats = get_dashboard_stats() if backend_online else {}
queues = get_queues() if backend_online else []
tokens = get_tokens() if backend_online else []

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Users", stats.get("total_users", 0))

with col2:
    st.metric("Queues", stats.get("total_queues", len(queues)))

with col3:
    st.metric("Tokens", stats.get("total_tokens", len(tokens)))

with col4:
    st.metric("Active Tokens", stats.get("active_tokens", 0))

st.markdown("---")

st.subheader("What You Can Do")

col1, col2 = st.columns(2)

with col1:
    st.write("- Create, update, and delete queues")
    st.write("- Register customers into live queues")
    st.write("- Generate queue tokens with priority")

with col2:
    st.write("- Call the next waiting token")
    st.write("- Update token status")
    st.write("- View dashboard, analytics, and CSV reports")

st.markdown("---")

if queues:
    st.subheader("Available Queues")
    st.dataframe(
        queues,
        use_container_width=True
    )
else:
    st.info("No queues found yet. Create one from Queue Management.")
