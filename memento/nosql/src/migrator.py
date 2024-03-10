from memento.nosql.src.manager import Manager
from beanie import init_beanie


class Migrator(Manager):
    def __init__(self, client) -> None:
        super().__init__(client)

    async def migrate(self) -> None:
        try:
            await self.register_assistant(name="assistant", system="You are a helpful assistant")
            await self.register_conversation(idx="default", user="user", assistant="assistant")
        except Exception:
            return

    async def update(self) -> None:
        await self.on()
        await self.migrate()
