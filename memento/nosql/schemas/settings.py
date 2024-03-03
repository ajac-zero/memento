from pydantic.dataclasses import dataclass
from typing import Optional
from uuid import uuid4


def idmaker():
    return str(uuid4())


@dataclass
class Settings:
    conversation: Optional[str] = None
    user: str = "user"
    assistant: str = "assistant"
