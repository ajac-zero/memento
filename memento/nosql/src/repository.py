from memento.nosql.schemas.models import Assistant, Conversation, Message
from motor.motor_asyncio import AsyncIOMotorClient
from typing import overload, Literal
from beanie import init_beanie


class Repository:
    def __init__(self, client) -> None:
        self.client = client
        self.database = client.memento

    @classmethod
    def create(cls, connection: str):
        client = AsyncIOMotorClient(connection)
        return cls(client)

    async def on(self) -> None:
        await init_beanie(
            database=self.database, document_models=[Assistant, Conversation, Message]
        )

    @overload
    async def read(
        self, model: type[Assistant], all: Literal[False] = False, **kwargs
    ) -> Assistant | None:
        ...

    @overload
    async def read(
        self, model: type[Assistant], all: Literal[True], **kwargs
    ) -> list[Assistant] | None:
        ...

    @overload
    async def read(
        self, model: type[Conversation], all: Literal[False] = False, **kwargs
    ) -> Conversation | None:
        ...

    @overload
    async def read(
        self, model: type[Conversation], all: Literal[True], **kwargs
    ) -> list[Conversation] | None:
        ...

    async def read(
        self,
        model: type[Assistant] | type[Conversation],
        all: bool = False,
        **kwargs,
    ):
        results = await model.find(kwargs).to_list()
        if all:
            return results if results else None
        return results[-1] if results else None
