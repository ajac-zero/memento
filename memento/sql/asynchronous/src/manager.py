from memento.sql.asynchronous.schemas.models import Assistant, Conversation, Message, User
from memento.sql.asynchronous.src.repository import Repository
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import Any, Literal
from json import loads, dumps


class Manager(Repository):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__(sessionmaker)

    async def register_user(self, name: str) -> int:
        return await self.create(User(name=name))

    async def register_assistant(
        self,
        name: str,
        system: str,
        model: str | None = None,
        tokens: int | None = None,
    ) -> int:
        return await self.create(
            Assistant(
                name=name,
                system=system,
                model=model,
                tokens=tokens,
            )
        )

    async def register_conversation(self, user: str, assistant: str) -> int:
        user_instance = await self.read(User, name=user)
        assistant_instance = await self.read(Assistant, name=assistant)
        if user_instance and assistant_instance:
            return await self.create(
                Conversation(user=user_instance.id, assistant=assistant_instance.id)
            )
        else:
            raise ValueError(
                "Could not register conversation because either user or assistant do not exist."
            )

    async def commit_message(self, role: str, content: str, conversation: int, augment: Any | None = None) -> int:
        return await self.create(
            Message(
                role=role,
                content=content,
                augment=augment,
                conversation=conversation,
                prompt=dumps({"role": role, "content": content}),
            )
        )

    async def pull_messages(self, conversation: int) -> tuple[list[dict], str | None]:
        conversation_instance = await self.read(Conversation, id=conversation)
        if conversation_instance:
            messages = [loads(message.prompt) for message in conversation_instance.messages]
            augment = conversation_instance.messages[-1].augment
            return messages, augment
        else:
            raise ValueError(
                "Could not pull messages because conversation does not exist."
            )

    async def pull_conversations(
        self, user: str = "user", assistant: str = "assistant"
    ) -> list[int] | None:
        user_instance = await self.read(User, name=user)
        assistant_instance = await self.read(Assistant, name=assistant)
        if user_instance and assistant_instance:
            conversations = await self.read(Conversation, all=True, user=user_instance.id, assistant=assistant_instance.id)
            if conversations:
                return [conversation.id for conversation in conversations]
            else:
                return None
        else:
            raise ValueError(
                "Could not pull conversations because either user or assistant do not exist."
            )

    async def delete_user(self, name: str):
        return await self.delete(User, name=name)

    async def delete_assistant(self, name: str):
        return await self.delete(Assistant, name=name)

    async def delete_conversation(self, id: int):
        return await self.delete(Conversation, id=id)

    async def query(
        self,
        model: Literal["Assistant", "Conversation"],
        all: bool = False,
        **kwargs
    ):
        if model is "Assistant":
            return await self.read(Assistant, all, **kwargs)
        elif model is "Conversation":
            return await self.read(Conversation, all, **kwargs)
        else:
            raise ValueError("Invalid model, only 'Assistant', 'Conversation', 'Message' allowed.")
