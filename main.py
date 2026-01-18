import streamlit as st
from frontend.role_selector import show_role_selector
from frontend.auth import show_auth_page
from frontend.admin_login import show_admin_login
from frontend.upload import show_upload_page
from frontend.history import show_history_page
from frontend.search import show_search_page
from frontend.admin_dashboard import show_admin_dashboard 
from frontend.admin_user import show_admin_users
from frontend.admin_books import show_admin_books
from frontend.user_dashboard import show_user_dashboard

st.set_page_config(page_title="AI Book Summarizer", layout="centered")

# ---------- SESSION DEFAULTS ----------
if "role" not in st.session_state:
    st.session_state.role = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False 

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ---------- ROLE SELECTION ----------
if not st.session_state.role:
    show_role_selector()
    st.stop()

# ---------- USER FLOW ----------
if st.session_state.role == "user":

    if not st.session_state.logged_in:
        show_auth_page()
        st.stop()

    st.sidebar.title("👤 User Panel")

    page = st.sidebar.radio(
        "Navigation",
        [ "Dashboard" ,"Upload", "Search", "History", "Logout"]
    )
    if page == "Dashboard":
        show_user_dashboard(st.session_state.user_id)


    elif page == "Upload": 
      show_upload_page(st.session_state.user_id)

    elif page == "Search":
        show_search_page(st.session_state.user_id)

    elif page == "History":
        show_history_page(st.session_state.user_id)

    elif page == "Logout":
        st.session_state.clear()
        st.rerun()

# ---------- ADMIN FLOW ----------
elif st.session_state.role == "admin":

    if not st.session_state.admin_logged_in:
        show_admin_login()
        st.stop()

    st.sidebar.title("🛠 Admin Panel")

    admin_page = st.sidebar.radio(
        "Admin Navigation",
        ["Dashboard", "Users", "Books", "Logout"]
    )

    if admin_page == "Dashboard":
        show_admin_dashboard()

    elif admin_page == "Users":
        show_admin_users()

    elif admin_page == "Books":
        show_admin_books()

    elif admin_page == "Logout":
        st.session_state.clear()
        st.rerun()
st.sidebar.markdown("---")

if st.sidebar.button("🔁 Switch Role"):
    st.session_state.role = None
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.rerun()