from typing import Optional, List
from datetime import datetime, UTC

from sqlalchemy import JSON, ForeignKey
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

    def to_openai_format(self):
        return [message.to_openai_format() for message in self.messages]

    async def to_openai_format_async(self):
        return [
            message.to_openai_format()
            for message in (await self.awaitable_attrs.messages)
        ]


class Message(Base, BaseMixin):
    __tablename__ = "message"

    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversation.id"))
    role: Mapped[str] = mapped_column(default="system")
    content: Mapped[Optional[str]] = mapped_column(default=None)
    tools: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    feedback: Mapped[Optional[bool]] = mapped_column(default=None)

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages", init=False
    )

    def to_openai_format(self):
        return {"role": self.role, "content": self.content, **(self.tools or {})}
