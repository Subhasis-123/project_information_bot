from config import config
from utils.vector_store import vector_store_service


class RetrievalAgent:

    def __init__(self):

        self.top_k = config.TOP_K

        # Smaller score = better match (FAISS L2 distance)
        self.similarity_threshold = 100

    def retrieve_documents(

        self,

        db,

        query

    ):

        results = vector_store_service.similarity_search_with_score(

            db,

            query,

            k=self.top_k

        )

        context = ""

        documents = []

        for doc, score in results:

            print(f"Score : {score}")

            # Reject unrelated chunks
            if score > self.similarity_threshold:

                continue

            doc.metadata["score"] = float(score)

            context += doc.page_content + "\n\n"

            documents.append(doc)

        return context, documents


retrieval_agent = RetrievalAgent()