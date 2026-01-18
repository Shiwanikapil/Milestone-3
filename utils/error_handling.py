# utils/error_handling.py
import streamlit as st

# ---------- SAFE AI CALL ----------
def safe_ai_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        return "⚠️ Unable to generate summary. Please try shorter text."

# ---------- SAFE DATABASE CALL ----------
def safe_db_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        return None

# ---------- FILE VALIDATION ----------
def validate_file(uploaded_file, max_mb=10):
    if not uploaded_file:
        st.warning("Please upload a file")
        return False

    if uploaded_file.size > max_mb * 1024 * 1024:
        st.error("File size must be under 10 MB")
        return False

    return True

# ---------- USER FRIENDLY ERROR ----------
def show_user_error(msg="Something went wrong. Please try again."):
    st.error(msg)