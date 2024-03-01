from memento.nosql.schemas.settings import idmaker
from pydantic import BaseModel, Field
from beanie import Document, Indexed
from typing import List, Annotated


class MessageContent(BaseModel):
    role: str
    content: str


class Message(Document):
    idx: str = Field(default_factory=idmaker)  # type: ignore
    content: MessageContent


class Conversation(Document):
    idx: str = Field(default_factory=idmaker)  # type: ignore
    user: Annotated[str, Indexed()]
    assistant: str
    messages: List[Message]


class Assistant(Document):
    idx: str = Field(default_factory=idmaker)  # type: ignore
    name: Annotated[str, Indexed()]
    system: str
