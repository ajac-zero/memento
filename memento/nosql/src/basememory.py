from memento.nosql.schemas.settings import Settings
from memento.nosql.src.manager import Manager
from typing import List, Dict


class BaseMemory(Manager):
    async def set_settings(self, **kwargs):
        settings = Settings(**kwargs)
        if await self.get_conversation(settings.conversation) == None:
            settings.conversation = await self.register_conversation(user=settings.user,assistant=settings.assistant)
        return settings

    async def message(self, role: str, content: str, settings: Settings) -> None:
        await self.commit_message(settings.conversation, role, content)

    async def history(self, settings: Settings) -> List[Dict[str, str]]:
        return await self.pull_messages(settings.conversation)

    def __call__(self, prompt: str, **kwargs):
        async def wrapper(func):
            settings = await self.set_settings(**kwargs)
            await self.message("user", prompt, settings)
            messages = await self.history(settings)
            response = func(messages, **kwargs)
            await self.message("assistant", response, settings)
        return wrapper
