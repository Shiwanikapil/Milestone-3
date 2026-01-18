import streamlit as st
from utils.database import get_user_dashboard_stats

def show_user_dashboard(user_id):

    stats = get_user_dashboard_stats(user_id)

    st.markdown("## 📊 User Dashboard")
    st.caption("Your activity overview")

    # ---------- STATS CARDS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="padding:20px;border-radius:12px;
                        background:linear-gradient(135deg,#1f4037,#99f2c8);
                        color:white;text-align:center;">
                <h2>{stats['books_count']}</h2>
                <p>📚 Books Uploaded</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="padding:20px;border-radius:12px;
                        background:linear-gradient(135deg,#42275a,#734b6d);
                        color:white;text-align:center;">
                <h2>{stats['summaries_count']}</h2>
                <p>📝 Summaries Generated</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---------- RECENT UPLOADS ----------
    st.markdown("### 📘 Recently Uploaded Books")

    if not stats["recent_books"]:
        st.info("No books uploaded yet. Start by uploading a book!")
    else:
        for book in stats["recent_books"]:
            st.markdown(
                f"""
                <div style="padding:15px;border-radius:10px;
                            background-color:#1c1c1c;
                            border-left:5px solid #4CAF50;
                            margin-bottom:10px;">
                    <strong>{book['title']}</strong><br>
                    <small style="color:gray;">
                        Uploaded on {book['created_at'].strftime('%d %b %Y')}
                    </small>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ---------- MOTIVATION ----------
    st.success("🚀 Keep uploading books to generate more summaries!")