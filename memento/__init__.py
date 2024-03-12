from memento.nosql import AsyncNoSQLMemory
from memento.sql import SQLMemory
from typing import Any, Callable


class Memento(SQLMemory):
    def __init__(self, connection: str = "sqlite:///:memory:", **kwargs):
        super().__init__(connection, **kwargs)

    @staticmethod
    def nosql(connection: str) -> AsyncNoSQLMemory:
        return AsyncNoSQLMemory.create(connection)


def patch(
    connection: str,
    nosql: bool = False,
    stream: bool = False,
    openai: Any | None = None,
    function: Callable | None = None,
    template_factory: Callable | None = None,
):
    if nosql:
        memento = Memento.nosql(connection)
    else:
        memento = Memento(connection)

    if openai:
        func = openai.chat.completions.create
        openai.chat.completions.create = memento(
                func, stream=stream, template_factory=template_factory #type: ignore
            )
        return openai, memento
    elif function:
        function = memento(
            function, stream=stream, template_factory=template_factory #type: ignore
        )
        return function, memento
    else:
        raise ValueError("Either OpenAI client or generation function required.")
