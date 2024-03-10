from memento.nosql.src.basememory import AsyncNoSQLMemory
from openai.types.chat import ChatCompletion
from openai import AsyncAzureOpenAI
import pytest_asyncio
import pytest

@pytest_asyncio.fixture
async def mem():
    return AsyncNoSQLMemory.create("mongodb://localhost:27017")

@pytest_asyncio.fixture
async def ai():
    return AsyncAzureOpenAI()

@pytest.mark.asyncio
async def test_async_nosqlmemory(mem: AsyncNoSQLMemory):
    assert isinstance(mem, AsyncNoSQLMemory)

@pytest.mark.asyncio
async def test_async_azure_client(ai: AsyncAzureOpenAI):
    assert isinstance(ai, AsyncAzureOpenAI)

@pytest.mark.asyncio
async def test_async_response(ai: AsyncAzureOpenAI):
    memento = AsyncNoSQLMemory.create("mongodb://localhost:27017")
    await memento.on()

    gen = memento(ai.chat.completions.create)
    response = await gen(message="Hello", model="gpt4-2")

    assert isinstance(response, ChatCompletion)
