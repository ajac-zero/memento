from memento.sql.src.sync.migrator import Migrator
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Callable, Any
from functools import wraps


class SQLMemory(Migrator):
    def __init__(self, connection: str, **kwargs):
        super().__init__(sessionmaker(bind=create_engine(connection)))
        self.update_database(connection)
        self.current_conversation: int | None = None
        self.template_factory: Callable[..., str] | None = None

    def set_conversation(self, idx: int | None, user: str, assistant: str, **kwargs) -> int:
        if idx is None:
            if self.current_conversation is None:
                latest_conversation = self.pull_conversations(user=user, assistant=assistant)
                if latest_conversation:
                    idx = latest_conversation[-1]
                else:
                    idx = self.register_conversation(user=user, assistant=assistant)
                self.current_conversation = idx
            else:
                idx = self.current_conversation
        return idx

    def prev_messages(self, conversation: int) -> list[dict[str, str]]:
        messages, augment = self.pull_messages(conversation)
        if augment:
            if self.template_factory:
                messages[-1]["content"] = self.template_factory(augment, messages)
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
            idx: int | None = None,
            username: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            conversation = self.set_conversation(idx, username, assistant)
            self.commit_message("user", message, conversation, augment)
            kwargs["messages"] = self.prev_messages(conversation)
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
            idx: int | None = None,
            username: str = "user",
            assistant: str = "assistant",
            *args,
            **kwargs,
        ):
            conversation = self.set_conversation(idx, username, assistant)
            self.commit_message("user", message, conversation, augment)
            kwargs["messages"] = self.prev_messages(conversation)
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

    def __call__(self, func: Callable | None, *, stream: bool = False, template_factory: Callable | None = None):
        if template_factory:
            self.template_factory = template_factory
        if func:
            return self.stream_decorator(func) if stream else self.decorator(func)
        else:
            return self.stream_decorator if stream else self.decorator
