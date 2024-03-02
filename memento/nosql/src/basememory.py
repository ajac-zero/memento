from memento.nosql.schemas.settings import Settings
from memento.nosql.src.manager import Manager
from typing import List, Dict, Optional


class BaseMemory(Manager):
    def __init__(self) -> None:
        self.conversation: Optional[str] = None

    async def set_settings(self, idx: Optional[str], user: str, assistant: str, **kwargs):
        settings = Settings(conversation=idx, user=user, assistant=assistant)
        if settings.conversation == None:
            if self.conversation == None:
                settings.conversation = await self.register_conversation(user=settings.user, assistant=settings.assistant)
                self.conversation = settings.conversation
            else:
                settings.conversation = self.conversation
        else:
            if await self.get_conversation(settings.conversation) == None:
                raise ValueError("Conversation does not exist.")
        return settings

    async def message(self, role: str, content: str, settings: Settings) -> None:
        await self.commit_message(settings.conversation, role, content) #type: ignore

    async def history(self, settings: Settings) -> List[Dict[str, str]]:
        return await self.pull_messages(settings.conversation) #type: ignore

    def __call__(self, func):
        async def wrapper(prompt: str, idx: Optional[str] = None, user: str = "user", assistant: str = "assistant", *args, **kwargs):
            settings = await self.set_settings(idx, user, assistant)
            await self.message("user", prompt, settings)
            messages = await self.history(settings)
            response = await func(messages=messages, *args, **kwargs)
            await self.message("assistant", response, settings)
            return response
        return wrapper
