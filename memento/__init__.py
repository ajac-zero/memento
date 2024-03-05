from openai import OpenAI, AzureOpenAI, AsyncOpenAI, AsyncAzureOpenAI
from memento.nosql import NoSQLMemory
from memento.sql import SQLMemory


class Memento(SQLMemory):
    def __init__(self, connection: str = "sqlite:///:memory:", **kwargs):
        super().__init__(connection, **kwargs)

    @staticmethod
    def nosql(connection: str) -> NoSQLMemory:
        return NoSQLMemory.create(connection)


def memory(
    client: OpenAI | AzureOpenAI | AsyncOpenAI | AsyncAzureOpenAI,
    connection: str,
    nosql=False,
    stream=False,
    template_factory=None,
) -> tuple[
    OpenAI | AzureOpenAI | AsyncOpenAI | AsyncAzureOpenAI, SQLMemory | NoSQLMemory
]:
    if nosql is True:
        memento: NoSQLMemory = Memento.nosql(connection)
        client.chat.completions.create = memento(  # type: ignore
            func=client.chat.completions.create,
            stream=stream,
            template_factory=template_factory,
        )
        return client, memento
    else:
        raise NotImplementedError("SQL not yet implemented.")
