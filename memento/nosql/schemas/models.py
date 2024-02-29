from typing import List, Annotated
from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from uuid import uuid4

def idmaker():
    return str(uuid4())

class Message(Document):
    id: str = Field(default_factory=idmaker) #type: ignore
    role: str
    content: str

class Conversation(Document):
    id: str = Field(default_factory=idmaker) #type: ignore
    user: Annotated[str, Indexed()]
    assistant: str
    messages: List[Message]
