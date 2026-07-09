from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text_cleaner import clean_text

def score_resume(resume_text, job_description):
    corpus = [
        clean_text(job_description),
        clean_text(resume_text)
    ]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return score
