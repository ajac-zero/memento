from pydantic import BaseModel, Field, field_validator
from typing import Any, List, Annotated, Optional
from beanie import Document, Indexed
from uuid import uuid4


def idmaker():
    return uuid4().hex


class MessageContent(BaseModel):
    role: str
    content: str


class Message(Document):
    idx: str = Field(default_factory=idmaker)
    augment: Optional[Any] = None
    content: MessageContent


class Conversation(Document):
    idx: Optional[str]
    user: Annotated[str, Indexed()]
    assistant: str
    messages: List[Message]

    @field_validator('idx')
    @classmethod
    def setIDx(cls, idx: str | None) -> str:
        return idx if idx else idmaker()

class Assistant(Document):
    idx: str = Field(default_factory=idmaker)
    name: Annotated[str, Indexed()]
    system: str
