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

    def decorator(self, function, stream: bool = False):
        if not stream:
            async def wrapper(prompt: str, idx: Optional[str] = None, user: str = "user", assistant: str = "assistant", *args, **kwargs):
                settings = await self.set_settings(idx, user, assistant)
                await self.message("user", prompt, settings)
                messages = await self.history(settings)
                response = await function(messages=messages, *args, **kwargs)
                await self.message("assistant", response, settings)
                return response
            return wrapper
        else:
            async def stream_wrapper(prompt: str, idx: Optional[str] = None, user: str = "user", assistant: str = "assistant", *args, **kwargs):
                settings = await self.set_settings(idx, user, assistant)
                await self.message("user", prompt, settings)
                messages = await self.history(settings)
                buffer = ""
                response = await function(messages=messages, *args, **kwargs)
                async for chunk in response:
                    if len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            buffer += content
                            yield content
                await self.message("assistant", buffer, settings)
            return stream_wrapper

    def __call__(self, func = None, *, stream: bool = False):
        if func != None:
            return self.decorator(func, stream)
        else:
            def wrapped(func):
                return self.decorator(func, stream)
            return wrapped
