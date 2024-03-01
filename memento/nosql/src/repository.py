from memento.nosql.schemas.models import Assistant, Conversation, Message
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Union


class Repository:
    @classmethod
    async def nosql(cls, connection: str):
        self = cls()
        mongo = AsyncIOMotorClient(connection)
        database = mongo.memento
        await init_beanie(
            database=database, document_models=[Assistant, Conversation, Message]
        )
        return self

    async def read(
        self,
        model: Union[Assistant, Conversation, Message],
        all: bool = False,
        **kwargs,
    ):
        results = await model.find(kwargs).to_list()
        return results if all else results[0] if len(results) > 0 else None


if __name__ == "__main__":
    import asyncio

    async def main():
        repo = await Repository.nosql("mongodb://localhost:27017")
        result = await repo.read(
            model=Conversation, idx="7a5e1b3b-7398-41d5-bd14-a3f83edf0b6d"
        )
        print(result)

    asyncio.run(main())
