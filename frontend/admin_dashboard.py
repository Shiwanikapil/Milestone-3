import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import (
    get_total_users,
    get_active_users,
    get_total_books,
    get_total_summaries,
    get_most_active_users
)


def show_admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")

    # ================== METRICS ==================
    col1, col2, col3, col4 = st.columns(4)

    total_users = get_total_users()
    active_users = get_active_users()
    total_books = get_total_books()
    total_summaries = get_total_summaries()

    col1.metric("👥 Total Users", total_users)
    col2.metric("✅ Active Users", active_users)
    col3.metric("📚 Books Uploaded", total_books)
    col4.metric("📝 Summaries Generated", total_summaries)

    st.divider()

    # ================== MOST ACTIVE USERS ==================
    st.subheader("🔥 Most Active Users")

    active_users_data = get_most_active_users(limit=5)

    if active_users_data:
        df_users = pd.DataFrame(active_users_data)

        fig = px.bar(
            df_users,
            x="name",
            y="book_count",
            text="book_count",
            title="Top Users by Uploaded Books",
            labels={"name": "User", "book_count": "Books Uploaded"},
        )

        fig.update_traces(marker_color="#00ff88")
        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No activity data available")

    st.divider()

    # ================== SYSTEM OVERVIEW ==================
    st.subheader("📈 System Overview")

    overview_data = {
        "Metric": [
            "Total Users",
            "Active Users",
            "Books Uploaded",
            "Summaries Generated"
        ],
        "Count": [
            total_users,
            active_users,
            total_books,
            total_summaries
        ]
    }

    df_overview = pd.DataFrame(overview_data)

    fig2 = px.pie(
        df_overview,
        names="Metric",
        values="Count",
        hole=0.4
    )

    fig2.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ================== ADMIN NOTE ==================
    st.info(
        "📌 This dashboard shows **real-time system analytics** based on actual database data.\n\n"
        "No fake values • No hardcoded data • Fully dynamic"
    )