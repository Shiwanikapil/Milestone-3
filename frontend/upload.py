from datetime import datetime
import streamlit as st
from docx import Document
import PyPDF2

from utils.full_summary import summarize_large_text
from utils.pdf_export import generate_pdf
from utils.database import (
    create_book,
    save_summary,
    update_book_status
)

MAX_FILE_SIZE_MB = 10
from utils.error_handling import safe_ai_call 


# ---------- TEXT EXTRACTORS ----------
def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8", errors="ignore")


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


# ---------- UPLOAD PAGE ----------
def show_upload_page(user_id):

    if not user_id:
        st.error("Please logout and login again")
        return

    st.header("📤 Upload Book")

    uploaded_file = st.file_uploader(
        "Upload TXT / PDF / DOCX (Max 10 MB)",
        type=["txt", "pdf", "docx"]
    )

    title = st.text_input("📘 Book Title")
    #title = st.text_input("Summary type") 

    author = st.text_input("✍️ Author (optional)")
    summary= st.text_input("Summary type") 

    extracted_text = None

    # ---------- FILE VALIDATION ----------
    if uploaded_file:

        file_size_mb = uploaded_file.size / (1024 * 1024)

        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error("❌ File size must be less than 10 MB")
            return

        try:
            if uploaded_file.name.endswith(".txt"):
                extracted_text = extract_text_from_txt(uploaded_file)

            elif uploaded_file.name.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(uploaded_file)

            elif uploaded_file.name.endswith(".docx"):
                extracted_text = extract_text_from_docx(uploaded_file)

            st.success("✅ File uploaded successfully")

            st.text_area(
                "📄 File Preview (first 1000 characters)",
                extracted_text[:1000],
                height=200
            )

        except Exception as e:
            st.error(f"File reading error: {e}")
            return

    # ---------- GENERATE SUMMARY ----------
    if st.button("🚀 Generate Summary", use_container_width=True):

        if not uploaded_file or not title or not extracted_text:
            st.warning("Please upload file and enter book title")
            return

        with st.spinner("🤖 Generating AI summary..."):
            summary = safe_ai_call(summarize_large_text,extracted_text) 

        # ---------- SAVE TO DATABASE ----------
        book_id = create_book(
            user_id=user_id,
            title=title,
            text=extracted_text,
            author=author
        )

        save_summary(book_id, user_id, summary)
        update_book_status(book_id, "summarized")

        # ---------- UI OUTPUT ----------
        st.success("🎉 Summary generated successfully")
        st.balloons()

        st.subheader("📑 Generated Summary")
        st.text_area("Summary", summary, height=300)

        # ---------- DOWNLOAD OPTIONS ----------
        st.markdown("### 📥 Download Summary")

        txt_content = f"""Title: {title}
Author: {author if author else 'N/A'}
Date: {datetime.now().strftime('%d-%m-%Y')}

Summary:
{summary}
"""

        st.download_button(
            "⬇️ Download Summary (TXT)",
            txt_content,
            file_name=f"{title.replace(' ', '_')}_summary.txt",
            mime="text/plain"
        )

        pdf_path = generate_pdf(title, author, summary)

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                "⬇️ Download Summary (PDF)",
                pdf_file,
                file_name=f"{title.replace(' ', '_')}_summary.pdf",
                mime="application/pdf"
            )

        st.text_area("📋 Copy Summary", summary, height=200)