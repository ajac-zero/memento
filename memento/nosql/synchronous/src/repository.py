from memento.nosql.synchronous.schemas.models import Assistant, Conversation, Message
from typing import overload, Literal
from pymongo import MongoClient
from bunnet import init_bunnet


class Repository:
    def __init__(self, client) -> None:
        self.client = client
        self.database = client.memento

    @classmethod
    def create(cls, connection: str):
        client = MongoClient(connection)
        return cls(client)

    def on(self) -> None:
        init_bunnet(
            database=self.database, document_models=[Assistant, Conversation, Message] #type: ignore
        )

    @overload
    def read(self, model: type[Assistant], all: Literal[False] = False, **kwargs) -> Assistant | None: ...

    @overload
    def read(self, model: type[Assistant], all: Literal[True], **kwargs) -> list[Assistant] | None: ...

    @overload
    def read(self, model: type[Conversation], all: Literal[False] = False, **kwargs) -> Conversation | None: ...

    @overload
    def read(self, model: type[Conversation], all: Literal[True], **kwargs) -> list[Conversation] | None: ...

    @overload
    def read(self, model: type[Assistant] | type[Conversation], all: bool = False, **kwargs): ...

    def read(
        self,
        model: type[Assistant] | type[Conversation],
        all: bool = False,
        **kwargs,
    ):
        results = model.find(kwargs).to_list()
        if all:
            return results if results else None
        return results[-1] if results else None
