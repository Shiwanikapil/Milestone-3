import streamlit as st

def show_role_selector():

    # ---------- PAGE CONFIG ---------- 
    st.set_page_config(
        page_title="Select Role",
        layout="centered"
    )

    # ---------- CUSTOM DARK CSS ----------
    st.markdown(""" 
        <style>
        body {
            background-color: #0e1117;
            color: white;
        }

        .role-card {
            background: #161b22;
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            transition: 0.3s;
            border: 1px solid #30363d;
        }

        .role-card:hover {
            transform: scale(1.05);
            border-color: #58a6ff;
        }

        .role-title {
            font-size: 26px;
            font-weight: bold;
            margin-top: 10px;
        }

        .role-desc {
            font-size: 14px;
            color: #8b949e;
            margin-bottom: 20px;
        }

        .stButton > button {
            background-color: #238636;
            color: white;
            border-radius: 10px;
            height: 45px;
            width: 100%;
            font-size: 16px;
        }

        .stButton > button:hover {
            background-color: #2ea043;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- TITLE ----------
    st.markdown("<h1 style='text-align:center;'>🔐 Select Your Role</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#8b949e;'>Choose how you want to continue</p>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ---------- ROLE CARDS ----------
    col1, col2 = st.columns(2)

    # ---------- USER ----------
    with col1:
        st.markdown("""
        <div class="role-card">
            <h2>👤</h2>
            <div class="role-title">User</div>
            <div class="role-desc">
                Upload books, generate summaries and manage your content
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as User"):
            st.session_state["role"] = "user"
            st.rerun()

    # ---------- ADMIN ----------
    with col2:
        st.markdown("""
        <div class="role-card">
            <h2>🛠</h2>
            <div class="role-title">Admin</div>
            <div class="role-desc">
                Manage users, books, analytics and system settings
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as Admin"):
            st.session_state["role"] = "admin"
            st.rerun() 