from memento.nosql.schemas.settings import Settings
from memento.nosql.src.manager import Manager
from typing import Callable, Any


class AsyncNoSQLMemory(Manager):
    def __init__(self, client) -> None:
        super().__init__(client)
        self.conversation: str | None = None
        self.template_factory: Callable | None = None

    async def set_settings(
        self, idx: str | None, user: str, assistant: str, **kwargs
    ):
        settings = Settings(conversation=idx, user=user, assistant=assistant)
        if settings.conversation == None:
            if self.conversation == None:
                settings.conversation = await self.register_conversation(
                    user=settings.user, assistant=settings.assistant
                )
                self.conversation = settings.conversation
            else:
                settings.conversation = self.conversation
        else:
            if await self.get_conversation(settings.conversation) == None:
                raise ValueError("Conversation does not exist.")
        return settings

    async def message(
        self, role: str, content: str, settings: Settings, augment: str | None = None
    ) -> None:
        if settings.conversation:
            await self.commit_message(settings.conversation, role, content, augment)
        else:
            raise ValueError("Could not save message as conversation does not exist.")

    async def history(self, settings: Settings) -> list[dict[str, str]]:
        if settings.conversation:
            messages, augment = await self.pull_messages(settings.conversation)
            if augment != None:
                if self.template_factory != None:
                    messages[-1]["content"] = self.template_factory(
                        augment, messages[-1]["content"]
                    )
                else:
                    try:
                        messages[-1]["content"] = augment + "\n" + messages[-1]["content"]
                    except Exception:
                        raise ValueError(
                            f"Default augmentation accepts 'str' only, but '{type(augment).__name__}' was given. Please set template_factory in decorator if another type is needed."
                        )
            return messages
        else:
            raise ValueError("Could not get history as conversation does not exist.")

    def decorator(self, function):
        async def wrapper(
            prompt: str,
            augment: Any | None = None,
            idx: str | None = None,
            user: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            settings = await self.set_settings(idx, user, assistant)
            await self.message("user", prompt, settings, augment)
            messages = await self.history(settings)
            response = await function(messages=messages, *args, **kwargs)
            content = response.choices[0].message.content
            await self.message("assistant", content, settings)
            return content

        return wrapper

    def stream_decorator(self, function):
        async def stream_wrapper(
            prompt: str,
            augment: Any | None = None,
            idx: str | None = None,
            user: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            settings = await self.set_settings(idx, user, assistant)
            await self.message("user", prompt, settings, augment)
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

    def __call__(
        self,
        func=None,
        *,
        stream: bool = False,
        template_factory: Callable | None = None,
    ) :
        if template_factory != None:
            self.template_factory = template_factory
        if func != None:
            return self.decorator(func)
        else:
            return self.stream_decorator if stream else self.decorator
