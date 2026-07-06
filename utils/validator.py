import re

from pydantic import BaseModel, Field, ValidationError


class PromptRequest(BaseModel):
    """
    Prompt Validation Model
    """

    prompt: str = Field(

        min_length=6,

        max_length=500

    )


class PromptValidator:
    """
    Enterprise Prompt Validator

    Responsibilities
    ----------------
    1. Empty prompt validation
    2. Length validation
    3. Invalid character validation
    4. Numeric validation
    5. Prompt sanitization
    """

    def validate_prompt(

        self,

        prompt

    ):

        prompt = prompt.strip()

        try:

            request = PromptRequest(

                prompt=prompt

            )

        except ValidationError as e:

            return (

                False,

                e.errors()[0]["msg"]

            )

        # ----------------------------
        # Only Numbers
        # ----------------------------

        if request.prompt.isdigit():

            return (

                False,

                "Prompt cannot contain only numbers."

            )

        # ----------------------------
        # Only Special Characters
        # ----------------------------

        if re.fullmatch(

            r"[^A-Za-z0-9]+",

            request.prompt

        ):

            return (

                False,

                "Prompt cannot contain only special characters."

            )

        # ----------------------------
        # Repeated Character
        # ----------------------------

        if len(set(request.prompt)) == 1:

            return (

                False,

                "Please enter a meaningful question."

            )

        return (

            True,

            request.prompt

        )


# ==========================================
# Singleton Instance
# ==========================================

prompt_validator = PromptValidator()