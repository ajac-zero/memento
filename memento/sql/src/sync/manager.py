from memento.sql.schemas.models import Assistant, Conversation, Message, User
from memento.sql.src.sync.repository import Repository
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
import json


class Manager(Repository):
    def __init__(self, sessionmaker: sessionmaker):
        super().__init__(sessionmaker)

    def register_user(self, name: str = "user") -> int:
        return self.create(User(name=name))

    def register_assistant(
        self,
        name: str = "assistant",
        system: str = "You are a helpful assistant",
        model: Optional[str] = None,
        tokens: Optional[int] = None,
    ) -> int:
        return self.create(
            Assistant(
                name=name,
                system=system,
                model=model,
                tokens=tokens,
            )
        )

    def register_conversation(
        self, user: str = "user", assistant: str = "assistant"
    ) -> int:
        user_instance = self.read(User, name=user)
        assistant_instance = self.read(Assistant, name=assistant)
        if user_instance is not None and assistant_instance is not None:
            return self.create(
                Conversation(user=user_instance.id, assistant=assistant_instance.id)
            )
        else:
            raise ValueError(
                "Could not register conversation because either user or assistant do not exist."
            )

    def commit_message(self, conversation: int, role: str, content: str) -> int:
        return self.create(
            Message(
                conversation=conversation,
                role=role,
                content=content,
                prompt=json.dumps({"role": role, "content": content}),
            )
        )

    def pull_messages(self, conversation: int) -> List[dict]:
        conversation_instance = self.read(Conversation, id=conversation)
        if conversation_instance is not None:
            messages = [
                json.loads(message.prompt) for message in conversation_instance.messages
            ]
            return messages
        else:
            raise ValueError(
                "Could not pull messages because conversation does not exist."
            )

    def pull_conversations(
        self, user: str = "user", assistant: str = "assistant"
    ) -> List[int]:
        user_instance = self.read(User, name=user)
        assistant_instance = self.read(Assistant, name=assistant)
        if user_instance is not None and assistant_instance is not None:
            return [
                conversation.id
                for conversation in self.read(  # type: ignore
                    Conversation,
                    all=True,
                    user=user_instance.id,
                    assistant=assistant_instance.id,
                )
            ]
        else:
            raise ValueError(
                "Could not pull conversations because either user or assistant do not exist."
            )

    def delete_user(self, name: str):
        return self.delete(User, name=name)

    def delete_assistant(self, name: str):
        return self.delete(Assistant, name=name)

    def delete_conversation(self, id: int):
        return self.delete(Conversation, id=id)
