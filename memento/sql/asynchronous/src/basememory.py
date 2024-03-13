from makefun import wraps, add_signature_parameters, remove_signature_parameters
from memento.sql.asynchronous.src.migrator import Migrator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from inspect import signature, Parameter
from typing import Callable, Any


PARAMS = [
    Parameter("message", kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
    Parameter("augment", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None, annotation=Any),
    Parameter("idx", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None, annotation=str),
    Parameter("username", kind=Parameter.POSITIONAL_OR_KEYWORD, default="username", annotation=str),
    Parameter("assistant", kind=Parameter.POSITIONAL_OR_KEYWORD, default="assistant", annotation=str),
]


class AsyncSQLMemory(Migrator):
    def __init__(self, connection: str, **kwargs):
        super().__init__(async_sessionmaker(bind=create_async_engine(connection)))
        self.update_database(connection)
        self.current_conversation: int | None = None
        self.template_factory: Callable[..., str] | None = None

    async def set_conversation(self, idx: int | None, user: str, assistant: str, **kwargs) -> int:
        if idx is None:
            if self.current_conversation is None:
                latest_conversation = await self.pull_conversations(user=user, assistant=assistant)
                if latest_conversation:
                    idx = latest_conversation[-1]
                else:
                    idx = await self.register_conversation(user=user, assistant=assistant)
                self.current_conversation = idx
            else:
                idx = self.current_conversation
        return idx

    async def prev_messages(self, conversation: int) -> list[dict[str, str]]:
        messages, augment = await self.pull_messages(conversation)
        if augment:
            if self.template_factory:
                messages[-1]["content"] = self.template_factory(augment, messages)
            else:
                try:
                    messages[-1]["content"] = messages[-1]["content"] + "\n" + augment
                except Exception:
                    raise ValueError(f"Default augmentation accepts 'str' only, but '{type(augment).__name__}' was given. Please set template_factory in decorator if another type is needed.")
        return messages

    def build_signature(self, func):
        old_signature = signature(func)
        new_signature = add_signature_parameters(old_signature, first=PARAMS)
        if 'messages' in new_signature.parameters:
            new_signature = remove_signature_parameters(new_signature, 'messages')
        return new_signature

    def decorator(self, function):
        @wraps(function, new_sig=self.build_signature(function))
        async def wrapper(
            message: str,
            augment: Any | None = None,
            idx: int | None = None,
            username: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            conversation = await self.set_conversation(idx, username, assistant)
            await self.commit_message("user", message, conversation, augment)
            kwargs["messages"] = await self.prev_messages(conversation)
            response = await function(*args, **kwargs)
            content = response.choices[0].message.content
            await self.commit_message("assistant", content, conversation)
            return response

        return wrapper

    def stream_decorator(self, function):
        @wraps(function, new_sig=self.build_signature(function))
        async def stream_wrapper(
            message: str,
            augment: Any | None = None,
            idx: int | None = None,
            username: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            conversation = await self.set_conversation(idx, username, assistant)
            await self.commit_message("user", message, conversation, augment)
            kwargs["messages"] = await self.prev_messages(conversation)
            buffer = ""
            response = await function(*args, **kwargs)
            async for chunk in response:
                choices = chunk.choices
                if choices:
                    content = choices[0].delta.content
                    if content:
                        buffer += content
                yield chunk
            await self.commit_message("assistant", buffer, conversation)

        return stream_wrapper

    def __call__(self, func: Callable | None = None, *, stream: bool = False, template_factory: Callable | None = None):
        if template_factory:
            self.template_factory = template_factory
        if func:
            return self.stream_decorator(func) if stream else self.decorator(func)
        else:
            return self.stream_decorator if stream else self.decorator
