import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
except ImportError:
    st = None

# ==========================================================
# API Key
# ==========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY and st is not None:
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_PATH = os.path.join(BASE_DIR, "knowledge")

VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_db")