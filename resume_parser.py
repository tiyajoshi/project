import pdfplumber 
import re
SKILLS_DB = [
    "python", "sql", "machine learning", "deep learning", "nlp", "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "communication", "leadership", "problem solving", "c++", "java", "tableau", "power bi"
]

def extract_text_from_pdf(pdf_path): 
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text 

def extract_skills(text):
    text_lower = text.lower()
    found_skills = [skill for skill in SKILLS_DB if skill in text_lower]
    return list(set(found_skills))

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not found"

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    return {
        "raw_text": text,
        "skills": extract_skills(text),
        "email": extract_email(text),
        "word_count": len(text.split())
    }


    