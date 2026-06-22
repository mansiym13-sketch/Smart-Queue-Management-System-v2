import streamlit as st

from api import login, signup
from ui_helpers import show_api_error


st.set_page_config(
    page_title="Login",
    page_icon="random",
    layout="centered"
)

st.title("Login")

login_tab, signup_tab = st.tabs(
    [
        "Login",
        "Sign Up"
    ]
)

with login_tab:
    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", type="primary"):
        if not email.strip() or not password:
            st.error("Email and password are required")
        else:
            result = login(
                email.strip(),
                password
            )

            if not show_api_error(st, result, "Login failed"):
                st.session_state["token"] = result.get("access_token")
                st.session_state["username"] = result.get("username")
                st.session_state["email"] = result.get("email")
                st.session_state["role"] = result.get("role")
                st.success("Login successful")

with signup_tab:
    username = st.text_input(
        "Name",
        key="signup_name"
    )

    signup_email = st.text_input(
        "Email",
        key="signup_email"
    )

    signup_password = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )

    role = st.selectbox(
        "Role",
        [
            "customer",
            "staff",
            "admin"
        ]
    )

    if st.button("Create Account"):
        if not username.strip() or not signup_email.strip() or not signup_password:
            st.error("Name, email, and password are required")
        else:
            result = signup(
                username.strip(),
                signup_email.strip(),
                signup_password,
                role
            )

            if not show_api_error(st, result, "Signup failed"):
                st.success("Account created. You can log in now.")
                st.json(result)
