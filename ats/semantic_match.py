from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(job_description, resume_text):
    model = load_model()

    jd_embedding = model.encode([job_description])
    resume_embedding = model.encode([resume_text])

    similarity = cosine_similarity(
        jd_embedding,
        resume_embedding
    )[0][0]

    return round(similarity * 100, 2)