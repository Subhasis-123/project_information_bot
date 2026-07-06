import streamlit as st

from config import KNOWLEDGE_PATH

# ===========================
# Utils
# ===========================

from utils.loaders import load_documents
from utils.chunking import chunk_documents
from utils.embeddings import get_embeddings
from utils.vector_store import get_vector_store
from utils.knowledge_indexer import prepare_knowledge_base
from utils.validator import PromptValidator

from utils.chat_memory import (
    initialize_chat,
    add_user_message,
    add_ai_message,
    get_chat_history
)

# ===========================
# Agents
# ===========================

from agents.retrieval_agent import retrieve_documents
from agents.answer_agent import generate_answer
from agents.reviewer_agent import review_answer

# ===========================
# Streamlit Config
# ===========================

st.set_page_config(

    page_title="AI Project Knowledge Assistant",

    page_icon="🤖",

    layout="wide"
)

# ===========================
# Initialize Chat
# ===========================

initialize_chat()

# ===========================
# Header
# ===========================

col1, col2 = st.columns([4,1])

with col1:

    st.title("🤖 CIS Project Knowledge Assistant")

    st.caption(
        "Enterprise Chatbot"
    )

st.markdown(
        """
        <div style="text-align:right;">
            <b>👨‍💻 Author</b><br>
            <span style="font-size:18px;">Subhasis Acharjee</span><br>
            <span style="font-size:13px;color:gray;">
            Mainframe Developer <br>
            AI & Data Engineering Enthusiast
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ===========================
# Initialize Knowledge Base
# ===========================

embeddings = get_embeddings()

with st.spinner("Preparing Knowledge Base..."):

    prepare_knowledge_base(

        KNOWLEDGE_PATH,

        embeddings

    )

    docs = load_documents(KNOWLEDGE_PATH)

    chunks = chunk_documents(docs)

    db = get_vector_store(

        chunks,

        embeddings

    )

# ===========================
# Chat History
# ===========================

history = get_chat_history()

for chat in history:

    with st.chat_message(chat["role"]):

        st.markdown(chat["content"])

# ===========================
# Chat Input
# ===========================

query = st.chat_input(

    "Ask anything about your project..."

)

if query:


    valid, result = PromptValidator.validate(query)

    if not valid:

        st.warning(result)

        st.stop()

    query = result
    # Show User Message

    add_user_message(query)

    with st.chat_message("user"):

        st.markdown(query)

    # ----------------------------

    with st.spinner("Searching Knowledge Base..."):

        context, documents = retrieve_documents(

            db,

            query

        )

    # ----------------------------

    with st.spinner("Generating Answer..."):

        answer = generate_answer(

            context,

            query,

            get_chat_history()

        )

    # ----------------------------

    valid, final_answer = review_answer(

        answer,

        documents

    )

    # ----------------------------

    if valid:

        add_ai_message(final_answer)

        with st.chat_message("assistant"):

            st.markdown(final_answer)

    else:

        with st.chat_message("assistant"):

            st.error(final_answer)

    # ===========================
    # Sources
    # ===========================

    with st.expander("📚 Sources Used"):

        for i, doc in enumerate(documents):

            st.markdown(
                f"### Source {i+1}"
            )

            st.write(
                f"📄 File : {doc.metadata.get('source','Unknown')}"
            )

            st.write(
                f"📂 Type : {doc.metadata.get('file_type','Unknown')}"
            )

            if "page" in doc.metadata:

                st.write(
                    f"📃 Page : {doc.metadata.get('page')}"
                )

            if "score" in doc.metadata:

                st.write(
                    f"🎯 Similarity Score : {round(doc.metadata['score'],4)}"
                )

            st.code(
                doc.page_content
            )