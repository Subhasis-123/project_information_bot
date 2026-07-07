from pydantic import BaseModel, Field, ValidationError


class PromptModel(BaseModel):

    prompt: str = Field(
        min_length=6,
        max_length=1000
    )


class PromptValidator:

    def validate_prompt(self, prompt: str):

        # Check empty prompt
        if prompt is None or prompt.strip() == "":
            return False, "❌ Prompt cannot be empty."

        try:
            data = PromptModel(
                prompt=prompt.strip()
            )
            return True, data.prompt

        except ValidationError as e:

            error = e.errors()[0]

            if error["type"] == "string_too_short":
                return False, "❌ Prompt must contain at least 6 characters."

            if error["type"] == "string_too_long":
                return False, "❌ Prompt is too long."

            return False, "❌ Invalid prompt."


prompt_validator = PromptValidator()