from datetime import datetime, UTC

from sqlmodel import Field, SQLModel, DateTime, JSON


class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), sa_type=DateTime
    )
    updated_at: datetime | None = Field(default=None, sa_type=DateTime)
    agent: str = Field(index=True)


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), sa_type=DateTime
    )
    updated_at: datetime | None = Field(default=None, sa_type=DateTime)
    role: str = Field(default="system")
    content: str | None = Field(default=None)
    tools: dict | None = Field(default=None, sa_type=JSON)
    feedback: bool | None = Field(default=None)
    conversation_id: int = Field(foreign_key="conversation.id")
