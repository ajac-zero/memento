from memento.nosql.schemas.models import Assistant, Conversation, Message
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import overload


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
        self, model: type[Assistant], all: bool = False, **kwargs
    ) -> Assistant | None:
        ...

    @overload
    async def read(
        self, model: type[Conversation], all: bool = False, **kwargs
    ) -> Conversation | None:
        ...

    @overload
    async def read(
        self, model: type[Message], all: bool = False, **kwargs
    ) -> Message | None:
        ...

    async def read(
        self,
        model: type[Assistant] | type[Conversation] | type[Message],
        all: bool = False,
        **kwargs,
    ):
        results = await model.find(kwargs).to_list()
        return results if all else results[-1] if len(results) > 0 else None
