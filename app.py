import streamlit as st

from config import config

# =====================================================
# Services
# =====================================================

from utils.embeddings import embedding_service
from utils.loaders import document_loader
from utils.chunking import text_chunker
from utils.vector_store import vector_store_service
from utils.knowledge_indexer import knowledge_indexer
from utils.chat_memory import chat_memory
from utils.validator import prompt_validator
from utils.ui import ui
from utils.sidebar import sidebar
# =====================================================
# Agents
# =====================================================

from agents.answer_agent import answer_agent
from agents.reviewer_agent import reviewer_agent
from agents.retrieval_agent import retrieval_agent

# =====================================================
# Streamlit Configuration
# =====================================================

st.set_page_config(

    page_title="AI Project Knowledge Assistant",

    page_icon="🤖",

    layout="wide"

)

ui.load_css()

# =====================================================
# Initialize Chat
# =====================================================

chat_memory.initialize_chat()

# =====================================================
# Header
# =====================================================

col1, col2 = st.columns([4,1])

with col1:

  
    ui.title("🤖 CIS Project Knowledge Assistant",
             "Enterprise AI powered by Gemini + LangChain + FAISS")


    st.markdown(
        """
        <div style="text-align:left;">
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

with col2:
    
    if st.button("🗑 Clear Chat"):

        chat_memory.clear_chat()

        st.rerun()

st.divider()

# =====================================================
# Initialize Knowledge Base
# =====================================================

embeddings = embedding_service.get_embeddings()

with st.spinner("Preparing Knowledge Base..."):

    knowledge_indexer.prepare_knowledge_base(

        config.KNOWLEDGE_PATH,

        embeddings

    )

    docs = document_loader.load_documents(

        config.KNOWLEDGE_PATH

    )

    chunks = text_chunker.chunk_documents(

        docs

    )

    db = vector_store_service.get_vector_store(

        chunks,

        embeddings

    )
    

# =====================================================
# Display Chat History
# =====================================================

history = chat_memory.get_chat_history()

chat_count = len(
    [msg for msg in history if msg["role"] == "user"])

sidebar.render(

    total_docs=len(docs),

    total_chunks=len(chunks),

    total_chat=chat_count

)

for chat in history:

    with st.chat_message(chat["role"]):

        st.markdown(chat["content"])

# =====================================================
# User Input
# =====================================================

query = st.chat_input(

    "Ask anything about your project..."

)

if query:

    # =============================================
    # Validate Prompt
    # =============================================

    valid, result = prompt_validator.validate_prompt(

        query

    )

    if not valid:

        st.warning(result)

        st.stop()

    query = result

    # =============================================
    # Save User Message
    # =============================================

    chat_memory.add_user_message(

        query

    )

    with st.chat_message("user"):

        st.markdown(query)

    # =============================================
    # Retrieve Documents
    # =============================================

    with st.spinner(

        "Searching Knowledge Base..."

    ):

        context, documents = retrieval_agent.retrieve_documents(

            db,

            query

        )

    # =============================================
    # Generate Answer
    # =============================================

    with st.spinner(

        "Generating Answer..."

    ):

        answer = answer_agent.generate_answer(

            context,

            query,

            chat_memory.get_chat_history()

        )

    # =============================================
    # Review Answer
    # =============================================

    valid, final_answer = reviewer_agent.review_answer(

        answer,

        documents

    )

    # =============================================
    # Display Answer
    # =============================================

    if valid:

        chat_memory.add_ai_message(

            final_answer

        )

        with st.chat_message(

            "assistant"

        ):

            st.markdown(

                final_answer

            )
            st.rerun()

    else:

        with st.chat_message(

            "assistant"

        ):

            st.error(

                final_answer

            )

    # =============================================
    # Sources
    # =============================================

    with st.expander(

        "📚 Sources Used"

    ):

        for i, doc in enumerate(

            documents

        ):

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