from langchain_google_genai import ChatGoogleGenerativeAI
from utils.prompt import build_reviewer_prompt
from config import GOOGLE_API_KEY


llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

    temperature=0,

    google_api_key=GOOGLE_API_KEY

)


def review_answer(

    answer,

    documents

):

    # -----------------------------
    # Basic Validation
    # -----------------------------

    if not answer.strip():

        return False, "No answer was generated."

    if len(documents) == 0:

        return False, "No relevant documents were retrieved."

    # -----------------------------
    # Build Context
    # -----------------------------

    context = ""

    for doc in documents:

        context += doc.page_content + "\n\n"

    # -----------------------------
    # AI Review
    # -----------------------------

    prompt = build_reviewer_prompt(

        context,

        answer

    )

    response = llm.invoke(prompt)

    reviewed_answer = response.content

    return True, reviewed_answer