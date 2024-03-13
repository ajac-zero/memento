from memento.nosql.synchronous.src.manager import Manager
from bunnet import init_bunnet


class Migrator(Manager):
    def __init__(self, client) -> None:
        super().__init__(client)

    def migrate(self) -> None:
        try:
            self.register_assistant(name="assistant", system="You are a helpful assistant")
            self.register_conversation(idx="default", user="user", assistant="assistant")
        except Exception:
            return

    def update(self) -> None:
        self.on()
        self.migrate()
