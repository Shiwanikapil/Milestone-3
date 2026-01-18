import streamlit as st
from datetime import datetime
from utils.database import (
    get_books,
    delete_book,
    get_all_summaries,
    set_favorite_summary,
    set_default_summary
)
from utils.diff_utils import highlight_diff  


# ================= SUMMARY VERSION VIEW =================
def show_summary_versions(book_id):
    st.subheader("📜 Summary Versions")

    summaries = get_all_summaries(book_id)
    if not summaries:
        st.info("No summaries found")
        return

    # ---------- SHOW ALL VERSIONS ----------
    for i, s in enumerate(summaries):
        st.markdown(f"### 📝 Version {len(summaries) - i}")
        st.write(s["summary_text"])
        st.divider()

    # ---------- COMPARE LATEST TWO ----------
    if len(summaries) >= 2:
        st.subheader("🔍 Compare Latest Two Versions")

        diff_text = highlight_diff(
            summaries[1]["summary_text"],   # older
            summaries[0]["summary_text"]    # latest
        )

        st.text_area("Differences", diff_text, height=300)


# ================= HISTORY PAGE =================
def show_history_page(user_id):
    st.header("📚 History")

    books = get_books(user_id)
    if not books:
        st.info("No uploads yet")
        return

    for book in books:
        with st.expander(f"📘 {book['title']}"):

            summaries = get_all_summaries(book["_id"])
            if not summaries:
                st.info("No summaries generated yet")
                continue

            # ---------- PICK DEFAULT OR LATEST ----------
            default_summary = next(
                (s for s in summaries if s.get("is_default")),
                summaries[0]
            )

            col1, col2, col3 = st.columns([4, 1, 1])

            # ---------- BOOK DETAILS ----------
            with col1:
                st.write(f"**Author:** {book.get('author', 'N/A')}")
                st.write(f"**Status:** {book.get('status', 'uploaded')}")

            # ---------- DELETE BOOK ----------
            with col2:
                if st.button("🗑️", key=f"del_{book['_id']}"):
                    delete_book(book["_id"], user_id)
                    st.success("❌ Book & summaries deleted")
                    st.rerun()

            # ---------- DOWNLOAD SUMMARY ----------
            with col3:
                txt_content = f"""Title: {book['title']}
Author: {book.get('author', 'N/A')}
Date: {datetime.now().strftime('%d-%m-%Y')}

Summary:
{default_summary["summary_text"]}
"""
                downloaded = st.download_button(
                    "⬇️",
                    txt_content,
                    file_name=f"{book['title'].replace(' ', '_')}_summary.txt",
                    mime="text/plain",
                    key=f"txt_{book['_id']}"
                )

                if downloaded:
                    st.success("⬇️ Summary downloaded")

            # ---------- SHOW SUMMARY ----------
            st.subheader("📝 Latest / Default Summary")
            st.write(default_summary["summary_text"])

            # ---------- FAV + DEFAULT BUTTONS ----------
            colF, colD = st.columns(2)

            with colF:
                fav_label = "⭐ Mark Favourite" if not default_summary.get("is_favorite") else "✅ Favourite"
                if st.button(fav_label, key=f"fav_{default_summary['_id']}"):
                    set_favorite_summary(default_summary["_id"], book["_id"])
                    st.success("⭐ Marked as favourite summary")
                    st.rerun()

            with colD:
                def_label = "🏷️ Set Default" if not default_summary.get("is_default") else "✅ Default"
                if st.button(def_label, key=f"def_{default_summary['_id']}"):
                    set_default_summary(default_summary["_id"], book["_id"])
                    st.success("🏷️ Set as default summary")
                    st.rerun()

            st.divider()

            # ---------- VIEW VERSIONS ----------
            if st.button("🔁 View Versions", key=f"versions_{book['_id']}"):
                st.session_state["show_versions_for"] = book["_id"]

    # ---------- VERSION PANEL ----------
    if st.session_state.get("show_versions_for"):
        show_summary_versions(st.session_state["show_versions_for"])