from resume_parser import parse_resume
from matcher import calculate_match_score, get_missing_keywords

result = parse_resume("Tiya_Joshi_Resume.pdf")
resume_text = result["raw_text"]
job_desc = """
We are looking for a Data Analyst with skills in Python, SQL, pandas, data visualization, Power Bi, and machine learning. Strong communication and problem solving skills are required. 
"""
score = calculate_match_score(resume_text, job_desc)
missing = get_missing_keywords(resume_text, job_desc)

print("Resume Skills:", result["skills"])
print("Match Score:", score, "%")
print("Missing Keywords:", missing)

