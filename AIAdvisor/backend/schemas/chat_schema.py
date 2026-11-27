
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    user_id: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    message: str = Field(
        min_length=1,
        max_length=2000
    )

    conversation_history: list[dict] = Field(
        default_factory=list,
        max_length=6
    )


class ChatResponse(BaseModel):
    user_id: Optional[str] = None
    message: str
    response: str
