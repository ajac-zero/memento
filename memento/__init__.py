from memento.nosql import AsyncNoSQLMemory
from typing import Any, Callable, Literal
from memento.sql import SQLMemory


class Memento(SQLMemory):
    def __init__(self, connection: str = "sqlite:///:memory:", **kwargs):
        super().__init__(connection, **kwargs)

    @staticmethod
    def nosql(connection: str) -> AsyncNoSQLMemory:
        return AsyncNoSQLMemory.create(connection)


def patch(
    client: Any,
    connection: str,
    nosql: bool = False,
    stream: bool = False,
    template_factory: Callable | None = None,
):
    func: Callable = client.chat.completions.create
    if nosql:
        memento = Memento.nosql(connection)
        client.chat.completions.create = memento(
            func, stream=stream, template_factory=template_factory #type: ignore
        )
        return client, memento
    else:
        memento = Memento(connection)
        client.chat.completions.create = memento(
            func, stream=stream, template_factory=template_factory
        )
        return client
