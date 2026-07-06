from utils.llm import llm_service
from utils.prompt import prompt_builder


class AnswerAgent:
    """
    Enterprise Answer Agent

    Responsibilities
    ----------------
    1. Build conversation history
    2. Build answer prompt
    3. Invoke LLM
    4. Return generated answer
    """

    def __init__(self):

        self.llm = llm_service.get_llm()

    # ==================================================
    # Generate Answer
    # ==================================================

    def generate_answer(

        self,

        context,

        question,

        history

    ):
        
        if not context.strip():

            return (
            "I couldn't find this information "
            "in the project knowledge base."
            )

        history_text = ""

        for chat in history:

            history_text += (

                f"{chat['role']} : "

                f"{chat['content']}\n"

            )

        prompt = prompt_builder.build_answer_prompt(

            context,

            question,

            history_text

        )

        # =============================================
        # Debug (Optional)
        # =============================================

        print("=" * 80)
        print("QUESTION")
        print(question)

        print("=" * 80)
        print("CONTEXT")
        print(context)

        print("=" * 80)
        print("PROMPT")
        print(prompt)

        print("=" * 80)

        response = self.llm.invoke(

            prompt

        )

        return response.content


# =====================================================
# Singleton Instance
# =====================================================

answer_agent = AnswerAgent()