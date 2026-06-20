import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api import login
st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Smart Queue Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    result = login(username, password)

    if "access_token" in result:

        st.session_state["token"] = result["access_token"]

        if "role" in result:
            st.session_state["role"] = result["role"]

        st.success("Login Successful ✅")

    else:
        st.error("Invalid Username or Password")
        st.write(result)