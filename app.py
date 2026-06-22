import streamlit as st
from resume_parser import parse_resume
from matcher import calculate_match_score, get_missing_keywords
from optimizer import get_ats_suggestions
from cover_letter import generate_cover_letter
from database import init_db, add_application, get_all_applications
import tempfile
import os

st.set_page_config(page_title="AI Career Assistant & ATS Optimizer", page_icon="🤎", layout="wide")
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Jost:wght@300;400;500;600&display=swap');

.stApp {
    background-color: #F5F0E8;
}

* {
    font-family: 'Jost', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 1.5rem !important;
    max-width: 1100px;
}

.hero {
    text-align: center;
    padding: 1rem 0 1.5rem 0;
}

.hero-eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #8B9A8B;
    font-weight: 500;
    margin-bottom: 0.8rem;
}

.hero h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 600;
    color: #5C4F44;
    margin: 0;
    letter-spacing: 0.01em;
}

.hero p {
    color: #A8998A;
    font-size: 1rem;
    margin-top: 0.6rem;
    font-weight: 300;
}

.section-label {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #FFFDFA;
    background: #8B9A8B;
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.8rem;
}

.soft-card {
    background: #FFFDFA;
    border: 1px solid #E8DCC8;
    border-radius: 18px;
    padding: 1.6rem;
    margin-bottom: 1rem;
}

.stamp-wrap {
    display: flex;
    justify-content: center;
    padding: 1rem 0 2rem 0;
}

.stamp {
    width: 190px;
    height: 190px;
    border-radius: 50%;
    background: #FFFDFA;
    border: 3px solid #C9A876;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 24px rgba(180, 160, 130, 0.25);
}

.stamp-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #5C4F44;
    line-height: 1;
}

.stamp-label {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8B9A8B;
    margin-top: 0.4rem;
}

.stat-row {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.stat-pill {
    background: #EFE7D8;
    border-radius: 14px;
    padding: 0.9rem 1.4rem;
    text-align: center;
    min-width: 110px;
}

.stat-pill .num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #6B5D52;
}

.stat-pill .lab {
    font-size: 0.7rem;
    color: #A8998A;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.tag-found {
    display: inline-block;
    background: #DCE3D6;
    color: #5A6B57;
    padding: 5px 14px;
    border-radius: 20px;
    margin: 4px;
    font-size: 0.85rem;
    font-weight: 500;
}

.tag-missing {
    display: inline-block;
    background: #F0DCC8;
    color: #9C6B3F;
    padding: 5px 14px;
    border-radius: 20px;
    margin: 4px;
    font-size: 0.85rem;
    font-weight: 500;
}

.suggestion-row {
    background: #FFFDFA;
    border-left: 3px solid #8B9A8B;
    padding: 0.75rem 1.1rem;
    border-radius: 0 12px 12px 0;
    margin-bottom: 0.55rem;
    color: #6B5D52;
    font-size: 0.92rem;
}

.stButton > button {
    background: #6B5D52;
    color: #FFFDFA;
    border: none;
    border-radius: 30px;
    padding: 0.7rem 2.5rem;
    font-weight: 500;
    letter-spacing: 0.03em;
}

.stButton > button:hover {
    background: #5C4F44;
}

.stDownloadButton > button {
    background: #8B9A8B;
    color: white;
    border: none;
    border-radius: 30px;
    padding: 0.6rem 2rem;
}

.stTextInput input, .stTextArea textarea {
    background-color: #FFFDFA !important;
    border: 1px solid #E8DCC8 !important;
    border-radius: 10px !important;
    color: #5C4F44 !important;
}

.stFileUploader {
    background-color: #FFFDFA;
    border: 1.5px dashed #C9A876;
    border-radius: 14px;
    padding: 0.6rem;
}

.stDataFrame {
    background-color: #FFFDFA;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Smart Resume Analysis</div>
    <h1>AI Career Assistant & ATS Optimizer</h1>
    <p>Upload your resume, paste a job description, see where you stand.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 Analyze Resume", "📋 Past Applications"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-label">Resume</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    with col2:
        st.markdown('<p class="section-label">Job Description</p>', unsafe_allow_html=True)
        job_desc = st.text_area("JD", height=150, label_visibility="collapsed", placeholder="Paste the job description here...")

    st.markdown('<p class="section-label">A Little About You</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Name", placeholder="Tiya Joshi", label_visibility="collapsed")
    with c2:
        job_title = st.text_input("Role", placeholder="Data Analyst", label_visibility="collapsed")
    with c3:
        company = st.text_input("Company", placeholder="Yash Technologies", label_visibility="collapsed")
    experience = st.text_input("Exp", placeholder="One line about your experience...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("Analyze My Resume")

    if analyze:
        if uploaded_file and job_desc:
            with st.spinner("Reading between the lines..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                result = parse_resume(tmp_path)
                resume_text = result["raw_text"]
                score = calculate_match_score(resume_text, job_desc)
                missing = get_missing_keywords(resume_text, job_desc)
                suggestions = get_ats_suggestions(resume_text, job_desc, missing)
                os.unlink(tmp_path)

                # Save to database automatically
                add_application(
                    name=name or "Unknown",
                    job_title=job_title or "Not specified",
                    company=company or "Not specified",
                    score=score,
                    skills_count=len(result["skills"]),
                    missing_count=len(missing)
                )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="stamp-wrap">
                <div class="stamp">
                    <div class="stamp-number">{score}%</div>
                    <div class="stamp-label">Match Score</div>
                </div>
            </div>
            <div class="stat-row">
                <div class="stat-pill"><div class="num">{len(result['skills'])}</div><div class="lab">Skills Found</div></div>
                <div class="stat-pill"><div class="num">{len(missing)}</div><div class="lab">Missing</div></div>
                <div class="stat-pill"><div class="num">{result['word_count']}</div><div class="lab">Words</div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<p class="section-label">Skills Found</p>', unsafe_allow_html=True)
                tags = "".join([f'<span class="tag-found">{s}</span>' for s in result["skills"]]) or "<span style='color:#A8998A'>None detected</span>"
                st.markdown(f'<div class="soft-card">{tags}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<p class="section-label">Worth Adding</p>', unsafe_allow_html=True)
                tags2 = "".join([f'<span class="tag-missing">{m}</span>' for m in missing]) or "<span style='color:#A8998A'>Nothing missing</span>"
                st.markdown(f'<div class="soft-card">{tags2}</div>', unsafe_allow_html=True)

            st.markdown('<p class="section-label">Suggestions</p>', unsafe_allow_html=True)
            for s in suggestions:
                st.markdown(f'<div class="suggestion-row">{s}</div>', unsafe_allow_html=True)

            if name and job_title and company:
                st.markdown('<p class="section-label">Your Cover Letter</p>', unsafe_allow_html=True)
                letter = generate_cover_letter(name, job_title, company, result["skills"], experience)
                st.text_area("Letter", letter, height=280, label_visibility="collapsed")
                st.download_button("Download Letter", letter, file_name="cover_letter.txt")
        else:
            st.error("Please upload a resume and paste a job description.")

with tab2:
    st.markdown('<p class="section-label">Your Application History</p>', unsafe_allow_html=True)
    records = get_all_applications()

    if records:
        import pandas as pd
        df = pd.DataFrame(records, columns=["Job Title", "Company", "Match Score (%)", "Skills Found", "Missing Keywords", "Date Added"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="soft-card">No applications analyzed yet. Run an analysis in the first tab to see it here.</div>', unsafe_allow_html=True)

