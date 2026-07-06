import os

from langchain_community.vectorstores import FAISS

from config import config


class VectorStoreService:
    """
    Enterprise Vector Store Service

    Responsibilities:
    -----------------
    1. Create FAISS database
    2. Load existing FAISS database
    3. Check whether vector DB exists
    4. Perform similarity search
    5. Perform similarity search with scores
    """

    def __init__(self):

        self.vector_db_path = config.VECTOR_DB_PATH

        self.index_file = os.path.join(

            self.vector_db_path,

            "index.faiss"

        )

    # =====================================================
    # Create Vector Store
    # =====================================================

    def create_vector_store(

        self,

        chunks,

        embeddings

    ):

        if not os.path.exists(

            self.vector_db_path

        ):

            os.makedirs(

                self.vector_db_path

            )

        db = FAISS.from_documents(

            chunks,

            embeddings

        )

        db.save_local(

            self.vector_db_path

        )

        return db

    # =====================================================
    # Load Vector Store
    # =====================================================

    def load_vector_store(

        self,

        embeddings

    ):

        return FAISS.load_local(

            self.vector_db_path,

            embeddings,

            allow_dangerous_deserialization=True

        )

    # =====================================================
    # Check Vector DB
    # =====================================================

    def vector_store_exists(self):

        return os.path.exists(

            self.index_file

        )

    # =====================================================
    # Get Vector Store
    # =====================================================

    def get_vector_store(

        self,

        chunks,

        embeddings

    ):

        if self.vector_store_exists():

            print(

                "Loading existing FAISS database..."

            )

            return self.load_vector_store(

                embeddings

            )

        print(

            "Creating new FAISS database..."

        )

        return self.create_vector_store(

            chunks,

            embeddings

        )

    # =====================================================
    # Similarity Search
    # =====================================================

    def similarity_search(

        self,

        db,

        query,

        k=5

    ):

        return db.similarity_search(

            query,

            k=k

        )

    # =====================================================
    # Similarity Search with Score
    # =====================================================

    def similarity_search_with_score(

        self,

        db,

        query,

        k=5

    ):

        return db.similarity_search_with_score(

            query,

            k=k

        )


# =====================================================
# Singleton Instance
# =====================================================

vector_store_service = VectorStoreService()