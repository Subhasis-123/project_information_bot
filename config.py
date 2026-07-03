import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

KNOWLEDGE_PATH = "knowledge"

VECTOR_DB_PATH = "vector_db"