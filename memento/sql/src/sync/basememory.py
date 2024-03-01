from memento.sql.src.sync.migrator import Migrator
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dataclasses import dataclass
from typing import List


@dataclass
class Settings:
    user: str = "user"
    assistant: str = "assistant"
    conversation: int = 0


class BaseMemory(Migrator):
    def __init__(self, connection: str, **kwargs):
        super().__init__(sessionmaker(bind=create_engine(connection)))
        self.update_database(connection)
        self.settings = self.set_settings(**kwargs)

    def set_settings(self, **kwargs) -> Settings:
        settings = Settings(**kwargs)
        if settings.conversation == 0:
            settings.conversation = self.get_conversation(settings)
        return settings

    def get_conversation(self, settings: Settings) -> int:
        recent_conversation = self.pull_conversations(settings.user, settings.assistant)
        if not recent_conversation:
            return self.register_conversation(settings.user, settings.assistant)
        return recent_conversation[-1]

    def update_settings(self, **kwargs) -> None:
        for attribute, value in kwargs.items():
            setattr(self.settings, attribute, value)

    def message(self, role: str, content: str) -> int:
        return self.commit_message(self.settings.conversation, role, content)

    def history(self) -> List[dict]:
        return self.pull_messages(self.settings.conversation)

    def __call__(self, func):
        def wrapper(prompt: str, *args, **kwargs):
            self.message("user", prompt)
            messages = self.history()
            response = func(messages=messages, *args, **kwargs)
            self.message("assistant", response)
            return response

        return wrapper
