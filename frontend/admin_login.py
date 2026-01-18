import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def show_admin_login():
    st.title("🛠 Admin Login")

    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.success("✅ Admin login successful")
            st.rerun()
        else:
            st.error("❌ Invalid admin credentials")