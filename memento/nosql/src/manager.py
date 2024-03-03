from memento.nosql.src.repository import Repository
from typing import Dict, List, Optional, Tuple
from memento.nosql.schemas.models import (
    Assistant,
    Conversation,
    Message,
    MessageContent,
)


class Manager(Repository):
    async def register_conversation(self, user: str, assistant) -> str:
        existing_assistant: Assistant = await self.read(Assistant, name=assistant)  # type: ignore
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
        existing_assistant: Assistant = await self.read(Assistant, name=name)  # type: ignore
        if existing_assistant:
            raise ValueError("Assistant already exists")
        else:
            assistant = Assistant(name=name, system=system)
            await assistant.insert_one(assistant)
            return assistant.idx

    async def commit_message(
        self, conversation_idx: str, role: str, content: str, augment: Optional[str]
    ) -> str:
        conversation: Conversation = await self.read(Conversation, idx=conversation_idx)  # type: ignore
        message = Message(
            content=MessageContent(role=role, content=content), augment=augment
        )
        conversation.messages.append(message)
        await conversation.save()  # type: ignore
        return message.idx

    async def pull_messages(
        self, conversation_idx: str
    ) -> Tuple[List[Dict[str, str]], Optional[str]]:
        conversation: Conversation = await self.read(Conversation, idx=conversation_idx)  # type: ignore
        return [
            message.content.dict() for message in conversation.messages
        ], conversation.messages[-1].augment

    async def delete_assistant(self, name: str):
        assistant: Assistant = await self.read(Assistant, name=name)  # type: ignore
        await assistant.delete()  # type: ignore

    async def delete_conversation(self, idx: str):
        conversation: Conversation = await self.read(Conversation, idx=idx)  # type: ignore
        await conversation.delete()  # type: ignore

    async def get_conversation(self, idx: str) -> Optional[str]:
        conversation: Conversation = await self.read(Conversation, idx=idx)  # type: ignore
        return conversation.idx if conversation else None
