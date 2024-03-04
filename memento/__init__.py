from memento.sql import SQLMemory
from memento.nosql import NoSQLMemory


class Memento(SQLMemory):
    def __init__(self, connection: str = "sqlite:///:memory:", **kwargs):
        super().__init__(connection, **kwargs)

    @staticmethod
    def nosql(connection: str) -> NoSQLMemory:
        return NoSQLMemory.create(connection)
