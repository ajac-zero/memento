import json
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from memento import crud, models


class BaseRecorder:
    def __init__(self, conversation: models.Conversation) -> None:
        self.conversation = conversation

    def add_message(
        self,
        role: str,
        content: str | None = None,
        tools: dict | None = None,
        uuid: UUID | None = None,
    ) -> None:
        message = models.Message(
            self.conversation.id,
            role=role,
            content=content,
            tools=json.dumps(tools) if tools else None,
            feedback=None,
            uuid=uuid,
        )
        self.conversation.messages.append(message)

    def to_openai_format(self) -> list[dict]:
        return [message.to_openai_format() for message in self.conversation.messages]

    def add_openai_response(self, response) -> None:
        message = response.choices[0].message

        self.add_message(
            role=message.role,
            content=message.content,
            tools=tools if (tools := message.tools) else None,
        )


class Recorder(BaseRecorder):
    def __init__(self, conversation: models.Conversation) -> None:
        super().__init__(conversation)

    @classmethod
    def from_conversation(cls, session: Session, id: int | UUID) -> "Recorder":
        conversation = crud.get_conversation(session, id)
        return cls(conversation)

    def save(self, session: Session) -> list[int]:
        session.commit()

        session.refresh(self.conversation)

        return [message.id for message in self.conversation.messages]


class AsyncRecorder(BaseRecorder):
    def __init__(self, conversation: models.Conversation) -> None:
        super().__init__(conversation)

    @classmethod
    async def from_conversation(
        cls, session: AsyncSession, id: int | UUID
    ) -> "AsyncRecorder":
        conversation = await crud.get_conversation_async(session, id)
        return cls(conversation)

    async def save(self, session: AsyncSession) -> list[int]:
        await session.commit()

        await session.refresh(self.conversation, ["messages"])

        return [message.id for message in self.conversation.messages]
