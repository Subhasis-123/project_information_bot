import hashlib
import os
import pickle

from utils.loaders import document_loader
from utils.chunking import text_chunker
from utils.vector_store import vector_store_service


class KnowledgeIndexer:
    """
    Enterprise Knowledge Indexer

    Responsibilities:
    -----------------
    1. Detect knowledge base changes
    2. Load documents
    3. Chunk documents
    4. Build Vector Database
    5. Store latest hash
    """

    def __init__(self):

        self.hash_file = os.path.join(
            "vector_db",
            "knowledge.hash"
        )

    # =====================================================
    # Calculate Folder Hash
    # =====================================================

    def calculate_hash(self, folder):

        md5 = hashlib.md5()

        for root, _, files in os.walk(folder):

            for file in sorted(files):

                path = os.path.join(root, file)

                with open(path, "rb") as f:

                    md5.update(f.read())

        return md5.hexdigest()

    # =====================================================
    # Save Hash
    # =====================================================

    def save_hash(self, hash_value):

        with open(self.hash_file, "wb") as f:

            pickle.dump(hash_value, f)

    # =====================================================
    # Load Hash
    # =====================================================

    def load_hash(self):

        if not os.path.exists(self.hash_file):

            return None

        with open(self.hash_file, "rb") as f:

            return pickle.load(f)

    # =====================================================
    # Prepare Knowledge Base
    # =====================================================

    def prepare_knowledge_base(

        self,

        folder,

        embeddings

    ):

        current_hash = self.calculate_hash(

            folder

        )

        previous_hash = self.load_hash()

        # No changes

        if current_hash == previous_hash:

            print(
                "Knowledge Base already up-to-date."
            )

            return False

        print(
            "Knowledge Base changed. Rebuilding..."
        )

        docs = document_loader.load_documents(

            folder

        )

        chunks = text_chunker.chunk_documents(

            docs

        )

        vector_store_service.create_vector_store(

            chunks,

            embeddings

        )

        self.save_hash(

            current_hash

        )

        print(
            "Knowledge Base successfully indexed."
        )

        return True


# =====================================================
# Singleton Instance
# =====================================================

knowledge_indexer = KnowledgeIndexer()