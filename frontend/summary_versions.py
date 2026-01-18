import streamlit as st
from utils.database import get_all_summaries, mark_favorite_summary, delete_summary


def show_summary_versions(book_id):
    st.subheader("🕒 Summary Versions")

    summaries = get_all_summaries(book_id)

    if not summaries:
        st.info("No summary versions found.")
        return

    for idx, s in enumerate(summaries, start=1):
        with st.expander(f"Version {idx} — {s['created_at'].strftime('%d-%m-%Y %H:%M')}"):

            st.write(s["summary_text"])

            col1, col2 = st.columns(2)

            # ⭐ Favorite
            with col1:
                if st.button("⭐ Mark Favorite", key=f"fav_{s['_id']}"):
                    mark_favorite_summary(s["_id"])
                    st.success("Marked as favorite ⭐")
                    st.rerun()

            # 🗑️ Delete version
            with col2:
                if st.button("🗑️ Delete Version", key=f"del_{s['_id']}"):
                    delete_summary(s["_id"])
                    st.warning("Summary version deleted")
                    st.rerun()