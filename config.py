import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
except ImportError:
    st = None


class Config:
    """
    Enterprise Configuration Class
    """

    def __init__(self):

        # ==========================================
        # Base Directory
        # ==========================================

        self.BASE_DIR = os.path.dirname(
            os.path.abspath(__file__)
        )

        # ==========================================
        # Project Paths
        # ==========================================

        self.KNOWLEDGE_PATH = os.path.join(
            self.BASE_DIR,
            "RDB"
        )

        self.VECTOR_DB_PATH = os.path.join(
            self.BASE_DIR,
            "vector_db"
        )

        # ==========================================
        # Google API Key
        # ==========================================

        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        if not self.GOOGLE_API_KEY and st is not None:

            try:
                self.GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
            except Exception:
                pass

        # ==========================================
        # Gemini Configuration
        # ==========================================

        self.LLM_MODEL = "gemini-2.5-flash"

        self.TEMPERATURE = 0

        # ==========================================
        # Embedding Model
        # ==========================================

        self.EMBEDDING_MODEL = "models/gemini-embedding-001"

        # ==========================================
        # Chunk Settings
        # ==========================================

        self.CHUNK_SIZE = 1000

        self.CHUNK_OVERLAP = 200

        # ==========================================
        # Retrieval Settings
        # ==========================================

        self.TOP_K = 5


# =====================================================
# Singleton Instance
# =====================================================

config = Config()