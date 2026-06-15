from resume_parser import parse_resume
result = parse_resume("Tiya_Joshi_Resume.pdf")
print("Email:", result["email"])
print("Skills:", result["skills"])
print("Word Count:", result["word_count"])
