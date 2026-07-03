from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_API_KEY
from utils.prompt import build_prompt


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)


def generate_answer(context, question, history):

    history_text = ""

    for chat in history:
        history_text += f"{chat['role']} : {chat['content']}\n"

    prompt = build_prompt(
        context,
        question,
        history_text
    )

    response = llm.invoke(prompt)

    return response.content