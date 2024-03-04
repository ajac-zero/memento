from memento.nosql.schemas.models import Assistant, Conversation, Message
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import overload


class Repository:
    @classmethod
    async def init(cls, connection: str):
        self = cls()
        mongo = AsyncIOMotorClient(connection)
        database = mongo.memento
        await init_beanie(
            database=database, document_models=[Assistant, Conversation, Message]
        )
        return self

    @overload
    async def read(self, model: type[Assistant], all: bool = False, **kwargs) -> Assistant | None:
        ...

    @overload
    async def read(self, model: type[Conversation], all: bool = False, **kwargs) -> Conversation | None:
        ...

    @overload
    async def read(self, model: type[Message], all: bool = False, **kwargs) -> Message | None:
        ...

    async def read(
        self,
        model: type[Assistant] | type[Conversation] | type[Message],
        all: bool = False,
        **kwargs,
    ):
        results = await model.find(kwargs).to_list()
        return results if all else results[-1] if len(results) > 0 else None
