from memento.nosql.src.repository import Repository
from memento.nosql.schemas.models import (
    Assistant,
    Conversation,
    Message,
    MessageContent,
)


class Manager(Repository):
    def __init__(self, client) -> None:
        super().__init__(client)

    async def register_conversation(self, user: str, assistant) -> str:
        existing_assistant = await self.read(Assistant, name=assistant)
        if existing_assistant:
            system_message = Message(
                content=MessageContent(role="system", content=existing_assistant.system)
            )
            conversation = Conversation(
                user=user, assistant=assistant, messages=[system_message]
            )
            await Conversation.insert_one(conversation)
            return conversation.idx
        else:
            raise ValueError(
                "Could not register conversation because Assistant does not exist."
            )

    async def register_assistant(self, name: str, system: str) -> str:
        existing_assistant = await self.read(Assistant, name=name)
        if existing_assistant:
            raise ValueError("Assistant already exists")
        else:
            assistant = Assistant(name=name, system=system)
            await assistant.insert_one(assistant)
            return assistant.idx

    async def commit_message(
        self, conversation_idx: str, role: str, content: str, augment: str | None
    ) -> str:
        conversation = await self.read(Conversation, idx=conversation_idx)
        if isinstance(conversation, Conversation):
            message = Message(
                content=MessageContent(role=role, content=content), augment=augment
            )
            conversation.messages.append(message)
            await conversation.save() #type: ignore
            return message.idx
        else:
            raise ValueError("Could not save message as conversation does not exist.")

    async def pull_messages(
        self, conversation_idx: str
    ) -> tuple[list[dict[str, str]], str | None]:
        conversation = await self.read(Conversation, idx=conversation_idx)
        if isinstance(conversation, Conversation):
            return [
                message.content.dict() for message in conversation.messages
            ], conversation.messages[-1].augment
        else:
            raise ValueError("Could not pull messages as conversation does not exist.")

    async def delete_assistant(self, name: str):
        assistant = await self.read(Assistant, name=name)
        if isinstance(assistant, Assistant):
            await assistant.delete() #type: ignore
        else:
            raise ValueError("Could not delete assistant as it does not exist.")

    async def delete_conversation(self, idx: str):
        conversation = await self.read(Conversation, idx=idx)
        if isinstance(conversation, Conversation):
            await conversation.delete() #type: ignore
        else:
            raise ValueError("Could not delete conversation as it does not exist.")

    async def get_conversation(self, idx: str) -> str | None:
        conversation = await self.read(Conversation, idx=idx)
        return conversation.idx if conversation else None
