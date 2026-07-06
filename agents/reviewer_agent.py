from utils.llm import llm_service
from utils.prompt import prompt_builder


class ReviewerAgent:
    """
    Enterprise Reviewer Agent

    Responsibilities
    ----------------
    1. Validate generated answer
    2. Validate retrieved documents
    3. Review answer using LLM
    4. Improve grammar and formatting
    5. Remove hallucinations
    """

    def __init__(self):

        self.llm = llm_service.get_llm()

    # =====================================================
    # Review Answer
    # =====================================================

    def review_answer(
        self,
        answer,
        documents
    ):

        # -------------------------------------------------
        # No Answer Generated
        # -------------------------------------------------

        if not answer or not answer.strip():

            return (
                True,
                "I couldn't find this information in the project knowledge base."
            )

        # -------------------------------------------------
        # No Documents Retrieved
        # -------------------------------------------------

        if len(documents) == 0:

            return (
                True,
                "I couldn't find this information in the project knowledge base."
            )

        # -------------------------------------------------
        # Build Context
        # -------------------------------------------------

        context = ""

        for doc in documents:

            context += doc.page_content

            context += "\n\n"

        # -------------------------------------------------
        # Build Prompt
        # -------------------------------------------------

        prompt = prompt_builder.build_reviewer_prompt(

            context,

            answer

        )

        # -------------------------------------------------
        # Debug (Optional)
        # -------------------------------------------------

        print("=" * 80)
        print("REVIEWER PROMPT")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        # -------------------------------------------------
        # Invoke LLM
        # -------------------------------------------------

        response = self.llm.invoke(

            prompt

        )

        reviewed_answer = response.content.strip()

        # -------------------------------------------------
        # Empty Response
        # -------------------------------------------------

        if not reviewed_answer:

            reviewed_answer = answer

        return (

            True,

            reviewed_answer

        )


# =====================================================
# Singleton Instance
# =====================================================

reviewer_agent = ReviewerAgent()