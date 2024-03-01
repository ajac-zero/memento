from memento.nosql.schemas.settings import Settings
from memento.nosql.src.manager import Manager
from typing import List, Dict, Optional


class BaseMemory(Manager):
    def __init__(self) -> None:
        self.conversation: Optional[str] = None

    async def set_settings(self, local: bool, **kwargs):
        settings = Settings(**kwargs)
        if local == True:
            if self.conversation == None:
                settings.conversation = await self.register_conversation(
                    user=settings.user, assistant=settings.assistant
                )
                self.conversation = settings.conversation
            else:
                settings.conversation = self.conversation
        if await self.get_conversation(settings.conversation) == None:
            raise ValueError("Conversation does not exist.")
        return settings

    async def message(self, role: str, content: str, settings: Settings) -> None:
        await self.commit_message(settings.conversation, role, content)

    async def history(self, settings: Settings) -> List[Dict[str, str]]:
        return await self.pull_messages(settings.conversation)

    def __call__(self, _func=None, **sttargs):
        def decorator(func, local: bool = False):
            async def wrapper(prompt: str, *args, **kwargs):
                settings = await self.set_settings(local, **sttargs)
                await self.message("user", prompt, settings)
                messages = await self.history(settings)
                response = await func(messages=messages, *args, **kwargs)
                await self.message("assistant", response, settings)
                return response
            return wrapper

        if _func is None:
            return decorator
        else:
            return decorator(_func, local=True)
