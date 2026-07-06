import os
import pandas as pd
import streamlit as st

from resume_parser.pdf_parser import extract_pdf_text
from resume_parser.docx_parser import extract_docx_text
from resume_parser.excel_parser import extract_excel_text
from resume_parser.extract_details import extract_details

from ats.ats_score import calculate_ats_score
from ats.semantic_match import semantic_similarity

from database.database import (
    create_table,
    save_candidate,
    get_all_candidates,
    delete_candidate
)

# ----------------------------------------
# Initialize Database
# ----------------------------------------
create_table()

st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide"
)

st.title("📄 AI Resume Screening System")

# ----------------------------------------
# Sidebar Menu
# ----------------------------------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "📤 Upload Resumes",
        "🎯 Screen Candidates",
        "📂 Candidate Database",
        "🤖 Resume Chat"
    ]
)

# ==========================================================
# Upload Resume
# ==========================================================

if menu == "📤 Upload Resumes":

    st.header("📤 Upload New Resumes")

    uploaded_files = st.file_uploader(
        "Upload Resume(s)",
        type=["pdf", "docx", "xlsx", "xls"],
        accept_multiple_files=True
    )

    if st.button("Save Resumes"):

        if not uploaded_files:
            st.warning("Please upload resumes.")
            st.stop()

        os.makedirs("uploads", exist_ok=True)
        resume_texts = []

        for file in uploaded_files:

            resume_path = os.path.join(
                "uploads",
                file.name
            )

            with open(resume_path, "wb") as f:
                f.write(file.getbuffer())

            extension = file.name.split(".")[-1].lower()

            if extension == "pdf":
                text = extract_pdf_text(file)
                

            elif extension == "docx":
                text = extract_docx_text(file)

            elif extension in ["xlsx", "xls"]:
                text = extract_excel_text(file)

            else:
                st.error(f"Unsupported file type: {extension}")
                
                continue
            resume_texts.append(text)


            details = extract_details(text)

            saved = save_candidate(

                details.get("Name", "Unknown"),
                details.get("Email", ""),
                details.get("Phone", ""),
                ",".join(details.get("Skills", [])),
                resume_path,
                text

            )

        

            if saved:
                st.success(f"✅ {file.name} saved successfully.")

            else:
                st.info(f"⚠ {file.name} already exists.")

        from rag.vector_store import create_vector_store

        if resume_texts:
            create_vector_store(resume_texts)
            st.success("✅ FAISS Vector Database Updated Successfully!")

# ==========================================================
# Screen Candidates
# ==========================================================

elif menu == "🎯 Screen Candidates":

    st.header("🎯 Find Best Candidates")

    job_description = st.text_area(
        "Paste Job Description",
        height=200
    )

    if st.button("Analyze Candidates"):

        if not job_description.strip():
            st.warning("Please enter the Job Description.")
            st.stop()

        candidates = get_all_candidates()

        if len(candidates) == 0:
            st.warning("No resumes found in database.")
            st.stop()

        results = []

        for candidate in candidates:

            name = candidate[1]
            email = candidate[2]
            phone = candidate[3]

            skills = candidate[4].split(",")

            resume_text = candidate[6]

            keyword_score, matched = calculate_ats_score(
                job_description,
                skills
            )

            semantic_score = semantic_similarity(
                job_description,
                resume_text
            )

            final_score = round(
                keyword_score * 0.4 +
                semantic_score * 0.6,
                2
            )

            results.append({

                "Candidate": name,
                "Email": email,
                "Phone": phone,
                "Matched Skills": ", ".join(matched),
                "Keyword Score": keyword_score,
                "Semantic Score": semantic_score,
                "ATS Score": final_score

            })

        df = pd.DataFrame(results)

        df = df.sort_values(
            by="ATS Score",
            ascending=False
        )

        df.index = df.index + 1
        df.index.name = "Rank"

        st.success("Analysis Completed Successfully!")

        st.subheader("🏆 Candidate Ranking")

        st.dataframe(
            df,
            use_container_width=True
        )

# ==========================================================
# Candidate Database
# ==========================================================

elif menu == "📂 Candidate Database":

    st.header("📂 Candidate Database")

    search = st.text_input("🔍 Search Candidate")

    rows = get_all_candidates()

    if search:

        rows = [
            row
            for row in rows
            if search.lower() in str(row).lower()
        ]

    if len(rows) == 0:

        st.info("No candidates found.")

    else:

        for row in rows:

            st.markdown("---")

            col1, col2, col3 = st.columns([5, 3, 2])

            with col1:

                st.subheader(row[1])

                st.write("**Skills:**")
                st.write(row[4])

            with col2:

                st.write(f"📧 {row[2]}")
                st.write(f"📞 {row[3]}")

            with col3:

                if os.path.exists(row[5]):

                    with open(row[5], "rb") as resume:

                        st.download_button(

                            "📄 Download Resume",

                            resume,

                            file_name=os.path.basename(row[5]),

                            key=f"download_{row[0]}"

                        )

                if st.button(

                    "🗑 Delete",

                    key=f"delete_{row[0]}"

                ):

                    delete_candidate(row[0])

                    if os.path.exists(row[5]):
                        os.remove(row[5])

                    st.success("Candidate deleted successfully.")

                    st.rerun()
  # ==========================================================
# Resume Chat (RAG)
# ==========================================================

elif menu == "🤖 Resume Chat":

    st.header("🤖 Chat with Uploaded Resumes")

    question = st.text_input(
        "Ask anything about your uploaded resumes"
    )

    if st.button("Ask"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            st.stop()

        from rag.rag_chat import ask_resume

        answer = ask_resume(question)

        st.markdown("### 💬 Answer")

        st.write(answer)