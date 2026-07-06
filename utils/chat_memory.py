import streamlit as st


class ChatMemoryService:
    """
    Enterprise Chat Memory Service

    Responsibilities
    ----------------
    1. Initialize chat history
    2. Store user messages
    3. Store AI messages
    4. Retrieve chat history
    5. Clear chat history
    """

    def __init__(self):

        self.memory_key = "chat_history"

    # ==========================================
    # Initialize Chat
    # ==========================================

    def initialize_chat(self):

        if self.memory_key not in st.session_state:

            st.session_state[self.memory_key] = []

    # ==========================================
    # Add User Message
    # ==========================================

    def add_user_message(self, message):

        st.session_state[self.memory_key].append(

            {

                "role": "user",

                "content": message

            }

        )

    # ==========================================
    # Add AI Message
    # ==========================================

    def add_ai_message(self, message):

        st.session_state[self.memory_key].append(

            {

                "role": "assistant",

                "content": message

            }

        )

    # ==========================================
    # Get Chat History
    # ==========================================

    def get_chat_history(self):

        return st.session_state.get(

            self.memory_key,

            []

        )

    # ==========================================
    # Clear Chat
    # ==========================================

    def clear_chat(self):

        st.session_state[self.memory_key] = []


# ==================================================
# Singleton Instance
# ==================================================

chat_memory = ChatMemoryService()