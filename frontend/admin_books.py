import streamlit as st
from utils.database import (
    get_users_with_books,
    admin_get_latest_summary,
    admin_delete_book
)

def show_admin_books():
    st.markdown("## 📚 Users & Their Uploaded Books")

    users = get_users_with_books()
    if not users:
        st.info("No users or books found")
        return

    for user in users:
        if not user.get("books"):
            continue

        with st.expander(f"👤 {user['name']}  |  {user['email']}"):

            for book in user["books"]:
                col1, col2, col3 = st.columns([5, 2, 1])

                # ---- Book Title ----
                col1.markdown(f"📘 **{book['title']}**")

                # ---- View Summary ----
                with col2:
                    if st.button("👁 View Summary", key=f"view_{book['_id']}"):
                        summary_doc = admin_get_latest_summary(book["_id"])

                        if summary_doc:
                            # ✅ SAFE ACCESS
                            summary_text = (
                                summary_doc.get("summary_text")
                                or summary_doc.get("summary")
                                or "Summary text not found"
                            )

                            st.text_area(
                                "Summary",
                                summary_text,
                                height=220
                            )
                        else:
                            st.warning("No summary found")

                # ---- Delete Book ----
                with col3:
                    if st.button("🗑", key=f"del_{book['_id']}"):
                        admin_delete_book(book["_id"])
                        st.success("Book deleted successfully")
                        st.rerun()

                st.markdown(
                    f"<small style='color:gray'>Uploaded: {book['created_at'].strftime('%d-%m-%Y')}</small>",
                    unsafe_allow_html=True
                )
                st.divider()