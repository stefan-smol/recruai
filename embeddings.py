import cohere
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(api_key)


def get_embeddings(texts, model="embed-english-v3.0", input_type="search_document"):
    try:
        response = co.embed(
            texts=texts,
            model=model,
            input_type=input_type
        )
        return response.embeddings
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return None


def calculate_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


def screen_resumes(job_description, resumes):
    job_embeddings = get_embeddings([job_description])
    if not job_embeddings:
        return []
    job_embedding = job_embeddings[0]

    results = []
    for resume in resumes:
        resume_embeddings = get_embeddings([resume])
        if not resume_embeddings:
            continue
        resume_embedding = resume_embeddings[0]
        similarity_score = calculate_similarity(
            job_embedding, resume_embedding)
        if similarity_score >= 0.8:
            match_type = "excellent match"
        elif similarity_score >= 0.4:
            match_type = "good match"
        else:
            match_type = "bad match"
        results.append((resume, similarity_score, match_type))
    results.sort(key=lambda x: x[1], reverse=True)
    return results
