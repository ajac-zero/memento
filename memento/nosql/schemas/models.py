from typing import Any, List, Annotated, Optional
from pydantic import BaseModel, Field
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
    idx: str = Field(default_factory=idmaker)
    user: Annotated[str, Indexed()]
    assistant: str
    messages: List[Message]


class Assistant(Document):
    idx: str = Field(default_factory=idmaker)
    name: Annotated[str, Indexed()]
    system: str
