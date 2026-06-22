def get_ats_suggestions(resume_text, job_description, missing_keywords):
    suggestions = []
    resume_lower = resume_text.lower()

    if "summary" not in resume_lower and "objective" not in resume_lower:
        suggestions.append("Add a professional Summary or Objective section at the top.")

    if "experience" not in resume_lower and "work" not in resume_lower:
        suggestions.append("Add a Work Experience section.")

    if "education" not in resume_lower: 
        suggestions.append("Add an Education section.")

    if "skills" not in resume_lower:
        suggestions.append("Add a dedicated Skills section.")
    
    word_count = len(resume_text.split())
    if word_count < 200:
        suggestions.append("Resume is too short - add more details about your experience and projects.")
    elif word_count > 800:
        suggestions.append("Resume is too long - try to keep it under 1 page for freshers.")

    if missing_keywords:
        suggestions.append(f"Add these misisng keywords to your resume: {', '.join(missing_keywords[:8])}")

    if "@" not in resume_text: 
        suggestions.append("Add a email address.")
    
    if "linkedin" not in resume_lower:
        suggestions.append("Add your LinkedIn profile URL.")
    
    if "github" not in resume_lower:
        suggestions.append("Add your GitHub profile URL.")

    return suggestions
