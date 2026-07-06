from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import config


class EmbeddingService:
    """
    Enterprise Embedding Service

    Responsibilities:
    -----------------
    1. Initialize embedding model
    2. Return embedding instance
    3. Keep embedding configuration centralized
    """

    def __init__(self):

        self.embeddings = GoogleGenerativeAIEmbeddings(

            model=config.EMBEDDING_MODEL,

            google_api_key=config.GOOGLE_API_KEY

        )

    def get_embeddings(self):

        return self.embeddings


# Singleton Instance
embedding_service = EmbeddingService()