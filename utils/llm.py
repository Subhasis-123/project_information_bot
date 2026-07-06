from langchain_google_genai import ChatGoogleGenerativeAI

from config import config


class LLMService:
    """
    Enterprise LLM Service

    Responsibilities
    ----------------
    1. Initialize the LLM
    2. Return the LLM instance
    3. Hide LLM implementation details
    """

    def __init__(self):

        self._llm = ChatGoogleGenerativeAI(

            model=config.LLM_MODEL,

            temperature=config.TEMPERATURE,

            google_api_key=config.GOOGLE_API_KEY

        )

    # ==================================================
    # Get LLM
    # ==================================================

    def get_llm(self):

        return self._llm


# ==================================================
# Singleton Instance
# ==================================================

llm_service = LLMService()