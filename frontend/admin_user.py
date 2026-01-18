import streamlit as st
from utils.database import (
    get_all_users,
    deactivate_user,
    activate_user,
    delete_user,
    get_user_book_count
)

def show_admin_users():
    st.subheader("👥 All Users")

    users = get_all_users()
    if not users:
        st.info("No users found")
        return

    # ---- TABLE HEADER ----
    header = st.columns([2, 3, 2, 2, 2, 3])
    header[0].markdown("**Username**")
    header[1].markdown("**Email**")
    header[2].markdown("**Joined**")
    header[3].markdown("**Status**")
    header[4].markdown("**Books**")
    header[5].markdown("**Actions**")

    st.divider()

    # ---- TABLE ROWS ----
    for user in users:
        cols = st.columns([2, 3, 2, 2, 2, 3])

        # Username
        cols[0].write(user["name"])

        # Email
        cols[1].write(user["email"])

        # Joined Date
        joined = user["created_at"].strftime("%d-%m-%Y")
        cols[2].write(joined)

        # Status
        status = "Active" if user.get("is_active", True) else "Inactive"
        color = "🟢" if status == "Active" else "🔴"
        cols[3].write(f"{color} {status}")

        # Book Count
        book_count = get_user_book_count(user["_id"])
        cols[4].write(book_count)

        # Actions
        with cols[5]:
            if user.get("is_active", True):
                if st.button("Deactivate", key=f"deact_{user['_id']}"):
                    deactivate_user(user["_id"])
                    st.success("User deactivated")
                    st.rerun()
            else:
                if st.button("Activate", key=f"act_{user['_id']}"):
                    activate_user(user["_id"])
                    st.success("User activated")
                    st.rerun()

            if st.button("🗑 Delete", key=f"del_{user['_id']}"):
                delete_user(user["_id"])
                st.success("User deleted")
                st.rerun()