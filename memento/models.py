from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, UTC
import json

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    MappedAsDataclass,
    relationship,
)
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, MappedAsDataclass, AsyncAttrs): ...


class BaseMixin(MappedAsDataclass):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    uuid: Mapped[UUID] = mapped_column(default_factory=uuid4, init=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(UTC), init=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None, init=False)
    archived: Mapped[bool] = mapped_column(default=False, init=False)


class Conversation(Base, BaseMixin):
    __tablename__ = "conversation"

    agent: Mapped[str]

    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation", init=False
    )


class Message(Base, BaseMixin):
    __tablename__ = "message"

    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversation.id"))

    role: Mapped[str]
    content: Mapped[Optional[str]]
    tools: Mapped[Optional[str]]
    feedback: Mapped[Optional[bool]]

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages", init=False
    )

    def to_openai_format(self):
        return {
            "role": self.role,
            "content": self.content,
            **json.loads(self.tools or "{}"),
        }
