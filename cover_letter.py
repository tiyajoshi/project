def generate_cover_letter(name, job_title, company_name, skills, experience):
    """ Generates a cover letter using templates. """

    skills_text = ', '.join(skills[:5]) if skills else "various technical skills"

    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company_name}. As a motivated and skilled professional, I am confident that my background and abilites make me an excellent candidate for this role. 

Throughout my academic and professional journey, I have developed a strong expertise in {skills_text}. {experience}

I am particularly drawn to {company_name} because of its reputation for innovation and excellence. I am eager to contribute my skills and grow as part of your team.

I have attached my resume for your consideration and would welcome the opportunity to discuss how my background aligns with your needs.

Thank you for your time and consideration.

Sincerely,
{name}
    """
    return cover_letter.strip()
