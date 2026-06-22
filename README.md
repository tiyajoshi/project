# 🎯 AI Career Assistant & ATS Optimizer

An AI-powered resume analysis tool that compares your resume against a job description, calculates a match score, identifies missing keywords, suggests ATS improvements, and generates a personalized cover letter — all with application history tracking.

## ✨ Features

- **Resume Parsing** — extracts text, skills, and contact info from any PDF resume
- **Job Match Scoring** — TF-IDF + cosine similarity to score resume-to-job fit
- **ATS Optimization** — flags missing sections, keywords, and resume length issues
- **Cover Letter Generator** — creates a tailored cover letter from your resume and the job details
- **Application Tracker** — saves every analysis to a local database so you can review past applications

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **NLP/ML:** scikit-learn (TF-IDF, cosine similarity)
- **PDF Processing:** pdfplumber
- **Database:** SQLite
- **Libraries:** pandas, numpy

## 🚀 Running Locally

1. Clone the repo: