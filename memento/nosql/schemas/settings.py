from pydantic.dataclasses import dataclass
from uuid import uuid4


def idmaker():
    return str(uuid4())


@dataclass
class Settings:
    conversation: str | None = None
    user: str = "user"
    assistant: str = "assistant"
