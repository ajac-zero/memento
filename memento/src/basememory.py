from typing import Optional, List, Union
from sqlalchemy.orm import sessionmaker
from memento.src.manager import Manager
from sqlalchemy import create_engine
from dataclasses import dataclass
from alembic.config import Config
from alembic import command
import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_INI_PATH = os.path.join(DIR_PATH, '..', 'alembic.ini')
MIGRATION_DIR_PATH = os.path.join(DIR_PATH, '..', 'migrations')

@dataclass
class Settings:
    user: str = "user"
    assistant: str = "assistant"
    conversation: int = 0

class BaseMemory(Manager):
    def __init__(self, connection: str, **kwargs):
        super().__init__(sessionmaker(bind=create_engine(connection)))
        self.update_database(connection)
        self.settings = self.set_settings(**kwargs)

    def update_database(self, connection: str) -> None:
        alembic_cfg = Config(ALEMBIC_INI_PATH)
        alembic_cfg.set_main_option("script_location", MIGRATION_DIR_PATH)
        alembic_cfg.set_main_option("sqlalchemy.url", connection)
        command.upgrade(alembic_cfg, "head")

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

    def message(self, role: str, content: str) -> Optional[int]:
        return self.commit_message(self.settings.conversation, role, content)

    def history(self) -> Optional[List[dict]]:
        return self.pull_messages(self.settings.conversation)

    def __call__(self, func, assistant: Optional[str] = None):
        def wrapper(prompt: str, *args, **kwargs):
            self.message("user", prompt)
            messages = self.history()
            response = func(messages=messages, *args, **kwargs)
            self.message("assistant", response)
            return response
        return wrapper
