import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
except ImportError:
    st = None

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# If running on Streamlit Cloud, read from Secrets
if not GOOGLE_API_KEY and st is not None:
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

KNOWLEDGE_PATH = "knowledge"

VECTOR_DB_PATH = "vector_db"