import os

from langchain_community.vectorstores import FAISS

from config import VECTOR_DB_PATH


INDEX_FILE = os.path.join(
    VECTOR_DB_PATH,
    "index.faiss"
)


def create_vector_store(chunks, embeddings):

    """
    Create FAISS vector database
    and save it locally.
    """

    if not os.path.exists(VECTOR_DB_PATH):

        os.makedirs(VECTOR_DB_PATH)

    db = FAISS.from_documents(
        chunks,
        embeddings
    )

    db.save_local(VECTOR_DB_PATH)

    return db


def load_vector_store(embeddings):

    """
    Load existing FAISS database.
    """

    db = FAISS.load_local(

        VECTOR_DB_PATH,

        embeddings,

        allow_dangerous_deserialization=True

    )

    return db


def vector_store_exists():

    """
    Check whether the FAISS index exists.
    """

    return os.path.exists(INDEX_FILE)


def get_vector_store(chunks, embeddings):

    """
    Enterprise method.

    If vector DB exists → Load

    Else → Create & Save
    """

    if vector_store_exists():

        print("Loading existing FAISS database...")

        return load_vector_store(embeddings)

    print("Creating new FAISS database...")

    return create_vector_store(
        chunks,
        embeddings
    )


def similarity_search(
    db,
    query,
    k=5
):

    """
    Retrieve Top-K similar chunks.
    """

    results = db.similarity_search(
        query,
        k=k
    )

    return results


def similarity_search_with_score(
    db,
    query,
    k=5
):

    """
    Retrieve Top-K chunks with similarity score.
    """

    results = db.similarity_search_with_score(
        query,
        k=k
    )

    return results