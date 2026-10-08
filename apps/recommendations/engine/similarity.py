import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_content_similarities(student_text, course_texts):
    if not course_texts:
        return []

    corpus = [student_text] + course_texts
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        student_vec = tfidf_matrix[0]
        course_vecs = tfidf_matrix[1:]
        
        sim_matrix = cosine_similarity(student_vec, course_vecs)
        scores = sim_matrix[0].tolist()
        return [float(max(0.0, min(1.0, score))) for score in scores]
    except Exception as e:
        # Fallback if text matrix is empty or error occurs
        return [0.0] * len(course_texts)
