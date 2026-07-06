from langchain_community.vectorstores import FAISS
from rag.embedding import embeddings


# Create Vector Database
def create_vector_store(texts):

    db = FAISS.from_texts(
        texts,
        embeddings
    )

    db.save_local("faiss_index")


# Load Existing Vector Database
def load_vector_store():

    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )