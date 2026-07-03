from utils.vector_store import similarity_search_with_score


def retrieve_documents(
    db,
    query,
    k=5
):
    """
    Retrieve the Top-K most similar chunks
    from the FAISS vector database.
    """

    results = similarity_search_with_score(
        db,
        query,
        k
    )

    documents = []

    context = ""

    for doc, score in results:

        doc.metadata["score"] = float(score)

        documents.append(doc)

        context += doc.page_content + "\n\n"

    return context, documents