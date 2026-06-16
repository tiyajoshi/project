from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_description):
    documents = [resume_text, job_description]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2]) [0][0]
    match_percentage = round(score * 100, 2)

    return match_percentage

def get_missing_keywords(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit([job_description])
    job_keywords = set(vectorizer.get_feature_names_out())
    resume_words = set(resume_text.lower().split())

    missing = job_keywords - resume_words
    return list(missing)[:15] 