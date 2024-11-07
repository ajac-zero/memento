import json
from datetime import UTC, datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase, MappedAsDataclass, AsyncAttrs):
    ...


class BaseMixin(MappedAsDataclass):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    created_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(UTC), init=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None, init=False)
    archived: Mapped[bool] = mapped_column(default=False, init=False)


class Conversation(Base, BaseMixin):
    __tablename__ = "memento_conversation"

    agent: Mapped[str]
    uuid: Mapped[UUID] = mapped_column(default_factory=uuid4, init=False, index=True)

    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation", init=False
    )


class Message(Base, BaseMixin):
    __tablename__ = "memento_message"

    conversation_id: Mapped[int] = mapped_column(ForeignKey("memento_conversation.id"))

    role: Mapped[str]
    content: Mapped[Optional[str]]
    tools: Mapped[Optional[str]]
    feedback: Mapped[Optional[bool]]

    uuid: Mapped[Optional[UUID]] = mapped_column(default=None, index=True)
    origin_message_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("memento_message.id"), default=None
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages", init=False
    )
    origin_message: Mapped["Message"] = relationship(init=False)

    def to_openai_format(self):
        return {
            "role": self.role,
            "content": self.content,
            **json.loads(self.tools or "{}"),
        }
