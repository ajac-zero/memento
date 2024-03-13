from memento.nosql.synchronous.src.repository import Repository
from memento.nosql.synchronous.schemas.models import (
    Assistant,
    Conversation,
    Message,
    MessageContent,
)


class Manager(Repository):
    def __init__(self, client) -> None:
        super().__init__(client)

    def register_conversation(self, user: str, assistant: str, idx: str | None = None) -> str:
        existing_assistant = self.read(Assistant, name=assistant)
        if existing_assistant:
            system_message = Message(
                content=MessageContent(role="system", content=existing_assistant.system)
            )
            conversation = Conversation(
                idx=idx, user=user, assistant=assistant, messages=[system_message]
            )
            Conversation.insert_one(conversation)
            return conversation.idx # type: ignore
        else:
            raise ValueError(
                "Could not register conversation because Assistant does not exist."
            )

    def register_assistant(self, name: str, system: str) -> str:
        existing_assistant = self.read(Assistant, name=name)
        if existing_assistant:
            raise ValueError("Assistant already exists")
        else:
            assistant = Assistant(name=name, system=system)
            assistant.insert_one(assistant)
            return assistant.idx

    def commit_message(
        self, role: str, content: str, conversation: str, augment: str | None = None
    ) -> str:
        conversation_obj = self.read(Conversation, idx=conversation)
        if conversation_obj:
            message = Message(
                content=MessageContent(role=role, content=content), augment=augment
            )
            conversation_obj.messages.append(message)
            await conversation_obj.save()  # type: ignore
            return message.idx
        else:
            raise ValueError("Could not save message as conversation does not exist.")

    def pull_messages(
        self, conversation_idx: str
    ) -> tuple[list[dict[str, str]], str | None]:
        conversation = self.read(Conversation, idx=conversation_idx)
        if conversation:
            return [
                message.content.model_dump() for message in conversation.messages
            ], conversation.messages[-1].augment
        else:
            raise ValueError("Could not pull messages as conversation does not exist.")

    def delete_assistant(self, name: str) -> str:
        assistant = self.read(Assistant, name=name)
        if assistant:
            await assistant.delete()  # type: ignore
            return assistant.idx
        else:
            raise ValueError("Could not delete assistant as it does not exist.")

    def delete_conversation(self, idx: str) -> str:
        conversation = self.read(Conversation, idx=idx)
        if conversation:
            await conversation.delete()  # type: ignore
            return conversation.idx #type: ignore
        else:
            raise ValueError("Could not delete conversation as it does not exist.")

    def get_conversation(self, **kwargs) -> str | None:
        conversation = self.read(Conversation, **kwargs)
        return conversation.idx if conversation else None
