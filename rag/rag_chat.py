from rag.vector_store import load_vector_store
from gemini.gemini_api import model


def ask_resume(question):

    db = load_vector_store()

    docs = db.similarity_search(
        question,
        k=3
    )

    context = ""

    for doc in docs:

        context += doc.page_content + "\n\n"

    prompt = f"""
Answer ONLY from the resumes.

If information is unavailable say
"Not Found".

Resumes

{context}

Question

{question}
"""

    response = model.generate_content(prompt)

    return response.text