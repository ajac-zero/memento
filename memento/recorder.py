import json
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from memento import crud, models


class Recoder:
    def __init__(
        self, conversation: models.Conversation, messages: list[models.Message]
    ) -> None:
        self.conversation = conversation
        self.messages = messages
        self.new_messages = []

    @classmethod
    def from_conversation(cls, session: Session, id: int | UUID) -> "Recoder":
        conversation = crud.get_conversation(session, id)
        messages = conversation.messages
        return cls(conversation, messages)

    @classmethod
    async def from_conversation_async(
        cls, session: AsyncSession, id: int | UUID
    ) -> "Recoder":
        conversation = await crud.get_conversation_async(session, id)
        messages = await conversation.awaitable_attrs.messages
        return cls(conversation, messages)

    def add_message(
        self,
        role: str,
        content: str | None = None,
        tools: dict | None = None,
        uuid: UUID | None = None,
    ):
        message = models.Message(
            self.conversation.id,
            role=role,
            content=content,
            tools=json.dumps(tools) if tools else None,
            feedback=None,
            uuid=uuid,
        )
        self.messages.append(message)
        self.new_messages.append(message)

    def commit_new_messages(self, session: Session):
        session.add_all(self.new_messages)
        session.commit()

        return [message.id for message in self.new_messages]

    async def commit_new_messages_async(self, session: AsyncSession):
        session.add_all(self.new_messages)
        await session.commit()

        return [message.id for message in self.new_messages]

    def to_openai_format(self):
        return [message.to_openai_format() for message in self.messages]

    def add_openai_response(self, response):
        message = response.choices[0].message

        message = models.Message(
            self.conversation.id,
            role=message.role,
            content=message.content,
            tools=json.dumps(tools) if (tools := message.tools) else None,
            feedback=None,
        )
        self.messages.append(message)
        self.new_messages.append(message)
