from memento.nosql.synchronous.src.migrator import Migrator
from typing import Any, Callable
from functools import wraps


class NoSQLMemory(Migrator):
    def __init__(self, client) -> None:
        super().__init__(client)
        self.local_conversation: str | None = None
        self.template_factory: Callable | None = None

    def set_conversation(self, idx: str | None, user: str, assistant: str, **kwargs) -> str:
        if idx is None:
            if self.local_conversation is None:
                recent_conversation = self.get_conversation(
                    user=user, assistant=assistant
                )
                if recent_conversation is None:
                    idx = self.register_conversation(
                        user=user, assistant=assistant
                    )
                else:
                    idx = recent_conversation
                self.local_conversation = idx
            else:
                idx = self.local_conversation
        return idx

    def prev_messages(self, conversation: str, augment: Any | None = None) -> list[dict[str, str]]:
        messages = self.pull_messages(conversation)
        if augment:
            if self.template_factory:
                messages[-1]["content"] = self.template_factory(augment, messages[-1]["content"])
            else:
                try:
                    messages[-1]["content"] = (messages[-1]["content"] + "\n" + augment)
                except Exception:
                    raise ValueError(f"Default augmentation accepts 'str' only, but '{type(augment).__name__}' was given. Please set template_factory in decorator if another type is needed.")
        return messages

    def decorator(self, function):
        @wraps(function)
        def wrapper(
            message: str,
            augment: Any | None = None,
            idx: str | None = None,
            username: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            conversation = self.set_conversation(idx, username, assistant)
            self.commit_message("user", message, conversation, augment)
            kwargs["messages"] = self.prev_messages(conversation, augment)
            response = function(*args, **kwargs)
            content = response.choices[0].message.content
            self.commit_message("assistant", content, conversation)
            return response

        return wrapper

    def stream_decorator(self, function):
        @wraps(function)
        def stream_wrapper(
            message: str,
            augment: Any | None = None,
            idx: str | None = None,
            username: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            conversation = self.set_conversation(idx, username, assistant)
            self.commit_message("user", message, conversation, augment)
            kwargs["messages"] = self.prev_messages(conversation, augment)
            buffer = ""
            response = function(*args, **kwargs)
            for chunk in response:
                choices = chunk.choices
                if choices:
                    content = choices[0].delta.content
                    if content:
                        buffer += content
                yield chunk
            self.commit_message("assistant", buffer, conversation)

        return stream_wrapper

    def __call__(
        self,
        func: Callable | None = None,
        *,
        stream: bool = False,
        template_factory: Callable | None = None,
    ):
        if template_factory:
            self.template_factory = template_factory
        if func:
            return self.stream_decorator(func) if stream else self.decorator(func)
        else:
            return self.stream_decorator if stream else self.decorator
