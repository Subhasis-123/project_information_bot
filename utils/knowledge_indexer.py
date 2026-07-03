import hashlib
import os
import pickle

from utils.loaders import load_documents
from utils.chunking import chunk_documents
from utils.vector_store import create_vector_store

HASH_FILE = "vector_db/knowledge.hash"


def calculate_hash(folder):

    md5 = hashlib.md5()

    for root, _, files in os.walk(folder):

        for file in sorted(files):

            path = os.path.join(root, file)

            with open(path, "rb") as f:

                md5.update(f.read())

    return md5.hexdigest()


def save_hash(hash_value):

    with open(HASH_FILE, "wb") as f:

        pickle.dump(hash_value, f)


def load_hash():

    if not os.path.exists(HASH_FILE):

        return None

    with open(HASH_FILE, "rb") as f:

        return pickle.load(f)


def prepare_knowledge_base(folder, embeddings):

    current_hash = calculate_hash(folder)

    previous_hash = load_hash()

    if current_hash == previous_hash:

        return False

    docs = load_documents(folder)

    chunks = chunk_documents(docs)

    create_vector_store(
        chunks,
        embeddings
    )

    save_hash(current_hash)

    return True