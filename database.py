import sqlite3
from datetime import datetime

DB_NAME = "career_assistant.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_name TEXT,
            job_title TEXT,
            company TEXT,
            match_score REAL,
            skills_found INTEGER,
            missing_keywords INTEGER,
            date_added TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_application(name, job_title, company, score, skills_count, missing_count):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (applicant_name, job_title, company, match_score, skills_found, missing_keywords, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, job_title, company, score, skills_count, missing_count, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_all_applications():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, job_title, company, match_score, skills_found, missing_keywords, date_added FROM applications ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_application(app_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()
