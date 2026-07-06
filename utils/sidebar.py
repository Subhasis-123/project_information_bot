import streamlit as st

from config import config


class Sidebar:

    def render(

        self,

        total_docs,

        total_chunks,

        total_chat

    ):

        with st.sidebar:

            st.markdown("# 🤖 CIS AI")

            st.divider()

            st.markdown("## 📂 Knowledge Base")

            st.metric(

                "Documents",

                total_docs

            )

            st.metric(

                "Chunks",

                total_chunks

            )

            st.metric(

                "Chat",

                total_chat

            )

            st.divider()

            st.markdown("## 🧠 AI Model")

            st.success(

                config.LLM_MODEL

            )

            st.markdown("## 📦 Vector DB")

            st.info(

                "FAISS"

            )

            st.divider()

            st.markdown("## ⚙ System")

            st.success(

                "Healthy"

            )

            st.divider()

            st.caption(

                "Version 2.0"

            )


sidebar = Sidebar()