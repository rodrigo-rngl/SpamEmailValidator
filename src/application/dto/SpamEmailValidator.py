from pydantic import BaseModel, Field, StrictBool


class SpamEmailValidator(BaseModel):
    is_spam: StrictBool = Field(
        ...,
        description="Whether the email is spam.",
    )
    reason: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="A brief explanation of whether or not the email is spam.",
    )
