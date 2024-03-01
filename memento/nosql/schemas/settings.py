from pydantic import BaseModel, Field
from typing import Annotated
from uuid import uuid4


def idmaker():
    return str(uuid4())


class Settings(BaseModel):
    conversation: Annotated[
        str, "ID of current conversation; Generated if not given."
    ] = Field(default_factory=idmaker)
    user: Annotated[str, "Username of the user as stored in the database"] = Field(
        default="user"
    )
    assistant: Annotated[
        str, "Name of the assistant handling the conversation"
    ] = Field(default="assistant")
