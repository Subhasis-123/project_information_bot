import re

from pydantic import BaseModel, Field, ValidationError


class PromptRequest(BaseModel):

    prompt: str = Field(
        min_length=6,
        max_length=500
    )


class PromptValidator:

    @staticmethod
    def validate(prompt):

        prompt = prompt.strip()

        try:

            request = PromptRequest(
                prompt=prompt
            )

            # Only numbers
            if request.prompt.isdigit():

                return False, "Prompt cannot contain only numbers."

            # Only special characters
            if re.fullmatch(r'[^A-Za-z0-9]+', request.prompt):

                return False, "Please enter a meaningful question."

            # Same character repeated
            if len(set(request.prompt)) == 1:

                return False, "Please enter a meaningful question."

            return True, request.prompt

        except ValidationError as e:

            return False, e.errors()[0]["msg"]